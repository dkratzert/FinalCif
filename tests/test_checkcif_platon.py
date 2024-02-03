import os

os.environ["RUNNING_TEST"] = 'True'
import time
import unittest
from pathlib import Path

from finalcif import VERSION
from finalcif.appwindow import AppWindow
from tests.helpers import get_platon_exe

filenames = (
    'tests/examples/checkcif-1979688-finalcif.html',
    'tests/examples/1979688-finalcif.chk',
    'tests/examples/1979688-finalcif.ckf',
    'tests/examples/1979688-finalcif.vrf',
    'tests/examples/1979688-finalcif.cif',
    'tests/examples/1979688-finalcif.gif',
    'tests/examples/1979688-finalcif.fcf',
    'tests/examples/1979688.ckf',
    'tests/examples/1979688.chk',
    'tests/examples/check.def',
    'test-data/check.def',
    'tests/examples/platon.out',
    'tests/examples/work/platon.out',
    'tests/examples/work/check.def',
    'test-data/1000007-finalcif.chk',
    'test-data/1000007-finalcif.cif',
    'test-data/1000007-finalcif.vrf',
)


@unittest.skip('time')
class TestPlatonCheckCIF(unittest.TestCase):

    def setUp(self) -> None:
        if not get_platon_exe() or os.environ.get('NO_NETWORK'):
            self.skipTest('No PLATON executable found or no network. Skipping test!')
        self.myapp = AppWindow(file=Path('tests/examples/1979688.cif').resolve())
        self.myapp.hide()

    def tearDown(self) -> None:
        for file in filenames:
            Path(file).unlink(missing_ok=True)
        self.myapp.close()

    def test_checkcif_offline(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        timediff = int(Path('tests/examples/1979688-finalcif.chk').stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago

    def test_checkdef_contains_text(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        time.sleep(0.3)
        self.assertEqual('FINALCIF V{}'.format(VERSION) in Path('tests/examples/1979688-finalcif.chk').read_text(),
                         True)
        self.assertEqual('SumFormula C77 H80 O25' in Path('tests/examples/1979688-finalcif.chk').read_text(), True)

    def test_offline_checkcif_writes_gif(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        self.assertFalse(Path('1979688-finalcif.gif').exists())


@unittest.skip('time')
class TestPlatonCheckCIFwithCIFwithoutHKLdata(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        if not get_platon_exe() or os.environ.get('NO_NETWORK'):
            self.skipTest('No PLATON executable found or NO_NETWORK is set. Skipping test!')
        self.myapp = AppWindow(file=Path('./test-data/1000007.cif').resolve())
        self.myapp.hide()
        self.myapp.ui.structfactCheckBox.setChecked(True)

    def tearDown(self) -> None:
        for file in filenames:
            Path(file).unlink(missing_ok=True)
        self.myapp.close()

    def test_checkcif_offline(self):
        self.myapp.hide()
        self.myapp.ui.CheckcifButton.click()
        timediff = int(Path('./test-data/1000007-finalcif.chk').resolve().stat().st_mtime) - int(time.time())
        self.assertLess(timediff, 5)  # .chk file was modified less than 5 seconds ago
