from abc import ABC, abstractmethod
import subprocess
import time
import logging
from command import run
from model.os import OS
from model.vm import VM

POLL_INTERVAL = 5

class WindowsVM(VM):
    """Domain object that represents a Windows VM."""
    def start(self):
        logging.info("Waiting for VM to be ready...")
        SECONDS_WAITED = 0
        MAX_WAIT_SECONDS = 300

        while SECONDS_WAITED < MAX_WAIT_SECONDS:
            self.send_start_command()
            result = run(["VBoxManage", 
                                    "guestcontrol", 
                                    self.name, "run", 
                                    "c:\\Windows\\System32\\ipconfig.exe", 
                                    f'--username={self.username}', 
                                    f'--password={self.password}']
                         )
            if result.returncode == 0:
                logging.info("VM is running.")
                break
            else:
                time.sleep(POLL_INTERVAL)
                SECONDS_WAITED += POLL_INTERVAL
                logging.info(f"Waited {SECONDS_WAITED} seconds")

    def stop(self):
        run(["VBoxManage", "controlvm", self.name, "shutdown"])

    def execute_command(self, input_path: str) -> None:
        logging.info("Copying command to VM")
        command_full_path = f"c:\\Users\\{self.username}\\Documents\\filename.bat"
        run([
            "VBoxManage", 
            "guestcontrol", 
            self.name, 
            "copyto",
            input_path, 
            "--target-directory", command_full_path,
            f'--username={self.username}', 
            f'--password={self.password}'
        ])
        logging.info("Running command in VM")
        run([
            "VBoxManage", "guestcontrol", self.name, "run",
            command_full_path, f'--username={self.username}', 
            f'--password={self.password}'
        ])
        run([
            "VBoxManage", "guestcontrol", self.name, "rm", command_full_path, 
            f'--username={self.username}', f'--password={self.password}'
        ])
        logging.info("Removing command in VM")

    def send_start_command(self) -> None:
        vm_info_command = f'VBoxManage showvminfo "{self.name}" --machinereadable'
        try:
            vm_info = subprocess.check_output(vm_info_command, shell=True, text=True)
            if 'VMState="running"' not in vm_info:
                logging.info(f"Starting VM: {self.name}")
                start_command = f'VBoxManage startvm "{self.name}" --type=headless'
                run(start_command, shell=True)
            else:
                logging.info(f"VM {self.name} is already running.")
        except subprocess.CalledProcessError as e:
            logging.info(f"An error occurred while checking VM state: {e}")
