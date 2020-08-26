import os
import sys


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    # noinspection PyProtectedMember
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
