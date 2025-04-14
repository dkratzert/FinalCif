from __future__ import annotations

import enum
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import gemmi
from PySide6 import QtWidgets, QtCore

from finalcif.cif import cif_order
from finalcif.ciforder.order_ui import Ui_CifOrderForm
from finalcif.gui import dialogs
from finalcif.gui.custom_classes import CifOrderItem
from finalcif.gui.dialogs import cif_file_save_dialog, show_general_warning
from finalcif.gui.new_key_dialog import NewKey

if TYPE_CHECKING:
    from finalcif.tools.settings import FinalCifSettings


class Column(enum.IntEnum):
    key = 0


class CifOrder(QtWidgets.QGroupBox):
    def __init__(self, parent=None, cif_file: Path | None = None):
        super().__init__(parent)
        self.ui = Ui_CifOrderForm()
        self.ui.setupUi(self)
        self.cif = None
        self.settings = None
        self.essential_keys = cif_order.essential_keys
        self.set_keys(cif_order.order)
        if cif_file is not None:
            self.set_keys_from_cif(cif_file)
        self.connect_signals_and_slots()

    def set_order_from_settings(self, settings: FinalCifSettings = None):
        self.settings = settings
        if settings is not None:
            order = settings.load_settings_list('cif_order', 'order')
            essentials = settings.load_settings_list('cif_order', 'essentials')
            if order:
                self.essential_keys = essentials
                self.set_keys(order)

    def connect_signals_and_slots(self):
        self.ui.importCifPushButton.clicked.connect(self.import_cif)
        self.ui.restoreDefaultPushButton.clicked.connect(self.restore_default)
        self.ui.addKeyPushButton.clicked.connect(self.open_add_cif_key)
        self.ui.saveSettingPushButton.clicked.connect(self.save_setting)
        self.ui.deleteKeyPushButton.clicked.connect(self.delete_keys)
        self.ui.exportToCifPushButton.clicked.connect(self.export_cif)
        # Connect signals for moveUpPushButton
        self.ui.moveUpPushButton.pressed.connect(lambda: self.start_repeated_action(self.move_row_up))
        self.ui.moveUpPushButton.released.connect(self.stop_repeated_action)
        # Connect signals for moveDownPushButton
        self.ui.moveDownPushButton.pressed.connect(lambda: self.start_repeated_action(self.move_row_down))
        self.ui.moveDownPushButton.released.connect(self.stop_repeated_action)
        # Timer for repeated actions
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(170)
        self.timer.timeout.connect(self.perform_repeated_action)
        self.current_action = None

    def start_repeated_action(self, action):
        """Start the timer with the given action."""
        self.current_action = action
        action()  # Perform the action immediately
        self.timer.start()

    def stop_repeated_action(self):
        """Stop the timer and reset the current action."""
        self.timer.stop()
        self.current_action = None

    def perform_repeated_action(self):
        """Perform the currently set action."""
        if self.current_action:
            self.current_action()

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

    def set_keys_from_cif(self, cif_file) -> None:
        try:
            self.cif = gemmi.cif.read_file(cif_file)
            block = self.cif.sole_block()
        except Exception:
            show_general_warning(self, 'Unable to load file')
            return
        keys = [x.pair[0] for x in block if x.pair is not None]
        essentials = [x.pair[0] for x in block if x.pair is not None and x.pair[1] == 'True']
        self.set_essentials(essentials)
        self.set_keys(keys)

    def set_essentials(self, essentials):
        self.essential_keys = essentials

    def set_keys(self, order_keys: list[str] | None = None):
        self.ui.cifOrderTableWidget.setRowCount(0)
        row = 0
        for key_text in order_keys:
            if not key_text:
                continue
            self.ui.cifOrderTableWidget.insertRow(row)
            self.set_row_text(key_text, row)
            row += 1
        # self.ui.cifOrderTableWidget.resizeColumnsToContents()

    def set_row_text(self, key_text: str, row: int) -> None:
        item1 = CifOrderItem(key_text)
        item1.setFlags(item1.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        item1.setText(key_text)
        if key_text in self.essential_keys:
            item1.setEssential(True)
        else:
            item1.setEssential(False)
        self.ui.cifOrderTableWidget.setItem(row, Column.key, item1)

    def set_keys_from_settings(self, keys: list[str]):
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
        self.essential_keys = self.order_essentials

    def delete_keys(self):
        items = self.ui.cifOrderTableWidget.selectedItems()
        for item in items:
            self.ui.cifOrderTableWidget.removeRow(item.row())

    def export_cif(self):
        doc = gemmi.cif.Document()
        blockname = 'FinalCif_keys_order'
        block = doc.add_new_block(blockname)
        for key in self.order_keys:
            value = 'True' if key in self.order_essentials else 'False'
            block.set_pair(key, value)
        filename = cif_file_save_dialog(blockname.lower() + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=gemmi.cif.Style.Indent35)
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning(self, f'No permission to write file to {Path(filename).resolve()}')


if __name__ == "__main__":
    from finalcif.tools.settings import FinalCifSettings

    app = QtWidgets.QApplication(sys.argv)
    # form = CifOrder(parent=None, cif_file=Path('test-data/1000007.cif').resolve())
    settings = FinalCifSettings()
    form = CifOrder(parent=None)
    form.set_order_from_settings(settings)
    form.show()
    form.raise_()
    sys.exit(app.exec())
