
REM execute me from the main directory

CALL venv\Scripts\activate.bat

venv\Scripts\python -m pip install -U pip

venv\Scripts\pip3.exe install -r requirements.txt

venv\Scripts\python.exe scripts\make_win_release.py