import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from qtpy.QtCore import Qt, QTimer
from qtpy.QtTest import QTest
from qtpy.QtWidgets import QApplication, QLineEdit

from tests.helpers import AppWindowTestCase
from finalcif.appwindow import AppWindow
from finalcif.tools.settings import FinalCifSettings


class RenameSettingsTestCase(unittest.TestCase):
    """Unit tests for FinalCifSettings.rename_template() — no GUI needed."""

    def setUp(self) -> None:
        self._tmp = NamedTemporaryFile(suffix='.json', delete=False)
        self._tmp.close()
        self._path = Path(self._tmp.name)
        self.settings = FinalCifSettings(settings_path=self._path)

    def tearDown(self) -> None:
        self._path.unlink(missing_ok=True)
        self._path.with_suffix('.tmp').unlink(missing_ok=True)

    def test_rename_equipment(self):
        self.settings.save_settings_list('equipment', 'Old Name', [['_key', 'value']])
        self.settings.rename_template('equipment', 'Old Name', 'New Name')
        self.assertIn('New Name', self.settings.get_equipment_list())
        self.assertNotIn('Old Name', self.settings.get_equipment_list())
        data = self.settings.load_settings_list('equipment', 'New Name')
        self.assertEqual([['_key', 'value']], data)

    def test_rename_equipment_preserves_data(self):
        items = [['_diffrn_radiation_wavelength', '0.71073'], ['_diffrn_source', 'synchrotron']]
        self.settings.save_settings_list('equipment', 'Synchrotron', items)
        self.settings.rename_template('equipment', 'Synchrotron', 'Synchrotron Source')
        self.assertEqual(items, self.settings.load_settings_list('equipment', 'Synchrotron Source'))

    def test_rename_equipment_same_name_is_noop(self):
        self.settings.save_settings_list('equipment', 'MyEquip', [['_key', 'val']])
        self.settings.rename_template('equipment', 'MyEquip', 'MyEquip')
        self.assertIn('MyEquip', self.settings.get_equipment_list())

    def test_rename_equipment_empty_new_name_is_noop(self):
        self.settings.save_settings_list('equipment', 'MyEquip', [['_key', 'val']])
        self.settings.rename_template('equipment', 'MyEquip', '')
        self.assertIn('MyEquip', self.settings.get_equipment_list())

    def test_rename_equipment_does_not_add_to_deleted(self):
        self.settings.save_settings_list('equipment', 'Old Name', [['_key', 'val']])
        self.settings.rename_template('equipment', 'Old Name', 'New Name')
        self.assertNotIn('Old Name', self.settings.deleted_equipment)
        self.assertNotIn('New Name', self.settings.deleted_equipment)

    def test_rename_equipment_removes_from_deleted_if_present(self):
        self.settings.save_settings_list('equipment', 'Old Name', [['_key', 'val']])
        # Manually add old_name to deleted list to simulate the edge case
        self.settings.save_key_value(name='deleted_templates', item=['Old Name'])
        self.settings.rename_template('equipment', 'Old Name', 'New Name')
        self.assertNotIn('Old Name', self.settings.deleted_equipment)

    def test_rename_property(self):
        self.settings.save_settings_list('property', 'Crystal Shape', ['_exptl_crystal_description', ['block']])
        self.settings.rename_template('property', 'Crystal Shape', 'Crystal Form')
        self.assertIn('Crystal Form', self.settings.get_properties_list())
        self.assertNotIn('Crystal Shape', self.settings.get_properties_list())

    def test_rename_property_preserves_data(self):
        items = ['_exptl_crystal_colour', ['red', 'blue']]
        self.settings.save_settings_list('property', 'Crystal Color', items)
        self.settings.rename_template('property', 'Crystal Color', 'Crystal Colour')
        self.assertEqual(items, self.settings.load_settings_list('property', 'Crystal Colour'))

    def test_rename_property_same_name_is_noop(self):
        self.settings.save_settings_list('property', 'MyProp', ['_key', ['val']])
        self.settings.rename_template('property', 'MyProp', 'MyProp')
        self.assertIn('MyProp', self.settings.get_properties_list())

    def test_rename_property_empty_new_name_is_noop(self):
        self.settings.save_settings_list('property', 'MyProp', ['_key', ['val']])
        self.settings.rename_template('property', 'MyProp', '')
        self.assertIn('MyProp', self.settings.get_properties_list())

    def test_rename_author(self):
        author_data = {'name': 'John Doe', 'email': 'john@example.com'}
        self.settings.save_settings_dict('authors_list', 'John Doe', author_data)
        self.settings.rename_template('authors_list', 'John Doe', 'John D.')
        self.assertIn('John D.', self.settings.list_saved_items('authors_list'))
        self.assertNotIn('John Doe', self.settings.list_saved_items('authors_list'))
        self.assertEqual(author_data, self.settings.load_settings_dict('authors_list', 'John D.'))

    def test_rename_author_same_name_is_noop(self):
        author_data = {'name': 'Jane'}
        self.settings.save_settings_dict('authors_list', 'Jane', author_data)
        self.settings.rename_template('authors_list', 'Jane', 'Jane')
        self.assertIn('Jane', self.settings.list_saved_items('authors_list'))

    def test_rename_nonexistent_old_name_is_noop(self):
        self.settings.rename_template('equipment', 'Does Not Exist', 'New Name')
        self.assertNotIn('New Name', self.settings.get_equipment_list())

    def test_rename_equipment_duplicate_name_is_noop(self):
        self.settings.save_settings_list('equipment', 'Alpha', [['_key', 'val']])
        self.settings.save_settings_list('equipment', 'Beta', [['_key2', 'val2']])
        # Attempting to rename 'Alpha' to 'Beta' (which already exists) must be a no-op
        self.settings.rename_template('equipment', 'Alpha', 'Beta')
        self.assertIn('Alpha', self.settings.get_equipment_list())
        self.assertIn('Beta', self.settings.get_equipment_list())
        # Data under 'Beta' must be unchanged
        self.assertEqual([['_key2', 'val2']], self.settings.load_settings_list('equipment', 'Beta'))

    def test_rename_property_duplicate_name_is_noop(self):
        self.settings.save_settings_list('property', 'Prop A', ['_key_a', ['x']])
        self.settings.save_settings_list('property', 'Prop B', ['_key_b', ['y']])
        self.settings.rename_template('property', 'Prop A', 'Prop B')
        self.assertIn('Prop A', self.settings.get_properties_list())
        self.assertIn('Prop B', self.settings.get_properties_list())
        self.assertEqual(['_key_b', ['y']], self.settings.load_settings_list('property', 'Prop B'))

    def test_rename_author_duplicate_name_is_noop(self):
        self.settings.save_settings_dict('authors_list', 'Author X', {'name': 'x'})
        self.settings.save_settings_dict('authors_list', 'Author Y', {'name': 'y'})
        self.settings.rename_template('authors_list', 'Author X', 'Author Y')
        self.assertIn('Author X', self.settings.list_saved_items('authors_list'))
        self.assertIn('Author Y', self.settings.list_saved_items('authors_list'))
        self.assertEqual({'name': 'y'}, self.settings.load_settings_dict('authors_list', 'Author Y'))


