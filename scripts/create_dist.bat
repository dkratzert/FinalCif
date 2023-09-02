@echo off

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
rmdir /s /q %PACKAGE_DIR%
dir "%PACKAGE_DIR%" | findstr /v "\<.*\>"
if not errorlevel 1 (
    echo Directory is not empty.
    exit /b
) else (
    echo Package dir is empty
)
mkdir %PACKAGE_DIR%

tar -xf python-%PYTHON_VERSION%.zip -C %PACKAGE_DIR%
del python-%PYTHON_VERSION%.zip

echo python%SHORT_PYTHON_VERSION%.zip > %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
echo . >> %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
echo import site >> %PACKAGE_DIR%\python%SHORT_PYTHON_VERSION%._pth
endlocal

del vc_redist.x64.exe

curl -L https://aka.ms/vs/17/release/vc_redist.x64.exe -o vc_redist.x64.exe
rem vc_redist.x64.exe /passive /quiet /install

cd %PACKAGE_DIR%

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rem del get-pip.py

rem python -m pip install virtualenv
rem python -m virtualenv venv --clear --no-periodic-update
mkdir _venv
mkdir _venv\scripts\nt
curl -L https://github.com/python/cpython/raw/3.11/Lib/venv/__init__.py -o _venv\__init__.py
curl -L https://github.com/python/cpython/raw/3.11/Lib/venv/__main__.py -o _venv\__main__.py
curl -L https://github.com/python/cpython/raw/3.11/Lib/venv/scripts/nt/activate.bat -o _venv\scripts\nt\activate.bat

python -m _venv venv
call venv\Scripts\activate.bat

call pip install -r %SCRIPT_DIR%\..\requirements.txt

cd %SCRIPT_DIR%\..
