
REM execute me from the main directory

rmdir /S dist /Q
rmdir /S build /Q

CALL venv\Scripts\activate.bat

git restore *
git switch last_win_7
git pull

venv\Scripts\python -m pip install -U pip
venv\Scripts\python -m pip install wheel
venv\Scripts\python -m pip install -U pyinstaller
venv\Scripts\python -m pip install -U pyinstaller-hooks-contrib

CALL C:\Users\daniel\Documents\sign_bootloader.bat

venv\Scripts\pip3.exe install -r requirements.txt -U

venv\Scripts\python.exe scripts\make_win_release.py