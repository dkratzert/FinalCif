import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase

from finalcif.tools.settings import FinalCifSettings


class TestFinalCifSettings(TestCase):

    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        # Create a temp JSON file with test fixture data
        self.tmpdir = tempfile.mkdtemp()
        self.settings_path = Path(self.tmpdir) / 'test_settings.json'
        fixture = {
            'property': {
                '_chemical_absolute_configuration': [
                    '_chemical_absolute_configuration',
                    ['', 'rm', 'ad', 'rmad', 'syn', 'unk']
                ],
                '_exptl_absorpt_correction_type': [
                    '_exptl_absorpt_correction_type',
                    ['', 'analytical', 'cylinder', 'empirical', 'gaussian', 'integration',
                     'multi-scan', 'none', 'numerical', 'psi-scan', 'refdelf', 'sphere']
                ],
                '_diffrn_ambient_environment': [
                    '_diffrn_ambient_environment',
                    ['', 'N~2~', 'He', 'vacuum', 'mother liquor', 'Ar', 'H~2~']
                ],
            }
        }
        self.settings_path.write_text(json.dumps(fixture), encoding='utf-8')
        self.s = FinalCifSettings(settings_path=self.settings_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_load_property_values_by_key(self):
        result = [(0, ''), (1, 'N~2~'), (2, 'He'), (3, 'vacuum'), (4, 'mother liquor'), (5, 'Ar'), (6, 'H~2~')]
        self.assertEqual(result, self.s.load_property_values_by_key('_diffrn_ambient_environment'))

    def test_load_cif_keys_of_properties(self):
        self.assertEqual(['_chemical_absolute_configuration', '_exptl_absorpt_correction_type'],
                         self.s.load_cif_keys_of_properties()[:2])

    def test_load_property_values_by_key_empty(self):
        self.assertEqual([(0, '')], self.s.load_property_values_by_key(''))


class TestSettingsSaveLoad(TestCase):

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        self.settings_path = Path(self.tmpdir) / 'test_settings.json'
        self.s = FinalCifSettings(settings_path=self.settings_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_load_key_value(self):
        self.s.save_key_value('test_key', 'test_value')
        self.assertEqual('test_value', self.s.load_value_of_key('test_key'))

    def test_save_and_load_options(self):
        opts = {'report_text': False, 'picture_width': 5.0}
        self.s.save_options(opts)
        loaded = self.s.load_options()
        self.assertFalse(loaded['report_text'])
        self.assertEqual(5.0, loaded['picture_width'])

    def test_save_and_load_settings_list(self):
        self.s.save_settings_list('equipment', 'TestEquip', [['key1', 'val1'], ['key2', 'val2']])
        result = self.s.load_settings_list('equipment', 'TestEquip')
        self.assertEqual([['key1', 'val1'], ['key2', 'val2']], result)

    def test_delete_template(self):
        self.s.save_settings_list('equipment', 'ToDelete', [['a', 'b']])
        self.assertIn('ToDelete', self.s.get_equipment_list())
        self.s.delete_template('equipment', 'ToDelete')
        self.assertNotIn('ToDelete', self.s.get_equipment_list())

    def test_save_and_load_workdir(self):
        self.s.save_current_dir('/some/path')
        self.assertEqual('/some/path', self.s.load_last_workdir())

    def test_recent_files(self):
        self.s.save_recent_files(['/a.cif', '/b.cif'])
        self.assertEqual(['/a.cif', '/b.cif'], self.s.load_recent_files())

    def test_empty_recent_files(self):
        self.assertEqual([], self.s.load_recent_files())

    def test_property_list(self):
        self.assertIsNone(self.s.load_property_list())
        self.s.save_key_value('property_list', ['a', 'b'])
        self.assertEqual(['a', 'b'], self.s.load_property_list())

    def test_json_persistence(self):
        """Verify settings survive a new FinalCifSettings instance."""
        self.s.save_key_value('persist_test', 42)
        s2 = FinalCifSettings(settings_path=self.settings_path)
        self.assertEqual(42, s2.load_value_of_key('persist_test'))

    def test_load_settings_dict(self):
        self.s.save_settings_dict('authors_list', 'Jane', {'name': 'Jane', 'email': 'j@e.com'})
        result = self.s.load_settings_dict('authors_list', 'Jane')
        self.assertEqual({'name': 'Jane', 'email': 'j@e.com'}, result)

    def test_load_settings_dict_returns_non_dict_values(self):
        """Non-dict stored values (e.g. Author dataclass) must not be discarded."""
        # Simulate storing a non-dict value (e.g. a list) – load_settings_dict
        # must return it unchanged rather than returning an empty dict.
        self.s.save_settings_dict('misc', 'key', ['a', 'b', 'c'])
        result = self.s.load_settings_dict('misc', 'key')
        self.assertEqual(['a', 'b', 'c'], result)

    def test_load_settings_dict_returns_empty_dict_when_missing(self):
        """Missing key should still return {}."""
        result = self.s.load_settings_dict('authors_list', 'NonExistent')
        self.assertEqual({}, result)

    def test_default_options(self):
        """When no options are saved, defaults should be returned."""
        opts = self.s.load_options()
        self.assertTrue(opts['report_text'])
        self.assertEqual(7.5, opts['picture_width'])
        self.assertTrue(opts['atoms_table'])

    def test_saved_options_override_defaults(self):
        """Saved option values should be returned instead of defaults."""
        self.s.save_options({'report_text': False, 'picture_width': 3.0, 'without_h': True})
        opts = self.s.load_options()
        self.assertFalse(opts['report_text'])
        self.assertEqual(3.0, opts['picture_width'])
        self.assertTrue(opts['without_h'])
        # Hard-coded overrides should still be present
        self.assertTrue(opts['atoms_table'])
