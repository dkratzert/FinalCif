@echo on

REM This script builds a working Python environment into ..\dist of the current file location.

REM Set the Python version here:
set PYTHON_VERSION=3.11.5

set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip

for %%A in ("%~dp0.") do set "SCRIPT_DIR=%%~fA"
set BUILD_DIR=%SCRIPT_DIR%\..\dist
set PACKAGE_DIR=%BUILD_DIR%\python_dist


setlocal enabledelayedexpansion
for %%a in (!PYTHON_VERSION!) do (
    set "NEW_PYTHON_VERSION=%%~na"
)
set "SHORT_PYTHON_VERSION=!NEW_PYTHON_VERSION:.=!"

mkdir %BUILD_DIR%
cd %BUILD_DIR%

curl %PYTHON_URL% -o python-%PYTHON_VERSION%.zip

del /S /Q /F %PACKAGE_DIR%\*.* >NUL
rmdir %PACKAGE_DIR%
mkdir %PACKAGE_DIR%

tar -xf python-%PYTHON_VERSION%.zip -C %PACKAGE_DIR%
del python-%PYTHON_VERSION%.zip

echo python%SHORT_PYTHON_VERSION%.zip > %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
echo . >> %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
echo import site >> %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
endlocal

del vc_redist.x64.exe

rem curl -L https://aka.ms/vs/17/release/vc_redist.x64.exe -o vc_redist.x64.exe
rem vc_redist.x64.exe /passive /quiet /install

cd %PACKAGE_DIR%

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

python -m pip install virtualenv
python -m virtualenv venv
call venv\Scripts\activate.bat

call pip install -r %SCRIPT_DIR%\..\requirements.txt

cd %SCRIPT_DIR%\..

rem call run_finalcif.bat

rem * zip the python-dist dir (in inno setup)
rem * add Github/FinalCif/finalcif/* and FinalCif/run_finalcif.bat
rem * add update.exe
rem * add a C++ start program finalcif.exe
rem * install ms vc_redist with inno setup