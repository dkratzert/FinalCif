"""
:: Moiety_Formula = C24 H27 Au Cl N P, C H2 Cl2, Cl
"""
import os
from pathlib import Path


class PlatonOut():
    def __init__(self, basename: str):
        p = Path('./')
        platfiles = p.glob('*.chk')
        platfiles = sorted(platfiles, key=os.path.getmtime, reverse=True)
        for platfile in platfiles:
            if platfile:
                self._fileobj = Path(platfile)
                self.filename = self._fileobj.absolute()
        if not self._fileobj.is_dir():
            self._text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
            self.formula_moiety = ''
            self.parse_file()

    def parse_file(self):
        """
        """
        for num, line in enumerate(self._text):
            if line.startswith('# MoietyFormula'):
                self.formula_moiety = ' '.join(line.split(' ')[2:])

    def __repr__(self):
        return 'Platon:\n{}'.format(self.formula_moiety)

if __name__ == '__main__':
    print('###############\n\n')
    s = PlatonOut(r'./')
    print(s)
