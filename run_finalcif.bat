@ECHO OFF

REM Runs the FinalCif application

REM Before running this script, you probably need to run 'install_requirements.bat' one time.

TITLE "FinalCif"

set PYTHONPATH=%PYTHONPATH%;.
CALL venv\Scripts\activate.bat

venv\Scripts\python.exe finalcif\finalcif_start.py %*