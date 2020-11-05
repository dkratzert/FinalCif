
REM execute me from the main directory

CALL venv\Scripts\activate.bat

pip install pip -U

pip install -r requirements.txt

venv\Scripts\python.exe scripts\make_win_release.py