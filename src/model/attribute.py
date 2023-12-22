class Attribute:
    """Domain object that represents an NTFS attribute"""
    def __init__(self):
        pass

class StandardInformationAttribute(Attribute):
    """Domain object that represents a StandardInformation NTFS attribute"""
    def __init__(self, modified, accessed, created, changed):
        self.modified = modified
        self.accessed = accessed
        self.created = created
        self.changed = changed

class FileNameAttribute(Attribute):
    """Domain object that represents a FileName NTFS Attribute"""
    def __init__(self, modified, accessed, created, changed):
        self.modified = modified
        self.accessed = accessed
        self.created = created
        self.changed = changed