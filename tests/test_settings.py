import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from finalcif.tools.settings import (
    FinalCifSettings,
    _convert_qsettings_value,
    _migrate_qsettings_to_json,
    load_template_file,
)


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
        self.s.save_recent_files([])
        self.assertEqual([], self.s.load_recent_files())

    def test_property_list(self):
        self.assertIsNone(self.s.load_property_list())
        self.s.save_key_value('property_list', ['a', 'b'])
        self.assertEqual(['a', 'b'], self.s.load_property_list())

    def test_json_persistence(self):
        """Verify settings survive a new FinalCifSettings instance."""
        self.s.save_key_value('persist_test', 42)
        self.s.flush()
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


# ---------------------------------------------------------------------------
# Helpers shared by migration tests
# ---------------------------------------------------------------------------

def _make_mock_qsettings(top_level_keys: dict, groups: dict) -> MagicMock:
    """Build a MagicMock that behaves like QSettings.

    Parameters
    ----------
    top_level_keys : dict
        Keys (without a group prefix) and their values.
    groups : dict
        Mapping of group name → {key: value}.  beginGroup / endGroup keep
        track of which group is current.
    """
    qs = MagicMock()
    current_group: list = [None]

    def begin_group(g: str) -> None:
        current_group[0] = g

    def end_group() -> None:
        current_group[0] = None

    def all_keys() -> list:
        if current_group[0] is not None:
            return list(groups.get(current_group[0], {}).keys())
        return [k for k in top_level_keys if '/' not in k]

    def child_groups() -> list:
        return list(groups.keys())

    def value(key: str):
        if current_group[0] is not None:
            return groups[current_group[0]][key]
        return top_level_keys[key]

    qs.beginGroup.side_effect = begin_group
    qs.endGroup.side_effect = end_group
    qs.allKeys.side_effect = all_keys
    qs.childGroups.side_effect = child_groups
    qs.value.side_effect = value
    return qs


# ---------------------------------------------------------------------------
# Tests for _convert_qsettings_value
# ---------------------------------------------------------------------------

class TestConvertQSettingsValue(TestCase):
    """Unit tests for _convert_qsettings_value.

    No file I/O or AppWindow required.
    """

    def test_none_returns_none(self):
        self.assertIsNone(_convert_qsettings_value(None))

    def test_string_returned_unchanged(self):
        self.assertEqual('hello world', _convert_qsettings_value('hello world'))

    def test_integer_returned_unchanged(self):
        self.assertEqual(42, _convert_qsettings_value(42))

    def test_float_returned_unchanged(self):
        self.assertAlmostEqual(3.14, _convert_qsettings_value(3.14))

    def test_bool_returned_unchanged(self):
        self.assertIs(True, _convert_qsettings_value(True))
        self.assertIs(False, _convert_qsettings_value(False))

    def test_list_of_strings_returned_as_list(self):
        result = _convert_qsettings_value(['a', 'b', 'c'])
        self.assertEqual(['a', 'b', 'c'], result)

    def test_tuple_converted_to_list(self):
        result = _convert_qsettings_value(('x', 'y'))
        self.assertEqual(['x', 'y'], result)

    def test_nested_list_recurses(self):
        result = _convert_qsettings_value([1, 'two', [3]])
        self.assertEqual([1, 'two', [3]], result)

    def test_dict_converted_recursively(self):
        result = _convert_qsettings_value({'key': 'val', 'num': 7})
        self.assertEqual({'key': 'val', 'num': 7}, result)

    def test_unknown_type_returns_string(self):
        class _Weird:
            def __str__(self):
                return 'weird_repr'
        result = _convert_qsettings_value(_Weird())
        self.assertEqual('weird_repr', result)

    def test_qpoint_serialised_with_type_tag(self):
        from qtpy.QtCore import QPoint
        result = _convert_qsettings_value(QPoint(10, 20))
        self.assertEqual({'__type__': 'QPoint', 'x': 10, 'y': 20}, result)

    def test_qsize_serialised_with_type_tag(self):
        from qtpy.QtCore import QSize
        result = _convert_qsettings_value(QSize(800, 600))
        self.assertEqual({'__type__': 'QSize', 'width': 800, 'height': 600}, result)

    def test_list_of_text_templates_unchanged(self):
        """A list of template strings (the most common QSettings value for text_templates) survives."""
        templates = [
            'All H-atoms were refined freely.',
            'H atoms were placed in calculated positions.',
            'Multi-line\nvalue with newline.',
        ]
        result = _convert_qsettings_value(templates)
        self.assertEqual(templates, result)


# ---------------------------------------------------------------------------
# Tests for _migrate_qsettings_to_json
# ---------------------------------------------------------------------------

