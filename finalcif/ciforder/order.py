import enum
import sys
from pathlib import Path
from typing import List

from PyQt5 import QtWidgets, QtCore

from finalcif.cif import cif_order
from finalcif.cif.cif_file_io import CifContainer
from finalcif.ciforder.order_ui import Ui_CifOrderForm
from finalcif.gui import dialogs
from finalcif.gui.custom_classes import MyTableWidgetItem


class Column(enum.IntEnum):
    key = 0
    essential = 1


class CifOrder(QtWidgets.QWidget):
    def __init__(self, parent, cif_file: Path = None):
        super().__init__(parent)
        self.ui = Ui_CifOrderForm()
        self.ui.setupUi(self)
        self.cif = None
        if cif_file is not None:
            self.set_keys_from_cif(cif_file)
        else:
            QtCore.QTimer(self).singleShot(0, lambda: self.set_keys(cif_order.order))
        self.connect_signals_and_slots()

    def connect_signals_and_slots(self):
        self.ui.importCifPushButton.clicked.connect(self.import_cif)

    @property
    def order_keys(self):
        keys = []
        for row in range(self.ui.cifOrderTableWidget.rowCount()):
            key = self.ui.cifOrderTableWidget.item(row, Column.key).text()
            keys.append(key)
        return keys

    def set_keys_from_cif(self, cif_file):
        self.cif = CifContainer(cif_file)
        self.set_keys(self.cif.keys())

    def set_keys(self, keys: List[str] = None):
        self.ui.cifOrderTableWidget.setRowCount(0)
        row = 0
        for key in keys:
            if not key:
                continue
            self.ui.cifOrderTableWidget.insertRow(row)
            item1 = MyTableWidgetItem(key)
            self.ui.cifOrderTableWidget.setItem(row, Column.key, item1)
            row += 1
        self.ui.cifOrderTableWidget.resizeColumnsToContents()

    def import_cif(self):
        cif_file = dialogs.cif_file_open_dialog()
        if self._file_is_there(cif_file):
            self.set_keys_from_cif(cif_file)

    def _file_is_there(self, cif_file: str) -> bool:
        return cif_file is not None and Path(cif_file).is_file() and Path(cif_file).exists()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # form = CifOrder(parent=None, cif_file=Path('test-data/1000007.cif').resolve())
    form = CifOrder(parent=None)
    form.show()
    form.raise_()
    sys.exit(app.exec_())
