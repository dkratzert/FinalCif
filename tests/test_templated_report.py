import os
import sys
import time
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


# @unittest.skip('foo')
class TemplateReportTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.myapp = AppWindow()
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp.load_cif_file(self.testcif.absolute())
        self.myapp.running_inside_unit_test = True
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.import_templates()
        self.myapp.ui.TemplatesListWidget.setCurrentRow(2)
        self.reportdoc = Path('report_' + self.testcif.stem + '-finalcif.docx')
        self.report_zip = Path(self.testcif.stem + '-finalcif.zip')
        self.myapp.set_report_picture(Path('../../icon/finalcif.png'))
        self.myapp.hide()

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.5)

    def import_templates(self):
        # blocking signals, because signal gets fired after delete and crashes: 
        self.myapp.ui.TemplatesListWidget.blockSignals(True)
        for num in range(1, self.myapp.ui.TemplatesListWidget.count()):
            self.myapp.ui.TemplatesListWidget.setCurrentRow(num)
            self.myapp.templates.remove_current_template()
        self.myapp.templates.add_new_template(str(Path('../../template/template_text.docx').absolute()))
        self.myapp.templates.add_new_template(str(Path('../../template/template_without_text.docx').absolute()))
        print('imported templates')
        self.myapp.ui.TemplatesListWidget.blockSignals(False)

    #@unittest.skip('')
    def test_with_report_text(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        self.assertEqual('The following text is only', doc.paragraphs[2].text[:26])

    @unittest.skip('I am unable to access the respective paragraph, they are in w:ins')
    def test_citations(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        self.assertEqual(
            '[6] 	D. Kratzert, FinalCif, V{}, https://dkratzert.de/finalcif.html.'.format(VERSION),
            doc.paragraphs[-1].text)

    def test_ccdc_num_in_table(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        table: Table = doc.tables[0]
        self.assertEqual('1979688', table.cell(row_idx=0, col_idx=1).text)

    def test_picture_has_correct_size(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.43).emu, shapes[0].width)


if __name__ == '__main__':
    unittest.main()
