"""
:: Moiety_Formula = C24 H27 Au Cl N P, C H2 Cl2, Cl
"""
#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

import os
import subprocess
from pathlib import Path
from time import sleep

from tools.pupdate import get_platon


def run_platon(file: Path, param='-u', timeout=200, local_exe=True):
    plat = None
    chkfile = Path(file.absolute().stem + '.chk')
    os.chdir(file.absolute().parent.parent)
    timeticks = 0
    # a fresh platon exe from the web:
    if not local_exe:
        pexe = get_platon()
    else:
        pexe = False
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags = 1
        si.wShowWindow = 0
    except AttributeError:
        si = None
    try:
        if pexe:
            plat = subprocess.Popen([pexe, param, file.name], startupinfo=si)
        else:
            print('trying local platon')
            print(file.name)
            plat = subprocess.Popen(['platon', '-u', file.name], startupinfo=si)
    except (FileNotFoundError, PermissionError) as e:
        print(e)
        print('Platon not found.')
        return
    # waiting for chk file to appear:
    while not chkfile.is_file():
        timeticks = timeticks + 1
        sleep(0.01)
        if timeticks > 1000:
            print('Platon statup took too long. Killing Platon...')
            try:
                print('Platon took too much time, terminating platon. (1)')
                plat.terminate()
                break
            except Exception as e:
                print(e)
                break
    size1 = chkfile.stat().st_size
    size2 = 99999999
    timeticks = 0
    # waiting until size does not increase anymore:
    while size1 <= size2:
        timeticks = timeticks + 1
        size2 = chkfile.stat().st_size
        # print(size1, size2)
        sleep(0.1)
        size1 = chkfile.stat().st_size
        if timeticks > timeout:  # 20s
            try:
                print('Platon took too much time, terminating platon. (2)')
                plat.terminate()
                break
            except Exception:
                pass
                break
    try:
        plat.terminate()
    except Exception:
        pass


class PlatonOut():
    def __init__(self, file: Path):
        self.cif_fileobj = file
        platfiles = self.get_chkfiles()
        self._fileobj = Path('.')
        self.filename = Path('')
        if not platfiles:
            run_platon(self.cif_fileobj)
        platfiles = self.get_chkfiles()
        for platfile in platfiles:
            if platfile:
                self._fileobj = Path(platfile)
                self.filename = self._fileobj.absolute()
        if not self._fileobj.is_dir():
            self._text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
            self.formula_moiety = ''
            self.parse_file()

    def get_chkfiles(self):
        p = Path('./')
        platfiles = p.glob('*.chk')
        platfiles = sorted(platfiles, key=os.path.getmtime, reverse=True)
        return platfiles

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
    fname = Path(r'test-data/DK_zucker2_0m.cif')
    s = PlatonOut(fname)
    print(s)
    chkfile = Path(fname.stem + '.chk')
    chkfile.unlink()
