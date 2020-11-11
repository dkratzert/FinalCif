#REM execute me from the main directory
git pull

source venv/bin/activate

DISTR="linux"
if cat /etc/os-release |grep -c "ubuntu" -gt 0; then
  DISTR="ubuntu"
fi
if cat /etc/os-release |grep -c "suse" -gt 0; then
  DISTR="opensuse"
fi

pip install pip -U

pip3 install -r requirements.txt

pyinstaller Finalcif_onefile.spec --clean -y

VER=$(cat tools/version.py | grep VERSION | cut -d ' ' -f 3)

mv dist/FinalCif "dist/FinalCif-v${VER}_${DISTR}"

echo "FinalCif version ${VER} finished"
