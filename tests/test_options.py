import sys
import unittest

from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow

app = QApplication(sys.argv)


class TestOptions(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow()
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.myapp.hide()

    def tearDown(self) -> None:
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)

    def test_save_picture_with(self):
        self.assertEqual(self.myapp.ui.PictureWidthDoubleSpinBox.value(), 0.0)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.myapp.options.picture_width, 7.6)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(12.5)
        self.assertEqual(self.myapp.options.picture_width, 12.5)

    def test_without_h(self):
        self.assertEqual(self.myapp.ui.HAtomsCheckBox.isChecked(), False)
        self.myapp.ui.HAtomsCheckBox.setChecked(True)
        self.assertEqual(self.myapp.options.without_H, True)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.without_H, False)

    def test_report_text(self):
        self.assertEqual(self.myapp.ui.ReportTextCheckBox.isChecked(), False)
        self.myapp.ui.ReportTextCheckBox.setChecked(True)
        self.assertEqual(self.myapp.options.report_text, False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.report_text, True)

    def test_checkcif_url(self):
        self.assertEqual(self.myapp.ui.CheckCIFServerURLTextedit.text(),
                         'https://checkcif.iucr.org/cgi-bin/checkcif_with_hkl')
        self.myapp.ui.CheckCIFServerURLTextedit.setText('foobar')
        self.assertEqual(self.myapp.options.checkcif_url, 'foobar')

    def test_option_picture_width(self):
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        # a width od < 0.001 defaults to 7.5 cm
        self.assertEqual(self.myapp.options.picture_width, 7.5)
        #
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.6)
        self.assertEqual(self.myapp.options.picture_width, 7.6)

    def test_without_H_option(self):
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.assertEqual(self.myapp.options.without_H, False)
