"""Tests for the LaTeX report generation path in templated_report.py.

Covers:
- LaTeXFormatter: bonds/angles return plain Bond/Angle objects (not dicts with RichText);
  symminfo methods return plain text without HTML markup; hyphens are replaced by the
  Unicode minus sign (U+2212).
- text_factory: ReportFormat.LATEX is registered and produces a LaTeXFormatter instance.
- TemplatedReport.make_templated_latex_report(): returns True, writes a file, and the
  rendered output contains the expected LaTeX table commands and data.  Both report.tex
  and report2.tex templates are exercised.
"""
import os
import tempfile
import unittest
from pathlib import Path

os.environ['RUNNING_TEST'] = 'True'

from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.templated_report import (
    Angle,
    Bond,
    LaTeXFormatter,
    ReportFormat,
    TemplatedReport,
    text_factory,
)
from finalcif.tools.misc import minus_sign
from finalcif.tools.options import Options

# Paths used throughout the tests
TESTS_DIR = Path('tests')
TEST_DATA_DIR = Path('test-data')
TEMPLATE_DIR = Path('finalcif/template')

# A CIF that has: atoms, ADPs, bonds and angles, and symmetry-generated atoms.
CIF_WITH_BONDS_AND_SYMM = TEST_DATA_DIR / 'sad-final.cif'
# A simple CIF with bonds but no special symmetry codes in bonds.
CIF_WITH_BONDS = TESTS_DIR / 'examples/1979688.cif'
# A CIF with a single atom and no bonds (exercises empty-table branches).
CIF_DIAMOND = TEST_DATA_DIR / 'diamond/9008564.cif'


def _make_options(bonds_table: bool = False, report_adp: bool = False) -> Options:
    # Use the private-attribute debug path supported by Options._get_setting().
    # This is the established test pattern in this codebase (see test_templated_report.py).
    opts = Options()
    opts._bonds_table = bonds_table
    opts._report_adp = report_adp
    opts._without_h = False
    return opts


class TestTextFactoryRegistersLatex(unittest.TestCase):
    """text_factory must include ReportFormat.LATEX → LaTeXFormatter."""

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS)
        self.options = _make_options()

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_latex_key_present_in_factory(self):
        factory = text_factory(self.options, self.cif)
        self.assertIn(ReportFormat.LATEX, factory)

    def test_factory_returns_latex_formatter_instance(self):
        factory = text_factory(self.options, self.cif)
        self.assertIsInstance(factory[ReportFormat.LATEX], LaTeXFormatter)

    def test_templated_report_uses_latex_formatter(self):
        t = TemplatedReport(format=ReportFormat.LATEX, options=self.options, cif=self.cif)
        self.assertIsInstance(t.text_formatter, LaTeXFormatter)


class TestLaTeXFormatterBondsAngles(unittest.TestCase):
    """LaTeXFormatter.get_bonds() / get_angles() must return plain Bond/Angle objects."""

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS)
        self.options = _make_options()
        self.fmt = LaTeXFormatter(self.options, self.cif)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_get_bonds_returns_list(self):
        bonds = self.fmt.get_bonds()
        self.assertIsInstance(bonds, list)

    def test_get_bonds_items_are_bond_objects(self):
        bonds = self.fmt.get_bonds()
        self.assertGreater(len(bonds), 0)
        for bond in bonds:
            self.assertIsInstance(bond, Bond)

    def test_get_bonds_items_have_string_fields(self):
        """All fields of Bond (atoms, symm, dist) must be plain strings."""
        for bond in self.fmt.get_bonds():
            self.assertIsInstance(bond.atoms, str)
            self.assertIsInstance(bond.symm, str)
            self.assertIsInstance(bond.dist, str)

    def test_get_angles_returns_list(self):
        angles = self.fmt.get_angles()
        self.assertIsInstance(angles, list)

    def test_get_angles_items_are_angle_objects(self):
        angles = self.fmt.get_angles()
        self.assertGreater(len(angles), 0)
        for angle in angles:
            self.assertIsInstance(angle, Angle)

    def test_get_angles_items_have_string_fields(self):
        """All fields of Angle must be plain strings."""
        for angle in self.fmt.get_angles():
            self.assertIsInstance(angle.atom1, str)
            self.assertIsInstance(angle.atom2, str)
            self.assertIsInstance(angle.symm1, str)
            self.assertIsInstance(angle.symm2, str)
            self.assertIsInstance(angle.angle, str)

    def test_bond_distances_use_unicode_minus(self):
        """Hyphen in bond distances must have been replaced by U+2212."""
        for bond in self.fmt.get_bonds():
            self.assertNotIn('-', bond.dist, msg=f'Hyphen found in {bond.dist!r}')

    def test_angle_values_use_unicode_minus(self):
        """Hyphen in angle values must have been replaced by U+2212."""
        for angle in self.fmt.get_angles():
            self.assertNotIn('-', angle.angle, msg=f'Hyphen found in {angle.angle!r}')


