#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import sys
import time
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow
from gui.custom_classes import COL_EDIT
from tools.misc import strip_finalcif_of_name

app = QApplication(sys.argv)


class TestCheckCif(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.myapp = AppWindow(Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute())
        self.myapp.hide()  # For full screen view
        self.resobj = Path('checkcif-' + strip_finalcif_of_name(self.myapp.cif.fileobj.stem) + '-finalcif.html')

    def tearDown(self) -> None:
        self.resobj.unlink(missing_ok=True)
        self.myapp.cif.fileobj.unlink()

    # @unittest.skip('temporary skip')
    def test_checkcif_html(self):
        """Runs a html checkcif without hkl and compares the result with the html file."""
        self.maxDiff = 500
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('D8 VENTURE', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.equipment.load_selected_equipment()
        item2 = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item2)
        self.myapp.equipment.load_selected_equipment()
        self.myapp.ui.cif_main_table.setText(key='_chemical_absolute_configuration', txt='ad', column=COL_EDIT)
        #
        # Remember: This test is without structure factors!
        self.myapp.ui.structfactCheckBox.setChecked(True)
        QTest.mouseClick(self.myapp.ui.CheckcifHTMLOnlineButton, Qt.LeftButton, Qt.NoModifier)
        time.sleep(5)
        # this is the file on github:
        self.html = Path('checkcif-' + strip_finalcif_of_name(self.myapp.cif.fileobj.stem) + '-test.html')
        htmlfile = self.html.read_text().splitlines()[28:-13]
        # this is the new downloadad file
        result = self.resobj.read_text().splitlines()[28:-13]
        self.assertEqual(htmlfile, result)
