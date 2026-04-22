@echo on

REM Execute me from the main directory

set PYTHON_VERSION=3.14.4

REM Check if uv is available, install if missing
where uv >NUL 2>&1
if %errorlevel% neq 0 (
    echo uv not found, installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

rmdir /S /Q dist 2>NUL
rmdir /S /Q build 2>NUL

call scripts\_create_dist.bat %PYTHON_VERSION%
if %errorlevel% neq 0 (
    echo _create_dist.bat failed. Stopping now.
    exit /b %errorlevel%
)
