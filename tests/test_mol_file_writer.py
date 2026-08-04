"""Tests for the MOL2 writer used by the Miew/three.js viewer in the HTML report."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from docxtpl import DocxTemplate

from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.templated_report import ReportFormat, TemplatedReport
from finalcif.tools.mol_file_writer import (
    MolFile,
    grown_atoms,
    mol_from_asymmetric_unit,
    mol_from_grown_atoms,
    mol_from_packed_cell,
    packed_cell_atoms,
)
from finalcif.tools.options import Options

TEST_DATA_DIR = Path('test-data')
CIF_FILE = TEST_DATA_DIR / 'p21c.cif'


def _make_options() -> Options:
    opts = Options()
    opts._bonds_table = False
    opts._report_adp = False
    opts._without_h = False
    return opts


def _counts_line(mol: str) -> tuple[int, int]:
    atoms, bonds = mol.splitlines()[4].split()[:2]
    return int(atoms), int(bonds)


def _bond_pairs(mol: str) -> list[tuple[int, int]]:
    bond_section = mol.split('@<TRIPOS>BOND\n')[1]
    return [(int(line.split()[1]), int(line.split()[2]))
            for line in bond_section.splitlines() if line.strip()]


class TestMolFile(unittest.TestCase):

    def setUp(self):
        self.cif = CifContainer(CIF_FILE)

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_mol2_sections_present(self):
        mol = mol_from_asymmetric_unit(self.cif)
        self.assertIn('@<TRIPOS>MOLECULE', mol)
        self.assertIn('@<TRIPOS>ATOM', mol)
        self.assertIn('@<TRIPOS>BOND', mol)

    def test_atom_count_equals_number_of_atoms(self):
        atoms = list(self.cif.atoms_orth)
        mol = mol_from_asymmetric_unit(self.cif)
        self.assertEqual(len(atoms), _counts_line(mol)[0])

    def test_bond_count_matches_bond_section(self):
        mol = mol_from_asymmetric_unit(self.cif)
        self.assertEqual(_counts_line(mol)[1], len(_bond_pairs(mol)))

    def test_bonds_are_not_duplicated(self):
        pairs = _bond_pairs(mol_from_asymmetric_unit(self.cif))
        unique = {frozenset(pair) for pair in pairs}
        self.assertEqual(len(pairs), len(unique))

    def test_first_atom_line_format(self):
        first_cif_atom = next(iter(self.cif.atoms_orth))
        mol = mol_from_asymmetric_unit(self.cif)
        first_atom = mol.split('@<TRIPOS>ATOM\n')[1].splitlines()[0].split()
        self.assertEqual('1', first_atom[0])
        self.assertEqual(first_cif_atom.label, first_atom[1])

    def test_grown_atoms_are_at_least_the_asymmetric_unit(self):
        self.assertGreaterEqual(len(grown_atoms(self.cif)), len(list(self.cif.atoms_orth)))

    def test_packed_cell_has_more_atoms_than_asymmetric_unit(self):
        self.assertGreater(len(packed_cell_atoms(self.cif)), len(list(self.cif.atoms_orth)))

    def test_packed_cell_mol_is_larger_than_asymmetric_unit_mol(self):
        self.assertGreater(_counts_line(mol_from_packed_cell(self.cif))[0],
                           _counts_line(mol_from_asymmetric_unit(self.cif))[0])

    def test_grown_mol_can_be_written(self):
        self.assertIn('@<TRIPOS>ATOM', mol_from_grown_atoms(self.cif))

    def test_quoted_mol_is_enclosed_in_backticks(self):
        mol = mol_from_asymmetric_unit(self.cif, quoted=True)
        self.assertTrue(mol.startswith('`'))
        self.assertTrue(mol.endswith('`\n'))

    def test_unquoted_mol_has_no_backticks(self):
        self.assertNotIn('`', mol_from_asymmetric_unit(self.cif))

    def test_no_atoms_gives_empty_atom_section(self):
        mol = MolFile().load_from_atoms([])
        self.assertEqual((0, 0), _counts_line(mol))


class TestMolFileWithoutStructure(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        cif_file = Path(self._tmpdir.name) / 'no_atoms.cif'
        cif_file.write_text('data_no_atoms\n_cell_length_a 10.0\n', encoding='utf-8')
        self.cif = CifContainer(cif_file)
        self.report = TemplatedReport(format=ReportFormat.HTML, options=_make_options(), cif=self.cif)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_grown_atoms_are_empty(self):
        self.assertEqual([], grown_atoms(self.cif))

    def test_packed_cell_atoms_are_empty(self):
        self.assertEqual([], packed_cell_atoms(self.cif))

    def test_report_returns_empty_string_for_all_variants(self):
        self.assertEqual('', self.report.get_xyz_fused(self.cif))
        self.assertEqual('', self.report.get_xyz_grow(self.cif))
        self.assertEqual('', self.report.get_xyz_filled_cell(self.cif))


class TestReportContext(unittest.TestCase):

    def setUp(self):
        self.cif = CifContainer(CIF_FILE)
        self.options = _make_options()

    def tearDown(self):
        self.cif.finalcif_file.unlink(missing_ok=True)

    def test_html_context_contains_viewer_data(self):
        report = TemplatedReport(format=ReportFormat.HTML, options=self.options, cif=self.cif)
        context = report.get_context(self.cif, self.options)
        for key in ('miew_js', 'three_js', 'lodash_js', 'miew_css'):
            self.assertTrue(context[key])
        for key in ('xyz_data_fill', 'xyz_data_grow', 'xyz_data_fuse'):
            self.assertIn('@<TRIPOS>ATOM', context[key])

    def test_docx_context_has_no_viewer_data(self):
        report = TemplatedReport(format=ReportFormat.RICHTEXT, options=self.options, cif=self.cif)
        tpl_doc = DocxTemplate(Path('finalcif/template/template_text.docx'))
        with patch('finalcif.report.templated_report._read_template_file') as reader:
            context = report.get_context(self.cif, self.options, tpl_doc)
        reader.assert_not_called()
        self.assertNotIn('miew_js', context)
        self.assertNotIn('xyz_data_fuse', context)

    def test_html_report_with_miew_template(self):
        report = TemplatedReport(format=ReportFormat.HTML, options=self.options, cif=self.cif)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'report.html'
            self.assertTrue(report.make_templated_html_report(output_filename=str(output),
                                                              template_path=Path('finalcif/template'),
                                                              template_file='report_miew.tmpl'))
            text = output.read_text(encoding='utf-8')
        self.assertIn('new Miew(', text)
        self.assertEqual(3, text.count('@<TRIPOS>ATOM'))


if __name__ == '__main__':
    unittest.main()
