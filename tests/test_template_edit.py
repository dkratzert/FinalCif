import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtTest import QTest

from finalcif.appwindow import AppWindow


class EquipmentTestCase(AppWindowTestCase):
    def setUp(self) -> None:
        self.myapp = AppWindow(Path('test-data/1000006.cif'))
        self.myapp.equipment.import_equipment_from_file('test-data/Crystallographer_Details.cif')
        self.myapp.hide()

    def tearDown(self) -> None:
        self.myapp.close()
        super().tearDown()

    def equipment_edit_click(self, field: str):
        listw = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = listw.findItems(field, Qt.MatchFlag.MatchStartsWith)[0]
        listw.setCurrentItem(item)
        self.assertEqual(field, item.text())
        rect = listw.visualItemRect(item)
        QTest.mouseClick(listw.viewport(), Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, rect.center())
        # This is necessary:
        self.myapp.equipment.edit_equipment_template()

    def test_template_edit_click(self):
        """
        The user makes a single click on the 'Crystallographer Details' template and clicks on "edit template".
        -> The result should be a table with keys and values:
        """
        self.equipment_edit_click('Crystallographer Details')
        self.assertEqual('_audit_contact_author_name', self.myapp.ui.EquipmentEditTableWidget.text(row=0, column=0))
        self.assertEqual('Dr. Daniel Kratzert', self.myapp.ui.EquipmentEditTableWidget.text(row=0, column=1))
        self.assertEqual('_audit_contact_author_email', self.myapp.ui.EquipmentEditTableWidget.text(row=1, column=0))
        self.assertEqual('dkratzert@gmx.de', self.myapp.ui.EquipmentEditTableWidget.text(row=1, column=1))
        # and so on...


class PropertiesTestCase(AppWindowTestCase):
    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.myapp = AppWindow(file=Path('test-data/1000006.cif'))
        self.myapp.hide()

    def property_edit_click(self, field: str):
        listw = self.myapp.ui.PropertiesTemplatesListWidget
        self.myapp.ui.PropertiesTemplatesListWidget.setCurrentRow(0)
        item = listw.findItems(field, Qt.MatchFlag.MatchStartsWith)[0]
        listw.setCurrentItem(item)
        self.assertEqual(field, item.text())
        rect = listw.visualItemRect(item)
        QTest.mouseClick(listw.viewport(), Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, rect.center())
        # self.myapp.properties.edit_property_template()
        self.myapp.ui.EditPropertyTemplateButton.click()

    def test_property_crystal_color(self):
        # The user clicks on the Crystal Color list item in the properties list
        self.property_edit_click('Crystal Color')
        # First we delete the contents to be sure that there is nothing saved different to the default:
        self.myapp.ui.DeletePropertiesButton.click()
        self.property_edit_click('Crystal Color')
        # This loads the contents of the saved values to the PropertiesEditTableWidget
        table = self.myapp.ui.PropertiesEditTableWidget
        colors = ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue', 'green', 'gray', 'pink',
                  'orange', 'violet', 'brown', '']
        totest = [table.cellWidget(row, 0).toPlainText() for row in range(table.rowCount())]
        self.assertListEqual(colors, totest)
        # Also cifKeywordLineEdit is filled with the respective cif key:
        self.assertEqual('_exptl_crystal_colour', self.myapp.ui.cifKeywordLineEdit.text())

        if __name__ == '__main__':
            unittest.main()
