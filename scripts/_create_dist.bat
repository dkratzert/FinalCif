@echo off

REM This script builds a working Python environment into ..\dist of the current file location.

REM Accept PYTHON_VERSION as first argument, see make_win_release.bat
set PYTHON_VERSION=%~1

set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip

for %%A in ("%~dp0.") do set "SCRIPT_DIR=%%~fA"
set BUILD_DIR=%SCRIPT_DIR%\..\dist
set PACKAGE_DIR=%BUILD_DIR%\python_dist

REM Check if uv is available
where uv >NUL 2>&1
if %errorlevel% neq 0 (
    echo uv not found, installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%;%PACKAGE_DIR%\Scripts"
)

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

cd %SCRIPT_DIR%\..

REM Create a venv for the release build
rem uv venv --python %PYTHON_VERSION% .venv --clear

REM Install the project and its dependencies into the venv used by the release scripts
REM (uv pip install <dir> installs the project defined by pyproject.toml in that directory)
REM uv pip install --python .venv\Scripts\python.exe %SCRIPT_DIR%\..
REM if %errorlevel% neq 0 (
REM     echo uv pip install into .venv failed. Stopping now.
REM     exit /b %errorlevel%
REM )
REM Install all dependencies from pyproject.toml into the embedded Python
REM (uv pip install <dir> installs the project defined by pyproject.toml in that directory)
uv pip install --python "%PACKAGE_DIR%\python.exe" "%SCRIPT_DIR%\.." --link-mode=copy
if %errorlevel% neq 0 (
    echo uv pip install failed. Stopping now.
    exit /b %errorlevel%
)

REM Remove the FinalCif package itself (it's provided in-tree, not as an installed package)
uv pip uninstall --python "%PACKAGE_DIR%\python.exe" finalcif ipython ruff ty

echo - finished environment install!

CALL "%PACKAGE_DIR%\python.exe" "%SCRIPT_DIR%\_make_win_release.py"