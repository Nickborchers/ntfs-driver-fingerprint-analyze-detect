from typing import List

from model.statement import Statement
from model.file import File
from model.attribute import Attribute

class FileAnalysis():
    SYSTEM_VOLUME_INFORMATION = b'System Volume Information'
    FSEVENTSD = b'.fseventsd'
    UGM = b'$UGM'

    statements: List[Statement]

    def __repr__(self) -> str:
        return f"FileAnalysis, src: {self.src}, statements: {self.statements}"

    def __init__(self, file: File):
        self.src = file
        self.statements = []
        self.statements += self.scan_filename(file.name)

        # security ID, class id?, owner id?
        if file.security_id == 0:
            self.statements.append(Statement.SECURITY_ID_ZERO)

        # analyze logfile sequence nr.
        if file.logfile_sequence_nr == 0:
            self.statements.append(Statement.LOGFILE_SEQUENCE_NR_ZERO)

        # analyze timestamps granularity geq, leq, etc.

        # logfile present?
    
        # USN journal present?

        # on what OS was partition formatted?

        # symlinks? MFT slack? object id? mft mirr

    # analyze filename: IndexerVolumeGuid, fseventsd-uuid, $UGM as well?
    def scan_filename(self, name):
        result = []
        if name == self.SYSTEM_VOLUME_INFORMATION:
            result.append(Statement.SYSTEM_VOLUME_INFORMATION_PRESENT)
        if name == self.FSEVENTSD:
            result.append(Statement.FSEVENTSD_PRESENT)
        if name == self.UGM:
            result.append(Statement.UGM_PRESENT)

        return result        