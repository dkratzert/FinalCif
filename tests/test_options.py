import os

import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from finalcif import appwindow

data = Path('.')
os.environ["RUNNING_TEST"] = 'True'


class TestOptions(AppWindowTestCase):

    def setUp(self) -> None:
        self.app = appwindow.AppWindow(file=data / 'test-data/1000006.cif')
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.app.ui.ReportTextCheckBox.setChecked(False)
        self.app.ui.ADPTableCheckBox.setChecked(False)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(0.0)

    def tearDown(self) -> None:
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.app.ui.ReportTextCheckBox.setChecked(False)
        self.app.ui.ADPTableCheckBox.setChecked(False)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.app.ui.trackChangesCifCheckBox.setChecked(False)
        self.app.close()
        super().tearDown()

    def test_save_picture_with(self):
        self.assertEqual(self.app.ui.PictureWidthDoubleSpinBox.value(), 0.0)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.app.options.picture_width, 7.6)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(12.5)
        self.assertEqual(self.app.options.picture_width, 12.5)

    def test_without_h(self):
        self.assertEqual(self.app.ui.HAtomsCheckBox.isChecked(), False)
        self.app.ui.HAtomsCheckBox.setChecked(True)
        self.assertEqual(self.app.options.without_h, True)
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.app.options.without_h, False)

    def test_report_adp_checked(self):
        self.app.ui.ADPTableCheckBox.setChecked(True)
        self.assertEqual(True, self.app.ui.ADPTableCheckBox.isChecked())
        self.assertEqual(True, self.app.options.report_adp)

    def test_report_adp_unchecked(self):
        self.app.ui.ADPTableCheckBox.setChecked(False)
        self.assertEqual(False, self.app.options.report_adp)

    def test_report_text(self):
        self.assertEqual(self.app.ui.ReportTextCheckBox.isChecked(), False)
        self.app.ui.ReportTextCheckBox.setChecked(True)
        self.assertEqual(self.app.options.report_text, False)
        self.app.ui.ReportTextCheckBox.setChecked(False)
        self.assertEqual(self.app.options.report_text, True)

    def test_checkcif_url(self):
        self.assertEqual('https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl',
                         self.app.ui.CheckCIFServerURLTextedit.text())

    def test_option_picture_width(self):
        self.app.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        # a width od < 0.001 defaults to 7.5 cm
        self.assertEqual(self.app.options.picture_width, 7.5)
        #
        self.app.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.app.options.picture_width, 7.6)

    def test_without_H_option(self):
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.app.options.without_h, False)
