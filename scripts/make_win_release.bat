
cd ..

.\venv\Scripts\activate

pip install -r ..\requirements.txt

.\venv\Scripts\pyinstaller.exe -D Finalcif_installer.spec --clean -y