import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_add_loop(self):
        self.assertEqual(9, self.cif.n_loops)
        self.cif.add_loop_to_cif(loop_tags=['_foo', '_bar'], row_values=['fooval', 'barval'])
        self.assertEqual(10, self.cif.n_loops)
        self.assertEqual(['fooval', 'barval'], self.cif.get_loop('_foo').values)

    def test_add_complete_loop(self):
        loop_data = {'_foo_bar': ['1', '2', '3', '4'], '_baz_hhk': ['omega', 'phi', 'phi', 'chi']}
        self.cif.add_loop_from_columns(list(loop_data.keys()), list(loop_data.values()))
        self.assertEqual(['1', 'omega', '2', 'phi', '3', 'phi', '4', 'chi'],
                         self.cif.get_loop('_foo_bar').values)

    def test_hklf(self):
        self.assertEqual(4, self.cif.hklf_number)

    def test_hkl_as_cif(self):
        result = ('data_cu_BruecknerJK_153F40_0m\n'
                  'loop_\n'
                  '_refln_index_h\n'
                  '_refln_index_k\n'
                  '_refln_index_l\n'
                  '_refln_F_squared_meas\n'
                  '_refln_F_squared_sigma\n'
                  '_refln_scale_group_code\n'
                  '1 0 0 0.36031 0.34981 12\n'
                  '-1 0 0 -0.0279 0.03389 7\n')
        self.assertEqual(result, self.cif.hkl_as_cif[:200])

    def test_publ_flag_not_set(self):
        self.assertEqual("bond(label1='C1', label2='O1', dist='1.438(3)', symm='.')", str(next(iter(self.cif.bonds()))))
        self.cif.block.find_loop('_geom_bond_publ_flag')[0] = 'no'
        # This is not C1-O1, but C1-C14, because the first bond is with publ_flag 'no'.
        self.assertEqual("bond(label1='C1', label2='C14', dist='1.519(3)', symm='.')", str(next(iter(self.cif.bonds()))))
        self.cif.block.find_loop('_geom_bond_publ_flag').erase()
        self.assertEqual([], list(self.cif.block.find_loop('_geom_bond_publ_flag')))
        self.assertEqual("bond(label1='C1', label2='O1', dist='1.438(3)', symm='.')", str(next(iter(self.cif.bonds()))))


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


class TestVrfKeyOrdering(unittest.TestCase):
    """Tests that _vrf_* keys are moved to the top by order_cif_keys() and keys_with_essentials()."""

    def setUp(self) -> None:
        self.cif = CifContainer(data / 'tests/examples/work/cu_BruecknerJK_153F40_0m.cif')

    def test_order_cif_keys_puts_vrf_first(self):
        """After order_cif_keys(), the first key in the block must be a _vrf_* key."""
        self.cif.order_cif_keys()
        keys = self.cif.keys()
        vrf_keys = [k for k in keys if k.startswith('_vrf')]
        self.assertTrue(len(vrf_keys) > 0, 'Test CIF should contain at least one _vrf_* key')
        # All _vrf_* keys should appear before any non-_vrf_* key
        first_non_vrf_index = next((i for i, k in enumerate(keys) if not k.startswith('_vrf')), len(keys))
        last_vrf_index = max((i for i, k in enumerate(keys) if k.startswith('_vrf')), default=-1)
        self.assertLess(last_vrf_index, first_non_vrf_index,
                        '_vrf_* keys should all appear before non-_vrf_* keys after ordering')

    def test_keys_with_essentials_puts_vrf_first_in_questions(self):
        """_vrf_* question keys must appear before non-_vrf_* question keys in the table."""
        questions, _ = self.cif.keys_with_essentials()
        vrf_indices = [i for i, (k, _v) in enumerate(questions) if k.startswith('_vrf')]
        non_vrf_indices = [i for i, (k, _v) in enumerate(questions) if not k.startswith('_vrf')]
        if vrf_indices and non_vrf_indices:
            self.assertLess(max(vrf_indices), min(non_vrf_indices),
                            '_vrf_* question keys should precede non-_vrf_* question keys')

    def test_keys_with_essentials_puts_vrf_first_in_with_values(self):
        """_vrf_* answered keys must appear before non-_vrf_* answered keys in the table."""
        _, with_values = self.cif.keys_with_essentials()
        vrf_indices = [i for i, (k, _v) in enumerate(with_values) if k.startswith('_vrf')]
        non_vrf_indices = [i for i, (k, _v) in enumerate(with_values) if not k.startswith('_vrf')]
        if vrf_indices and non_vrf_indices:
            self.assertLess(max(vrf_indices), min(non_vrf_indices),
                            '_vrf_* answered keys should precede non-_vrf_* answered keys')

    def test_get_vrf_entries_returns_vrf_entries(self):
        """get_vrf_entries() should return VRFEntry instances for each _vrf_* key."""
        from finalcif.cif.vrf_entry import VRFEntry
        entries = self.cif.get_vrf_entries()
        self.assertTrue(len(entries) > 0, 'Test CIF should contain at least one _vrf_* key')
        for entry in entries:
            self.assertIsInstance(entry, VRFEntry)

    def test_get_vrf_entries_key_and_data_name(self):
        """get_vrf_entries() should parse key and data_name correctly."""
        entries = self.cif.get_vrf_entries()
        entry = entries[0]
        self.assertTrue(entry.key.startswith('_vrf_'), f'key should start with _vrf_: {entry.key}')
        self.assertNotEqual('', entry.data_name)

    def test_get_vrf_entries_problem_and_response(self):
        """get_vrf_entries() should parse problem and response from the CIF value."""
        entries = self.cif.get_vrf_entries()
        entry = entries[0]
        self.assertNotEqual('', entry.problem)
        # The test CIF has a response of 'foobar'
        self.assertEqual('foobar', entry.response)


