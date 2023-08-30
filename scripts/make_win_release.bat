
REM execute me from the main directory

rmdir /S dist /Q
rmdir /S build /Q
del /S /Q *.pyc



rem git restore *
rem git switch master
rem git pull

rem venv\Scripts\python -m pip install -U pip
rem venv\Scripts\python -m pip install wheel
rem venv\Scripts\python -m pip install -U pyinstaller
rem venv\Scripts\python -m pip install -U pyinstaller-hooks-contrib

rem CALL C:\Users\daniel\Documents\sign_bootloader.bat

rem venv\Scripts\pip3.exe install -r requirements.txt -U

call create_dist.bat

CALL venv\Scripts\activate.bat
venv\Scripts\python.exe scripts\make_win_release.py
CALL venv\Scripts\deactivate.bat
cd scripts