class EquipmentRenameGUITestCase(AppWindowTestCase):
    """Integration tests for renaming equipment templates via the GUI helpers."""

    def setUp(self) -> None:
        self.app = AppWindow(Path('test-data/1000006.cif'))
        self.app.equipment.import_equipment_from_file('test-data/Crystallographer_Details.cif')
        # Clean up any leftover renamed entry from a previous test run
        self.app.equipment.settings.delete_template('equipment', 'Crystallographer Details Renamed')
        self.app.hide()

    def tearDown(self) -> None:
        # Clean up renamed entry so it does not bleed into subsequent test runs
        self.app.equipment.settings.delete_template('equipment', 'Crystallographer Details Renamed')
        self.app.close()
        super().tearDown()

    def test_rename_equipment_via_handler(self):
        """Simulate a rename by calling on_equipment_item_renamed directly."""
        listw = self.app.ui.EquipmentTemplatesListWidget
        items = listw.findItems('Crystallographer Details', Qt.MatchFlag.MatchExactly)
        self.assertTrue(items, 'Template not found in list')
        item = items[0]

        # Simulate what the context menu does: set old name, make editable
        self.app.equipment._rename_old_name = 'Crystallographer Details'
        item.setText('Crystallographer Details Renamed')
        # itemChanged fires automatically above; but call handler explicitly too for safety
        # (in tests itemChanged may not fire depending on event loop)
        self.app.equipment.on_equipment_item_renamed(item)

        equip_list = self.app.equipment.settings.get_equipment_list()
        self.assertIn('Crystallographer Details Renamed', equip_list)
        self.assertNotIn('Crystallographer Details', equip_list)

    def test_rename_equipment_noop_if_no_old_name(self):
        """Handler must do nothing when _rename_old_name is empty."""
        listw = self.app.ui.EquipmentTemplatesListWidget
        items = listw.findItems('Crystallographer Details', Qt.MatchFlag.MatchExactly)
        self.assertTrue(items)
        item = items[0]

        # _rename_old_name is '' by default — no rename should occur
        self.app.equipment._rename_old_name = ''
        self.app.equipment.on_equipment_item_renamed(item)
        equip_list = self.app.equipment.settings.get_equipment_list()
        self.assertIn('Crystallographer Details', equip_list)

    def test_rename_equipment_to_existing_name_is_rejected(self):
        """Renaming to an already-existing template name must leave both templates intact."""
        equip_list_before = self.app.equipment.settings.get_equipment_list()
        # Pick the first two templates in the list for the conflict test
        self.assertGreaterEqual(len(equip_list_before), 2, 'Need at least two templates')
        existing_name = equip_list_before[0]
        other_name = equip_list_before[1]

        listw = self.app.ui.EquipmentTemplatesListWidget
        items = listw.findItems(other_name, Qt.MatchFlag.MatchExactly)
        self.assertTrue(items)
        item = items[0]

        self.app.equipment._rename_old_name = other_name
        item.setText(existing_name)
        self.app.equipment.on_equipment_item_renamed(item)

        equip_list = self.app.equipment.settings.get_equipment_list()
        self.assertIn(other_name, equip_list)
        self.assertIn(existing_name, equip_list)

    def test_rename_equipment_via_context_menu_mouse_click(self):
        """Context-menu → Rename → QTest mouse click + keyboard input renames the template.

        This test exercises the QTimer.singleShot fix end-to-end:
        - customContextMenuRequested is emitted (what a right-click produces)
        - show_equipment_rename_menu schedules editItem() via QTimer.singleShot(0, ...)
        - processEvents() fires the timer so the inline editor opens
        - QTest.mouseClick on the editor is the 'actual mouse click'
        - QTest.keyClicks + Key_Return complete the rename
        """
        listw = self.app.ui.EquipmentTemplatesListWidget
        items = listw.findItems('Crystallographer Details', Qt.MatchFlag.MatchExactly)
        self.assertTrue(items, 'Template not found in list')
        item = items[0]
        listw.setCurrentItem(item)

        # Schedule: once menu.exec() opens its nested event loop, trigger "Rename"
        # so the loop exits.  We use a list to communicate between the callbacks.
        triggered = [False]

        def click_rename_in_menu():
            if triggered[0]:
                return
            popup = QApplication.activePopupWidget()
            if popup is not None:
                for action in popup.actions():
                    if action.text() == 'Rename':
                        triggered[0] = True
                        action.trigger()
                        return
            # Menu not visible yet — retry on the next event-loop tick
            QTimer.singleShot(20, click_rename_in_menu)

        QTimer.singleShot(20, click_rename_in_menu)

        # Emitting customContextMenuRequested is exactly what a right-click produces.
        # The connected handler (show_equipment_rename_menu) calls menu.exec() which
        # blocks in a nested event loop until click_rename_in_menu() triggers the action.
        rect = listw.visualItemRect(item)
        listw.customContextMenuRequested.emit(rect.center())

        # Run one event-loop pass so the deferred QTimer.singleShot(0, editItem) fires
        # and creates the inline editor.
        QApplication.instance().processEvents()

        self.assertTrue(triggered[0], 'Rename menu action was not triggered')

        # The inline QLineEdit created by Qt for the item editor must now exist.
        editor = listw.viewport().findChild(QLineEdit)
        self.assertIsNotNone(editor, 'Inline editor did not open after deferred editItem()')

        # Actual mouse click to focus the editor, then type the new name and confirm.
        QTest.mouseClick(editor, Qt.MouseButton.LeftButton)
        QTest.keyClick(editor, Qt.Key.Key_A, Qt.KeyboardModifier.ControlModifier)
        QTest.keyClicks(editor, 'Crystallographer Details Renamed')
        QTest.keyClick(editor, Qt.Key.Key_Return)
        QApplication.instance().processEvents()

        equip_list = self.app.equipment.settings.get_equipment_list()
        self.assertIn('Crystallographer Details Renamed', equip_list)
        self.assertNotIn('Crystallographer Details', equip_list)


