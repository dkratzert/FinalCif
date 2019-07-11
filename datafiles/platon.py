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
from subprocess import Popen, TimeoutExpired, PIPE
import sys
from pathlib import Path
from time import sleep


class Platon():
    def __init__(self, file: Path):
        self.cif_fileobj = file
        curdir = Path(os.curdir).absolute()
        self.chkfile = Path(self.cif_fileobj.stem + '.chk')
        self.vrf_file = Path(self.cif_fileobj.stem + '.vrf')
        try:
            self.chkfile.unlink()
        except (ValueError, FileNotFoundError):
            pass
        try:
            self.vrf_file.unlink()
        except (ValueError, FileNotFoundError):
            pass
        os.chdir(self.cif_fileobj.absolute().parent)
        self.platon_output = ''
        try:
            self.run_platon(self.chkfile)
        except Exception as e:
            print('Platon failed to run:')
            print(e)
            return
        try:
            self.chk_file_text = self.chkfile.read_text(encoding='ascii', errors='ignore')
        except FileNotFoundError:
            self.chk_file_text = ''
        try:
            self.vrf_txt = self.vrf_file.read_text(encoding='ascii')
        except FileNotFoundError:
            self.vrf_txt = ''
        self.formula_moiety = ''
        self.Z = ''
        self.parse_file()
        # delete orphaned files:
        for ext in ['.ckf', '.fcf', '.def', '.lis', '.sar', '.ckf', '.sum', '.hkp', '.pjn', '.bin', '_pl.res',
                    '_pl.spf']:
            try:
                file = Path(self.cif_fileobj.stem + ext)
                if file.stat().st_size < 100:
                    file.unlink()
                if file.suffix in ['.sar', '_pl.res', '_pl.spf', '.ckf']:
                    file.unlink()
            except FileNotFoundError:
                print('##')
                pass
        os.chdir(curdir.absolute())

    def parse_file(self):
        """
        """
        for num, line in enumerate(self.chk_file_text.splitlines(keepends=False)):
            if line.startswith('# MoietyFormula'):
                self.formula_moiety = ' '.join(line.split(' ')[2:])
            if line.startswith('# Z'):
                self.Z = line[19:24].strip(' ')

    def run_platon(self, chkfile: Path):
        """
        >>> fname = Path(r'/Users/daniel/GitHub/FinalCif/test-data/DK_zucker2_0m.cif')
        >>> Platon(fname)
        Platon:
        C12 H22 O11
        """
        plat = None
        os.chdir(self.cif_fileobj.absolute().parent)
        timeticks = 0
        try:
            # This is only available on windows:
            si = subprocess.STARTUPINFO()
            si.dwFlags = 1
            si.wShowWindow = 0
        except AttributeError:
            si = None
        try:
            print('trying local platon')
            with Popen([r'platon', '-u', self.cif_fileobj.name], 
                       startupinfo=si, stdout=PIPE, stderr=PIPE, shell=True, env=os.environ) as plat:
                try:
                    stdout, stderr = plat.communicate(sys.stdin, timeout=20)
                except TimeoutExpired:
                    print('Terminating platon (1)')
                    plat.terminate()
                    stdout, stderr = plat.communicate()
                    # waiting until size does not increase anymore:
                size1 = chkfile.stat().st_size
                size2 = 99999999
                timeticks = 0
                while size1 <= size2:
                    timeticks = timeticks + 1
                    size2 = chkfile.stat().st_size
                    # print(size1, size2)
                    sleep(0.1)
                    size1 = chkfile.stat().st_size
                    if timeticks > 10:
                        try:
                            #print('Platon took too much time, terminating platon. (2)')
                            plat.terminate()
                            break
                        except Exception:
                            pass
                            break
            output = stdout.decode('ascii')
            if output:
                self.platon_output = output.strip()
        except Exception as e:
            print('Could not run local platon:', e)
            self.platon_output = str(e)
            return
        #self.platon_output = plat.stdout.decode('ascii')
        #self.platon_output += plat.stderr.decode('ascii')
        # a fresh platon exe from the web:
        # this runs only wif salflibc.dll. I have to find a solution to download it.
        # Here is the link to salflib: http://www.chem.gla.ac.uk/~louis/software/dll/salflibc.dll
        # pexe = get_platon()

    def __repr__(self):
        return 'Platon:\n{}'.format(self.formula_moiety)


if __name__ == '__main__':
    os.chdir("/Users/daniel/GitHub")
    fname = Path(r'/Users/daniel/GitHub/FinalCif/test-data/DK_zucker2_0m.cif')
    s = Platon(fname)
    print(s)
    print(s.chkfile)
    # print(s.chk_file_text)
    # chkfile = Path(fname.stem + '.chk')
    # chkfile.unlink()
