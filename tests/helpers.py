#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import sys
from shutil import which
import unittest
from qtpy.QtWidgets import QApplication

addr = """Albert-Ludwigs-Universität Freiburg
Institut für Anorganische und Analytische Chemie
Albertstraße 21
Freiburg i. Br.
79104
Germany"""


def get_platon_exe() -> str:
    if sys.platform.startswith('win'):
        platon_exe = r'C:\pwt\platon.exe'
    else:
        platon_exe = which('platon')
    return platon_exe

class AppWindowTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        if hasattr(self, 'myapp') and getattr(self, 'myapp') is not None:
            self.myapp.close()
            self.myapp.deleteLater()
            self.myapp = None
        if hasattr(self, 'app') and getattr(self, 'app') is not None and type(self.app).__name__ == 'AppWindow':
            self.app.close()
            self.app.deleteLater()
            self.app = None
        qt_app = QApplication.instance()
        if qt_app is not None:
            qt_app.processEvents()
        super().tearDown()
