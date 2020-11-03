
#source venv/bin/activate

pip3 install -r requirements.txt

pyinstaller Finalcif_mac.spec --clean -y
