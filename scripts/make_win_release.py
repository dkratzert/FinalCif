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
from datetime import datetime
from pathlib import Path

application_path = Path(os.path.abspath(__file__)).parent.parent

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(application_path))

from scripts.compile_ui_files import compile_ui
from finalcif.tools.misc import sha512_checksum_of_file
from finalcif import VERSION


def disable_debug(filepath: str):
    pth = Path(filepath)
    file_lst = pth.read_text(encoding="UTF-8", errors='ignore').split("\n")
    for num, line in enumerate(file_lst):
        if line.startswith("DEBUG") or line.startswith("PROFILE"):
            l = line.split()
            print(f"DEBUG/PROFILE.. {l[2]}, {filepath}")
            l[2] = '{}'.format("False")
            file_lst[num] = " ".join(l)
    pth.write_text("\n".join(file_lst), encoding="UTF-8")


def make_shasum(filename):
    sha = sha512_checksum_of_file(filename)
    shafile = Path(f'scripts/Output/FinalCif-setup-x64-v{VERSION}-sha512.sha')
    shafile.unlink(missing_ok=True)
    shafile.write_text(sha)
    print(f"SHA512: {sha}")


def make_installer(iss_file: str):
    innosetup_compiler = r'D:\Programme\Inno Setup 6/ISCC.exe'
    innosetup_compiler2 = r'C:\Program Files (x86)\Inno Setup 6/ISCC.exe'
    if not Path(innosetup_compiler).exists():
        innosetup_compiler = innosetup_compiler2
    subprocess.run([innosetup_compiler, '/Qp', f'/dMyAppVersion={VERSION}', iss_file], check=False)


def compile_python_files():
    import compileall
    compileall.compile_dir(dir='dist', workers=2, force=True, quiet=True)
    compileall.compile_dir(dir='finalcif', workers=2, force=True, quiet=True)


if __name__ == '__main__':
    iss_file = 'scripts/finalcif-install_win64.iss'

    compile_ui()
    compile_python_files()
    disable_debug('finalcif/appwindow.py')

    os.chdir(application_path)

    make_installer(iss_file)

    make_shasum(f"scripts/Output/FinalCif-setup-x64-v{VERSION}.exe")

    print(f'Created version: {VERSION}')
    print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    subprocess.call([f"scripts/Output/FinalCif-setup-x64-v{VERSION}.exe", '/SILENT'])
