#!/bin/bash

# Ubuntu installer script
#
# This script either installs FinalCif vom the source repository or simply runs FinalCif.
# Prior to installation, a recent Python version is needed.
# Everything (except Python3) is installed below the ./FinalCif directory and nowhere else.
# This script might work in other Linux distributions, except for the -pyinst option.
#
# Commandline Options:
#
# ./finalcif-start.sh [-option]
#
# -pyinst  :  Adds a Python repository (deadsnakes) and installs Python3.9
# -install :  Install FinalCif from GitHub. The installer asks about the version number to install.
#             Use 'trunk' as version to get the most recent unstable source code.
#
# without any option: Run FinalCif
#

if [ ! "$(which python3.9)" ] && [ ! "$1" == "-pyinst" ]; then
  echo You need to install Python3.9 first:
  echo
  echo ./finalcif-start.sh -pyinst
  echo "This will add the deadsnakes repository to your installation: https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa"
  exit
fi

if [ "$1" == "-pyinst" ]; then
  # Add python repository and install new Python3.9
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt install python3.9
  sudo apt install python3.9-venv
  exit
fi

if [ "$1" == "-install" ]; then
  echo
  echo Which version number of FinalCif should be installed? Use a number like 91 or 'trunk' for the latest unstable source.
  read version
  # Get the FinalCif code:
  if [ "$version" == "trunk" ]; then
    git clone --depth 1 https://github.com/dkratzert/FinalCif.git
  else
    git clone --depth 1 --branch Version-$version https://github.com/dkratzert/FinalCif.git
  fi
fi

# Create a virtual environment and activate it:
if [ ! -d "./FinalCif" ]; then
  echo FinalCif is not installed here.
  echo Install it with \"./finalcif-start.sh -install\"
  exit
fi

cd FinalCif || echo FinalCif not found
python3.9 -m venv venv
source venv/bin/activate

if [ "$1" == "-install" ]; then
  # Install required Python packages:
  venv/bin/pip install pip -U
  venv/bin/pip install -r requirements.txt -U
  echo ""
  echo Installation finished! Run FinalCif with './finalcif-start.sh'
  exit
fi

# Finally, run FinalCif
echo Running FinalCif ...
python3 finalcif.py
