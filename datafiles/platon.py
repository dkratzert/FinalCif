"""
:: Moiety_Formula = C24 H27 Au Cl N P, C H2 Cl2, Cl
"""
import os
import subprocess
from pathlib import Path
from time import sleep

from PyQt5.QtWidgets import QMessageBox


class PlatonOut():
    def __init__(self, file: Path):
        self.cif_fileobj = file
        platfiles = self.get_chkfiles()
        if not platfiles:
            #info = QMessageBox()
            #info.setIcon(QMessageBox.Information)
            #info.setText('Running PLATON, this may take a while.')
            #info.show()
            self.run_platon()
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

    def run_platon(self):
        plat = None
        chkfile = Path(self.cif_fileobj.stem + '.chk')
        print(chkfile.name)
        timeticks = 0
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags = 1
            si.wShowWindow = 0
            plat = subprocess.Popen([r'platon.exe', '-u', self.cif_fileobj.name], startupinfo=si)
        except FileNotFoundError:
            print('Platon not found.')
        # waiting for chk file to appear:
        while not chkfile.is_file():
            timeticks = timeticks + 1
            print('not there', timeticks)
            sleep(0.01)
            if timeticks > 500:
                print('Platon statup took too long. Killing Platon...')
                try:
                    print('terminating platon1')
                    plat.terminate()
                except Exception as e:
                    print(e)
        size1 = chkfile.stat().st_size
        size2 = 99999999
        timeticks = 0
        # waiting until size does not increase anymore:
        while size1 <= size2:
            timeticks = timeticks + 1
            size2 = chkfile.stat().st_size
            print(size1, size2)
            sleep(0.2)
            size1 = chkfile.stat().st_size
            if timeticks > 50:  # 10s
                try:
                    print('terminating platon2')
                    plat.terminate()
                except Exception:
                    pass
        try:
            plat.terminate()
        except Exception:
            pass

    def __repr__(self):
        return 'Platon:\n{}'.format(self.formula_moiety)


if __name__ == '__main__':
    print('###############\n\n')
    s = PlatonOut(Path(r'D:\\frames\\guest\\Esser_JW283\\Esser_JW283'))
    print(s)
