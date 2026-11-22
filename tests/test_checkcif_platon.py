import os

import time
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from finalcif import VERSION
from finalcif.appwindow import AppWindow
from tests.helpers import get_platon_exe

data = Path('tests')


filenames = (
    data / 'examples/checkcif-1979688-finalcif.html',
    data / 'examples/1979688-finalcif.chk',
    data / 'examples/1979688-finalcif.ckf',
    data / 'examples/1979688-finalcif.vrf',
    data / 'examples/1979688-finalcif.cif',
    data / 'examples/1979688-finalcif.gif',
    data / 'examples/1979688-finalcif.fcf',
    data / 'examples/1979688.ckf',
    data / 'examples/1979688.chk',
    data / 'examples/check.def',
    data / 'examples/check.def',
    data / 'examples/platon.out',
    data / 'examples/work/platon.out',
    data / 'examples/work/check.def',
    data / 'examples/1000007-finalcif.chk',
    data / 'examples/1000007-finalcif.cif',
    data / 'examples/1000007-finalcif.vrf',
)


@unittest.skip('time')
class TestPlatonCheckCIF(AppWindowTestCase):

    def setUp(self) -> None:
        if not get_platon_exe() or os.environ.get('NO_NETWORK'):
            self.skipTest('No PLATON executable found or no network. Skipping test!')
        self.app = AppWindow(file=(data / 'examples/1979688.cif').resolve())
        self.app.hide()

    def tearDown(self) -> None:
        for file in filenames:
            Path(file).unlink(missing_ok=True)
        self.app.close()
        super().tearDown()

    def test_checkcif_offline(self):
        self.app.hide()
        self.app.ui.CheckcifButton.click()
        timediff = int((data / 'examples/1979688-finalcif.chk').stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago

    def test_checkdef_contains_text(self):
        self.app.hide()
        self.app.ui.CheckcifButton.click()
        time.sleep(0.3)
        self.assertEqual('FINALCIF V{}'.format(VERSION) in (data / 'examples/1979688-finalcif.chk').read_text(),
                         True)
        self.assertEqual('SumFormula C77 H80 O25' in (data / 'examples/1979688-finalcif.chk').read_text(), True)

    def test_offline_checkcif_writes_gif(self):
        self.app.hide()
        self.app.ui.CheckcifButton.click()
        self.assertFalse(Path('1979688-finalcif.gif').exists())


@unittest.skip('time')
class TestPlatonCheckCIFwithCIFwithoutHKLdata(AppWindowTestCase):

    def setUp(self) -> None:
        if not get_platon_exe() or os.environ.get('NO_NETWORK'):
            self.skipTest('No PLATON executable found or NO_NETWORK is set. Skipping test!')
        self.app = AppWindow(file=(data / 'examples/1000007.cif').resolve())
        self.app.hide()
        self.app.ui.structfactCheckBox.setChecked(True)

    def tearDown(self) -> None:
        for file in filenames:
            Path(file).unlink(missing_ok=True)
        self.app.close()
        super().tearDown()

    def test_checkcif_offline(self):
        self.app.hide()
        self.app.ui.CheckcifButton.click()
        timediff = int((data / 'examples/1000007-finalcif.chk').resolve().stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago
