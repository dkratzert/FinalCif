"""Tests for the PLATON runner's structure factor (.fcf) handling.

Background
----------
FinalCif runs the offline checkCIF on '<name>-finalcif.cif'.  PLATON locates the
structure factors by basename, so it looks for '<name>-finalcif.fcf'.  When that
file is absent PLATON tries to regenerate it by calling SHELXL; if that fails it
reports

    995_ALERT_1_B  Can not Recreate .fcf from Embedded .res & .hkl

and silently skips every structure factor based check (912, 969, 978, ...).

These tests cover the two ways FinalCif can supply the file (embedded
'_shelx_fcf_file' data, or a sibling '<name>.fcf'), that a pre-existing file is
never clobbered or deleted, and that PLATON is pointed at a SHELXL executable.
They do not need PLATON itself.
"""
import os

os.environ["RUNNING_TEST"] = 'True'

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from finalcif.tools.platon import PlatonRunner

FCF_TEXT = 'data_test\n_shelx_refln_list_code 4\nloop_\n_refln_index_h\n1\n'


class PlatonFcfTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def make_runner(self, cif_name: str = 'foo-finalcif.cif', fcf_data: str = '') -> PlatonRunner:
        cif = self.dir / cif_name
        cif.write_text('data_foo\n_cell_length_a 10\n', encoding='ascii')
        return PlatonRunner(parent=None, output_widget=Mock(), log_widget=Mock(),
                            cif_file=cif, fcf_data=fcf_data)

    def test_fcf_target_uses_cif_basename(self):
        runner = self.make_runner()
        self.assertEqual('foo-finalcif.fcf', runner.fcf_target.name)

    def test_embedded_fcf_data_is_written(self):
        runner = self.make_runner(fcf_data=FCF_TEXT)
        runner._provide_fcf_file()
        self.assertTrue(runner.fcf_target.is_file())
        self.assertEqual(FCF_TEXT.replace('\n', '\n'), runner.fcf_target.read_text(encoding='latin1'))

    def test_sibling_fcf_is_copied_to_finalcif_basename(self):
        (self.dir / 'foo.fcf').write_text(FCF_TEXT, encoding='ascii')
        runner = self.make_runner()
        runner._provide_fcf_file()
        self.assertTrue(runner.fcf_target.is_file())
        self.assertEqual(FCF_TEXT, runner.fcf_target.read_text(encoding='latin1'))

    def test_embedded_data_wins_over_sibling_file(self):
        (self.dir / 'foo.fcf').write_text('sibling', encoding='ascii')
        runner = self.make_runner(fcf_data=FCF_TEXT)
        runner._provide_fcf_file()
        self.assertEqual(FCF_TEXT, runner.fcf_target.read_text(encoding='latin1'))

    def test_no_fcf_anywhere_creates_nothing(self):
        runner = self.make_runner()
        runner._provide_fcf_file()
        self.assertFalse(runner.fcf_target.exists())
        self.assertIsNone(runner._temporary_fcf)

    def test_existing_fcf_is_not_overwritten(self):
        target = self.dir / 'foo-finalcif.fcf'
        target.write_text('user data', encoding='ascii')
        runner = self.make_runner(fcf_data=FCF_TEXT)
        runner._provide_fcf_file()
        self.assertEqual('user data', target.read_text(encoding='latin1'))
        self.assertIsNone(runner._temporary_fcf)

    def test_created_fcf_is_removed_afterwards(self):
        runner = self.make_runner(fcf_data=FCF_TEXT)
        runner._provide_fcf_file()
        self.assertTrue(runner.fcf_target.is_file())
        runner._remove_temporary_fcf()
        self.assertFalse(runner.fcf_target.exists())

    def test_user_fcf_survives_orphan_cleanup(self):
        """A small .fcf belonging to the user must not be deleted."""
        target = self.dir / 'foo-finalcif.fcf'
        target.write_text('tiny', encoding='ascii')  # < 100 bytes
        runner = self.make_runner()
        runner._provide_fcf_file()
        runner.delete_orphaned_files()
        runner._remove_temporary_fcf()
        self.assertTrue(target.is_file())

    def test_cif_without_finalcif_suffix_finds_no_sibling(self):
        """'foo.cif' and 'foo.fcf' already share a basename; nothing to copy."""
        (self.dir / 'foo.fcf').write_text(FCF_TEXT, encoding='ascii')
        runner = self.make_runner(cif_name='foo.cif')
        self.assertIsNone(runner._find_sibling_fcf())

    def test_shelxl_exe_accepts_the_bruker_xl_name(self):
        """PLATON falls back from 'shelxl' to 'xl'; so must we."""
        import finalcif.tools.platon as platon_module

        calls = []

        def fake_which(name):
            calls.append(name)
            return str(self.dir / 'xl.exe') if name == 'xl' else None

        (self.dir / 'xl.exe').write_text('', encoding='ascii')
        original = platon_module.which
        platon_module.which = fake_which
        try:
            runner = self.make_runner()
            self.assertEqual(str((self.dir / 'xl.exe').resolve()), runner.shelxl_exe)
        finally:
            platon_module.which = original
        self.assertEqual(['shelxl', 'xl'], calls)

    def test_shelxl_exe_empty_when_nothing_found(self):
        import finalcif.tools.platon as platon_module

        original = platon_module.which
        platon_module.which = lambda name: None
        try:
            runner = self.make_runner()
            self.assertEqual('', runner.shelxl_exe)
        finally:
            platon_module.which = original


if __name__ == '__main__':
    unittest.main()
