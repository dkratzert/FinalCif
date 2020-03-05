


rem .\venv\Scripts\activate

pip install -r requirements.txt

pyinstaller.exe -D Finalcif_installer.spec --clean -y

"c:\Program Files (x86)\Inno Setup 6\ISCC.exe" scripts\finalcif-install_win64.iss