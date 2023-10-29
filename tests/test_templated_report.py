import os
from unittest.mock import Mock

os.environ['RUNNING_TEST'] = 'True'
import unittest
from pathlib import Path

from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.shape import InlineShapes
from docx.shared import Cm
from docx.table import Table

from finalcif import VERSION
from finalcif.appwindow import AppWindow
from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.templated_report import TemplatedReport

data = Path('tests')
test_data = Path('test-data')


# noinspection PyMissingTypeHints
class TemplateReportTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testcif = (data / 'examples/1979688.cif').absolute()
        self.myapp = AppWindow(file=self.testcif)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.options = Mock()
        self.options.picture_width = 7.43
        self.options.without_h = False
        self.text_template = Path('finalcif/template/template_text.docx').absolute()
        self.template_without_text = Path('finalcif/template/template_without_text.docx').absolute()
        self.import_templates()
        self.myapp.ui.docxTemplatesListWidget.setCurrentRow(2)
        self.reportdoc = self.myapp.cif.finalcif_file_prefixed(prefix='report_', suffix='-finalcif.docx')
        self.report_zip = self.myapp.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif.zip')
        self.report_pic = Path('finalcif/icon/finalcif.png')
        self.myapp.select_report_picture(self.report_pic)

    def tearDown(self) -> None:
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.5)
        self.myapp.ui.docxTemplatesListWidget.blockSignals(True)
        for num in range(1, self.myapp.ui.docxTemplatesListWidget.count()):
            self.myapp.ui.docxTemplatesListWidget.setCurrentRow(num)
            self.myapp.templates.remove_current_template()
        self.myapp.ui.docxTemplatesListWidget.blockSignals(False)
        self.myapp.close()

    def import_templates(self):
        # blocking signals, because signal gets fired after delete and crashes: 
        self.myapp.ui.docxTemplatesListWidget.blockSignals(True)
        for num in range(1, self.myapp.ui.docxTemplatesListWidget.count()):
            self.myapp.ui.docxTemplatesListWidget.setCurrentRow(num)
            self.myapp.templates.remove_current_template()
        self.myapp.templates.add_new_template(str(self.text_template))
        self.myapp.templates.add_new_template(str(self.template_without_text))
        print('imported templates')
        self.myapp.ui.docxTemplatesListWidget.blockSignals(False)

    def test_with_report_text(self):
        self.import_templates()
        self.myapp.ui.docxTemplatesListWidget.setCurrentRow(2)
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
        t = TemplatedReport()
        ok = t.make_templated_report(options=self.options,
                                     cif=CifContainer(self.testcif),
                                     output_filename=self.reportdoc,
                                     picfile=self.report_pic,
                                     template_path=self.text_template)
        self.assertTrue(ok)
        doc = Document(str(self.reportdoc.absolute()))
        table: Table = doc.tables[0]
        # This is with the 'CCDC' string, because CCDC will be deleted during CIF save in  main application:
        self.assertEqual('CCDC 1979688', table.cell(row_idx=0, col_idx=1).text)

    def test_picture_has_correct_size(self):
        """
        For this test, self.myapp.set_report_picture(Path('finalcif/icon/finalcif.png'))
        has to be set correctly.
        """
        t = TemplatedReport()
        ok = t.make_templated_report(options=self.options,
                                     cif=CifContainer(self.testcif),
                                     output_filename=self.reportdoc,
                                     picfile=self.report_pic,
                                     template_path=self.text_template)
        self.assertTrue(ok)
        doc = Document(self.reportdoc.absolute())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.43).emu, shapes[0].width)


