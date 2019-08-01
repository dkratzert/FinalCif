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
from pathlib import Path

from PyQt5 import uic

from tools.version import VERSION


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


disable_debug('finalcif.py')

recompile_ui()

subprocess.run(r""".\venv\Scripts\pyinstaller.exe Finalcif.spec -F --clean""".split())

print('copying file')

#print(r'dist\FinalCif.exe', r'W:\htdocs\finalcif\FinalCif-v{}.exe'.format(VERSION))

shutil.copy(r'dist\FinalCif.exe', r'W:\htdocs\finalcif\FinalCif-v{}.exe'.format(VERSION))
