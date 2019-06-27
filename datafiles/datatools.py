from pathlib import Path

from datafiles.bruker_frame import BrukerFrameHeader
from datafiles.p4p_reader import P4PFile
from datafiles.sadabs import Sadabs
from datafiles.saint import SaintListFile


class MissingCifData():
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value


def get_saint(name_patt='*_0m._ls'):
    """
    returns a saint parser object from the ._ls file.
    """
    p = Path('./')
    saintfiles = p.rglob(name_patt)
    saint = None
    for s in saintfiles:
        saint = SaintListFile(s.as_posix())
        if saint:
            # TODO: This is a relly stupid approach!
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


def get_frame():
    p = Path('./')
    frames = p.rglob('*.sfrm')
    header = None
    for fr in frames:
        header = BrukerFrameHeader(fr.as_posix())
        if header:
            return header
    return header


def get_p4p():
    p = Path('./')
    p4p_files = p.rglob('*.p4p')
    p4p = None
    for p in p4p_files:
        p4p = P4PFile(p.as_posix())
        if p4p:
            return p4p
    return p4p
