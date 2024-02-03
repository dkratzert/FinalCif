import shutil
import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer

data = Path('.')


class CifFileCRCTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(data / 'tests/examples/1979688.cif')

    def test_calc_crc(self):
        self.assertEqual(20714, self.cif.calc_checksum(self.cif['_shelx_hkl_file']))


class CifFileCRClargerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(data / 'test-data/DK_Zucker2_0m.cif')

    def test_calc_crc(self):
        self.assertEqual(26780, self.cif.calc_checksum(self.cif['_shelx_hkl_file']))


class CifFileTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(data / 'tests/examples/1979688.cif')

    def test_calc_crc(self):
        self.assertEqual(3583, self.cif.calc_checksum('hello world'))

    def test_res_crc(self):
        self.assertEqual(17612, self.cif.res_checksum_calcd)

    def test_hkl_crc(self):
        self.assertEqual(20714, self.cif.hkl_checksum_calcd)

    def test_res_crc_without_res(self):
        self.assertEqual(0, CifContainer(data / 'test-data/1000006.cif').res_checksum_calcd)

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
        c = CifContainer(data / 'test-data/DK_ML7-66-final.cif')
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
        self.assertEqual(True, CifContainer(data / 'test-data/1000006.cif').test_res_checksum())
        self.assertEqual(True, CifContainer(data / 'test-data/1000006.cif').test_hkl_checksum())

    def test_distance_from_string(self):
        self.assertEqual('1.527(3)', self.cif.bond_dist('C1-C2'))

    def test_distance_from_false_string(self):
        self.assertEqual(None, self.cif.bond_dist('C1-C999'))

    def test_angle_from_string(self):
        self.assertEqual('109.9', self.cif.angle('C1-C2-H2'))

    def test_angle_from_false_string(self):
        self.assertEqual(None, self.cif.angle('C1-C2-Hxx'))

    def test_torsion_angle_from_string(self):
        self.assertEqual('173.5(2)', self.cif.torsion('C1-C2-C3-C4'))

    def test_torsion_angle_from_false_string(self):
        self.assertEqual(None, self.cif.torsion('C1-C2-C3-C999'))


class TestQuotationMark(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(data / 'tests/examples/1979688.cif')
        shutil.copyfile(self.cif.fileobj, data / 'test.cif')
        self.cif2 = CifContainer(data / 'test.cif')

    def tearDown(self) -> None:
        self.cif2.fileobj.unlink(missing_ok=True)

    def test_insert_quotation_mark(self):
        self.cif['_diffrn_detector'] = "Jesus' live"
        self.assertEqual("Jesus' live", self.cif['_diffrn_detector'])
        self.cif.save(self.cif2.fileobj)
        self.cif2 = CifContainer(self.cif2.fileobj)
        self.assertEqual("Jesus' live", self.cif['_diffrn_detector'])


class TestMultiCif(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(data / 'tests/examples/multi.cif')

    def test_ismulti(self):
        self.assertEqual(True, self.cif.is_multi_cif)

    def test_isempty(self):
        self.assertEqual(False, self.cif.is_empty())


if __name__ == '__main__':
    unittest.main()
