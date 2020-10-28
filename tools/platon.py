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
from contextlib import suppress
from pathlib import Path
from subprocess import TimeoutExpired

from PyQt5.QtCore import QThread


class Platon(QThread):
    def __init__(self, cif: Path):
        super().__init__()
        self.cif_fileobj = cif
        self.vrf_file = Path(self.cif_fileobj.stem + '.vrf')
        self.chkfile = None
        try:
            self.vrf_file.unlink()
        except (ValueError, FileNotFoundError):
            pass
        self.platon_output = ''
        self.chk_file_text = ''
        self.formula_moiety = ''
        self.Z = ''
        self.vrf_txt = ''
        self.delete_orphaned_files()

    def kill(self):
        subprocess.run(["taskkill", "/f", "/im", "platon.exe"])

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
        >>> fname = Path(r'./tests/examples/1979688.cif')
        >>> p = Platon(fname)
        >>> p.run_platon()
        trying local platon on 1979688.cif
        >>> p.formula_moiety
        C12 H22 O11
        """
        curdir = Path(os.curdir).absolute()
        self.chkfile = Path(self.cif_fileobj.with_suffix('.chk'))
        with suppress(FileNotFoundError):
            self.chkfile.unlink()
        os.chdir(str(self.cif_fileobj.absolute().parent))
        try:
            print('running local platon on', self.cif_fileobj.name)
            subprocess.call([r'platon', '-u', self.cif_fileobj.name],
                            startupinfo=None,
                            shell=False, env=os.environ, timeout=30)
        except TimeoutExpired:
            pass
        except Exception as e:
            print('Could not run local platon:' + str(e))
            self.platon_output = str(e)
        with suppress(FileNotFoundError):
            self.vrf_txt = self.vrf_file.read_text(encoding='ascii')
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