class TestLaTeXFormatterSymminfo(unittest.TestCase):
    """LaTeXFormatter symminfo methods must return plain text, not HTML."""

    def setUp(self):
        # sad-final.cif has symmetry-generated atoms so symminfo is non-empty.
        self.cif = CifContainer(CIF_WITH_BONDS_AND_SYMM)
        self.options = _make_options()
        self.fmt = LaTeXFormatter(self.options, self.cif)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_bonds_angles_symminfo_is_str(self):
        info = self.fmt.get_bonds_angles_symminfo()
        self.assertIsInstance(info, str)

    def test_bonds_angles_symminfo_no_html_br(self):
        info = self.fmt.get_bonds_angles_symminfo()
        self.assertNotIn('<br>', info)

    def test_bonds_angles_symminfo_no_html_nbsp(self):
        info = self.fmt.get_bonds_angles_symminfo()
        self.assertNotIn('&nbsp;', info)

    def test_bonds_angles_symminfo_uses_unicode_minus(self):
        """Any minus in the symmetry string should be U+2212, not ASCII hyphen."""
        info = self.fmt.get_bonds_angles_symminfo()
        if info:
            # If the raw symminfo contained a '-', it must now be the Unicode minus.
            self.assertNotIn('-', info)

    def test_bonds_angles_symminfo_is_non_empty(self):
        """sad-final.cif has symmetry-generated atoms, so symminfo must not be empty."""
        info = self.fmt.get_bonds_angles_symminfo()
        self.assertTrue(info, 'Expected non-empty symminfo for sad-final.cif')

    def test_torsion_symminfo_is_str(self):
        self.assertIsInstance(self.fmt.get_torsion_symminfo(), str)

    def test_torsion_symminfo_no_html_markup(self):
        info = self.fmt.get_torsion_symminfo()
        self.assertNotIn('<br>', info)
        self.assertNotIn('&nbsp;', info)

    def test_hydrogen_symminfo_is_str(self):
        self.assertIsInstance(self.fmt.get_hydrogen_symminfo(), str)

    def test_hydrogen_symminfo_no_html_markup(self):
        info = self.fmt.get_hydrogen_symminfo()
        self.assertNotIn('<br>', info)
        self.assertNotIn('&nbsp;', info)


class TestLaTeXFormatterSymminfoEmpty(unittest.TestCase):
    """When there are no symmetry-generated atoms the symminfo must be an empty string."""

    def setUp(self):
        # Diamond CIF has no bonds at all → symminfo is definitely empty.
        self.cif = CifContainer(CIF_DIAMOND)
        self.options = _make_options()
        self.fmt = LaTeXFormatter(self.options, self.cif)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_bonds_angles_symminfo_empty_when_no_bonds(self):
        self.assertEqual('', self.fmt.get_bonds_angles_symminfo())

    def test_torsion_symminfo_empty_when_no_torsions(self):
        self.assertEqual('', self.fmt.get_torsion_symminfo())


class _LatexReportBase(unittest.TestCase):
    """Base class that renders a LaTeX report to a temp file and reads it back."""

    template_file = 'report2.tex'

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS)
        self.options = _make_options(bonds_table=True, report_adp=True)
        self.t = TemplatedReport(format=ReportFormat.LATEX, options=self.options, cif=self.cif)
        self._tmpfile = tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w')
        self._tmpfile.close()
        self.output_path = Path(self._tmpfile.name)
        self.ok = self.t.make_templated_latex_report(
            output_filename=str(self.output_path),
            template_path=TEMPLATE_DIR,
            template_file=self.template_file,
        )
        self.content = self.output_path.read_text(encoding='utf-8')

    def tearDown(self):
        self.output_path.unlink(missing_ok=True)
        self.cif.finalcif_file.unlink(missing_ok=True)


