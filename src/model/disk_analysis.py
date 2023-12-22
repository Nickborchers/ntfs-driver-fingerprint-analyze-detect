from typing import List, Set, Optional
from datetime import datetime

from model.statement import Statement
from model.file_analysis import FileAnalysis
from model.file import File
from model.attribute import FileNameAttribute, StandardInformationAttribute

import pytsk3
from dfir_ntfs import MFT, Attributes

class DiskAnalysis():
    """Domain object that represents disk analysis object"""
    statements: List[Statement]
    files: List[FileAnalysis]

    def __init__(self, filename: str):
        
        image = open(filename, 'rb')
        self.file_system = MFT.FileSystemParser(image)
        mft = MFT.MasterFileTableParser(self.file_system)
        img_info = pytsk3.Img_Info(filename)
        offset = 0

        # use TheSleuthKit to retrieve filenames, due to limitations in dfir_ntfs
        fs = pytsk3.FS_Info(img_info, offset=offset)

        visited = visit(["/"], set(), fs)

        self.files = {}
        for (inode, path) in visited:
            self.files[mft_addr(inode)] = analyze_file(mft, inode, path)

    def __repr__(self) -> str:
        result = ""
        for file in self.files:
            print(self.files[file])

        return result

def analyze_file(mft, inode, path):
    """Extract metadata from a file"""
    mft_address = mft_addr(inode)
    security_id = 0
    logfile_sequence_nr = 0
    attributes = []

    try:
        if mft_address == 0:
            return None

        dfir_record = mft.get_file_record_by_number(mft_address)
        logfile_sequence_nr = dfir_record.get_logfile_sequence_number()
        security_id = get_security_id(dfir_record)

        m, a, c, e = get_standard_information_mace(dfir_record)
        attributes.append(StandardInformationAttribute(m, a, c, e))
        m, a, c, e = get_filename_mace(dfir_record)
        attributes.append(FileNameAttribute(m, a, c, e))

    except: # Fix: handle more specific error
        print("Error parsing file with address: " + mft_address)

    file = File(name(inode), path, security_id, logfile_sequence_nr, attributes) # metadata object
    return FileAnalysis(file)

def visit(paths: List, visited: Set[str], fs) -> Set[tuple[pytsk3.File, str]]:
    """Recursively walk through files on a storage medium and return them as a set"""
    if paths == []:
        return visited

    BLACKLIST = [".", "..", "$Deleted", "$RmMetadata"]

    dirs = []
    for path in paths:
        if path in BLACKLIST:
            continue

        inodes = fs.open_dir(path=path)
        for inode in inodes:
            if inode in visited:
                continue
            visited.add((inode, path))

            if inode.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                dirs.append(name(inode).decode('utf-8'))
                continue

    return visit(dirs, visited, fs)

def name(inode) -> bytes:
    """Get the name of the file given the inode"""
    return inode.info.name.name

def mft_addr(inode) -> int:
    """Get the MFT address given an inode"""
    return inode.info.meta.addr

def get_security_id(dfir_record) -> int:
    """Get the security ID given a 'dfir_ntfs' file record"""
    security_ids = []
    for attr in dfir_record.attributes():

        if type(attr) == MFT.AttributeRecordNonresident:
            continue # dfir_ntfs cannot handle some of these attributes
        
        decoded = attr.value_decoded()
        if type(decoded) == Attributes.StandardInformation:
            security_ids.append(decoded.get_security_id())

        if len(security_ids) != 1:
            print(f'error: invalid number of securityids found: {len(security_ids)}')

        return security_ids[0]

def get_filename_mace(dfir_record) -> tuple[datetime, datetime, datetime, datetime]:
    """Get MACE timestamps for the $FileName NTFS attribute"""
    for attr in dfir_record.attributes():

        if type(attr) == MFT.AttributeRecordNonresident:
            continue # dfir_ntfs cannot handle some of these attributes
        
        decoded = attr.value_decoded()
        if type(decoded) == Attributes.StandardInformation:
            return (decoded.get_mtime(), 
                    decoded.get_atime(), 
                    decoded.get_ctime(), 
                    decoded.get_etime())

    raise Exception("Could not get filename attribute file")

def get_standard_information_mace(dfir_record) -> tuple[datetime, datetime, datetime, datetime]:
    """Get MACE timestamps for the $StandardInformation NTFS attribute"""
    for attr in dfir_record.attributes():

        if type(attr) == MFT.AttributeRecordNonresident:
            continue # dfir_ntfs cannot handle some of these attributes

        decoded = attr.value_decoded()
        if type(decoded) == Attributes.FileName:
            return (decoded.get_mtime(), 
                    decoded.get_atime(), 
                    decoded.get_ctime(), 
                    decoded.get_etime())

    raise Exception("Could not get filename attribute file")