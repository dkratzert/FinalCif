import os
import sys
from pathlib import Path
from shutil import which


def current_file_path():
    os.chdir(Path(__file__).resolve().parent.parent)


def get_platon_exe() -> str:
    if sys.platform.startswith('win'):
        platon_exe = r'C:\pwt\platon.exe'
    else:
        platon_exe = which('platon')
    return platon_exe