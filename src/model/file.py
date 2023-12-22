from typing import Any, List
from model.attribute import Attribute

class File():
    """Domain object representing an NTFS file"""
    name: str
    path: str
    security_id: int
    logfile_sequence_nr: int
    attributes: List[Attribute]

    def __init__(self, name: str, path: str, security_id: int, logfile_sequence_nr: int, attributes: List[Attribute]):
        self.name = name
        self.path = path
        self.security_id = security_id
        self.logfile_sequence_nr = logfile_sequence_nr
        self.attributes = attributes

    def __repr__(self) -> str:
        return 'File(name={}, path={}, security_id={})'.format(self.name, self.path, self.security_id)