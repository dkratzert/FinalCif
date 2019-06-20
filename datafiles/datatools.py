from pathlib import Path

from datafiles.sadabs import Sadabs
from datafiles.saint import SaintListFile


class MissingCifData():
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value


def get_saint():
    """
    returns a saint parser object from the ._ls file.
    """
    p = Path('./')
    saintfiles = p.rglob('*_0m._ls')
    saint = None
    for s in saintfiles:
        saint = SaintListFile(s.as_posix())
        if saint:
            return saint
    return saint


def get_sadabs():
    p = Path('./')
    sadfiles = p.rglob('*.abs')
    sadabs = None
    for s in sadfiles:
        sadabs = Sadabs(s.as_posix())
        if sadabs:
            return sadabs
    return sadabs
