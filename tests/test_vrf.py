"""Tests for VRF (Validation Response Form) handling.

Covers VRFEntry dataclass, MyVRFContainer widget, inline VRF placement in the
main CIF table, span clearing on reload, and the integrated save flow.
"""
import os
import shutil
import unittest
from pathlib import Path

os.environ['RUNNING_TEST'] = 'True'

from qtpy.QtWidgets import QApplication

from finalcif.cif.vrf_entry import VRFEntry

data = Path('tests')

# ---------------------------------------------------------------------------
# Pure-data tests (no Qt GUI required beyond QApplication init)
# ---------------------------------------------------------------------------


class TestVRFEntryDataclass(unittest.TestCase):
    """Tests for the VRFEntry dataclass methods and properties."""

    def test_default_source_is_checkcif(self):
        entry = VRFEntry(
            key='_vrf_PLAT035_foo',
            data_name='foo',
            problem='missing value',
            response='ok',
            alert_num='PLAT035',
        )
        self.assertEqual('checkcif', entry.source)

    def test_value_property_format(self):
        entry = VRFEntry(
            key='_vrf_PLAT035_foo',
            data_name='foo',
            problem='something bad',
            response='we fixed it',
            alert_num='PLAT035',
        )
        expected = 'PROBLEM: something bad\nRESPONSE: we fixed it\n'
        self.assertEqual(expected, entry.value)

    def test_value_property_empty_response(self):
        entry = VRFEntry(
            key='_vrf_PLAT035_foo', data_name='foo',
            problem='x', response='', alert_num='PLAT035',
        )
        self.assertIn('RESPONSE: \n', entry.value)

    def test_from_html_form_creates_entry(self):
        form = {
            'name': '_vrf_PLAT413_bar',
            'data_name': 'bar',
            'problem': 'short contacts',
            'alert_num': 'PLAT413',
            'level': 'PLAT413_ALERT_2_C',
        }
        entry = VRFEntry.from_html_form(form)
        self.assertEqual('_vrf_PLAT413_bar', entry.key)
        self.assertEqual('?', entry.response)
        self.assertEqual('PLAT413', entry.alert_num)
        self.assertEqual('PLAT413_ALERT_2_C', entry.level)
        self.assertEqual('checkcif', entry.source)

    def test_from_html_form_missing_level(self):
        form = {
            'name': '_vrf_PLAT413_bar',
            'data_name': 'bar',
            'problem': 'x',
            'alert_num': 'PLAT413',
        }
        entry = VRFEntry.from_html_form(form)
        self.assertEqual('', entry.level)

    def test_from_cif_pair_round_trip(self):
        """Create a CIF value, parse it back, verify fields match."""
        import gemmi
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: bad angle\nRESPONSE: angle is fine\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT307_mydata', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT307_mydata')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT307_mydata', raw_value)
        self.assertEqual('_vrf_PLAT307_mydata', entry.key)
        self.assertEqual('mydata', entry.data_name)
        self.assertEqual('PLAT307', entry.alert_num)
        self.assertEqual('bad angle', entry.problem)
        self.assertEqual('angle is fine', entry.response)
        self.assertEqual('cif', entry.source)

    def test_from_cif_pair_multiline_response(self):
        import gemmi
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: short contacts\nRESPONSE: line one\nline two\nline three\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT413_z', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT413_z')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT413_z', raw_value)
        self.assertEqual('line one\nline two\nline three', entry.response)

    def test_from_cif_pair_empty_response(self):
        import gemmi
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: test\nRESPONSE:\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT000_d', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT000_d')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT000_d', raw_value)
        self.assertEqual('', entry.response)

    def test_from_cif_pair_data_name_with_underscores(self):
        import gemmi
        from finalcif.cif.text import quote
        raw_text = 'PROBLEM: x\nRESPONSE: y\n'
        doc = gemmi.cif.Document()
        block = doc.add_new_block('test')
        block.set_pair('_vrf_PLAT307_foo_bar_baz', quote(raw_text))
        raw_value = block.find_value('_vrf_PLAT307_foo_bar_baz')
        entry = VRFEntry.from_cif_pair('_vrf_PLAT307_foo_bar_baz', raw_value)
        self.assertEqual('foo_bar_baz', entry.data_name)


# ---------------------------------------------------------------------------
# Widget-level tests
# ---------------------------------------------------------------------------