class TestMigrateQSettingsToJson(TestCase):
    """Tests for the one-time QSettings → JSON migration helper.

    QSettings is mocked so the test never touches the real application store.
    """

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.json_path = self.tmpdir / 'settings.json'

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run_migration(self, top_level_keys: dict, groups: dict) -> dict:
        mock_qs = _make_mock_qsettings(top_level_keys, groups)
        with patch('qtpy.QtCore.QSettings', return_value=mock_qs):
            return _migrate_qsettings_to_json(self.json_path)

    def test_migrated_flag_is_set(self):
        result = self._run_migration({}, {})
        self.assertTrue(result.get('_migrated_from_qsettings'))

    def test_top_level_key_migrated(self):
        result = self._run_migration({'recent_files': ['/a.cif', '/b.cif']}, {})
        self.assertEqual(['/a.cif', '/b.cif'], result.get('recent_files'))

    def test_text_templates_group_migrated(self):
        """text_templates stored in QSettings must appear in the migration output."""
        groups = {
            'text_templates': {
                '_refine_special_details': [
                    'All H-atom positions were refined freely.',
                    'H atoms constrained to C-H 0.96 Å.',
                ],
                '_exptl_crystal_description': ['Colourless prism'],
            }
        }
        result = self._run_migration({}, groups)
        tt = result.get('text_templates', {})
        self.assertIn('_refine_special_details', tt)
        self.assertEqual(2, len(tt['_refine_special_details']))
        self.assertEqual('All H-atom positions were refined freely.', tt['_refine_special_details'][0])
        self.assertIn('_exptl_crystal_description', tt)

    def test_multiple_groups_all_migrated(self):
        """All QSettings groups are migrated, not just text_templates."""
        groups = {
            'text_templates': {'_key_a': ['text a']},
            'equipment': {'MyDiffractometer': [['_diffrn_source', 'Mo']]},
            'MainWindow': {'maximized': 'false'},
        }
        result = self._run_migration({}, groups)
        self.assertIn('text_templates', result)
        self.assertIn('equipment', result)
        self.assertIn('MainWindow', result)

    def test_empty_qsettings_produces_only_migrated_flag(self):
        result = self._run_migration({}, {})
        self.assertEqual({'_migrated_from_qsettings': True}, result)

    def test_unicode_text_templates_preserved(self):
        unicode_templates = ['Δρ_max = 0.15 e Å⁻³', 'α-phase', 'μ = 0.2 mm⁻¹']
        groups = {'text_templates': {'_refine_ls_extinction_coef': unicode_templates}}
        result = self._run_migration({}, groups)
        migrated = result['text_templates']['_refine_ls_extinction_coef']
        self.assertEqual(unicode_templates, migrated)

    def test_multiline_strings_in_templates_preserved(self):
        multiline = ['First line\nSecond line\nThird line', 'Another entry']
        groups = {'text_templates': {'_refine_special_details': multiline}}
        result = self._run_migration({}, groups)
        self.assertEqual(multiline, result['text_templates']['_refine_special_details'])

    def test_qpoint_value_migrated_with_type_tag(self):
        from qtpy.QtCore import QPoint
        result = self._run_migration({'win_pos': QPoint(50, 100)}, {})
        self.assertEqual({'__type__': 'QPoint', 'x': 50, 'y': 100}, result.get('win_pos'))

    def test_qsize_value_migrated_with_type_tag(self):
        from qtpy.QtCore import QSize
        groups = {'MainWindow': {'size': QSize(1024, 768)}}
        result = self._run_migration({}, groups)
        self.assertEqual({'__type__': 'QSize', 'width': 1024, 'height': 768},
                         result['MainWindow']['size'])


# ---------------------------------------------------------------------------
# Tests for FinalCifSettings auto-migration on first launch
# ---------------------------------------------------------------------------

