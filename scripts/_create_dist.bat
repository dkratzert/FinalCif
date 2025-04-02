@echo off

REM This script builds a working Python environment into ..\dist of the current file location.

REM Set the Python version here:
set PYTHON_VERSION=3.12.9

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
rmdir /s /q %PACKAGE_DIR% > NUL
dir "%PACKAGE_DIR%" | findstr /v "\<.*\>" > NUL
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
del get-pip.py

set PYTHONPATH=%PACKAGE_DIR%
mkdir %PACKAGE_DIR%\Lib\site-packages > NUL

REM Not needed, because it just installs in local python path without venv:
rem python -m pip install virtualenv
rem python -m virtualenv venv --clear --no-periodic-update
rem call venv\Scripts\activate.bat

call Scripts\pip install -r %SCRIPT_DIR%\..\requirements.txt --no-warn-script-location
if %errorlevel% neq 0 (
    echo pip failed to install all packages. Stopping now.
    exit /b %errorlevel%
)

cd %SCRIPT_DIR%\..

echo - compiling python packages
%PACKAGE_DIR%\python.exe -m compileall -q .
echo - finished!