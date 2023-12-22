from model.statement import Statement
from model.os import OS

FINGERPRINTS = {
    OS.UBUNTU: {
        'driver': 'Native',
        'hints': [
            Statement.SYSTEM_VOLUME_INFORMATION_PRESENT,
            Statement.IN_LOGFILE,
            Statement.IN_USN_JOURNAL,
            Statement.EA_PRESENT,
            Statement.EA_INFORMATION_PRESENT
        ]
    },
    OS.MAC_OS: {
        'driver': 'Paragon',
        'hints': [
            Statement.FSEVENTSD_PRESENT,
            Statement.UGM_PRESENT,
            Statement.TIMESTAMPS_ALL_ZERO,
            Statement.EA_PRESENT,
            Statement.EA_INFORMATION_PRESENT,
            Statement.SECURITY_ID_259,
        ]
    },
    OS.UBUNTU: {
        'driver': 'ntfs3',
        'hints': [
            Statement.EA_PRESENT,
            Statement.EA_INFORMATION_PRESENT,
            Statement.SECURITY_ID_258
        ]
    }
}
