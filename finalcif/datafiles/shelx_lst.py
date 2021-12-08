#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from finalcif.cif.cif_file_io import CifContainer
from finalcif.datafiles.utils import ParserMixin


class SHELXTlistfile(ParserMixin):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.version = None
        self.filename = filename
        if not self._fileobj.is_dir():
            self._text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
            self.solutions = {}
            self.parse_file()

    def parse_file(self):
        """
         +  SHELXT  -  CRYSTAL STRUCTURE SOLUTION - VERSION 2018/2            +
        """
        for num, line in enumerate(self._text):
            if "CRYSTAL STRUCTURE SOLUTION" in line:
                line = line.strip().strip('+').strip()
                if 'SHELXTL' in line:
                    self.version = 'SHELXT ' + line.split()[-1]
            if line.strip().startswith('R1  Rweak Alpha'):
                for n in range(100):
                    if not self._text[num + 1 + n]:
                        break
                    if self._text[num + 1]:
                        self.solutions[self._text[num + 1 + n][58:76].strip()] = self._text[num + 1 + n][37:51].strip()


class SolutionProgram(object):
    """Handles the solution program: _computing_structure_solution"""

    def __init__(self, cif: CifContainer):
        self.cif_key = '_computing_structure_solution'
        self.cif = cif
        self.basename = cif.fileobj.stem.split('_0m')[0]
        self.method = ''
        self.program = self.get_solution_program()
        self.solution_listfile = ''

    def get_solution_program(self):
        """
        Tries to figure out which program was used for structure solution.
        """
        p = self.cif.fileobj.parent
        xt_files = p.glob(self.basename + '*.lxt')
        try:
            res = self.cif.block.find_pair('_shelx_res_file')[1]
        except (TypeError, AttributeError):
            res = ''
        byxt = res.find('REM SHELXT solution in')
        for x in xt_files:
            shelxt = SHELXTlistfile(x.as_posix())
            if shelxt.version and byxt:
                self.method = 'direct'
                self.solution_listfile = 'foo'  # x.name
                return shelxt
        if byxt > 0:
            xt = SHELXTlistfile('')
            xt.version = "SHELXT (G. Sheldrick)"
            self.method = 'direct'
            return xt
        xt = SHELXTlistfile('')
        xt.version = "SHELXS (G. Sheldrick)"
        self.method = 'direct'
        return xt

    def __repr__(self):
        return self.program
