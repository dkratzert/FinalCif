import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.shape import InlineShapes
from docx.shared import Cm

from appwindow import AppWindow

app = QApplication(sys.argv)


class TablesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()  # For full screen view
        self.myapp.ui.LoopsPushButton.click()
        self.reportdoc = Path('report_' + self.testcif.stem + '-finalcif.docx')
        self.report_zip = Path(self.testcif.stem + '-finalcif.zip')
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.myapp.set_report_picture(Path('../../icon/finalcif.png'))

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)

    def save_report_works(self):
        self.myapp.ui.SaveFullReportButton.click()
        self.assertEqual(True, self.reportdoc.exists())

    def test_picture_has_correct_size(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.43).emu, shapes[0].width)

    def test_default_picture_width(self):
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.5).emu, shapes[0].width)


if __name__ == '__main__':
    unittest.main()