class TestMyVRFContainerWidget(unittest.TestCase):
    """Tests for the MyVRFContainer QWidget."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure a QApplication exists for widget tests."""
        cls._app = QApplication.instance() or QApplication([])

    def _make_widget(self, source='checkcif', response='', level='PLAT035_ALERT_1_A'):
        from finalcif.gui.vrf_classes import MyVRFContainer
        entry = VRFEntry(
            key='_vrf_PLAT035_foo',
            data_name='foo',
            problem='something wrong',
            response=response,
            alert_num='PLAT035',
            level=level,
            source=source,
        )
        return MyVRFContainer(entry, help='help text', parent=None)

    def test_source_badge_checkcif(self):
        w = self._make_widget(source='checkcif')
        self.assertEqual('From CheckCIF', w.source_label.text())

    def test_source_badge_cif(self):
        w = self._make_widget(source='cif')
        self.assertEqual('Saved in CIF', w.source_label.text())

    def test_update_source_changes_badge(self):
        w = self._make_widget(source='cif')
        self.assertEqual('Saved in CIF', w.source_label.text())
        w.update_source('checkcif')
        self.assertEqual('From CheckCIF', w.source_label.text())
        self.assertEqual('checkcif', w.vrf_entry.source)

    def test_response_text_prefilled(self):
        w = self._make_widget(response='my response')
        self.assertEqual('my response', w.response_text_edit.toPlainText())

    def test_response_text_empty(self):
        w = self._make_widget(response='')
        self.assertEqual('', w.response_text_edit.toPlainText())

    def test_delete_signal_emitted(self):
        w = self._make_widget()
        received = []
        w.deleted.connect(lambda obj: received.append(obj))
        w.deletebutton.click()
        self.assertEqual(1, len(received))
        self.assertIs(w, received[0])

    def test_alert_label_A(self):
        w = self._make_widget(level='PLAT035_ALERT_1_A')
        # The alert label includes the type and number
        # Just verify the widget was created without error
        self.assertIsNotNone(w)

    def test_alert_label_B(self):
        w = self._make_widget(level='PLAT035_ALERT_1_B')
        self.assertIsNotNone(w)

    def test_alert_label_C(self):
        w = self._make_widget(level='PLAT413_ALERT_2_C')
        self.assertIsNotNone(w)

    def test_alert_label_G(self):
        w = self._make_widget(level='PLAT413_ALERT_2_G')
        self.assertIsNotNone(w)

    def test_selected_row_background_not_darker_than_lightgray(self):
        """VRF widget must declare a light background via its stylesheet so that
        the dark-blue Qt selection highlight is suppressed.  The background-color
        must be no darker than lightgray (lightness >= 211/255)."""
        from qtpy.QtGui import QColor
        import re
        w = self._make_widget()
        ss = w.styleSheet()
        self.assertIn('background-color', ss,
                      'stylesheet must set a background-color to suppress the selection highlight')
        match = re.search(r'background-color\s*:\s*([^;}\s]+)', ss)
        self.assertIsNotNone(match, 'Could not parse background-color from stylesheet')
        bg_color = QColor(match.group(1).strip())
        self.assertTrue(bg_color.isValid(), f'background-color value "{match.group(1)}" is not a valid QColor')
        lightgray_lightness = QColor('lightgray').lightness()
        self.assertGreaterEqual(
            bg_color.lightness(), lightgray_lightness,
            f'VRF widget background ({bg_color.name()}, lightness={bg_color.lightness()}) '
            f'is darker than lightgray (lightness={lightgray_lightness})',
        )


# ---------------------------------------------------------------------------
# Integration tests with AppWindow
# ---------------------------------------------------------------------------
from tests.helpers import AppWindowTestCase, processevents

unittest.addModuleCleanup(processevents)


