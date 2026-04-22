"""Tests for JSON-based export/import of all templates."""

import json
import pickle
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase

from finalcif.tools.settings import _custom_encoder, _custom_decoder, load_template_file


def _make_sample_templates(include_author: bool = False) -> dict:
    """Build sample template data.

    When *include_author* is True the authors list contains an Author-tagged
    dict that will trigger the full import chain of
    ``finalcif.equip_property.author_loop_templates``.  Set it to False for
    lightweight tests that should work without the full dependency tree.
    """
    authors: list = []
    if include_author:
        authors = [{
            '__type__': 'Author',
            'name': 'Jane Doe',
            'address': 'University',
            'email': 'jane@example.com',
            'phone': '',
            'orcid': '0000-0000-0000-0001',
            'footnote': '',
            'contact_author': True,
            'author_type': 'publ',
            'iucr_id': '',
        }]
    return {
        'text': [{'cif_key': '_refine_special_details', 'data': ['some text']}],
        'equipment': [{'name': 'Test Equip', 'data': [['_diffrn_source', 'Mo']], 'deleted': []}],
        'properties': [{'name': 'Test Prop', 'cif_key': '_exptl_absorpt_correction_type', 'data': ['multi-scan']}],
        'authors': authors,
        'cif_order': ['_cell_length_a', '_cell_length_b'],
        'cif_order_essential': ['_cell_length_a'],
    }


def _write_json(filepath: Path, templates: dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(templates, f, default=_custom_encoder, ensure_ascii=False, indent=2)


class TestLoadTemplateFile(TestCase):
    """Unit tests for load_template_file (no GUI required)."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # -- JSON round-trip ---------------------------------------------------

    def test_export_json_is_valid(self):
        """Exported JSON file should be parseable and contain expected keys."""
        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertIsInstance(loaded, dict)
        for key in ('text', 'equipment', 'properties', 'authors', 'cif_order', 'cif_order_essential'):
            self.assertIn(key, loaded)

    def test_json_text_templates_roundtrip(self):
        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertEqual([{'cif_key': '_refine_special_details', 'data': ['some text']}], loaded['text'])

    def test_json_equipment_roundtrip(self):
        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertEqual('Test Equip', loaded['equipment'][0]['name'])
        self.assertEqual([['_diffrn_source', 'Mo']], loaded['equipment'][0]['data'])

    def test_json_properties_roundtrip(self):
        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertEqual('Test Prop', loaded['properties'][0]['name'])
        self.assertEqual('_exptl_absorpt_correction_type', loaded['properties'][0]['cif_key'])

    def test_json_cif_order_roundtrip(self):
        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertEqual(['_cell_length_a', '_cell_length_b'], loaded['cif_order'])
        self.assertEqual(['_cell_length_a'], loaded['cif_order_essential'])

    def test_json_authors_roundtrip(self):
        """Author dataclass should survive JSON round-trip via object_hook.

        This test requires the full finalcif dependency tree (gemmi, numpy,
        shelxfile, etc.) because the custom decoder imports Author from
        author_loop_templates.
        """
        try:
            from finalcif.equip_property.author_loop_templates import Author
        except ImportError:
            self.skipTest("Full dependency tree not installed")

        filepath = self.tmpdir / 'templates.json'
        _write_json(filepath, _make_sample_templates(include_author=True))

        loaded = load_template_file(filepath)
        author = loaded['authors'][0]
        self.assertNotIsInstance(author, dict)
        self.assertEqual('Jane Doe', author.name)
        self.assertTrue(author.contact_author)

    # -- Legacy pickle fallback -------------------------------------------

    def test_legacy_pickle_dat_file(self):
        """A legacy .dat pickle file should still be importable."""
        filepath = self.tmpdir / 'legacy.dat'
        templates = _make_sample_templates()
        with open(filepath, 'wb') as f:
            pickle.dump(templates, f)

        loaded = load_template_file(filepath)
        self.assertIsInstance(loaded, dict)
        self.assertIn('text', loaded)
        self.assertIn('authors', loaded)

    # -- .dat file that contains JSON (edge case) -------------------------

    def test_dat_file_with_json_content(self):
        """A .dat file that actually contains JSON should be loaded as JSON."""
        filepath = self.tmpdir / 'new_format.dat'
        _write_json(filepath, _make_sample_templates())

        loaded = load_template_file(filepath)
        self.assertIsInstance(loaded, dict)
        self.assertEqual('Test Equip', loaded['equipment'][0]['name'])