class TestVRFEntry(unittest.TestCase):
    """Unit tests for the VRFEntry dataclass."""

    def test_value_property(self):
        from finalcif.cif.vrf_entry import VRFEntry
        entry = VRFEntry(
            key='_vrf_PLAT035_testdata',
            data_name='testdata',
            problem='something is wrong',
            response='it is fine',
            alert_num='PLAT035',
            level='PLAT035_ALERT_1_A',
        )
        self.assertEqual('PROBLEM: something is wrong\nRESPONSE: it is fine\n', entry.value)

    def test_from_html_form(self):
        from finalcif.cif.vrf_entry import VRFEntry
        form = {
            'name'     : '_vrf_PLAT035_DK_zucker2_0m',
            'data_name': 'DK_zucker2_0m',
            'problem'  : 'Missing value',
            'alert_num': 'PLAT035',
            'level'    : 'PLAT035_ALERT_1_B',
        }
        entry = VRFEntry.from_html_form(form)
        self.assertEqual('_vrf_PLAT035_DK_zucker2_0m', entry.key)
        self.assertEqual('DK_zucker2_0m', entry.data_name)
        self.assertEqual('Missing value', entry.problem)
        self.assertEqual('?', entry.response)
        self.assertEqual('PLAT035', entry.alert_num)
        self.assertEqual('PLAT035_ALERT_1_B', entry.level)


