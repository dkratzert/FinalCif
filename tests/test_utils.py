import os
from pathlib import Path


def current_file_path():
    os.chdir(Path(__file__).resolve().parent.parent)
