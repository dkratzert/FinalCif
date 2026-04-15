#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import sys
from shutil import which
import unittest

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
            try:
                self.myapp.close()
            except RuntimeError:
                pass
            self.myapp = None
        if hasattr(self, 'app') and getattr(self, 'app') is not None and type(self.app).__name__ == 'AppWindow':
            try:
                self.app.close()
            except RuntimeError:
                pass
            self.app = None
        super().tearDown()
