import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from finalcif.appwindow import AppWindow


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppWindow(unit_test=True)
        self.app.running_inside_unit_test = True
        self.app.equipment.import_equipment_from_file('test-data/Crystallographer_Details.cif')
        self.app.hide()

    def equipment_edit_click(self, field: str):
        listw = self.app.ui.EquipmentTemplatesListWidget
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = listw.findItems(field, Qt.MatchStartsWith)[0]
        listw.setCurrentItem(item)
        self.assertEqual(field, item.text())
        rect = listw.visualItemRect(item)
        QTest.mouseClick(listw.viewport(), Qt.LeftButton, Qt.NoModifier, rect.center())
        # This is necessary:
        self.app.equipment.edit_equipment_template()

    def test_template_edit_click(self):
        """
        The user makes a single click on the 'Crystallographer Details' template and clicks on "edit template".
        -> The result should be a table with keys and values:
        """
        self.equipment_edit_click('Crystallographer Details')
        self.assertEqual('_audit_contact_author_name', self.app.ui.EquipmentEditTableWidget.text(row=0, column=0))
        self.assertEqual('Dr. Daniel Kratzert', self.app.ui.EquipmentEditTableWidget.text(row=0, column=1))
        self.assertEqual('_audit_contact_author_email', self.app.ui.EquipmentEditTableWidget.text(row=1, column=0))
        self.assertEqual('dkratzert@gmx.de', self.app.ui.EquipmentEditTableWidget.text(row=1, column=1))
        # and so on...


if __name__ == '__main__':
    unittest.main()