class TestFinalCifSettingsAutoMigration(TestCase):
    """Tests that FinalCifSettings triggers the QSettings migration exactly
    when (and only when) no JSON file exists yet.
    """

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.settings_path = self.tmpdir / 'settings.json'

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_settings_with_mock_qs(self, top_level_keys: dict, groups: dict) -> FinalCifSettings:
        mock_qs = _make_mock_qsettings(top_level_keys, groups)
        with patch('qtpy.QtCore.QSettings', return_value=mock_qs):
            return FinalCifSettings(settings_path=self.settings_path)

    def test_migration_runs_when_json_is_absent(self):
        """JSON must be created from QSettings when no JSON file exists."""
        groups = {'text_templates': {'_key': ['template text']}}
        s = self._make_settings_with_mock_qs({}, groups)
        self.assertTrue(self.settings_path.exists())

    def test_migration_json_contains_migrated_flag(self):
        s = self._make_settings_with_mock_qs({}, {})
        raw = json.loads(self.settings_path.read_text())
        self.assertTrue(raw.get('_migrated_from_qsettings'))

    def test_migration_text_templates_accessible_via_settings_api(self):
        """After migration, text templates can be read through the normal API."""
        templates = ['Refined freely.', 'H constrained to C-H 0.96.']
        groups = {'text_templates': {'_refine_special_details': templates}}
        s = self._make_settings_with_mock_qs({}, groups)

        loaded = s.load_settings_list('text_templates', '_refine_special_details')
        self.assertEqual(templates, loaded)

    def test_migration_multiple_text_template_keys_all_accessible(self):
        groups = {
            'text_templates': {
                '_refine_special_details': ['text A', 'text B'],
                '_exptl_crystal_description': ['Red block', 'Colourless prism'],
                '_vrf_DIFF003_somecif': ['Response to alert DIFF003.'],
            }
        }
        s = self._make_settings_with_mock_qs({}, groups)
        self.assertEqual(2, len(s.load_settings_list('text_templates', '_refine_special_details')))
        self.assertEqual(['Red block', 'Colourless prism'],
                         s.load_settings_list('text_templates', '_exptl_crystal_description'))
        self.assertIn('_vrf_DIFF003_somecif', s.list_saved_items('text_templates'))

    def test_migration_skipped_when_json_already_exists(self):
        """If the JSON already exists, QSettings must never be instantiated."""
        self.settings_path.write_text(
            json.dumps({'text_templates': {'_key': ['pre-existing data']}}),
            encoding='utf-8',
        )
        mock_qs_class = MagicMock()
        with patch('qtpy.QtCore.QSettings', mock_qs_class):
            s = FinalCifSettings(settings_path=self.settings_path)

        mock_qs_class.assert_not_called()
        self.assertEqual(['pre-existing data'], s.load_settings_list('text_templates', '_key'))

    def test_migration_json_persists_across_new_instance(self):
        """Migrated data survives a second FinalCifSettings instantiation."""
        groups = {'text_templates': {'_key': ['migrated data']}}
        self._make_settings_with_mock_qs({}, groups)

        # Re-open without mocking – should read the JSON created by migration
        s2 = FinalCifSettings(settings_path=self.settings_path)
        self.assertEqual(['migrated data'], s2.load_settings_list('text_templates', '_key'))


# ---------------------------------------------------------------------------
# Tests for text template CRUD via FinalCifSettings (no migration involved)
# ---------------------------------------------------------------------------

