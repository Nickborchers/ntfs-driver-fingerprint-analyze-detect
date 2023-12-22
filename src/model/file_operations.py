import logging
import os

from tqdm import tqdm

from model.vm import VM, WindowsVM, OS, UbuntuVM, MacOSVM
from model.block_device import BlockDevice
from model.file_operation import FileOperation
from analysis import *


PROJECT_ROOT = "/home/nick/repos/ntfs-driver-finder"

windows_file_operations = [
    FileOperation("create", None, f'{PROJECT_ROOT}/src/bin/windows/experiment-create.bat', None, "a.txt"),
    FileOperation("access", f'{PROJECT_ROOT}/src/bin/windows/baseline-access.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-access.bat', "a.txt", "a.txt"),
    FileOperation("delete", f'{PROJECT_ROOT}/src/bin/windows/baseline-delete.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-delete.bat', "a.txt", None),
    FileOperation("rename", f'{PROJECT_ROOT}/src/bin/windows/baseline-rename.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-rename.bat', "a.txt", "b.txt"),
    FileOperation("update", f'{PROJECT_ROOT}/src/bin/windows/baseline-update.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-update.bat', "a.txt", "a.txt"),
    FileOperation("attr-change", f'{PROJECT_ROOT}/src/bin/windows/baseline-attr-change.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-attr-change.bat', "a.txt", "a.txt"),
    FileOperation("copy", f'{PROJECT_ROOT}/src/bin/windows/baseline-copy.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-copy.bat', "a.txt", "b.txt"),
    FileOperation("copy-overwrite", f'{PROJECT_ROOT}/src/bin/windows/baseline-copy-overwrite.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-copy-overwrite.bat', 'a.txt', 'b.txt'),
    FileOperation("move-within", f'{PROJECT_ROOT}/src/bin/windows/baseline-move-within.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-move-within.bat', 'a.txt', 'dir-a/a.txt'),
    FileOperation("move-other", f'{PROJECT_ROOT}/src/bin/windows/baseline-move-other.bat', f'{PROJECT_ROOT}/src/bin/windows/experiment-move-other.bat', None, 'a.txt')
]

ubuntu_file_operations = [
    FileOperation("create", None, f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-create.sh', None, "a.txt"),
    FileOperation("access", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-access.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-access.sh', "a.txt", "a.txt"),
    FileOperation("delete", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-delete.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-delete.sh', "a.txt", None),
    FileOperation("rename", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-rename.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-rename.sh', "a.txt", "b.txt"),
    FileOperation("update", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-update.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-update.sh', "a.txt", "a.txt"),
    FileOperation("attr-change", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-attr-change.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-attr-change.sh', "a.txt", "a.txt"),
    FileOperation("copy", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-copy.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-copy.sh', "a.txt", "b.txt"),
    FileOperation("copy-overwrite", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-copy-overwrite.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-copy-overwrite.sh', 'a.txt', 'b.txt'),
    FileOperation("move-within", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-move-within.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-move-within.sh', 'a.txt', 'dir-a/a.txt'),
    FileOperation("move-other", f'{PROJECT_ROOT}/src/bin/ubuntu/baseline-move-other.sh', f'{PROJECT_ROOT}/src/bin/ubuntu/experiment-move-other.sh', None, 'a.txt')
]

macos_file_operations = [
    FileOperation("create", None, f'{PROJECT_ROOT}/src/bin/macos/experiment-create.sh', None, "a.txt"),
    FileOperation("access", f'{PROJECT_ROOT}/src/bin/macos/baseline-access.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-access.sh', "a.txt", "a.txt"),
    FileOperation("delete", f'{PROJECT_ROOT}/src/bin/macos/baseline-delete.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-delete.sh', "a.txt", None),
    FileOperation("rename", f'{PROJECT_ROOT}/src/bin/macos/baseline-rename.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-rename.sh', "a.txt", "b.txt"),
    FileOperation("update", f'{PROJECT_ROOT}/src/bin/macos/baseline-update.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-update.sh', "a.txt", "a.txt"),
    FileOperation("attr-change", f'{PROJECT_ROOT}/src/bin/macos/baseline-attr-change.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-attr-change.sh', "a.txt", "a.txt"),
    FileOperation("copy", f'{PROJECT_ROOT}/src/bin/macos/baseline-copy.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-copy.sh', "a.txt", "b.txt"),
    FileOperation("copy-overwrite", f'{PROJECT_ROOT}/src/bin/macos/baseline-copy-overwrite.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-copy-overwrite.sh', 'a.txt', 'b.txt'),
    FileOperation("move-within", f'{PROJECT_ROOT}/src/bin/macos/baseline-move-within.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-move-within.sh', 'a.txt', 'dir-a/a.txt'),
    FileOperation("move-other", f'{PROJECT_ROOT}/src/bin/macos/baseline-move-other.sh', f'{PROJECT_ROOT}/src/bin/macos/experiment-move-other.sh', None, 'a.txt')
]
