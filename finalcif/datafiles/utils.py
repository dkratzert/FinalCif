#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#
import os
from pathlib import Path


class ParserMixin():
    """
    A Mxin class for all file parsers for data/list files.
    """

    def __init__(self, filename: str):
        self._fileobj = Path(filename)
        self.filename = self._fileobj.resolve()


def get_file_to_parse(fileobj: Path = None, name_pattern: str = '', base_directory: Path = '.'):
    """
    Either fileobjs is given, then the parser uses this file, or a name pattern is given, then
    a file is searched in base_directory in order to parse this file.
    :param fileobj: The Path object to parse.
    :param name_pattern: A pattern like '*_0m._ls' to find the file.
    :param base_directory: The directory where to find files.
    :return: a Path object

    >>> get_file_to_parse(base_directory=Path('test-data'), name_pattern='*_0*m._ls')
    PosixPath('test-data/DK_Zucker2_0m._ls')
    >>> get_file_to_parse(fileobj=Path('test-data/TB_fs20_v1_0m._ls'))
    PosixPath('test-data/TB_fs20_v1_0m._ls')
    """
    if fileobj and fileobj.is_file():
        return fileobj
    else:
        p = Path(base_directory)
        files = list(p.glob(name_pattern))
        files = sorted(files, key=os.path.getmtime, reverse=True)
        for saintfile in files:
            if saintfile:
                fileobj = Path(saintfile)
                return fileobj


class DSRFind():
    def __init__(self, resfile):
        self.resflie = resfile
        self.dsr_used = False
        if resfile:
            self.parse_res()

    def _isthere(self):
        self.dsr_used = True
        return True

    def parse_res(self):
        for line in self.resflie.split('\n'):
            if 'S1600576718004508' in line:
                self._isthere()
            if 'S1600576715005580' in line:
                self._isthere()
            if 'REM DSR PUT' in line.upper():
                self._isthere()
            if 'REM DSR REPLACE' in line.upper():
                self._isthere()
        return False
