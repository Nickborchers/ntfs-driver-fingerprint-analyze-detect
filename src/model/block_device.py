import os
import subprocess
from command import run
import logging
import time

POLL_INTERVAL = 1

class BlockDevice:
    """Domain object that represents a block device on the host machine."""
    def __init__(self, path):
        self.path = path

    
    def wait_until_present(self):
        """Waits for the block device to be available in the host machine. It
        polls every SLEEP_INTERVAL seconds"""
        logging.info(f"Waiting for device to be present: {self.path}")
        while (True):
            time.sleep(POLL_INTERVAL)            
            if os.path.exists(self.path):
                return 

    def record_state(self, target_directory, file_name):
        """Record the state of the block device through the 'dd' command. Note
        that this command is dangerous since 'dd' could overwrite important
        data on other block devices if used incorrectly.
        """
        target_path = os.path.join(target_directory, f'{file_name}')
        subprocess.run([f"mkdir -p {target_directory}"], shell=True)
        cmd = subprocess.Popen(['echo', os.getenv("ROOT_PASSWORD")], stdout=subprocess.PIPE)
        run(['sudo', '-S', "dd", f'if={self.path}', f'of={target_path}', 'conv=noerror,sync'], stdin=cmd.stdout)

    def set_state_from_file(self, path):
        """Overwrite the block device using the disk image located at 'path'"""
        sudo_password = os.getenv("ROOT_PASSWORD")
        cmd = subprocess.Popen(['echo', sudo_password], stdout=subprocess.PIPE)
        run(['sudo', '-S', "dd", f'if={path}', f'of={self.path}', 'conv=noerror,sync'], stdin=cmd.stdout)
        run(['sync'])