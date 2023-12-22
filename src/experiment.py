#!/usr/bin/python
import logging
import os

from tqdm import tqdm

from model.vm import VM
from model.windows_vm import WindowsVM
from model.macos_vm import MacOSVM
from model.ubuntu_vm import UbuntuVM
from model.block_device import BlockDevice
from model.file_operation import FileOperation
from model.file_operations import windows_file_operations, ubuntu_file_operations, macos_file_operations
from model.os import OS
from analysis import *
 
PROJECT_ROOT = "/home/nick/repos/ntfs-driver-finder"
BASE_IMAGE = f'{PROJECT_ROOT}/images/base.bin'
SNAPSHOT_DIR = f'{PROJECT_ROOT}/images'

WINDOWS_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "src/bin/windows")
UBUNTU_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "src/bin/ubuntu")
MACOS_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "src/bin/macos")

def drive_exists(path):
    """Checks if the path exists"""
    return os.path.exists(path)

def do_experiment(file_operation: FileOperation, vm: VM):
    """Performs some file_operation on a vm"""
    block_device = BlockDevice("/dev/sda1")
    block_device.set_state_from_file(BASE_IMAGE)

    if file_operation.baseline != None:
        vm.start()
        vm.execute_command(file_operation.baseline)
        vm.stop()

    block_device.wait_until_present()

    baseline_snapshot_filename = f'baseline-{file_operation.action}.bin'
    block_device.record_state(SNAPSHOT_DIR, baseline_snapshot_filename)

    vm.start()
    vm.execute_command(file_operation.experiment)
    vm.stop()

    block_device.wait_until_present()

    experiment_snapshot_filename = f'experiment-{file_operation.action}.bin'
    block_device.record_state(SNAPSHOT_DIR, experiment_snapshot_filename)

def do_experiments(file_operations, vm: VM):
    """Performs a sequence of file_operations on a vm"""
    print("Performing experiments...")
    for operation in tqdm(file_operations):
        do_experiment(operation, vm)

def analyze_results(file_operations):
    """Analyzes the result of a list of file operation experiments"""
    print("Analyzing results...")
    for operation in tqdm(file_operations):
        if operation.baseline_filename != None:
            baseline = baseline_to_file(operation.action, operation.baseline_filename, SNAPSHOT_DIR)
        if operation.experiment_filename != None:
            experiment = experiment_to_file(operation.action, operation.experiment_filename, SNAPSHOT_DIR)
        if (operation.baseline_filename != None and operation.experiment_filename != None):
            diff(baseline, experiment)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="experiment.log")
    assert os.getenv("ROOT_PASSWORD") != None, "sudo rights are required on the host machine"

    do_experiments(windows_file_operations, WindowsVM(OS.WINDOWS, "windows", "vboxuser", "changeme1"))
    analyze_results(windows_file_operations)

    do_experiments(ubuntu_file_operations, UbuntuVM(OS.UBUNTU, "ubuntu", "nick", "nick"))
    analyze_results(ubuntu_file_operations)

    do_experiments(macos_file_operations, MacOSVM(OS.MAC_OS, "macOS", "harry", "harry"))
    analyze_results(macos_file_operations)