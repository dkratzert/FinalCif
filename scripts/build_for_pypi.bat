call venv\Scripts\activate.bat
del /Q dist\*
del /q /s FinalCif.egg-info
python.exe -m pip install --upgrade pip
pip install --upgrade setuptools

venv\Scripts\python -m build
