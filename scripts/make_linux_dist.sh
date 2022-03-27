#!/bin/bash
#REM execute me from the main directory
git pull

source venv/bin/activate

DISTR="linux"
OS_RELEASE="$(cat /etc/os-release)"

if echo $OS_RELEASE | grep -q "ubuntu"; then
  DISTR="ubuntu"
fi
if echo $OS_RELEASE | grep -q "suse"; then
  DISTR="opensuse"
fi


/venv/bin/pip install pip -U

/venv/bin/pip install -r requirements.txt -U

/venv/bin/pyinstaller Finalcif_linux_onefile.spec --clean -y

VER=$(cat finalcif/__init__.py | grep VERSION | cut -d ' ' -f 3)

mv dist/FinalCif "dist/FinalCif-v${VER}_${DISTR}"

echo "FinalCif version ${VER} finished"
