import os

import unittest
from pathlib import Path

from finalcif import appwindow

data = Path('.')
os.environ["RUNNING_TEST"] = 'True'


class TestOptions(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = appwindow.AppWindow(file=data / 'test-data/1000006.cif')
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.ADPTableCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)

    def tearDown(self) -> None:
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.ADPTableCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.close()

    def test_save_picture_with(self):
        self.assertEqual(self.myapp.ui.PictureWidthDoubleSpinBox.value(), 0.0)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.myapp.options.picture_width, 7.6)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(12.5)
        self.assertEqual(self.myapp.options.picture_width, 12.5)

    def test_without_h(self):
        self.assertEqual(self.myapp.ui.HAtomsCheckBox.isChecked(), False)
        self.myapp.ui.HAtomsCheckBox.setChecked(True)
        self.assertEqual(self.myapp.options.without_h, True)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.without_h, False)

    def test_report_adp_checked(self):
        self.myapp.ui.ADPTableCheckBox.setChecked(True)
        self.assertEqual(True, self.myapp.ui.ADPTableCheckBox.isChecked())
        self.assertEqual(True, self.myapp.options.report_adp)

    def test_report_adp_unchecked(self):
        self.myapp.ui.ADPTableCheckBox.setChecked(False)
        self.assertEqual(False, self.myapp.options.report_adp)

    def test_report_text(self):
        self.assertEqual(self.myapp.ui.ReportTextCheckBox.isChecked(), False)
        self.myapp.ui.ReportTextCheckBox.setChecked(True)
        self.assertEqual(self.myapp.options.report_text, False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.report_text, True)

    def test_checkcif_url(self):
        self.assertEqual('https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl',
                         self.myapp.ui.CheckCIFServerURLTextedit.text())

    def test_option_picture_width(self):
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        # a width od < 0.001 defaults to 7.5 cm
        self.assertEqual(self.myapp.options.picture_width, 7.5)
        #
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.myapp.options.picture_width, 7.6)

    def test_without_H_option(self):
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.without_h, False)