class PropertiesRenameGUITestCase(AppWindowTestCase):
    """Integration tests for renaming property templates via the GUI helpers."""

    def setUp(self) -> None:
        self.app = AppWindow(Path('test-data/1000006.cif'))
        # Remove any leftover renamed entry from a previous test run
        self.app.properties.settings.delete_template('property', 'Crystal Colour')
        self.app.hide()

    def tearDown(self) -> None:
        # Remove renamed entry to avoid bleeding into subsequent test runs
        self.app.properties.settings.delete_template('property', 'Crystal Colour')
        self.app.close()
        super().tearDown()

    def test_rename_property_via_handler(self):
        listw = self.app.ui.PropertiesTemplatesListWidget
        items = listw.findItems('Crystal Color', Qt.MatchFlag.MatchStartsWith)
        self.assertTrue(items, 'Crystal Color template not found')
        item = items[0]
        original_name = item.text()

        self.app.properties._rename_old_name = original_name
        item.setText('Crystal Colour')
        self.app.properties.on_properties_item_renamed(item)

        prop_list = self.app.properties.settings.get_properties_list()
        self.assertIn('Crystal Colour', prop_list)
        self.assertNotIn(original_name, prop_list)

    def test_rename_property_noop_if_no_old_name(self):
        listw = self.app.ui.PropertiesTemplatesListWidget
        items = listw.findItems('Crystal Color', Qt.MatchFlag.MatchStartsWith)
        self.assertTrue(items)
        item = items[0]
        original_name = item.text()

        self.app.properties._rename_old_name = ''
        self.app.properties.on_properties_item_renamed(item)
        self.assertIn(original_name, self.app.properties.settings.get_properties_list())

    def test_rename_property_to_existing_name_is_rejected(self):
        """Renaming to an already-existing property template name must leave both intact."""
        prop_list = self.app.properties.settings.get_properties_list()
        self.assertGreaterEqual(len(prop_list), 2, 'Need at least two property templates')
        existing_name = prop_list[0]
        other_name = prop_list[1]

        listw = self.app.ui.PropertiesTemplatesListWidget
        items = listw.findItems(other_name, Qt.MatchFlag.MatchExactly)
        self.assertTrue(items)
        item = items[0]

        self.app.properties._rename_old_name = other_name
        item.setText(existing_name)
        self.app.properties.on_properties_item_renamed(item)

        result = self.app.properties.settings.get_properties_list()
        self.assertIn(other_name, result)
        self.assertIn(existing_name, result)


