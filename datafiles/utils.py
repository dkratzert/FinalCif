from pathlib import Path


class ParserMixin():
    """
    A Mxin class for all file parsers for data/list files.
    """

    def __init__(self, filename: str):
        self._fileobj = Path(filename)
        self.filename = self._fileobj.absolute()


class DSRFind():
    def __init__(self, resfile):
        self.resflie = resfile
        self.dsr_used = False
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