class TestVRFInlineInTable(AppWindowTestCase):
    """Verify VRF widgets are placed inline in the main CIF table."""

    def setUp(self) -> None:
        os.environ['RUNNING_TEST'] = 'True'
        self.testcif = (data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        from finalcif.appwindow import AppWindow
        self.app = AppWindow(file=self.testcif)

    def tearDown(self) -> None:
        finalcif_file = self.testcif.parent / 'cu_BruecknerJK_153F40_0m-finalcif.cif'
        finalcif_file.unlink(missing_ok=True)
        super().tearDown()

    def test_vrf_row_exists_in_table(self):
        """The main table should have a row keyed _vrf_PLAT307_BruecknerJK_153F40_0m."""
        table = self.app.ui.cif_main_table
        self.assertTrue(table.has_key('_vrf_PLAT307_BruecknerJK_153F40_0m'))

    def test_vrf_widget_is_placed(self):
        """The VRF row should have a MyVRFContainer widget placed on it."""
        from finalcif.gui.vrf_classes import MyVRFContainer
        table = self.app.ui.cif_main_table
        widget = table.get_vrf_widget('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertIsNotNone(widget)
        self.assertIsInstance(widget, MyVRFContainer)

    def test_vrf_widget_response_prefilled(self):
        """The VRF widget should have the CIF response pre-filled."""
        table = self.app.ui.cif_main_table
        widget = table.get_vrf_widget('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertEqual('foobar', widget.response_text_edit.toPlainText())

    def test_vrf_widget_source_is_cif(self):
        """VRF loaded from CIF should have source='cif' badge."""
        table = self.app.ui.cif_main_table
        widget = table.get_vrf_widget('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertEqual('Saved in CIF', widget.source_label.text())

    def test_vrf_row_is_spanned(self):
        """The VRF row should span all 3 columns."""
        table = self.app.ui.cif_main_table
        row = table.row_from_key('_vrf_PLAT307_BruecknerJK_153F40_0m')
        span = table.columnSpan(row, 0)
        self.assertEqual(3, span)

    def test_non_vrf_row_not_spanned(self):
        """A regular CIF row should not be spanned."""
        table = self.app.ui.cif_main_table
        row = table.row_from_key('_audit_creation_method')
        span = table.columnSpan(row, 0)
        self.assertEqual(1, span)

    def test_validation_forms_list_populated(self):
        """validation_response_forms_list should contain one entry for the CIF VRF."""
        self.assertEqual(1, len(self.app.validation_response_forms_list))

    def test_checkcif_alerts_tab_removed(self):
        """The 'checkcif alerts' tab (ResponsesTabWidgetPage2) should be removed."""
        tab_widget = self.app.ui.ResponsesTabWidget
        for i in range(tab_widget.count()):
            self.assertNotEqual(tab_widget.widget(i), self.app.ui.ResponsesTabWidgetPage2)


class TestSpanClearedOnReload(AppWindowTestCase):
    """Ensure column spans are cleared when the CIF table is reloaded."""

    def setUp(self) -> None:
        os.environ['RUNNING_TEST'] = 'True'
        self.testcif = (data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        from finalcif.appwindow import AppWindow
        self.app = AppWindow(file=self.testcif)

    def tearDown(self) -> None:
        finalcif_file = self.testcif.parent / 'cu_BruecknerJK_153F40_0m-finalcif.cif'
        finalcif_file.unlink(missing_ok=True)
        super().tearDown()

    def test_span_cleared_after_delete_content(self):
        """After delete_content(), no row should retain a 3-column span."""
        table = self.app.ui.cif_main_table
        # Verify the VRF row is spanned initially
        vrf_row = table.row_from_key('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertEqual(3, table.columnSpan(vrf_row, 0))
        # Now clear the table
        table.delete_content()
        # After clearing, the model is empty — verify via rows_count
        self.assertEqual(0, table.rows_count)

    def test_reload_gives_correct_spans(self):
        """After a full reload, VRF rows should be spanned and regular rows should not."""
        table = self.app.ui.cif_main_table
        # Record the VRF row (before reload)
        self.assertTrue(table.has_key('_vrf_PLAT307_BruecknerJK_153F40_0m'))
        # Reload the block
        self.app._load_block(0, load_changes=False)
        # After reload, VRF row should still be spanned
        vrf_row = table.row_from_key('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertEqual(3, table.columnSpan(vrf_row, 0))
        # And a regular row should not be spanned
        reg_row = table.row_from_key('_audit_creation_method')
        self.assertEqual(1, table.columnSpan(reg_row, 0))


class TestVRFSaveIntegration(AppWindowTestCase):
    """VRF responses are saved when save_current_cif_file is called."""

    def setUp(self) -> None:
        os.environ['RUNNING_TEST'] = 'True'
        import tempfile
        # Copy test CIF to a temp location so we can modify it
        src = (data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.work_dir = Path(tempfile.mkdtemp(prefix='test_vrf_save_'))
        self.testcif = self.work_dir / src.name
        shutil.copy2(src, self.testcif)
        # Copy companion files
        for ext in ['.res', '.hkl', '.lst', '.abs']:
            companion = src.with_suffix(ext)
            if companion.exists():
                shutil.copy2(companion, self.work_dir / companion.name)
        from finalcif.appwindow import AppWindow
        self.app = AppWindow(file=self.testcif)

    def tearDown(self) -> None:
        super().tearDown()
        shutil.rmtree(self.work_dir, ignore_errors=True)

    def test_edited_vrf_is_saved(self):
        """Editing a VRF response in the table widget and saving should persist."""
        table = self.app.ui.cif_main_table
        widget = table.get_vrf_widget('_vrf_PLAT307_BruecknerJK_153F40_0m')
        self.assertIsNotNone(widget)
        widget.response_text_edit.setPlainText('new response text')
        self.app.save_current_cif_file()
        # Re-read the CIF to verify the response was written
        from finalcif.cif.cif_file_io import CifContainer
        finalcif_file = self.work_dir / 'cu_BruecknerJK_153F40_0m-finalcif.cif'
        self.assertTrue(finalcif_file.exists())
        cif = CifContainer(finalcif_file)
        entries = cif.get_vrf_entries()
        # The data_name may be renamed by the combobox (cu_ prefix), so just
        # look for a PLAT307 VRF entry with the expected response.
        plat307 = [e for e in entries if 'PLAT307' in e.key]
        self.assertEqual(1, len(plat307), f'Expected one PLAT307 VRF entry, got: {[e.key for e in entries]}')
        self.assertEqual('new response text', plat307[0].response)


if __name__ == '__main__':
    unittest.main()