class TestMakeTemplatedLatexReport2(_LatexReportBase):
    """Integration tests for make_templated_latex_report() using report2.tex."""

    template_file = 'report2.tex'

    # --- basic success ---

    def test_returns_true(self):
        self.assertTrue(self.ok)

    def test_output_file_created(self):
        self.assertTrue(self.output_path.exists())
        self.assertGreater(self.output_path.stat().st_size, 0)

    def test_output_is_utf8(self):
        # No UnicodeDecodeError means the file is valid UTF-8
        self.assertIsInstance(self.content, str)

    # --- LaTeX document structure ---

    def test_document_class_present(self):
        self.assertIn(r'\documentclass', self.content)

    def test_begin_document_present(self):
        self.assertIn(r'\begin{document}', self.content)

    def test_end_document_present(self):
        self.assertIn(r'\end{document}', self.content)

    # --- booktabs rules ---

    def test_toprule_present(self):
        self.assertIn(r'\toprule', self.content)

    def test_midrule_present(self):
        self.assertIn(r'\midrule', self.content)

    def test_bottomrule_present(self):
        self.assertIn(r'\bottomrule', self.content)

    # --- table header row ---

    def test_table1_header_identification(self):
        self.assertIn(r'\textbf{Identification}', self.content)

    def test_table1_header_value(self):
        self.assertIn(r'\textbf{Value}', self.content)

    # --- arraystretch ---

    def test_arraystretch_set(self):
        self.assertIn(r'\renewcommand{\arraystretch}{1.2}', self.content)

    # --- crystal data content ---

    def test_block_name_present(self):
        self.assertIn(self.cif.block.name, self.content)

    def test_empirical_formula_label_present(self):
        self.assertIn('Empirical formula', self.content)

    def test_space_group_label_present(self):
        self.assertIn('Space group', self.content)

    # --- atomic coordinates table ---

    def test_table2_section_present(self):
        self.assertIn('Table 2', self.content)

    def test_table2_u_eq_header(self):
        self.assertIn(r'U_{eq}', self.content)

    # --- ADP table ---

    def test_table3_section_present(self):
        self.assertIn('Table 3', self.content)

    def test_table3_u11_header(self):
        self.assertIn(r'U_{11}', self.content)

    # --- bonds table (bonds_table=True, CIF has bonds) ---

    def test_table4_section_present(self):
        self.assertIn(r'\section*{Table 4', self.content)

    def test_bonds_table_has_length_header(self):
        self.assertIn(r'\textbf{Atom\,--\,Atom} & \textbf{Length', self.content)

    def test_bonds_table_has_angle_header(self):
        self.assertIn(r'\textbf{Atom\,--\,Atom\,--\,Atom} & \textbf{Angle', self.content)

    # --- caption placement ---

    def test_caption_above_tables(self):
        self.assertIn(r'\captionsetup[table]{position=above}', self.content)


class TestMakeTemplatedLatexReport1(TestMakeTemplatedLatexReport2):
    """Run the same suite against the legacy report.tex template."""

    template_file = 'report.tex'

    # report.tex uses a section heading before Table 1 (not a \caption inside the float)
    # so we override the caption test.
    def test_caption_above_tables(self):
        self.assertIn(r'\captionsetup[table]{position=above}', self.content)


class TestLatexBondsTableDisabled(unittest.TestCase):
    """When options.bonds_table is False the bonds section must not appear."""

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS)
        self.options = _make_options(bonds_table=False)
        self.t = TemplatedReport(format=ReportFormat.LATEX, options=self.options, cif=self.cif)
        self._tmpfile = tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w')
        self._tmpfile.close()
        self.output_path = Path(self._tmpfile.name)
        self.t.make_templated_latex_report(
            output_filename=str(self.output_path),
            template_path=TEMPLATE_DIR,
        )
        self.content = self.output_path.read_text(encoding='utf-8')

    def tearDown(self):
        self.output_path.unlink(missing_ok=True)
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_table4_section_absent(self):
        self.assertNotIn(r'\section*{Table 4', self.content)


