
REM execute me from the main directory

CALL venv\Scripts\activate.bat

venv\Scripts\pip.exe install pip -U

venv\Scripts\pip.exe install -r requirements.txt

venv\Scripts\python.exe scripts\make_win_release.py