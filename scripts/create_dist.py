from pathlib import Path
import shutil
import subprocess
import urllib.request
import zipfile
import os

"""
This file is not ready to work fine!!!
"""

PYTHON_VERSION = "3.11.5"
PYTHON_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"

SCRIPT_DIR = Path(__file__).resolve().parent
BUILD_DIR = (SCRIPT_DIR.parent / "dist").resolve()
PACKAGE_DIR = BUILD_DIR / "python_dist"


def create_build_and_package_directories():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(PACKAGE_DIR, ignore_errors=True)
    PACKAGE_DIR.mkdir()


def download_python_embeddable_package():
    python_zip_path = BUILD_DIR / f"python-{PYTHON_VERSION}.zip"
    urllib.request.urlretrieve(PYTHON_URL, python_zip_path)

    with zipfile.ZipFile(python_zip_path, 'r') as zip_ref:
        zip_ref.extractall(PACKAGE_DIR)
    python_zip_path.unlink()


def modify_pth_file():
    short_python_version = PYTHON_VERSION.replace('.', '')[:-1]
    _pth_content = [
        f"python{short_python_version}.zip",
        ".",
        "import site"
    ]
    _pth_path = PACKAGE_DIR / f"python{short_python_version}._pth"
    _pth_path.write_text('\n'.join(_pth_content))


def download_vc_redist():
    vc_redist_url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
    vc_redist_path = BUILD_DIR / "vc_redist.x64.exe"
    result = urllib.request.urlretrieve(vc_redist_url, vc_redist_path)
    print(result)


def setup_python_environment():
    os.chdir(PACKAGE_DIR)
    urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
    subprocess.run(["python", "get-pip.py"], shell=True)
    os.remove("get-pip.py")

    subprocess.run(["python", "-m", "pip", "install", "virtualenv"], shell=True)
    subprocess.run(["python", "-m", "virtualenv", "venv", "--clear", "--no-periodic-update"], shell=True)
    activate_script = os.path.join("venv", "Scripts", "activate.bat")
    subprocess.run([activate_script], shell=True)

    requirements_txt = SCRIPT_DIR.parent / "requirements.txt"
    subprocess.run(["pip", "install", "-r", str(requirements_txt)], shell=True)

    os.chdir(SCRIPT_DIR.parent)


if __name__ == '__main__':
    create_build_and_package_directories()
    download_python_embeddable_package()
    modify_pth_file()
    download_vc_redist()
    setup_python_environment()
