
source venv/bin/activate

pip3 install -r requirements.txt

pyinstaller Finalcif_onefile.spec --clean -y
