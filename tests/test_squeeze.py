#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

os.environ["RUNNING_TEST"] = 'True'

from qtpy.QtWidgets import QApplication

from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.squeeze import electrons_from_formula, build_details_text

app = QApplication.instance()
if app is None:
    app = QApplication([])

FIXTURES = Path(__file__).parent / 'fixtures'
SQF_FILE = FIXTURES / 'squeeze_test.sqf'
SMTBX_FILE = FIXTURES / 'smtbx_test.cif'


# ---------------------------------------------------------------------------
# Helper: build a minimal CIF with a SQUEEZE loop already loaded
# ---------------------------------------------------------------------------

def _make_cif_with_squeeze_loop() -> CifContainer:
    """Return a CifContainer that already has the SQUEEZE void loop populated."""
    cif = CifContainer(SQF_FILE)
    return cif


# ---------------------------------------------------------------------------
# electrons_from_formula
# ---------------------------------------------------------------------------

class TestElectronsFromFormula(unittest.TestCase):

    def test_water(self):
        # H2O: H=1*2 + O=8 = 10
        self.assertEqual(10, electrons_from_formula('H2O'))

    def test_two_water(self):
        # 2(H2O) = 20
        self.assertEqual(20, electrons_from_formula('2(H2O)'))

    def test_thf(self):
        # C4H8O: C=6*4 + H=1*8 + O=8 = 40
        self.assertEqual(40, electrons_from_formula('C4H8O'))

    def test_dcm(self):
        # CH2Cl2: C=6 + H=1*2 + Cl=17*2 = 42
        self.assertEqual(42, electrons_from_formula('CH2Cl2'))

    def test_empty_formula(self):
        self.assertEqual(0, electrons_from_formula(''))

    def test_question_mark(self):
        self.assertEqual(0, electrons_from_formula('?'))

    def test_none_like(self):
        self.assertEqual(0, electrons_from_formula('.'))

    def test_unknown_element(self):
        # Unknown element 'Xx' contributes 0
        self.assertEqual(0, electrons_from_formula('Xx2'))

    def test_mixed(self):
        # C4H8O + H2O part 2*(H2O) = 40 + 20 — not mixed in one call but individually fine
        self.assertEqual(40, electrons_from_formula('C4H8O'))
        self.assertEqual(20, electrons_from_formula('2(H2O)'))

    def test_nested_parens(self):
        # Diethyl ether: C4H10O
        self.assertEqual(42, electrons_from_formula('(C2H5)2O'))


# ---------------------------------------------------------------------------
# build_details_text
# ---------------------------------------------------------------------------

class TestBuildDetailsText(unittest.TestCase):

    def test_single_void(self):
        rows = [{'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': 'CH2Cl2'}]
        text = build_details_text(rows)
        self.assertIn('CH2Cl2', text)
        self.assertIn('42', text)
        self.assertIn('248.3', text)
        self.assertIn('SQUEEZE', text)

    def test_two_voids(self):
        rows = [
            {'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': 'CH2Cl2'},
            {'nr': 2, 'volume': '98.1', 'electrons_platon': '18', 'formula': '3(H2O)'},
        ]
        text = build_details_text(rows)
        self.assertEqual(2, text.count('SQUEEZE'))

    def test_empty_formula_skipped(self):
        rows = [{'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': ''}]
        self.assertEqual('', build_details_text(rows))

    def test_question_mark_skipped(self):
        rows = [{'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': '?'}]
        self.assertEqual('', build_details_text(rows))


# ---------------------------------------------------------------------------
# SqueezeSolventDialog – structural / logic tests (no window shown)
# ---------------------------------------------------------------------------

