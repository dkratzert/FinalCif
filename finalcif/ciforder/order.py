from __future__ import annotations
import enum
import sys
from pathlib import Path
from typing import List, TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore

from finalcif.cif import cif_order
from finalcif.cif.cif_file_io import CifContainer
from finalcif.ciforder.order_ui import Ui_CifOrderForm
from finalcif.gui import dialogs
from finalcif.gui.custom_classes import CifOrderItem
from finalcif.gui.new_key_dialog import NewKey

if TYPE_CHECKING:
    from finalcif.tools.settings import FinalCifSettings


class Column(enum.IntEnum):
    key = 0


class CifOrder(QtWidgets.QGroupBox):
    def __init__(self, parent, cif_file: Path = None, settings: FinalCifSettings = None):
        super().__init__(parent)
        self.ui = Ui_CifOrderForm()
        self.ui.setupUi(self)
        self.cif = None
        self.settings = settings
        if cif_file is not None:
            self.set_keys_from_cif(cif_file)
        elif settings is not None:
            order = self.settings.load_settings_list('cif_order', 'order')
            essentials = self.settings.load_settings_list('cif_order', 'essentials')
            if order:
                self.essential_keys = essentials
                self.set_keys(order)
            else:
                self.essential_keys = cif_order.essential_keys
                self.set_keys(cif_order.order)
        self.connect_signals_and_slots()

    def connect_signals_and_slots(self):
        self.ui.importCifPushButton.clicked.connect(self.import_cif)
        self.ui.moveUpPushButton.clicked.connect(self.move_row_up)
        self.ui.moveDownPushButton.clicked.connect(self.move_row_down)
        self.ui.restoreDefaultPushButton.clicked.connect(self.restore_default)
        self.ui.addKeyPushButton.clicked.connect(self.open_add_cif_key)
        self.ui.saveSettingPushButton.clicked.connect(self.save_setting)
        self.ui.deleteKeyPushButton.clicked.connect(self.delete_keys)

    def move_row_up(self):
        current_row = self.ui.cifOrderTableWidget.currentRow()
        if current_row > 0:
            self.swap_rows(current_row, current_row - 1)
            self.ui.cifOrderTableWidget.setCurrentCell(current_row - 1, Column.key)

    def move_row_down(self):
        table = self.ui.cifOrderTableWidget
        current_row = table.currentRow()
        if current_row < table.rowCount() - 1:
            self.swap_rows(current_row, current_row + 1)
            table.setCurrentCell(current_row + 1, Column.key)

    def swap_rows(self, row1, row2):
        table = self.ui.cifOrderTableWidget
        item1 = table.item(row1, Column.key)
        item2 = table.item(row2, Column.key)
        if item1 and item2:
            text1 = item1.text()
            text2 = item2.text()
            check_state1 = item1.checkState()
            check_state2 = item2.checkState()
            item1.setText(text2)
            item1.setCheckState(check_state2)
            item2.setText(text1)
            item2.setCheckState(check_state1)

    @property
    def order_keys(self):
        keys = []
        for row in range(self.ui.cifOrderTableWidget.rowCount()):
            key = self.ui.cifOrderTableWidget.item(row, Column.key).text()
            keys.append(key)
        return keys

    @property
    def order_essentials(self):
        essentials = []
        for row in range(self.ui.cifOrderTableWidget.rowCount()):
            item = self.ui.cifOrderTableWidget.item(row, Column.key)
            essential = item.checkState()
            if essential:
                essentials.append(item.text())
        return essentials

    def set_keys_from_cif(self, cif_file):
        self.cif = CifContainer(cif_file)
        self.set_keys(self.cif.keys())

    def set_keys(self, order_keys: List[str] = None):
        self.ui.cifOrderTableWidget.setRowCount(0)
        row = 0
        for key_text in order_keys:
            if not key_text:
                continue
            self.ui.cifOrderTableWidget.insertRow(row)
            self.set_row_text(key_text, row)
            row += 1
        #self.ui.cifOrderTableWidget.resizeColumnsToContents()

    def set_row_text(self, key_text: str, row: int) -> None:
        item1 = CifOrderItem(key_text)
        item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item1.setText(key_text)
        if key_text in self.essential_keys:
            item1.setEssential(True)
        else:
            item1.setEssential(False)
        self.ui.cifOrderTableWidget.setItem(row, Column.key, item1)

    def set_keys_from_settings(self, keys: List[str]):
        self.set_keys(keys)

    def import_cif(self):
        cif_file = dialogs.cif_file_open_dialog()
        if self._file_is_there(cif_file):
            self.set_keys_from_cif(cif_file)

    def _file_is_there(self, cif_file: str) -> bool:
        return cif_file is not None and Path(cif_file).is_file() and Path(cif_file).exists()

    def restore_default(self):
        self.essential_keys = cif_order.essential_keys
        self.settings.save_settings_list('cif_order', 'order', [])
        self.settings.save_settings_list('cif_order', 'essentials', [])
        self.set_keys(cif_order.order)

    def open_add_cif_key(self):
        new_key = NewKey(self)
        new_key.show()
        new_key.new_key_added.connect(self.add_key)

    def add_key(self, key: str) -> None:
        if key not in self.order_keys:
            self.ui.cifOrderTableWidget.insertRow(0)
            self.set_row_text(key, 0)

    def save_setting(self):
        self.settings.save_settings_list('cif_order', 'order', self.order_keys)
        self.settings.save_settings_list('cif_order', 'essentials', self.order_essentials)

    def delete_keys(self):
        items = self.ui.cifOrderTableWidget.selectedItems()
        for item in items:
            self.ui.cifOrderTableWidget.removeRow(item.row())


if __name__ == "__main__":
    from finalcif.tools.settings import FinalCifSettings
    app = QtWidgets.QApplication(sys.argv)
    # form = CifOrder(parent=None, cif_file=Path('test-data/1000007.cif').resolve())
    settings = FinalCifSettings()
    form = CifOrder(parent=None, settings=settings)
    form.show()
    form.raise_()
    sys.exit(app.exec_())
