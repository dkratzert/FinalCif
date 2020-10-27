
REM execute me from the main directory

rem .\venv\Scripts\activate

pip install -r requirements.txt

rem ### Not used anymore, because of python version:
rem pyinstaller.exe -D Finalcif_installer.spec --clean -y
rem "c:\Program Files (x86)\Inno Setup 6\ISCC.exe" scripts\finalcif-install_win64.iss


venv\Scripts\python.exe scripts\make_win_release.py