class TestReportFromMultiCif(unittest.TestCase):
    def setUp(self):
        self.reportdoc = Path('test.docx')
        self.reportdoc.unlink(missing_ok=True)
        self.docx_templ = test_data / 'templates/test_template_for_multitable_dist.docx'
        self.multi_cif = test_data / '1000007-multi.cif'
        self.cif = CifContainer(file=self.multi_cif)

    def tearDown(self):
        self.reportdoc.unlink(missing_ok=True)

    def test_get_distance_from_atoms(self):
        t = TemplatedReport()
        mock = Mock()
        mock.without_h = False
        mock.picture_width = 7.43
        ok = t.make_templated_report(options=mock, cif=self.cif,
                                     output_filename='test.docx', picfile=Path(),
                                     template_path=self.docx_templ)
        self.assertTrue(ok)
        doc = Document(self.reportdoc.resolve().__str__())
        self.assertEqual('C1-C2 in p-1 distance: 1.5123(17)', doc.paragraphs[0].text)
        self.assertEqual('C1-C2 in p21c distance: 1.544(3)', doc.paragraphs[1].text)


# noinspection PyMissingTypeHints
class TestData(unittest.TestCase):

    def setUp(self) -> None:
        # creating a new CIF with a new block:
        self.cif = CifContainer('foo.cif', 'testblock')

    def test_get_integration_program_with_spaces(self):
        # Here we have the special case, that there is no space character between the version number and the bracket.
        self.cif['_computing_data_reduction'] = 'CrysAlisPro 1.171.39.20a (Rigaku OD, 2015)'
        self.assertEqual('CrysAlisPro 1.171.39.20a (Rigaku OD, 2015)', self.cif['_computing_data_reduction'])
        r = TemplatedReport()
        result = r.get_integration_program(self.cif)
        self.assertEqual('CrysAlisPro', result)
        self.assertEqual('Crysalispro, 1.171.39.20a, 2015, Rigaku OD.', str(r.literature['integration']))

    def test_get_integration_program_with_line_break(self):
        # Here we have the special case, that there is no space character between the version number and the bracket.
        self.cif['_computing_data_reduction'] = "CrysAlisPro 1.171.39.20a\n" \
                                                "(Rigaku OD, 2015)\n"
        self.assertEqual('CrysAlisPro 1.171.39.20a\n(Rigaku OD, 2015)\n', self.cif['_computing_data_reduction'])
        r = TemplatedReport()
        result = r.get_integration_program(self.cif)
        self.assertEqual('CrysAlisPro', result)
        self.assertEqual('Crysalispro, 1.171.39.20a, 2015, Rigaku OD.', str(r.literature['integration']))

    def test_get_integration_program_with_missing_information(self):
        # Here we have all in one line with spaces inbetween:
        self.cif['_computing_data_reduction'] = 'CrysAlisPro 1.171.39.20a (Rigaku OD)'
        self.assertEqual('CrysAlisPro 1.171.39.20a (Rigaku OD)', self.cif['_computing_data_reduction'])
        r = TemplatedReport()
        result = r.get_integration_program(self.cif)
        self.assertEqual('CrysAlisPro', result)
        self.assertEqual('Crysalispro, unknown version, Rigaku OD.', str(r.literature['integration']))

    def test_get_integration_program_saint(self):
        # Here we have all in one line with spaces inbetween:
        self.cif['_computing_data_reduction'] = 'SAINT V8.40A'
        r = TemplatedReport()
        result = r.get_integration_program(self.cif)
        self.assertEqual('SAINT V8.40A', result)
        self.assertEqual('Bruker, SAINT, V8.40A, Bruker AXS Inc., Madison, Wisconsin, USA.',
                         str(r.literature['integration']))

    def test_get_integration_program_saint_without_version(self):
        # Here we have all in one line with spaces inbetween:
        self.cif['_computing_data_reduction'] = 'SAINT'
        r = TemplatedReport()
        result = r.get_integration_program(self.cif)
        self.assertEqual('SAINT', result)
        self.assertEqual('Bruker, SAINT, Bruker AXS Inc., Madison, Wisconsin, USA.', str(r.literature['integration']))


if __name__ == '__main__':
    unittest.main()
