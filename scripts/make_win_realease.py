#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
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
from datetime import date, datetime
from pathlib import Path

from PyQt5 import uic

from tools.version import VERSION

iss_file = r'scripts\finalcif-install_win64.iss'

try:
    arg = sys.argv[1]
except IndexError:
    arg=''

def disable_debug(filepath: str):
    pth = Path(filepath)
    file = pth.read_text(encoding="UTF-8", errors='ignore').split("\n")
    for num, line in enumerate(file):
        if line.startswith("DEBUG") or line.startswith("PROFILE"):
            l = line.split()
            print("DEBUG/PROFILE.. {}, {}".format(l[2], filepath))
            l[2] = '{}'.format("False")
            file[num] = " ".join(l)
            continue
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


def copy_to_remote():
    print('copying file')
    print(r'dist\FinalCif.exe', r'W:\htdocs\finalcif\FinalCif-v{}.exe'.format(VERSION))
    shutil.copy(r'dist\FinalCif.exe', r'W:\htdocs\finalcif\FinalCif-v{}.exe'.format(VERSION))
    Path(r'W:\htdocs\finalcif\version.txt').write_text(str(VERSION))

def update_installation():
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

disable_debug('finalcif.py')

recompile_ui()

print(arg)

process_iss(iss_file)

if arg == 'copy':
    subprocess.run(r""".\venv\Scripts\pyinstaller.exe -D Finalcif_installer.spec --clean -y""".split())
    #copy_to_remote()
    update_installation()
else:
    subprocess.run(r""".\venv\Scripts\pyinstaller.exe -D Finalcif_installer.spec --clean -y""".split())

    innosetup_compiler = r'D:/Program Files (x86)/Inno Setup 5/ISCC.exe'
    # Run 64bit setup compiler
    subprocess.run([innosetup_compiler, iss_file, ])

print('Created version: {}'.format(VERSION))
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))