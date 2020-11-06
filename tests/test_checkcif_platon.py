import os
import sys
import time
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow
from tools.version import VERSION

app = QApplication(sys.argv)


class TestPlatonCheckCIF(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.myapp = AppWindow(Path('tests/examples/1979688.cif').absolute())
        self.myapp.hide()

    def tearDown(self) -> None:
        Path('checkcif-1979688-finalcif.html').unlink(missing_ok=True)
        Path('1979688-finalcif.chk').unlink(missing_ok=True)
        Path('1979688-finalcif.ckf').unlink(missing_ok=True)
        Path('1979688-finalcif.vrf').unlink(missing_ok=True)
        Path('1979688-finalcif.cif').unlink(missing_ok=True)
        Path('1979688-finalcif.gif').unlink(missing_ok=True)
        Path('1979688-finalcif.fcf').unlink(missing_ok=True)
        Path('1979688.ckf').unlink(missing_ok=True)
        Path('1979688.chk').unlink(missing_ok=True)
        Path('check.def').unlink(missing_ok=True)
        Path('platon.out').unlink(missing_ok=True)
        Path('examples/work/platon.out').unlink(missing_ok=True)
        Path('examples/work/check.def').unlink(missing_ok=True)

    def test_checkcif_offline(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        timediff = int(Path('1979688-finalcif.chk').stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago

    def test_checkdef_contains_text(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        time.sleep(0.3)
        self.assertEqual('FINALCIF V{}'.format(VERSION) in Path('1979688-finalcif.chk').read_text(), True)

    def test_offline_checkcif_writes_gif(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        self.assertFalse(Path('1979688-finalcif.gif').exists())
