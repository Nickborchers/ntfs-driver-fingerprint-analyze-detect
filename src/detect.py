from model.disk_analysis import DiskAnalysis

def is_special_file(name: bytes):
    """Helper function to check if a filename signifies that it is a special file"""
    blacklist = [b'.', b'..']
    special_file_prefix = b'$'

    return not (name.startswith(special_file_prefix) or name in blacklist)

class Result():
    """Domain object that represents a detection result for NTFS driver differences"""
    def __init__(self, path, fingerprints):
        self.fingerprints = fingerprints
        self.os_analysis = DiskAnalysis(path)
        self.hints = {}

        for idx in self.os_analysis.files:
            file_analysis = self.os_analysis.files[idx]
            if not is_special_file(file_analysis.src.name):
                continue

            for os in self.fingerprints:
                if os not in self.hints:
                    self.hints[os] = 0

                self.hints[os] += sum(el in self.fingerprints[os] for el in file_analysis.statements)