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
import shutil
import subprocess

from tools.version import VERSION

subprocess.run(r""".\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F --clean""".split())

print('copying file')
print(r'dist\FinalCif.exe', r'W:\htdocs\finalcif')
shutil.copy(r'dist\FinalCif.exe', r'W:\htdocs\finalcif\FinalCif-v{}.exe'.format(VERSION))