class TestSqueezeSolventDialog(unittest.TestCase):

    def setUp(self):
        from finalcif.gui.squeeze_dialog import SqueezeSolventDialog
        self.SqueezeSolventDialog = SqueezeSolventDialog
        self.cif = _make_cif_with_squeeze_loop()

    def tearDown(self):
        if hasattr(self, 'dialog'):
            self.dialog.close()

    def _make_dialog(self) -> 'SqueezeSolventDialog':
        dlg = self.SqueezeSolventDialog(cif=self.cif)
        self.dialog = dlg
        return dlg

    def test_dialog_opens(self):
        dlg = self._make_dialog()
        self.assertIsNotNone(dlg)

    def test_table_has_two_rows(self):
        dlg = self._make_dialog()
        self.assertEqual(2, dlg.table.rowCount())

    def test_platon_electron_count_is_correct(self):
        dlg = self._make_dialog()
        # From fixture: void 1 has 42 electrons
        elec_item = dlg.table.item(0, 2)  # _COL_ELEC_PLATON
        self.assertEqual('42', elec_item.text())

    def test_formula_column_is_editable(self):
        dlg = self._make_dialog()
        from qtpy.QtCore import Qt
        item = dlg.table.item(0, 3)  # _COL_FORMULA
        self.assertTrue(bool(item.flags() & Qt.ItemFlag.ItemIsEditable))

    def test_volume_column_is_not_editable(self):
        dlg = self._make_dialog()
        from qtpy.QtCore import Qt
        item = dlg.table.item(0, 1)  # _COL_VOL
        self.assertFalse(bool(item.flags() & Qt.ItemFlag.ItemIsEditable))

    def test_fill_down_copies_formula(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')
        dlg.fill_down_btn.click()
        self.assertEqual('CH2Cl2', dlg.formula_for_row(1))

    def test_calculated_electrons_correct(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')  # 42 electrons
        self.assertEqual('42', dlg.table.item(0, 4).text())  # _COL_ELEC_CALC

    def test_delta_is_zero_for_exact_match(self):
        dlg = self._make_dialog()
        # Void 1 has 42 PLATON electrons; CH2Cl2 also has 42 electrons
        dlg.table.item(0, 3).setText('CH2Cl2')
        self.assertEqual('0', dlg.delta_for_row(0))

    def test_delta_coloring_ok(self):
        """Delta within ±5 should get green background."""
        from qtpy.QtGui import QColor
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')  # Δ = 0
        delta_item = dlg.table.item(0, 5)  # _COL_DELTA
        self.assertEqual(QColor(200, 255, 200), delta_item.background().color())

    def test_delta_coloring_warn(self):
        """Delta > 5 should get red background."""
        from qtpy.QtGui import QColor
        dlg = self._make_dialog()
        # C6H6 = 6*6 + 1*6 = 42 electrons; but void 1 has 42 — use H2O (10e) for red
        dlg.table.item(0, 3).setText('H2O')  # Δ = 10 - 42 = -32
        delta_item = dlg.table.item(0, 5)
        self.assertEqual(QColor(255, 200, 200), delta_item.background().color())

    def test_empty_formula_clears_delta_and_colors(self):
        """Clearing the formula should reset Δ and both calc/delta cells to neutral."""
        from qtpy.QtGui import QColor
        dlg = self._make_dialog()
        # First set a formula to get a colored delta
        dlg.table.item(0, 3).setText('H2O')
        # Now clear it
        dlg.table.item(0, 3).setText('')
        delta_item = dlg.table.item(0, 5)   # _COL_DELTA
        calc_item = dlg.table.item(0, 4)    # _COL_ELEC_CALC
        self.assertEqual('', delta_item.text())
        self.assertEqual('', calc_item.text())
        self.assertEqual(QColor(255, 255, 255), delta_item.background().color())
        self.assertEqual(QColor(255, 255, 255), calc_item.background().color())

    def test_manual_details_edit_not_overwritten(self):
        """If user has edited the details text, formula changes should not overwrite it."""
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')   # trigger auto-generation
        dlg.details_edit.setPlainText('My custom text')  # simulate user edit
        dlg.table.item(0, 3).setText('3(H2O)')   # change formula
        self.assertEqual('My custom text', dlg.details_edit.toPlainText())

    def test_auto_details_generated_before_manual_edit(self):
        """Auto-generation works normally until the user touches the text area."""
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')
        text_after_auto = dlg.details_edit.toPlainText()
        self.assertIn('CH2Cl2', text_after_auto)
        # Change formula — should still auto-update (no user edit yet)
        dlg.table.item(0, 3).setText('H2O')
        self.assertIn('H2O', dlg.details_edit.toPlainText())
        self.assertNotIn('CH2Cl2', dlg.details_edit.toPlainText())

    def test_details_auto_generated(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')
        text = dlg.details_edit.toPlainText()
        self.assertIn('CH2Cl2', text)
        self.assertIn('SQUEEZE', text)

    def test_accept_writes_to_cif(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')
        dlg.table.item(1, 3).setText('3(H2O)')
        dlg._on_accept()
        contents = self.cif.get_loop_column('_platon_squeeze_void_content')
        self.assertEqual('CH2Cl2', contents[0])
        self.assertEqual('3(H2O)', contents[1])

    def test_accept_writes_details_to_cif(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('CH2Cl2')
        dlg._on_accept()
        details = self.cif['_platon_squeeze_details']
        self.assertIn('CH2Cl2', details)
        self.assertIn('SQUEEZE', details)

    def test_fill_down_with_single_row(self):
        """Fill-down on a single-void structure should not raise."""
        # Build a CIF with only one void
        sqf_text = (
            'data_single\n'
            'loop_\n'
            ' _platon_squeeze_void_nr\n'
            ' _platon_squeeze_void_volume\n'
            ' _platon_squeeze_void_count_electrons\n'
            ' _platon_squeeze_void_content\n'
            ' _platon_squeeze_void_probe_radius\n'
            '  1  100.0  20  ?  1.20\n'
        )
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.cif', mode='w', delete=False) as f:
            f.write(sqf_text)
            tmp_path = Path(f.name)
        dlg = None
        try:
            cif = CifContainer(tmp_path)
            dlg = self.SqueezeSolventDialog(cif=cif)
            dlg.table.item(0, 3).setText('H2O')
            dlg.fill_down_btn.click()  # Should not raise
            self.assertEqual('H2O', dlg.formula_for_row(0))
        finally:
            tmp_path.unlink(missing_ok=True)
            if dlg is not None:
                dlg.close()


# ---------------------------------------------------------------------------
# build_details_text – smtbx method
# ---------------------------------------------------------------------------

class TestBuildDetailsTextSmtbx(unittest.TestCase):

    def test_default_method_is_squeeze(self):
        """build_details_text() without method argument should generate SQUEEZE text."""
        rows = [{'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': 'CH2Cl2'}]
        text = build_details_text(rows)
        self.assertIn('SQUEEZE', text)
        self.assertNotIn('SMTBX', text)

    def test_smtbx_mentions_olex2(self):
        rows = [{'nr': 1, 'volume': '471.7', 'electrons_platon': '165.7', 'formula': '16(H2O)'}]
        text = build_details_text(rows, method='smtbx')
        self.assertIn('Olex2', text)
        self.assertIn('SMTBX', text)
        self.assertNotIn('SQUEEZE', text)

    def test_smtbx_includes_formula_and_volume(self):
        rows = [{'nr': 1, 'volume': '471.7', 'electrons_platon': '165.7', 'formula': '16(H2O)'}]
        text = build_details_text(rows, method='smtbx')
        self.assertIn('16(H2O)', text)
        self.assertIn('471.7', text)

    def test_squeeze_still_mentions_squeeze(self):
        rows = [{'nr': 1, 'volume': '248.3', 'electrons_platon': '42', 'formula': 'CH2Cl2'}]
        text = build_details_text(rows, method='squeeze')
        self.assertIn('SQUEEZE', text)
        self.assertNotIn('SMTBX', text)


# ---------------------------------------------------------------------------
# SqueezeSolventDialog – smtbx masks mode
# ---------------------------------------------------------------------------

class TestSmtbxMasksDialog(unittest.TestCase):

    def setUp(self):
        from finalcif.gui.squeeze_dialog import SqueezeSolventDialog
        self.SqueezeSolventDialog = SqueezeSolventDialog
        self.cif = CifContainer(SMTBX_FILE)

    def tearDown(self):
        if hasattr(self, 'dialog'):
            self.dialog.close()

    def _make_dialog(self) -> 'SqueezeSolventDialog':
        dlg = self.SqueezeSolventDialog(cif=self.cif)
        self.dialog = dlg
        return dlg

    def test_auto_detects_smtbx_mode(self):
        from finalcif.gui.squeeze_dialog import SqueezeMode
        dlg = self._make_dialog()
        self.assertEqual(SqueezeMode.SMTBX, dlg._loop_mode)

    def test_title_reflects_smtbx(self):
        dlg = self._make_dialog()
        self.assertIn('SMTBX', dlg.windowTitle())
        self.assertIn('Olex2', dlg.windowTitle())

    def test_table_has_two_rows(self):
        dlg = self._make_dialog()
        self.assertEqual(2, dlg.table.rowCount())

    def test_electron_count_loaded(self):
        dlg = self._make_dialog()
        # Fixture: both voids have 165.7 electrons
        elec_item = dlg.table.item(0, 2)  # _COL_ELEC_PLATON
        self.assertEqual('165.7', elec_item.text())

    def test_volume_loaded(self):
        dlg = self._make_dialog()
        vol_item = dlg.table.item(0, 1)  # _COL_VOL
        self.assertEqual('471.7', vol_item.text())

    def test_formula_editable(self):
        dlg = self._make_dialog()
        from qtpy.QtCore import Qt
        item = dlg.table.item(0, 3)  # _COL_FORMULA
        self.assertTrue(bool(item.flags() & Qt.ItemFlag.ItemIsEditable))

    def test_fill_down_works(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('16(H2O)')
        dlg.fill_down_btn.click()
        self.assertEqual('16(H2O)', dlg.formula_for_row(1))

    def test_details_mentions_smtbx(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('16(H2O)')
        text = dlg.details_edit.toPlainText()
        self.assertIn('SMTBX', text)
        self.assertIn('Olex2', text)

    def test_accept_writes_content_to_cif(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('16(H2O)')
        dlg.table.item(1, 3).setText('16(H2O)')
        dlg._on_accept()
        contents = self.cif.get_loop_column('_smtbx_masks_void_content')
        self.assertEqual('16(H2O)', contents[0])
        self.assertEqual('16(H2O)', contents[1])

    def test_accept_writes_details_to_cif(self):
        dlg = self._make_dialog()
        dlg.table.item(0, 3).setText('16(H2O)')
        dlg._on_accept()
        details = self.cif['_smtbx_masks_special_details']
        self.assertIn('16(H2O)', details)
        self.assertIn('SMTBX', details)

    def test_explicit_mode_parameter(self):
        """Passing SqueezeMode.SMTBX explicitly should work even if auto-detection would differ."""
        from finalcif.gui.squeeze_dialog import SqueezeMode
        dlg = self.SqueezeSolventDialog(cif=self.cif, mode=SqueezeMode.SMTBX)
        self.dialog = dlg
        self.assertEqual(SqueezeMode.SMTBX, dlg._loop_mode)
        dlg.close()

    def test_invalid_mode_raises_type_error(self):
        """Passing an invalid mode should raise TypeError."""
        with self.assertRaises(TypeError):
            self.SqueezeSolventDialog(cif=self.cif, mode='invalid')


# ---------------------------------------------------------------------------
# has_smtbx_masks_loop helper
# ---------------------------------------------------------------------------

class TestHasSmtbxMasksLoop(unittest.TestCase):

    def test_detects_smtbx_loop(self):
        from finalcif.gui.squeeze_dialog import has_smtbx_masks_loop
        cif = CifContainer(SMTBX_FILE)
        self.assertTrue(has_smtbx_masks_loop(cif))

    def test_squeeze_cif_has_no_smtbx_loop(self):
        from finalcif.gui.squeeze_dialog import has_smtbx_masks_loop
        cif = CifContainer(SQF_FILE)
        self.assertFalse(has_smtbx_masks_loop(cif))


if __name__ == '__main__':
    unittest.main()
