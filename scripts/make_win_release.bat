
REM execute me from the main directory

rmdir /S dist /Q
rmdir /S build /Q

rem git restore *
rem git switch master
rem git pull

call scripts\create_dist.bat

CALL venv\Scripts\activate.bat
rem venv\Scripts\python.exe scripts\create_dist.py
venv\Scripts\python.exe scripts\make_win_release.py
CALL venv\Scripts\deactivate.bat
cd scripts