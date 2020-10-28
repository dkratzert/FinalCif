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
import sys
from contextlib import suppress
from pathlib import Path
from subprocess import TimeoutExpired

from PyQt5.QtCore import QThread


class Platon(QThread):
    def __init__(self, cif: Path, timeout: int = 300):
        super().__init__()
        self.timeout = timeout
        self.cif_fileobj = cif
        self.chkfile = None
        self.platon_output = ''
        self.chk_file_text = ''
        self.formula_moiety = ''
        self.Z = ''
        self.delete_orphaned_files()

    def kill(self):
        if sys.platform.startswith('win'):
            with suppress(FileNotFoundError):
                subprocess.run(["taskkill", "/f", "/im", "platon.exe"], shell=False)
        if sys.platform[:5] in ('linux', 'darwi'):
            with suppress(FileNotFoundError):
                subprocess.run(["killall", "platon"], shell=False)

    def delete_orphaned_files(self):
        # delete orphaned files:
        for ext in ['.ckf', '.fcf', '.def', '.lis', '.sar', '.ckf',
                    '.sum', '.hkp', '.pjn', '.bin', '_pl.res', '_pl.spf']:
            try:
                file = Path(self.cif_fileobj.stem + ext)
                if file.stat().st_size < 100:
                    file.unlink()
                if file.suffix in ['.sar', '_pl.res', '_pl.spf', '.ckf']:
                    file.unlink()
            except FileNotFoundError:
                # print('##')
                pass

    def parse_chk_file(self):
        """
        """
        chkfile = Path(self.cif_fileobj.stem + '.chk')
        try:
            self.chk_file_text = chkfile.read_text(encoding='ascii', errors='ignore')
        except FileNotFoundError as e:
            print('CHK file not found:', e)
            self.chk_file_text = ''
        for num, line in enumerate(self.chk_file_text.splitlines(keepends=False)):
            if line.startswith('# MoietyFormula'):
                self.formula_moiety = ' '.join(line.split(' ')[2:])
            if line.startswith('# Z'):
                self.Z = line[19:24].strip(' ')

    def run(self):
        """
        Runs the platon thread.
        """
        curdir = Path(os.curdir).absolute()
        with suppress(FileNotFoundError):
            Path(self.cif_fileobj.stem + '.vrf').unlink()
        self.chkfile = Path(self.cif_fileobj.with_suffix('.chk'))
        with suppress(FileNotFoundError):
            self.chkfile.unlink()
        os.chdir(str(self.cif_fileobj.absolute().parent))
        try:
            print('running local platon on', self.cif_fileobj.name)
            subprocess.run([r'platon', '-u', self.cif_fileobj.name],
                           startupinfo=self.hide_status_window(),
                           shell=False, env=os.environ, timeout=self.timeout)
        except TimeoutExpired:
            print('PLATON timeout!')
            pass
        except Exception as e:
            print('Could not run local platon:' + str(e))
            self.platon_output = str(e)
        self.delete_orphaned_files()
        os.chdir(curdir.absolute())

    @staticmethod
    def hide_status_window():
        try:
            # This is only available on windows:
            si = subprocess.STARTUPINFO()
            si.dwFlags = 1
            si.wShowWindow = 0
        except AttributeError:
            si = None
        return si

    def __repr__(self):
        return 'Platon:\n{}'.format(self.formula_moiety)


if __name__ == '__main__':
    fname = Path('test-data/DK_zucker2_0m.cif')
    p = Platon(fname)
    p.run_platon()
