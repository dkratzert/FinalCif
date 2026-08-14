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

    @property
    def abs_file(self) -> str:
        return str((self.tempdir / 'twin.abs').resolve())

    def _rint_source(self, component: int) -> str:
        return f'{self.abs_file} (singles of twin component {component}, point group -1)'

    def test_values_of_the_matching_hklf5_dataset(self):
        """
        Without reflection data the R(int) of the singly indexed reflections of the PART 2
        section is used, never the R(int) of the PART 3 extraction table.
        """
        data = self._bruker_data('t5_dom1.cif')
        self.assertEqual((20257, self.abs_file), data.sources['_diffrn_reflns_number'])
        self.assertEqual((0.0313, self._rint_source(1)),
                         data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_hklf5_values_override_the_cif_values(self):
        data = self._bruker_data('t5_dom1.cif')
        self.assertEqual({'_diffrn_reflns_number', '_diffrn_reflns_av_R_equivalents'}, data.overrides)

    def test_hklf4_values_do_not_override_the_cif_values(self):
        data = self._bruker_data('t4_dom1.cif')
        self.assertEqual((20257, self.abs_file), data.sources['_diffrn_reflns_number'])
        self.assertEqual(set(), data.overrides)

    def test_hklf4_still_uses_the_extraction_table(self):
        data = self._bruker_data('t4_dom1.cif')
        self.assertEqual((0.0398, self.abs_file), data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_all_domains_dataset(self):
        """The domain with the most singles is the reference domain, like in Olex2."""
        data = self._bruker_data('t5_dom-2.cif')
        self.assertEqual((32954, self.abs_file), data.sources['_diffrn_reflns_number'])
        self.assertEqual((0.0313, self._rint_source(1)),
                         data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_dataset_of_the_minor_domain(self):
        data = self._bruker_data('t5_dom2.cif')
        self.assertEqual((0.0442, self._rint_source(2)),
                         data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_finalcif_suffix_is_ignored_for_the_file_name_match(self):
        data = self._bruker_data('t5_dom2-finalcif.cif')
        self.assertEqual((32954, self.abs_file), data.sources['_diffrn_reflns_number'])


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
        self.assertEqual((152800, str((self.tempdir / 'IK_WU19.abs').resolve())),
                         self.data.sources['_diffrn_reflns_number'])

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
            self.assertEqual((0.0302, f'calculated from {cif_file.resolve()}'),
                             data.sources['_diffrn_reflns_av_R_equivalents'])
        finally:
            shutil.rmtree(tempdir, ignore_errors=True)


class RintOfTwinnedDataTestCase(unittest.TestCase):
    """
    SHELXL writes no R(int) for HKLF 5 data, therefore it is calculated from the singly indexed
    reflections of the major domain instead of being taken from the TWINABS listing file.
    """

    cif_text = """data_test
_audit_creation_method 'SHELXL-2018/3'
_space_group_name_H-M_alt 'P -1'
_diffrn_reflns_number 1234
_diffrn_reflns_av_R_equivalents ?
_shelx_res_file
;
TITL test
HKLF 5
;
_shelx_hkl_file
;
   1   0   0  100.00    1.00   1
  -1   0   0  110.00    1.00   1
   0   1   0  200.00    1.00   1
   0  -1   0  200.00    1.00   1
   2   0   0  500.00    1.00  -1
   2   0   0  500.00    1.00   2
   1   0   0  300.00    1.00   2
  -1   0   0  330.00    1.00   2
   0   0   0    0.00    0.00   0
;
"""

    def setUp(self) -> None:
        self.tempdir = Path(tempfile.mkdtemp())
        shutil.copy(Path('test-data/twinabs_multi_options.abs'), self.tempdir / 'twin.abs')
        cif_file = self.tempdir / 't5_dom1.cif'
        cif_file.write_text(self.cif_text, encoding='utf-8')
        self.cif_file = cif_file.resolve()
        self.data = BrukerData(FakeApp(), CifContainer(cif_file))

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_rint_is_calculated_from_the_reflection_data(self):
        # (|100-105| + |110-105|) / (100 + 110 + 200 + 200), the R(int) of twin.abs is ignored
        # and the singles of the minor domain would give 0.0476:
        self.assertEqual((0.0164, f'calculated from {self.cif_file} '
                                  f'(singles of twin component 1, merged in P -1)'),
                         self.data.sources['_diffrn_reflns_av_R_equivalents'])

    def test_the_calculated_value_overrides_the_cif_value(self):
        self.assertIn('_diffrn_reflns_av_R_equivalents', self.data.overrides)


if __name__ == '__main__':
    unittest.main()