class TestLatexReportWithSymmGeneratedAtoms(unittest.TestCase):
    """Symmetry-info footnote is rendered in the bonds table when present."""

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS_AND_SYMM)
        self.options = _make_options(bonds_table=True)
        self.t = TemplatedReport(format=ReportFormat.LATEX, options=self.options, cif=self.cif)
        self._tmpfile = tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w')
        self._tmpfile.close()
        self.output_path = Path(self._tmpfile.name)
        self.t.make_templated_latex_report(
            output_filename=str(self.output_path),
            template_path=TEMPLATE_DIR,
        )
        self.content = self.output_path.read_text(encoding='utf-8')

    def tearDown(self):
        self.output_path.unlink(missing_ok=True)
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_symminfo_footnote_present(self):
        """Symmetry transformations line must appear in the bonds section."""
        self.assertIn('Symmetry transformations', self.content)

    def test_symminfo_has_no_html_markup(self):
        """The rendered symminfo footnote must not contain HTML artefacts from HtmlFormatter.
        (Note: other fields like index_ranges may still contain HTML; we check the footnote only.)
        """
        idx = self.content.find('Symmetry transformations')
        self.assertGreater(idx, 0, 'Symmetry transformations footnote not found')
        footnote_area = self.content[idx:idx + 300]
        self.assertNotIn('<br>', footnote_area)
        self.assertNotIn('&nbsp;', footnote_area)


class TestLatexReportNoBonds(unittest.TestCase):
    """With bonds_table=True but a CIF that has no bonds, Table 4 is absent."""

    def setUp(self):
        self.cif = CifContainer(CIF_DIAMOND)
        self.options = _make_options(bonds_table=True)
        self.t = TemplatedReport(format=ReportFormat.LATEX, options=self.options, cif=self.cif)
        self._tmpfile = tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w')
        self._tmpfile.close()
        self.output_path = Path(self._tmpfile.name)
        self.t.make_templated_latex_report(
            output_filename=str(self.output_path),
            template_path=TEMPLATE_DIR,
        )
        self.content = self.output_path.read_text(encoding='utf-8')

    def tearDown(self):
        self.output_path.unlink(missing_ok=True)
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_table4_absent_when_no_bonds(self):
        """The bonds loop guard ({% if bonds %}) must suppress Table 4."""
        self.assertNotIn(r'\section*{Table 4', self.content)


class TestLaTeXFormatterGetAtomicCoordinates(unittest.TestCase):
    """get_atomic_coordinates returns dicts with minus-sign-substituted values."""

    def setUp(self):
        self.cif = CifContainer(CIF_WITH_BONDS)
        self.options = _make_options()
        self.fmt = LaTeXFormatter(self.options, self.cif)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_returns_non_empty_tuple(self):
        coords = self.fmt.get_atomic_coordinates(self.cif)
        self.assertIsInstance(coords, tuple)
        self.assertGreater(len(coords), 0)

    def test_coord_dicts_have_required_keys(self):
        for atom in self.fmt.get_atomic_coordinates(self.cif):
            for key in ('label', 'x', 'y', 'z', 'u_eq'):
                self.assertIn(key, atom)

    def test_coord_values_use_unicode_minus(self):
        """Hyphens in fractional coordinates must be replaced by U+2212."""
        for atom in self.fmt.get_atomic_coordinates(self.cif):
            for key in ('x', 'y', 'z'):
                self.assertNotIn('-', atom[key],
                                 msg=f'Hyphen found in {key}={atom[key]!r} for {atom["label"]}')


class TestLaTeXFormatterGetDisplacementParameters(unittest.TestCase):
    """get_displacement_parameters returns AdpWithMinus namedtuples with minus-sign values."""

    def setUp(self):
        # sad-final.cif has anisotropic displacement parameters.
        self.cif = CifContainer(CIF_WITH_BONDS_AND_SYMM)
        self.options = _make_options()
        self.fmt = LaTeXFormatter(self.options, self.cif)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_returns_non_empty_tuple(self):
        adps = self.fmt.get_displacement_parameters(self.cif)
        self.assertIsInstance(adps, tuple)
        self.assertGreater(len(adps), 0)

    def test_adp_fields_use_unicode_minus(self):
        """Hyphens in Uij values must be replaced by U+2212."""
        for adp in self.fmt.get_displacement_parameters(self.cif):
            for field in ('U11', 'U22', 'U33', 'U23', 'U13', 'U12'):
                val = getattr(adp, field)
                self.assertNotIn('-', val,
                                 msg=f'Hyphen found in {field}={val!r} for {adp.label}')


if __name__ == '__main__':
    unittest.main()
