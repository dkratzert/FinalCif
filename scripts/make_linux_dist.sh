
#REM execute me from the main directory

source venv/bin/activate

pip install pip -U

pip3 install -r requirements.txt

pyinstaller Finalcif_onefile.spec --clean -y
