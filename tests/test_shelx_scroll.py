"""Tests for SHELXL-file navigation helpers.

No AppWindow is instantiated.  Each test uses only:
- ``CifContainer`` to obtain a parsed ``shelxfile.Shelxfile`` (``shx``) and
  the raw SHELXL text.
- A plain ``QPlainTextEdit`` populated with that text.
- The two standalone functions from ``finalcif.gui.shelx_navigation``.
"""
import os

os.environ["RUNNING_TEST"] = "True"

import unittest
from pathlib import Path

import gemmi.cif as gcif
from qtpy.QtWidgets import QApplication, QPlainTextEdit

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.shelx_navigation import find_shelx_line_for_atom, scroll_and_highlight_shelx_atom

app = QApplication.instance() or QApplication([])

P21C = Path("test-data/p21c.cif")


def _make_text_edit(cif: CifContainer) -> QPlainTextEdit:
    """Return a QPlainTextEdit pre-filled with the SHELXL content from *cif*,
    using the same text source as AppWindow._show_shelx_file."""
    text_edit = QPlainTextEdit()
    text_edit.setPlainText(gcif.as_string(cif.res_file_data))
    return text_edit


class TestFindShelxLineForAtom(unittest.TestCase):
    """Unit tests for the atom→line-number lookup (pure logic, no Qt needed)."""

    @classmethod
    def setUpClass(cls) -> None:
        cif = CifContainer(P21C)
        cls.shx = cif.shx

    # ------------------------------------------------------------------
    # Case-insensitive matching
    # ------------------------------------------------------------------

    def test_exact_uppercase_match(self) -> None:
        self.assertEqual(37, find_shelx_line_for_atom(self.shx, "GA1"))

    def test_mixed_case_match(self) -> None:
        """CIF label 'Ga1' resolves to SHELXL 'GA1'."""
        self.assertEqual(37, find_shelx_line_for_atom(self.shx, "Ga1"))

    def test_all_lowercase_match(self) -> None:
        self.assertEqual(37, find_shelx_line_for_atom(self.shx, "ga1"))

    def test_unknown_atom_returns_minus_one(self) -> None:
        self.assertEqual(-1, find_shelx_line_for_atom(self.shx, "XX99"))

    # ------------------------------------------------------------------
    # Symmetry copies  (>>N suffix, single ASU entry)
    # ------------------------------------------------------------------

    def test_symm_copy_clamps_to_asu(self) -> None:
        """'Ga1>>3' (symmetry copy) maps to the same ASU line as 'Ga1'."""
        self.assertEqual(
            find_shelx_line_for_atom(self.shx, "Ga1"),
            find_shelx_line_for_atom(self.shx, "Ga1>>3"),
        )

    def test_large_occurrence_clamps(self) -> None:
        """Very large >>N index still finds the atom."""
        line = find_shelx_line_for_atom(self.shx, "Al1>>100")
        self.assertGreater(line, 0)

    def test_residue_symm_copy_clamps(self) -> None:
        """'F4_1>>5' (symm copy of residue atom) maps to the same line as 'F4_1'."""
        self.assertEqual(
            find_shelx_line_for_atom(self.shx, "F4_1"),
            find_shelx_line_for_atom(self.shx, "F4_1>>5"),
        )

    # ------------------------------------------------------------------
    # Residue atoms  (CIF label "F4_3" → SHELXL atom F4 in RESI 3)
    # ------------------------------------------------------------------

    def test_residue_atom_no_suffix(self) -> None:
        """'F4' without residue suffix matches the non-residue ASU atom (line 83)."""
        self.assertEqual(83, find_shelx_line_for_atom(self.shx, "F4"))

    def test_residue_atom_resi1(self) -> None:
        """'F4_1' resolves to F4 in residue 1 (line 199)."""
        self.assertEqual(199, find_shelx_line_for_atom(self.shx, "F4_1"))

    def test_residue_atom_resi2(self) -> None:
        """'F4_2' resolves to F4 in residue 2 (line 232)."""
        self.assertEqual(232, find_shelx_line_for_atom(self.shx, "F4_2"))

    def test_residue_atom_resi3(self) -> None:
        """'F4_3' resolves to F4 in residue 3 (line 265)."""
        self.assertEqual(265, find_shelx_line_for_atom(self.shx, "F4_3"))

    def test_residue_atom_resi4(self) -> None:
        """'F4_4' resolves to F4 in residue 4 (line 300)."""
        self.assertEqual(300, find_shelx_line_for_atom(self.shx, "F4_4"))

    def test_residue_atom_case_insensitive(self) -> None:
        """Residue atom lookup is case-insensitive: 'f4_1' == 'F4_1'."""
        self.assertEqual(
            find_shelx_line_for_atom(self.shx, "F4_1"),
            find_shelx_line_for_atom(self.shx, "f4_1"),
        )

    def test_residue_atom_unknown_resi(self) -> None:
        """An atom label with a non-existent residue number returns -1."""
        self.assertEqual(-1, find_shelx_line_for_atom(self.shx, "F4_99"))


