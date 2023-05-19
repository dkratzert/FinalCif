import unittest
from pathlib import Path

from docx import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.shape import InlineShapes
from docx.shared import Cm
from docx.table import Table

from finalcif import VERSION
from finalcif.appwindow import AppWindow


class TablesTestMixin():

    def setUp(self) -> None:
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif, unit_test=True)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(0.0)
        # make sure to use no template:
        self.myapp.ui.TemplatesListWidget.setCurrentRow(0)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.reportdoc = self.myapp.cif.finalcif_file_prefixed(prefix='report_', suffix='-finalcif.docx')
        self.report_zip = self.myapp.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif.zip')
        self.myapp.hide()

    def tearDown(self) -> None:
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)
        self.reportdoc.unlink(missing_ok=True)
        self.report_zip.unlink(missing_ok=True)
        self.myapp.ui.ReportTextCheckBox.setChecked(False)
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.5)
        self.myapp.close()


class TablesTestCase(TablesTestMixin, unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.myapp.ui.PictureWidthDoubleSpinBox.setValue(7.43)
        self.myapp.select_report_picture(Path('finalcif/icon/finalcif.png'))

    def test_save_report_works(self):
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
        doc = Document(self.reportdoc.resolve())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(WD_INLINE_SHAPE.PICTURE, shapes[0].type)
        self.assertEqual(Cm(7.5).emu, shapes[0].width)

    def test_option_with_h(self):
        self.myapp.ui.HAtomsCheckBox.setChecked(False)
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        table: Table = doc.tables[3]
        self.assertEqual('C1–H1', table.cell(row_idx=4, col_idx=0).text)

    def test_all_paragraphs(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.absolute())
        result = ('Structure Tables\n'
                  '\n'
                  '\n'
                  'The following text is only a suggestion: The compund was crystallized '
                  'fromhot methanol by cooling. A colourless, plate-shaped crystal of '
                  'cu_BruecknerJK_153F40_0m was mounted on a MiTeGen micromount with '
                  'perfluoroether oil. Data were collected from a shock-cooled single crystal '
                  'at 102(2)\xa0K on a Bruker D8 VENTURE dual wavelength Mo/Cu three-circle '
                  'diffractometer with a microfocus sealed X-ray tube using a mirror optics as '
                  'monochromator and a Bruker PHOTON III detector. The diffractometer was '
                  'equipped with an Oxford Cryostream 800 low temperature device and used CuKα '
                  'radiation (λ = 1.54178\xa0Å). All data were integrated with SAINT and a '
                  'multi-scan absorption correction using SADABS was applied.[1,2] The '
                  'structure was solved by direct methods using SHELXT and refined by '
                  'full-matrix least-squares methods against F2 by SHELXL-2018/3.[3,4] All '
                  'non-hydrogen atoms were refined with anisotropic displacement parameters. '
                  'All hydrogen atoms were refined isotropic on calculated positions using a '
                  'riding model with their Uiso values constrained to 1.5 times the Ueq of '
                  'their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other '
                  'carbon atoms. Disordered moieties were refined using bond lengths restraints '
                  'and displacement parameter restraints. Crystallographic data for the '
                  'structures reported here have been deposited with the Cambridge '
                  'Crystallographic Data Centre.[5] CCDC 1979688 contain the supplementary '
                  'crystallographic data for this paper. These data can be obtained free of '
                  'charge from The Cambridge Crystallographic Data Centre via '
                  'www.ccdc.cam.ac.uk/\u200bstructures. This report and the CIF file were '
                  'generated using FinalCif.[6]\n'
                  '\n'
                  'Table 1. Crystal data and structure refinement for cu_BruecknerJK_153F40_0m\n'
                  '\n'
                  '\n'
                  '\n'
                  'Refinement details for cu_BruecknerJK_153F40_0m\n'
                  'The methanol molecule is disordered around a special position and thus half '
                  'occupied.\n'
                  'Table 2. Atomic coordinates and Ueq\xa0[Å2] for cu_BruecknerJK_153F40_0m\n'
                  'Ueq is defined as 1/3 of the trace of the orthogonalized Uij tensor.\n'
                  '\n'
                  'Table 3. Anisotropic displacement parameters [Å2] for '
                  'cu_BruecknerJK_153F40_0m.\n'
                  'The anisotropic displacement factor exponent takes the form: −2π2[\u205f'
                  'h2(a*)2U11\u205f+\u205fk2(b*)2U22\u205f+\u205f…\u205f+\u205f2hka*b*U12\u205f'
                  ']\n'
                  'Table 4. Bond lengths and angles for cu_BruecknerJK_153F40_0m\n'
                  '\n'
                  '\n'
                  'Table 5. Torsion angles for cu_BruecknerJK_153F40_0m\n'
                  '\n'
                  '\n'
                  '\n'
                  'Bibliography\n'
                  '[1] \tBruker, SAINT, V8.40A, Bruker AXS Inc., Madison, Wisconsin, USA.\n'
                  '[2] \tL. Krause, R. Herbst-Irmer, G. M. Sheldrick, D. Stalke, J. Appl. '
                  'Cryst. 2015, 48, 3–10, doi:10.1107/S1600576714022985.\n'
                  '[3] \tG. M. Sheldrick, Acta Cryst. 2015, A71, 3–8, '
                  'doi:10.1107/S2053273314026370.\n'
                  '[4] \tG. M. Sheldrick, Acta Cryst. 2015, C71, 3–8, '
                  'doi:10.1107/S2053229614024218.\n'
                  '[5] \tC. R. Groom, I. J. Bruno, M. P. Lightfoot, S. C. Ward, Acta Cryst. '
                  '2016, B72, 171–179, doi:10.1107/S2052520616003954.\n'
                  '[6] \tD. Kratzert, FinalCif, V119, https://dkratzert.de/finalcif.html.')

        self.assertEqual(result, '\n'.join([x.text for x in doc.paragraphs]))


class TablesNoPictureTestCase(TablesTestMixin, unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_save_report_works(self):
        self.myapp.ui.SaveFullReportButton.click()
        self.assertEqual(True, self.reportdoc.exists())

    def test_picture_has_correct_size(self):
        self.myapp.ui.SaveFullReportButton.click()
        doc = Document(self.reportdoc.resolve())
        shapes: InlineShapes = doc.inline_shapes
        self.assertEqual(0, len(shapes))


if __name__ == '__main__':
    unittest.main()
