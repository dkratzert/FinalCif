@echo off

REM Installs the required packages to run the desktop application in Windows.
REM Change the path to the Python installation according to your needs:

call "c:\Program Files\Python39\python.exe" -m venv venv

call venv\Scripts\activate.bat
call venv\Scripts\python.exe -m pip install pip -U
call venv\Scripts\pip3.exe install -r requirements.txt