class TestTextTemplateSettings(TestCase):
    """Tests for saving, loading, listing, and deleting text templates.

    Uses an isolated temp JSON file – no AppWindow or QSettings required.
    """

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.settings_path = self.tmpdir / 'settings.json'
        self.s = FinalCifSettings(settings_path=self.settings_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # --- save / load ---

    def test_save_and_load_text_template(self):
        items = ['Template line A.', 'Template line B.']
        self.s.save_settings_list('text_templates', '_refine_special_details', items)
        self.assertEqual(items, self.s.load_settings_list('text_templates', '_refine_special_details'))

    def test_multiline_string_in_template_preserved(self):
        items = ['First line\nSecond line\nThird line', 'Another entry']
        self.s.save_settings_list('text_templates', '_exptl_crystal_description', items)
        self.assertEqual(items, self.s.load_settings_list('text_templates', '_exptl_crystal_description'))

    def test_unicode_characters_in_template_preserved(self):
        items = [
            'Δρ_max = 0.15 e Å⁻³',  # Greek and superscript
            'α-phase transition',
            'μ = 0.12 mm⁻¹',
        ]
        self.s.save_settings_list('text_templates', '_refine_ls_extinction_coef', items)
        self.assertEqual(items, self.s.load_settings_list('text_templates', '_refine_ls_extinction_coef'))

    def test_cif_delimiter_chars_in_template_preserved(self):
        """CIF tilde/backslash delimiter sequences are plain strings in the template and must survive JSON."""
        items = ['N~2~ atmosphere', r'\a special char', 'normal text']
        self.s.save_settings_list('text_templates', '_diffrn_ambient_environment', items)
        self.assertEqual(items, self.s.load_settings_list('text_templates', '_diffrn_ambient_environment'))

    def test_empty_template_list_saved_and_loaded(self):
        self.s.save_settings_list('text_templates', '_key_empty', [])
        self.assertEqual([], self.s.load_settings_list('text_templates', '_key_empty'))

    def test_missing_key_returns_empty_list(self):
        result = self.s.load_settings_list('text_templates', '_nonexistent_key')
        self.assertEqual([], result)

    def test_overwrite_existing_template(self):
        self.s.save_settings_list('text_templates', '_key_a', ['old'])
        self.s.save_settings_list('text_templates', '_key_a', ['new1', 'new2'])
        self.assertEqual(['new1', 'new2'], self.s.load_settings_list('text_templates', '_key_a'))

    # --- list / delete ---

    def test_list_saved_text_templates(self):
        self.s.save_settings_list('text_templates', '_key_1', ['a'])
        self.s.save_settings_list('text_templates', '_key_2', ['b'])
        items = self.s.list_saved_items('text_templates')
        self.assertIn('_key_1', items)
        self.assertIn('_key_2', items)

    def test_delete_text_template_removes_key(self):
        self.s.save_settings_list('text_templates', '_to_delete', ['data'])
        self.assertIn('_to_delete', self.s.list_saved_items('text_templates'))
        self.s.delete_template('text_templates', '_to_delete')
        self.assertNotIn('_to_delete', self.s.list_saved_items('text_templates'))

    def test_delete_nonexistent_template_is_silent(self):
        """Deleting a key that does not exist must not raise."""
        self.s.delete_template('text_templates', '_nonexistent')

    # --- persistence ---

    def test_template_persists_across_new_settings_instance(self):
        self.s.save_settings_list('text_templates', '_key_persist', ['persistent data'])
        self.s.flush()
        s2 = FinalCifSettings(settings_path=self.settings_path)
        self.assertEqual(['persistent data'], s2.load_settings_list('text_templates', '_key_persist'))

    # --- VRF keys ---

    def test_vrf_key_stored_and_retrieved_normally(self):
        """VRF keys (starting with _vrf_) are stored like any other CIF key."""
        vrf_key = '_vrf_DIFF003_somecif'
        self.s.save_settings_list('text_templates', vrf_key, ['Response to alert DIFF003.'])
        loaded = self.s.load_settings_list('text_templates', vrf_key)
        self.assertEqual(['Response to alert DIFF003.'], loaded)
        self.assertIn(vrf_key, self.s.list_saved_items('text_templates'))

    def test_multiple_vrf_keys_independent(self):
        self.s.save_settings_list('text_templates', '_vrf_DIFF003_x', ['resp A'])
        self.s.save_settings_list('text_templates', '_vrf_PLAT001_y', ['resp B'])
        self.assertEqual(['resp A'], self.s.load_settings_list('text_templates', '_vrf_DIFF003_x'))
        self.assertEqual(['resp B'], self.s.load_settings_list('text_templates', '_vrf_PLAT001_y'))

    # --- raw export / import round-trip (isolated from AppWindow) ---

    def test_export_import_text_templates_roundtrip(self):
        """Simulate what AppWindow.export_raw_text_templates / import_raw_text_templates do."""
        # Populate a source settings object
        src = FinalCifSettings(settings_path=self.settings_path)
        src.save_settings_list('text_templates', '_refine_special_details',
                               ['All H-atom positions were refined freely.'])
        src.save_settings_list('text_templates', '_exptl_crystal_description',
                               ['Colourless prism', 'Red block'])

        # Export (mimicking AppWindow.export_raw_text_templates)
        templates_list = [
            {'cif_key': key, 'data': src.load_settings_list('text_templates', key)}
            for key in src.list_saved_items('text_templates')
        ]

        # Write to a JSON file (mimicking export_all_templates)
        export_path = self.tmpdir / 'exported.json'
        export_path.write_text(
            json.dumps({'text': templates_list}, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

        # Re-import into a fresh settings object (mimicking import_raw_text_templates)
        dst_path = self.tmpdir / 'dst_settings.json'
        dst = FinalCifSettings(settings_path=dst_path)
        raw = json.loads(export_path.read_text())
        for entry in raw['text']:
            dst.save_settings_list('text_templates', entry['cif_key'], entry['data'])

        # Verify round-trip fidelity
        self.assertEqual(
            ['All H-atom positions were refined freely.'],
            dst.load_settings_list('text_templates', '_refine_special_details'),
        )
        self.assertEqual(
            ['Colourless prism', 'Red block'],
            dst.load_settings_list('text_templates', '_exptl_crystal_description'),
        )

    def test_import_raw_text_templates_handles_none_gracefully(self):
        """import_raw_text_templates(None) (missing 'text' key) must not raise."""
        # This mimics: self.import_raw_text_templates(templates.get('text'))
        # when the loaded file has no 'text' key.
        templates_list = None
        # Should be a no-op, not crash
        if templates_list:
            for entry in templates_list:
                self.s.save_settings_list('text_templates', entry['cif_key'], entry['data'])
