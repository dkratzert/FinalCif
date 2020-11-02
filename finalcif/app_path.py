import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    # noinspection PyProtectedMember
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    application_path = sys._MEIPASS
else:
    application_path = Path(os.path.abspath(__file__)).parent.parent
