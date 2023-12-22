from model.disk_analysis import DiskAnalysis as DA
from model.statement import Statement
from model.file_analysis import FileAnalysis
from model.file import File

import os

TEST_FILES_PATH = os.path.join("/home/nick/repos/ntfs-driver-finder/src/test/files/")

# ITs
def test_system_volume_information_present():
    actual = DA(TEST_FILES_PATH + "windows-file-folder.bin")
    for file in actual.files:
        if actual.files[file].src.name == b'System Volume Information':
            assert Statement.SYSTEM_VOLUME_INFORMATION_PRESENT in actual.files[file].statements

def test_system_volume_information_missing():
    actual = DA(TEST_FILES_PATH + "ntfs-format-linux.bin")
    TEST_FILE_MFT_ADDR = 36
    assert TEST_FILE_MFT_ADDR not in actual.files

def test_ugm_present():
    actual = DA(TEST_FILES_PATH + "ntfs-format-linux.bin")
    for file in actual.files:
        if actual.files[file].src.name == b'$UGM':
            assert Statement.UGM_PRESENT in actual.files[file].statements

def test_logfile_sequence_nr_positive():
    actual = DA(TEST_FILES_PATH + "windows-file-folder.bin")
    TEST_FILE_MFT_ADDR = 38
    assert TEST_FILE_MFT_ADDR in actual.files
    assert [] == actual.files[TEST_FILE_MFT_ADDR].statements

# odd test name since py.test has a hard time with 'zero' at the end of the testname
def test_logfile_sequence_nr_naught():
    actual = DA(TEST_FILES_PATH + "macos-mount.bin")
    TEST_FILE_MFT_ADDR = 27
    assert TEST_FILE_MFT_ADDR in actual.files
    assert Statement.LOGFILE_SEQUENCE_NR_ZERO in  actual.files[TEST_FILE_MFT_ADDR].statements

def test_security_id_positive():
    actual = DA(TEST_FILES_PATH + "windows-file-folder.bin")
    TEST_FILE_MFT_ADDR = 36
    assert TEST_FILE_MFT_ADDR in actual.files
    assert [] == actual.files[TEST_FILE_MFT_ADDR].statements

def test_security_id_naught():
    actual = DA(TEST_FILES_PATH + "ntfs-format-linux.bin")
    TEST_FILE_MFT_ADDR = 27
    assert TEST_FILE_MFT_ADDR in actual.files
    assert Statement.SECURITY_ID_ZERO in  actual.files[TEST_FILE_MFT_ADDR].statements

def test_fseventsd_present():
    actual = DA(TEST_FILES_PATH + "macos-mount.bin")
    TEST_FILE_MFT_ADDR = 27
    assert TEST_FILE_MFT_ADDR in actual.files
    for file in actual.files:
        if actual.files[file].src.name == b'.ftseventsd':
            assert Statement.FSEVENTSD_PRESENT in actual.files[file].statements

def test_fseventsd_missing():
    actual = DA(TEST_FILES_PATH + "ntfs-format-linux.bin")
    TEST_FILE_MFT_ADDR = 27
    assert TEST_FILE_MFT_ADDR in actual.files

# unit tests
def test_filename_contains_hint():
    file = File(b'System Volume Information', "/", 0, 0, [])
    actual = FileAnalysis(file)
    assert Statement.SYSTEM_VOLUME_INFORMATION_PRESENT in actual.statements

def test_filename_contains_no_hint():
    file = File(b'beach.jpg', '/', 0, 0, [])
    actual = FileAnalysis(file)
    assert Statement.SYSTEM_VOLUME_INFORMATION_PRESENT not in actual.statements

def test_security_id_zero():
    file = File(b'data.txt', '/', 0, 0, [])
    actual = FileAnalysis(file)
    assert Statement.SECURITY_ID_ZERO in actual.statements 

def test_security_id_non_zero():
    file = File(b'data.txt', '/', 19, 0, [])
    actual = FileAnalysis(file)
    assert Statement.SECURITY_ID_ZERO not in actual.statements 

def test_logfile_sequence_nr_zero():
    file = File(b'data.txt', '/', 0, 0, [])
    actual = FileAnalysis(file)
    assert Statement.LOGFILE_SEQUENCE_NR_ZERO in actual.statements 

def test_logfile_sequence_nr_non_zero():
    file = File(b'data.txt', '/', 0, 42, [])
    actual = FileAnalysis(file)
    assert Statement.LOGFILE_SEQUENCE_NR_ZERO not in actual.statements 