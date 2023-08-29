@echo off


set PYTHON_VERSION="3.11.5"

curl https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip -o python-%PYTHON_VERSION%.zip

del /S /Q python_dist\* >NUL
rmdir python_dist
mkdir python_dist

tar -xf python-%PYTHON_VERSION%.zip -C python_dist

echo python311.zip > python_dist\python311._pth
echo . >> python_dist\python311._pth
echo import site >> python_dist\python311._pth

del vc_redist.x64.exe

rem curl -L https://aka.ms/vs/17/release/vc_redist.x64.exe -o vc_redist.x64.exe
rem vc_redist.x64.exe /passive /quiet /install

cd python_dist

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

python -m pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate.bat

pip install -r ..\..\requirements.txt

cd ..\..

run_finalcif.bat