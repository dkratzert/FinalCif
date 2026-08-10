#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import shutil
import tempfile
import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer
from finalcif.datafiles.bruker_data import BrukerData

CIF_TEXT = """data_test
_audit_creation_method 'SHELXL-2018/3'
_diffrn_reflns_number 1234
_diffrn_reflns_av_R_equivalents ?
"""


class FakeApp:
    """BrukerData only uses the app to show warnings."""
    temperature_warning_displayed = True


class ReflectionsFromAbsFileTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tempdir = Path(tempfile.mkdtemp())
        shutil.copy(Path('test-data/twinabs_multi_options.abs'), self.tempdir / 'twin.abs')

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def _bruker_data(self, cif_name: str) -> BrukerData:
        cif_file = self.tempdir / cif_name
        cif_file.write_text(CIF_TEXT, encoding='utf-8')
        return BrukerData(FakeApp(), CifContainer(cif_file))

    def test_values_of_the_matching_hklf5_dataset(self):
        data = self._bruker_data('t5_dom1.cif')
        self.assertEqual((20257, 'twin.abs'), data.sources['_diffrn_reflns_number'])
        self.assertEqual((0.0398, 'twin.abs'), data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_hklf5_values_override_the_cif_values(self):
        data = self._bruker_data('t5_dom1.cif')
        self.assertEqual({'_diffrn_reflns_number', '_diffrn_reflns_av_R_equivalents'}, data.overrides)

    def test_hklf4_values_do_not_override_the_cif_values(self):
        data = self._bruker_data('t4_dom1.cif')
        self.assertEqual((20257, 'twin.abs'), data.sources['_diffrn_reflns_number'])
        self.assertEqual(set(), data.overrides)

    def test_all_domains_dataset(self):
        data = self._bruker_data('t5_dom-2.cif')
        self.assertEqual((32954, 'twin.abs'), data.sources['_diffrn_reflns_number'])
        self.assertEqual((0.0438, 'twin.abs'), data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_finalcif_suffix_is_ignored_for_the_file_name_match(self):
        data = self._bruker_data('t5_dom2-finalcif.cif')
        self.assertEqual((32954, 'twin.abs'), data.sources['_diffrn_reflns_number'])


class ReflectionsFromSadabsFileTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tempdir = Path(tempfile.mkdtemp())
        shutil.copy(Path('test-data/IK_WU19.abs'), self.tempdir / 'IK_WU19.abs')
        cif_file = self.tempdir / 'IK_WU19_0m.cif'
        cif_file.write_text(CIF_TEXT, encoding='utf-8')
        self.data = BrukerData(FakeApp(), CifContainer(cif_file))

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_written_reflections_are_used(self):
        self.assertEqual((152800, 'IK_WU19.abs'), self.data.sources['_diffrn_reflns_number'])

    def test_sadabs_values_never_override(self):
        self.assertEqual(set(), self.data.overrides)


class RintFallbackTestCase(unittest.TestCase):
    """
    SADABS writes no R(int), it is calculated from the reflection data, but only if the CIF
    does not contain the value already.
    """

    example = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif')

    def test_rint_of_shelxl_is_not_replaced(self):
        data = BrukerData(FakeApp(), CifContainer(self.example))
        self.assertIsNone(data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_rint_is_calculated_for_a_cif_without_rint(self):
        tempdir = Path(tempfile.mkdtemp())
        try:
            for suffix in ('.abs', '.p4p'):
                for source in self.example.parent.glob(f'cu_BruecknerJK_153F40*{suffix}'):
                    shutil.copy(source, tempdir / source.name)
            cif_file = tempdir / self.example.name
            cif_file.write_text(self.example.read_text(errors='ignore').replace(
                '_diffrn_reflns_av_R_equivalents   0.0302', '_diffrn_reflns_av_R_equivalents   ?'))
            data = BrukerData(FakeApp(), CifContainer(cif_file))
            self.assertEqual((0.0311, f'calculated from {cif_file.name}'),
                             data.sources['_diffrn_reflns_av_R_equivalents'])
        finally:
            shutil.rmtree(tempdir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
