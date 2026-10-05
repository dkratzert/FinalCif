import unittest
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

import pytest
from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.shape import InlineShapes
from docx.shared import Cm
from docxtpl import RichText

from finalcif.appwindow import AppWindow
from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.templated_report import ReportFormat, RichTextFormatter, TemplatedReport
from finalcif.tools.options import Options
from tests.helpers import AppWindowTestCase

data = Path('tests')
test_data = Path('test-data')


class TablesTestCase(AppWindowTestCase):

    def setUp(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.testcif = Path(copy2(data / 'examples/1979688_small.cif', directory.name))
        self.app = AppWindow(file=self.testcif)
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.app.ui.ReportTextCheckBox.setChecked(False)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        # Use the bundled default template.
        self.app.ui.docxTemplatesListWidget.setCurrentRow(0)
        self.reportdoc = self.app.cif.finalcif_file_prefixed(prefix='report_', suffix='-finalcif.docx')
        self.report_zip = self.app.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif.zip')
        self.app.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.app.select_report_picture(Path('finalcif/icon/finalcif.png'))

    def tearDown(self) -> None:
        self.app.cif.finalcif_file.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)
        self.app.ui.ReportTextCheckBox.setChecked(False)
        self.app.ui.HAtomsCheckBox.setChecked(False)
        self.app.ui.PictureWidthDoubleSpinBox.setValue(7.5)
        self.app.close()
        super().tearDown()

    def test_picture_has_correct_size(self):
        self.app.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.43).emu, shapes[0].width)

    def test_default_picture_width(self):
        self.app.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        self.app.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.resolve())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(Cm(7.5).emu, shapes[0].width)


def richtext_text(value: RichText) -> str:
    root = ElementTree.fromstring(
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">{value}</w:p>')
    return ''.join(root.itertext())


@pytest.mark.parametrize('without_h', [False, True])
def test_template_bonds_filter_hydrogens(without_h: bool):
    options = Options()
    options._without_h = without_h
    formatter = RichTextFormatter(options, CifContainer(data / 'examples/1979688.cif'))
    bonds = [richtext_text(bond['atoms']) for bond in formatter.get_bonds()]
    assert ('C1–H1' in bonds) == (not without_h)
    assert 'O1–C13' in bonds


@pytest.mark.parametrize('with_picture', [False, True])
def test_template_report_picture(tmp_path: Path, with_picture: bool, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr('finalcif.report.templated_report.show_general_warning',
                        lambda **kwargs: pytest.fail(str(kwargs)))
    options = Options()
    options._picture_width = 7.43
    if with_picture:
        options.structure_figure = Path('finalcif/icon/finalcif.png')
    report = TemplatedReport(options=options, cif=CifContainer(data / 'examples/1979688.cif'),
                            format=ReportFormat.RICHTEXT)
    output = tmp_path / 'report.docx'
    assert report.make_templated_docx_report(str(output), Path('finalcif/template/report_default.docx'))
    document = Document(output)
    assert len(document.inline_shapes) == int(with_picture)
    if with_picture:
        assert document.inline_shapes[0].width == Cm(7.43)


def test_template_symmetry_indicators():
    formatter = RichTextFormatter(Options(), CifContainer(test_data / 'p31c.cif'))
    assert 'C2–C3#1' in [richtext_text(bond['atoms']) for bond in formatter.get_bonds()]
    assert "C3'#1–C2'–C3'" in [richtext_text(angle['atoms']) for angle in formatter.get_angles()]
    assert 'C3#1–C2–C3–N1' in [richtext_text(torsion['atoms']) for torsion in formatter.get_torsion_angles()]
    assert 'N1^a–H1^a⋯Cl1#1' in [richtext_text(bond['atoms']) for bond in formatter.get_hydrogen_bonds()]


if __name__ == '__main__':
    unittest.main()
