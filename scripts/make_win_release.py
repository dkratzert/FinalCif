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
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

application_path = Path(os.path.abspath(__file__)).parent.parent

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(application_path))

from PyQt5 import uic

from finalcif.tools.misc import sha512_checksum_of_file
from finalcif.tools.version import VERSION

iss_file = 'scripts/finalcif-install_win64.iss'

try:
    arg = sys.argv[1]
except IndexError:
    arg = ''


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


def recompile_ui():
    try:
        print(os.path.abspath('./gui'))
        uic.compileUiDir('./gui')
        print('recompiled ui')
    except:
        print("Unable to compile UI!")
        raise


def make_shasum(filename):
    sha = sha512_checksum_of_file(filename)
    shafile = Path('scripts/Output/FinalCif-setup-x64-v{}-sha512.sha'.format(VERSION))
    shafile.unlink(missing_ok=True)
    shafile.write_text(sha)
    print("SHA512: {}".format(sha))


def copy_dist_to_install_dir():
    print('copying files')
    shutil.copytree(r'dist/FinalCif', r'C:\Program Files\FinalCif', dirs_exist_ok=True)


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


recompile_ui()

disable_debug('appwindow.py')

os.chdir(application_path)

print(arg)

process_iss(iss_file)

if arg == 'copy':
    subprocess.run("venv/Scripts/pyinstaller.exe -D Finalcif_installer_win.spec --clean -y".split())
    # this copies the content of the dist directory to the install directory
    copy_dist_to_install_dir()
else:
    # create executable
    pyin = subprocess.run("venv/Scripts/pyinstaller.exe -D Finalcif_installer_win.spec --clean -y".split())
    if pyin.returncode != 0:
        print('Pyinstaller failed with exit code', pyin.returncode)
        sys.exit()
    # Run 64bit Inno setup compiler
    innosetup_compiler = r'C:/Program Files (x86)/Inno Setup 6/ISCC.exe'
    subprocess.run([innosetup_compiler, iss_file, ])

make_shasum("scripts/Output/FinalCif-setup-x64-v{}.exe".format(VERSION))
print('Created version: {}'.format(VERSION))
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

subprocess.call("scripts/Output/FinalCif-setup-x64-v{}.exe".format(VERSION))