class AuthorRenameGUITestCase(AppWindowTestCase):
    """Integration tests for renaming author loop templates via the GUI helpers."""

    def setUp(self) -> None:
        self.testcif = Path('tests/examples/1979688.cif')
        self.testimport_author = Path('tests/other_templates/AATest_Author.cif')
        self.app = AppWindow(self.testcif)
        self.app.authors.import_author(str(self.testimport_author))
        self.app.hide()

    def tearDown(self) -> None:
        # Clean up both possible names
        for name in ('AATest Author', 'AATest Author Renamed'):
            self.app.authors.settings.delete_template('authors_list', name)
        self.app.close()
        super().tearDown()

    def _find_author_item(self, name: str):
        listw = self.app.ui.LoopTemplatesListWidget
        items = listw.findItems(name, Qt.MatchFlag.MatchStartsWith)
        return items[0] if items else None

    def test_rename_author_via_handler(self):
        item = self._find_author_item('AATest Author')
        self.assertIsNotNone(item, 'AATest Author not found in list')

        self.app.authors._rename_old_name = 'AATest Author'
        item.setText('AATest Author Renamed')
        self.app.authors.on_author_item_renamed(item)

        author_list = self.app.authors.settings.list_saved_items('authors_list')
        self.assertIn('AATest Author Renamed', author_list)
        self.assertNotIn('AATest Author', author_list)

    def test_rename_author_noop_if_no_old_name(self):
        item = self._find_author_item('AATest Author')
        self.assertIsNotNone(item)
        self.app.authors._rename_old_name = ''
        self.app.authors.on_author_item_renamed(item)
        self.assertIn('AATest Author', self.app.authors.settings.list_saved_items('authors_list'))

    def test_rename_author_to_existing_name_is_rejected(self):
        """Renaming to an already-existing author template name must leave both intact."""
        # Create a second author entry directly in settings so we have two names to conflict
        second_name = 'AATest Conflict Author'
        self.app.authors.settings.save_settings_dict(
            'authors_list', second_name,
            {'name': second_name, 'address': '', 'email': '', 'phone': '',
             'orcid': '', 'footnote': '', 'contact_author': False,
             'author_type': 'publ', 'iucr_id': ''}
        )
        self.app.authors.show_authors_list()

        item = self._find_author_item('AATest Author')
        self.assertIsNotNone(item, 'AATest Author not found')

        self.app.authors._rename_old_name = 'AATest Author'
        item.setText(second_name)
        self.app.authors.on_author_item_renamed(item)

        author_list = self.app.authors.settings.list_saved_items('authors_list')
        self.assertIn('AATest Author', author_list)
        self.assertIn(second_name, author_list)
        # Clean up the extra entry
        self.app.authors.settings.delete_template('authors_list', second_name)


if __name__ == '__main__':
    unittest.main()
