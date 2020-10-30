import os
import sys
import time
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from finalcif import AppWindow
from tools.version import VERSION

app = QApplication(sys.argv)


class TestPlaton(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.myapp = AppWindow(Path('tests/examples/1979688.cif').absolute())
        self.myapp.hide()

    def tearDown(self) -> None:
        Path('1979688-finalcif.chk').unlink(missing_ok=True)
        Path('1979688-finalcif.ckf').unlink(missing_ok=True)
        Path('1979688-finalcif.cif').unlink(missing_ok=True)
        Path('1979688-finalcif.fcf').unlink(missing_ok=True)
        Path('check.def').unlink(missing_ok=True)
        Path('platon.out').unlink(missing_ok=True)

    def test_checkcif_offline(self):
        self.myapp.ui.CheckcifButton.click()
        timediff = int(Path('1979688-finalcif.chk').stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago

    def test_checkdef_contains_text(self):
        self.myapp.ui.CheckcifButton.click()
        self.assertEqual('FINALCIF V{}'.format(VERSION) in Path('1979688-finalcif.chk').read_text(), True)
