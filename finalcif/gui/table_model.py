from contextlib import suppress
from enum import IntEnum
from typing import Any, List, Union, Tuple

import gemmi.cif
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.ciftable_view import CifTableView


class Column(IntEnum):
    CIF: int = 0
    DATA: int = 1
    EDIT: int = 2


class CifTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        if data is None:
            data = []
        self._data = data  # A list of rows where each row is a list of cells
        self.verticalHeaders = []
        self.horizontalHeaders = ['CIF data', 'Sources', 'Own Data']
        self.dataChanged.connect(self._on_data_changed)

    def _on_data_changed(self, *args):
        print('Data has changed', args)

    def flags(self, index: QModelIndex):
        if index.column() == Column.EDIT:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def resetInternalData(self) -> None:
        self._data.clear()

    def setCifData(self, data: List[Union[List, Tuple]]):
        self._data = [[gemmi.cif.as_string(x[1]), '', ''] if x[1] != '?' else ['?', '', ''] for x in data]
        self.verticalHeaders = [x[0] for x in data]

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not self._data:
            return None
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.DisplayRole:
            if isinstance(value, bytes):
                return value.decode('utf-8')
            else:
                return value
        if role == Qt.EditRole:
            return value

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            with suppress(IndexError):
                self.horizontalHeaders[section] = data
        if orientation == Qt.Vertical and role in (Qt.DisplayRole, Qt.EditRole):
            with suppress(IndexError):
                self.verticalHeaders[section] = data
        self.headerDataChanged.emit(orientation, section, section)
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            with suppress(IndexError, AttributeError):
                return self.horizontalHeaders[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            with suppress(IndexError):
                return self.verticalHeaders[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        """
        The length of the outer list.
        """
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Takes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        if not self._data:
            return 0
        return len(self._data[0])

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        row, col = index.row(), index.column()
        if not index:
            return False
        if index.isValid() and role == Qt.EditRole:
            self._data[row][col] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return super(CifTableModel, self).setData(index, value, role)

    def clear(self):
        self.resetInternalData()

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=True if order == Qt.DescendingOrder else False)
        # self._data, self.verticalHeaders = zip(*sorted(zip(self._data, self.verticalHeaders), key=lambda x: x[column]))
        self.layoutChanged.emit()
        # super(TableModel, self).sort(column, order)

    def appendRow(self, row_data):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(row_data)
        self.endInsertRows()

    def removeRow(self, row: int, parent: QModelIndex = None) -> bool:
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        del self._data[row]
        del self.vheaderitems[row]
        self.endRemoveRows()
        return True


def main():
    app = QApplication([])

    c = CifContainer('tests/examples/1979688.cif')
    data = [(key, value) for key, value in c.key_value_pairs()]

    main_window = QMainWindow()

    # Set up the QTableView
    table_view = CifTableView(main_window)
    model = CifTableModel(parent=main_window)
    table_view.setModel(model)
    model.setCifData(data)

    main_window.setCentralWidget(table_view)
    main_window.show()
    main_window.setMinimumSize(800, 600)

    app.exec_()


if __name__ == "__main__":
    main()
