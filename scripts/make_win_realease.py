# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -D     # one dir

# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F     # one file
# copy dist\FinalCif.exe W:\htdocs\finalcif
import shutil
import subprocess

subprocess.run(r""".\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F --clean""".split())

print('copying file')
print(r'dist\FinalCif.exe', r'W:\htdocs\finalcif')
shutil.copy(r'dist\FinalCif.exe', r'W:\htdocs\finalcif')
