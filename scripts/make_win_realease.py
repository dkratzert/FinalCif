# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -D     # one dir

# .\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F     # one file
# copy dist\FinalCif.exe W:\htdocs\finalcif
import subprocess

subprocess.run(r""".\venv\Scripts\pyinstaller.exe scripts\Finalcif.spec -F --clean""".split())

subprocess.run(r"copy dist\FinalCif.exe W:\htdocs\finalcif".split())
