"""
:: Moiety_Formula = C24 H27 Au Cl N P, C H2 Cl2, Cl
"""
#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
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
from time import sleep
from typing import Union

from PyQt5.QtCore import QThread


class Platon(QThread):
    def __init__(self, cif: Path, timeout: int = 300, cmdoption='-u'):
        """
        Option -u is for checkcif 
        """
        super().__init__()
        self.cmdoption = cmdoption
        self.timeout = timeout
        self.cif_path = cif
        self.chkfile = Path(self.cif_path.with_suffix('.chk'))
        self.platon_output = ''
        self.chk_file_text = ''
        self.formula_moiety = ''
        self.Z = ''
        self.delete_orphaned_files()
        self.plat: Union[subprocess.CompletedProcess, bool] = True

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
                    '.sum', '.hkp', '.pjn', '.bin', '.spf']:
            try:
                file = self.cif_path.resolve().with_suffix(ext)
                if file.stat().st_size < 100:
                    file.unlink()
                if file.suffix in ['.sar', '.spf', '.ckf']:
                    file.unlink()
            except FileNotFoundError:
                # print('##')
                pass

    def parse_chk_file(self):
        """
        """
        try:
            self.chk_file_text = self.chkfile.read_text(encoding='ascii', errors='ignore')
        except FileNotFoundError as e:
            print('CHK file not found:', e)
            self.chk_file_text = ''
        for num, line in enumerate(self.chk_file_text.splitlines(keepends=False)):
            if line.startswith('# MoietyFormula'):
                self.formula_moiety = ' '.join(line.split(' ')[2:])
            if line.startswith('# Z'):
                self.Z = line[19:24].strip(' ')

    @property
    def platon_exe(self):
        if sys.platform.startswith('win'):
            in_pwt = r'C:\pwt\platon.exe'
        else:
            in_pwt = 'platon'
        if Path(in_pwt).exists():
            return in_pwt
        else:
            return 'platon'

    def run(self):
        """
        Runs the platon thread.
        """
        curdir = Path(os.curdir).resolve()
        with suppress(FileNotFoundError):
            self.cif_path.with_suffix('.vrf').unlink()
        with suppress(FileNotFoundError):
            self.chkfile.unlink()
        os.chdir(str(self.cif_path.absolute().parent))
        try:
            print('running local platon on', self.cif_path.name)
            self.plat = subprocess.run([self.platon_exe, self.cmdoption, self.cif_path.name],
                                       startupinfo=self.hide_status_window(),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=False,
                                       env=os.environ,
                                       timeout=self.timeout)
        except TimeoutExpired:
            print('PLATON timeout!')
            self.platon_output = 'PLATON timeout!'
            pass
        except Exception as e:
            print('Could not run local platon:' + str(e))
            self.platon_output = str(e)
        if self.plat and hasattr(self.plat, 'stdout'):
            self.platon_output = self.plat.stdout.decode('ascii')
        # self.delete_orphaned_files()
        os.chdir(curdir)

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
    p.start()
    sleep(15)
    p.exit()
    p.kill()
