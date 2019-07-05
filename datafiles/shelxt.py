#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from datafiles.utils import ParserMixin


class SHELXTlistfile(ParserMixin):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.version = None
        if not self._fileobj.is_dir():
            self._text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
            self.solutions = {}
            self.parse_file()

    def parse_file(self):
        """
         +  SHELXT  -  CRYSTAL STRUCTURE SOLUTION - VERSION 2018/2            +
        """
        for num, line in enumerate(self._text):
            if "SOLUTION" in line:
                self.version = ' '.join(line.split()).strip('+').strip()
            if line.strip().startswith('R1  Rweak Alpha'):
                for n in range(100):
                    if not self._text[num + 1 + n]:
                        break
                    if self._text[num + 1]:
                        # TODO: is this fixed-char format?
                        # {'solution_name': 'space_group'}
                        self.solutions[self._text[num + 1 + n][58:76].strip()] = self._text[num + 1 + n][37:51].strip()
