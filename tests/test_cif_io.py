import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer


class CifFileCRCTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(Path('tests/examples/1979688.cif'))

    def test_calc_crc(self):
        self.assertEqual(20714, self.cif.calc_checksum(self.cif['_shelx_hkl_file']))


class CifFileCRClargerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(Path('test-data/DK_Zucker2_0m.cif'))

    def test_calc_crc(self):
        self.assertEqual(26780, self.cif.calc_checksum(self.cif['_shelx_hkl_file']))


class CifFileTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(Path('tests/examples/1979688.cif'))

    def test_calc_crc(self):
        self.assertEqual(3583, self.cif.calc_checksum('hello world'))

    def test_res_crc(self):
        self.assertEqual(17612, self.cif.res_checksum_calcd)

    def test_hkl_crc(self):
        self.assertEqual(20714, self.cif.hkl_checksum_calcd)

    def test_res_crc_without_res(self):
        self.assertEqual(0, CifContainer(Path('test-data/1000006.cif')).res_checksum_calcd)

    def test_get_unknown_value_from_key(self):
        self.assertEqual('', self.cif['_chemical_melting_point'])

    def test_get_known_value_from_key(self):
        self.assertEqual('702.70', self.cif['_chemical_formula_weight'])

    def test_get_spgr(self):
        self.assertEqual('P 21 21 2', self.cif.space_group)

    def test_symmops(self):
        self.assertEqual(['x, y, z', '-x, -y, z', '-x+1/2, y+1/2, -z', 'x+1/2, -y+1/2, -z'], self.cif.symmops)

    def test_symmops_from_spgr(self):
        self.assertEqual(['x,y,z', '-x,-y,z', 'x+1/2,-y+1/2,-z', '-x+1/2,y+1/2,-z'], self.cif.symmops_from_spgr)

    def test_centrosymm(self):
        self.assertEqual(False, self.cif.is_centrosymm)
        c = CifContainer(Path('test-data/DK_ML7-66-final.cif'))
        self.assertEqual(True, c.is_centrosymm)

    def test_ishydrogen(self):
        self.assertEqual(True, self.cif.ishydrogen('H18a'))
        self.assertEqual(True, self.cif.ishydrogen('H18A'))
        self.assertEqual(False, self.cif.ishydrogen('C2'))
        self.assertEqual(False, self.cif.ishydrogen('c2'))

    def test_cell(self):
        expected = [round(x, 8) for x in (19.678, 37.02290000000001, 4.772, 90.0, 90.0, 90.0, 3476.576780226401)]
        actual = [round(y, 8) for y in self.cif.cell]
        self.assertEqual(expected, actual)

    def test_natoms(self):
        self.assertEqual(94, self.cif.natoms())
        self.assertEqual(52, self.cif.natoms(without_h=True))

    def test_checksum_tests(self):
        self.assertEqual(True, self.cif.test_hkl_checksum())
        self.assertEqual(True, self.cif.test_res_checksum())

    def test_checksum_test_without_checksum(self):
        self.assertEqual(True, CifContainer('test-data/1000006.cif').test_res_checksum())
        self.assertEqual(True, CifContainer('test-data/1000006.cif').test_hkl_checksum())


if __name__ == '__main__':
    unittest.main()
