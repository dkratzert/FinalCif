#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -D     # one dir

# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F     # one file
# copy dist\FinalCif.exe W:\htdocs\finalcif
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
    file = pth.read_text(encoding="UTF-8", errors='ignore').split("\n")
    for num, line in enumerate(file):
        if line.startswith("DEBUG") or line.startswith("PROFILE"):
            l = line.split()
            print("DEBUG/PROFILE.. {}, {}".format(l[2], filepath))
            l[2] = '{}'.format("False")
            file[num] = " ".join(l)
    iss_file = "\n".join(file)
    pth.write_text(iss_file, encoding="UTF-8")


def make_shasum(filename):
    sha = sha512_checksum_of_file(filename)
    shafile = Path('scripts/Output/FinalCif-setup-x64-v{}-sha512.sha'.format(VERSION))
    shafile.unlink(missing_ok=True)
    shafile.write_text(sha)
    print("SHA512: {}".format(sha))


def process_iss(filepath):
    pth = Path(filepath)
    iss_file = pth.read_text(encoding="UTF-8").split("\n")
    for num, line in enumerate(iss_file):
        if line.startswith("#define MyAppVersion"):
            l = line.split()
            l[2] = '"{}"'.format(VERSION)
            iss_file[num] = " ".join(l)
            break
    iss_file = "\n".join(iss_file)
    print("windows... {}, {}".format(VERSION, filepath))
    pth.write_text(iss_file, encoding="UTF-8")


def make_executable():
    pyin = subprocess.run("venv/Scripts/pyinstaller.exe Finalcif_installer_win.spec --clean -y".split())
    if pyin.returncode != 0:
        print('Pyinstaller failed with exit code', pyin.returncode)
        sys.exit()


def make_installer():
    innosetup_compiler = r'C:/Program Files (x86)/Inno Setup 6/ISCC.exe'
    subprocess.run([innosetup_compiler, iss_file, ])
    make_shasum("scripts/Output/FinalCif-setup-x64-v{}.exe".format(VERSION))
    print('Created version: {}'.format(VERSION))
    print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))


if __name__ == '__main__':
    iss_file = 'scripts/finalcif-install_win64.iss'

    compile_ui()

    disable_debug('finalcif/appwindow.py')

    os.chdir(application_path)

    process_iss(iss_file)

    # create executable
    make_executable()
    # Run 64bit Inno setup compiler
    make_installer()

    subprocess.call("scripts/Output/FinalCif-setup-x64-v{}.exe".format(VERSION))