class TestScrollAndHighlight(unittest.TestCase):
    """Integration tests for scroll_and_highlight_shelx_atom using a bare QPlainTextEdit."""

    @classmethod
    def setUpClass(cls) -> None:
        cif = CifContainer(P21C)
        cls.shx = cif.shx
        cls.text_edit = _make_text_edit(cif)

    def _cursor_line(self) -> int:
        return self.text_edit.textCursor().blockNumber()

    # ------------------------------------------------------------------
    # Cursor position
    # ------------------------------------------------------------------

    def test_scroll_ga1_cursor_line(self) -> None:
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        self.assertEqual(37, self._cursor_line())

    def test_scroll_symm_copy_same_line_as_asu(self) -> None:
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        line_asu = self._cursor_line()
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1>>5")
        self.assertEqual(line_asu, self._cursor_line())

    def test_scroll_disorder_part1(self) -> None:
        """Scrolling to 'O1_1' (CIF label for O1 in residue 1) lands on line 185."""
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "O1_1")
        self.assertEqual(185, self._cursor_line())

    def test_scroll_disorder_part2(self) -> None:
        """Scrolling to 'O1_2' (CIF label for O1 in residue 2) lands on line 218."""
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "O1_2")
        self.assertEqual(218, self._cursor_line())

    def test_unknown_atom_no_crash(self) -> None:
        try:
            scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "NONEXISTENT99")
        except Exception as exc:
            self.fail(f"scroll_and_highlight_shelx_atom raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # Extra selection / highlight
    # ------------------------------------------------------------------

    def test_sets_one_extra_selection(self) -> None:
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        self.assertEqual(1, len(self.text_edit.extraSelections()))

    def test_extra_selection_on_correct_line(self) -> None:
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        sel = self.text_edit.extraSelections()[0]
        self.assertEqual(37, sel.cursor.blockNumber())

    def test_highlight_replaces_previous(self) -> None:
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Al1")
        sels = self.text_edit.extraSelections()
        self.assertEqual(1, len(sels))
        self.assertNotEqual(37, sels[0].cursor.blockNumber())

    def test_highlight_is_bold(self) -> None:
        from qtpy.QtGui import QFont
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "Ga1")
        sel = self.text_edit.extraSelections()[0]
        self.assertEqual(QFont.Weight.Bold, sel.format.fontWeight())

    def test_unknown_atom_leaves_no_extra_selection(self) -> None:
        self.text_edit.setExtraSelections([])
        scroll_and_highlight_shelx_atom(self.text_edit, self.shx, "NONEXISTENT99")
        self.assertEqual(0, len(self.text_edit.extraSelections()))


if __name__ == "__main__":
    unittest.main()