class TestCifAndMmcifNormalization(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_cif_with_cif2_header = Path('tests/statics/test_import_input_with_cif2_header.cif')
        self.temp_mmcif = Path('tests/statics/test_import_input.mmcif')
        self.temp_cif = Path('tests/statics/test_import_input.cif')
        cif_content = "data_test\n_foo_bar 'baz'\n"
        self.temp_cif_with_cif2_header.write_text("#\\#CIF_2.0\n" + cif_content, encoding='utf-8')
        self.temp_mmcif.write_text(cif_content, encoding='utf-8')
        self.temp_cif.write_text(cif_content, encoding='utf-8')

    def tearDown(self) -> None:
        self.temp_cif_with_cif2_header.unlink(missing_ok=True)
        self.temp_mmcif.unlink(missing_ok=True)
        self.temp_cif.unlink(missing_ok=True)

    def test_cif_with_cif2_header_is_normalized_to_cif11(self) -> None:
        with patch('finalcif.cif.cif_file_io.CifContainer._convert_doc_to_cif11',
                   wraps=CifContainer._convert_doc_to_cif11) as mocked:
            container = CifContainer(self.temp_cif_with_cif2_header)
        self.assertIsInstance(container, CifContainer)
        mocked.assert_called_once()

    def test_mmcif_is_normalized_to_cif11(self) -> None:
        with patch('finalcif.cif.cif_file_io.CifContainer._convert_doc_to_cif11',
                   wraps=CifContainer._convert_doc_to_cif11) as mocked:
            container = CifContainer(self.temp_mmcif)
        self.assertIsInstance(container, CifContainer)
        mocked.assert_called_once()

    def test_cif_stays_unchanged(self) -> None:
        with patch('finalcif.cif.cif_file_io.CifContainer._convert_doc_to_cif11',
                   wraps=CifContainer._convert_doc_to_cif11) as mocked:
            container = CifContainer(self.temp_cif)
        self.assertIsInstance(container, CifContainer)
        mocked.assert_not_called()

    def test_cif2_keywords_are_translated_to_cif11_names(self) -> None:
        modern_cif = Path('tests/statics/test_import_input_cif2_keywords.cif')
        modern_cif.write_text("#\\#CIF_2.0\ndata_test\n_cell.length_a 10.1\n", encoding='utf-8')
        self.addCleanup(modern_cif.unlink, missing_ok=True)
        container = CifContainer(modern_cif)
        self.assertEqual('10.1', container['_cell_length_a'])
        self.assertNotIn('_cell.length_a', container.keys())
        self.assertNotIn('_cell.length_a', container)
        self.assertEqual('', container['_cell.length_a'])

    def test_mmcif_keywords_are_translated_to_cif11_names(self) -> None:
        modern_mmcif = Path('tests/statics/test_import_input_mmcif_keywords.mmcif')
        modern_mmcif.write_text("data_test\n_cell.length_a 11.2\n", encoding='utf-8')
        self.addCleanup(modern_mmcif.unlink, missing_ok=True)
        container = CifContainer(modern_mmcif)
        self.assertEqual('11.2', container['_cell_length_a'])
        self.assertNotIn('_cell.length_a', container.keys())
        self.assertNotIn('_cell.length_a', container)

    def test_translation_table_overrides_simple_dot_conversion(self) -> None:
        modern_cif = Path('tests/statics/test_import_input_cif2_translation_table.cif')
        modern_cif.write_text(
            "#\\#CIF_2.0\n"
            "data_test\n"
            "_diffrn.ambient_temperature 120\n",
            encoding='utf-8',
        )
        self.addCleanup(modern_cif.unlink, missing_ok=True)
        container = CifContainer(modern_cif)
        self.assertEqual('120', container['_cell_measurement_temperature'])
        self.assertNotIn('_diffrn_ambient_temperature', container.keys())
        self.assertNotIn('_diffrn.ambient_temperature', container.keys())

    def test_translation_table_handles_space_group_aliases(self) -> None:
        modern_cif = Path('tests/statics/test_import_input_cif2_translation_table_space_group.cif')
        modern_cif.write_text(
            "#\\#CIF_2.0\n"
            "data_test\n"
            "_space_group.IT_number 14\n"
            "_space_group.name_H-M_alt 'P 21/c'\n"
            "_space_group_symop.operation_xyz 'x,y,z'\n",
            encoding='utf-8',
        )
        self.addCleanup(modern_cif.unlink, missing_ok=True)
        container = CifContainer(modern_cif)
        self.assertEqual('14', container['_symmetry_Int_Tables_number'])
        self.assertEqual('P 21/c', container['_symmetry_space_group_name_H-M'])
        self.assertEqual('x,y,z', container['_symmetry_equiv_pos_as_xyz'])
        self.assertNotIn('_space_group_IT_number', container.keys())
        self.assertNotIn('_space_group_name_H-M_alt', container.keys())
        self.assertNotIn('_space_group_symop_operation_xyz', container.keys())

    def test_translation_table_uses_civet_aliases_for_nontrivial_mappings(self) -> None:
        modern_cif = Path('tests/statics/test_import_input_cif2_translation_table_civet_aliases.cif')
        modern_cif.write_text(
            "#\\#CIF_2.0\n"
            "data_test\n"
            "_computing.diffrn_collection 'CrysAlisPro'\n"
            "_refine_ls.shift_over_su_max_lt 0.001\n",
            encoding='utf-8',
        )
        self.addCleanup(modern_cif.unlink, missing_ok=True)
        container = CifContainer(modern_cif)
        self.assertEqual('CrysAlisPro', container['_computing_data_collection'])
        self.assertEqual('0.001', container['_refine_ls_shift/su_max_lt'])
        self.assertNotIn('_computing_diffrn_collection', container.keys())
        self.assertNotIn('_refine_ls_shift_over_su_max_lt', container.keys())

    def test_text_block_content_is_not_keyword_translated(self) -> None:
        modern_cif = Path('tests/statics/test_import_input_cif2_text_block.cif')
        modern_cif.write_text(
            "#\\#CIF_2.0\n"
            "data_test\n"
            "_publ_section_comment\n"
            ";\n"
            "_cell.length_a should stay unchanged inside text blocks.\n"
            ";\n",
            encoding='utf-8',
        )
        self.addCleanup(modern_cif.unlink, missing_ok=True)
        container = CifContainer(modern_cif)
        self.assertIn('_cell.length_a', container['_publ_section_comment'])

    def test_from_cif_pair_parses_problem_and_response(self):
        """from_cif_pair() correctly extracts problem and response from a raw CIF value."""
        import gemmi
        from finalcif.cif.vrf_entry import VRFEntry
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: something is bad\nRESPONSE: it is actually fine\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT307_testdata', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT307_testdata')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT307_testdata', raw_value)
        self.assertEqual('_vrf_PLAT307_testdata', entry.key)
        self.assertEqual('testdata', entry.data_name)
        self.assertEqual('PLAT307', entry.alert_num)
        self.assertEqual('something is bad', entry.problem)
        self.assertEqual('it is actually fine', entry.response)
        self.assertEqual('', entry.level)

    def test_from_cif_pair_multiline_response(self):
        """from_cif_pair() supports multi-line response text."""
        import gemmi
        from finalcif.cif.vrf_entry import VRFEntry
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: short contacts\nRESPONSE: line one\nline two\nline three\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT413_mydata', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT413_mydata')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT413_mydata', raw_value)
        self.assertEqual('line one\nline two\nline three', entry.response)


if __name__ == '__main__':
    unittest.main()
