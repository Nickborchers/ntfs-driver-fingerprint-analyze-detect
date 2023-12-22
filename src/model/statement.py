from enum import Enum

class Statement(Enum):
    """Domain object that represents a statement about an NTFS storage medium"""
    SYSTEM_VOLUME_INFORMATION_PRESENT = 1
    FSEVENTSD_PRESENT = 2
    UGM_PRESENT = 4

    SECURITY_ID_ZERO = 8
    SECURITY_ID_258 = 16 
    SECURITY_ID_259 = 32
    LOGFILE_SEQUENCE_NR_ZERO = 64
    TIMESTAMPS_ALL_ZERO = 128

    IN_LOGFILE = 256
    IN_USN_JOURNAL = 512
    EA_PRESENT = 1024
    EA_INFORMATION_PRESENT = 2048