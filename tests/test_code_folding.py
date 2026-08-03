"""Tests for the lazy code folding of the CIF text view."""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest

from qtpy.QtWidgets import QApplication

from finalcif.gui.file_editor import (FoldRegion, QCodeEditor, build_folded_text, find_foldable_regions,
                                      fold_placeholder)
from finalcif.gui.syntax_highlighter import FOLD_PLACEHOLDER_PREFIX

app = QApplication.instance() or QApplication([])


def _cif_with_hkl(rows: int) -> str:
    lines = ['data_test', '_cell_length_a 10.0', '_shelx_hkl_file']
    lines.append(';')
    lines.extend(f'   1   2   {n}   12.34    1.23' for n in range(rows))
    lines.append(';')
    lines.append('_shelx_hkl_checksum 12345')
    return '\n'.join(lines)


def _cif_with_loop(rows: int) -> str:
    lines = ['data_test', 'loop_', '_refln_index_h', '_refln_index_k', '_refln_index_l']
    lines.extend(f'1 2 {n}' for n in range(rows))
    lines.append('')
    lines.append('_cell_length_a 10.0')
    return '\n'.join(lines)


class TestFindFoldableRegions(unittest.TestCase):

    def test_semicolon_field_is_foldable_without_its_delimiters(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        regions = find_foldable_regions(lines)
        self.assertEqual(1, len(regions))
        self.assertEqual(600, regions[0].line_count)
        self.assertEqual(';', lines[regions[0].first - 1])
        self.assertEqual(';', lines[regions[0].last + 1])

    def test_loop_body_is_foldable_without_its_tags(self) -> None:
        lines = _cif_with_loop(700).split('\n')
        regions = find_foldable_regions(lines)
        self.assertEqual(1, len(regions))
        self.assertEqual(700, regions[0].line_count)
        self.assertEqual('_refln_index_l', lines[regions[0].first - 1])
        self.assertEqual('1 2 0', lines[regions[0].first])

    def test_regions_below_the_threshold_are_kept_visible(self) -> None:
        self.assertEqual([], find_foldable_regions(_cif_with_hkl(499).split('\n')))
        self.assertEqual([], find_foldable_regions(_cif_with_loop(499).split('\n')))

    def test_threshold_is_configurable(self) -> None:
        regions = find_foldable_regions(_cif_with_loop(10).split('\n'), min_lines=5)
        self.assertEqual(1, len(regions))

    def test_several_regions_are_found(self) -> None:
        text = _cif_with_hkl(600) + '\n' + _cif_with_loop(600)
        self.assertEqual(2, len(find_foldable_regions(text.split('\n'))))

    def test_no_regions_in_a_cif_without_bulk_data(self) -> None:
        text = 'data_test\n_cell_length_a 10.0\n_cell_length_b 11.0\n'
        self.assertEqual([], find_foldable_regions(text.split('\n')))


class TestBuildFoldedText(unittest.TestCase):

    def test_folded_lines_are_replaced_by_a_single_placeholder(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        regions = find_foldable_regions(lines)
        folded = build_folded_text(lines, regions)
        self.assertEqual(len(lines) - 600 + 1, len(folded.lines))
        self.assertIn(fold_placeholder(regions[0]), folded.lines)

    def test_placeholder_uses_the_prefix_known_to_the_highlighter(self) -> None:
        self.assertTrue(fold_placeholder(FoldRegion(1, 600)).startswith(FOLD_PLACEHOLDER_PREFIX))

    def test_expanded_region_keeps_all_lines(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        regions = find_foldable_regions(lines)
        regions[0].folded = False
        folded = build_folded_text(lines, regions)
        self.assertEqual(lines, folded.lines)
        self.assertEqual(list(range(len(lines))), folded.line_map)

    def test_line_map_keeps_the_original_line_numbers(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        folded = build_folded_text(lines, find_foldable_regions(lines))
        self.assertEqual([0, 1, 2, 3, -1, 604, 605], folded.line_map)

    def test_marker_sits_only_on_the_header_line(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        folded = build_folded_text(lines, find_foldable_regions(lines))
        self.assertEqual({3: 0}, folded.marker_rows)

    def test_marker_stays_on_the_header_line_when_expanded(self) -> None:
        lines = _cif_with_hkl(600).split('\n')
        regions = find_foldable_regions(lines)
        regions[0].folded = False
        self.assertEqual({3: 0}, build_folded_text(lines, regions).marker_rows)


class TestQCodeEditorFolding(unittest.TestCase):

    def setUp(self) -> None:
        self.editor = QCodeEditor()
        self.editor.resize(800, 600)

    def tearDown(self) -> None:
        self.editor.deleteLater()

    def test_large_cif_is_folded_by_default(self) -> None:
        self.editor.set_cif_text(_cif_with_hkl(600))
        self.assertEqual(1, len(self.editor.fold_regions))
        self.assertTrue(self.editor.fold_regions[0].folded)
        self.assertEqual(7, self.editor.document().blockCount())

    def test_toggling_a_region_shows_and_hides_its_lines(self) -> None:
        self.editor.set_cif_text(_cif_with_hkl(600))
        self.assertTrue(self.editor.toggle_fold_of_block(3))
        self.assertEqual(606, self.editor.document().blockCount())
        self.assertTrue(self.editor.toggle_fold_of_block(3))
        self.assertEqual(7, self.editor.document().blockCount())

    def test_toggling_a_block_without_a_marker_does_nothing(self) -> None:
        self.editor.set_cif_text(_cif_with_hkl(600))
        self.assertFalse(self.editor.toggle_fold_of_block(0))
        self.assertEqual(7, self.editor.document().blockCount())

    def test_line_numbers_are_the_ones_of_the_file(self) -> None:
        self.editor.set_cif_text(_cif_with_hkl(600))
        self.assertEqual(4, self.editor.original_line_number(3))
        self.assertEqual(-1 + 1, self.editor.original_line_number(4))  # placeholder has no number
        self.assertEqual(605, self.editor.original_line_number(5))

    def test_small_cif_is_shown_completely(self) -> None:
        text = 'data_test\n_cell_length_a 10.0\n'
        self.editor.set_cif_text(text)
        self.assertEqual([], self.editor.fold_regions)
        self.assertEqual(text, self.editor.toPlainText())

    def test_placeholder_line_is_marked_for_the_highlighter(self) -> None:
        self.editor.set_cif_text(_cif_with_hkl(600))
        placeholder = self.editor.document().findBlockByNumber(4).text()
        self.assertTrue(placeholder.startswith(FOLD_PLACEHOLDER_PREFIX))
        self.assertIn('600 lines folded', placeholder)


if __name__ == '__main__':
    unittest.main()
