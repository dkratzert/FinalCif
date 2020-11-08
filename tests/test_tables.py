import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.shape import InlineShapes
from docx.shared import Cm
from docx.table import Table

from appwindow import AppWindow
from tools.version import VERSION

app = QApplication(sys.argv)


class TablesTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.reportdoc = Path('report_' + self.testcif.stem + '-finalcif.docx')
        self.report_zip = Path(self.testcif.stem + '-finalcif.zip')
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.myapp.set_report_picture(Path('../../icon/finalcif.png'))
        self.myapp.hide()
        app.processEvents()

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.5)

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

    def test_option_with_h(self):
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        table: Table = doc.tables[2]
        self.assertEqual('C1–H1', table.cell(row_idx=4, col_idx=0).text)

    def test_option_without_h(self):
        self.myapp.ui.HAtomsCheckBox.setChecked(True)
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        table: Table = doc.tables[2]
        self.assertEqual('O1–C13', table.cell(row_idx=4, col_idx=0).text)

    def test_option_no_report_text(self):
        self.myapp.ui.ReportTextCheckBox.setChecked(True)
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        self.assertEqual('Ueq is defined as 1/3 of t', doc.paragraphs[3].text[:26])

    def test_citations(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        self.assertEqual(
            '[6] 	D. Kratzert, FinalCif, V{}, https://www.xs3.uni-freiburg.de/research/finalcif.'.format(VERSION),
            doc.paragraphs[-1].text)

    def test_ccdc_num_in_table(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        table: Table = doc.tables[0]
        self.assertEqual('CCDC 1979688', table.cell(row_idx=0, col_idx=1).text)


if __name__ == '__main__':
    unittest.main()
