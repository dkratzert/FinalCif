from contextlib import suppress
from enum import IntEnum
from typing import Any, List, Union, Tuple

import gemmi.cif
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt

from finalcif.gui.ciftable_view import CifItemEditor, CifTableView


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
        self.vheaderItems = []
        self.horizontalHeaderItems = ['CIF data', 'Sources', 'Own Data']
        self._data = []
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
            with suppress(IndexError):
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


from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView


def main():
    app = QApplication([])

    # Sample data
    data = [
        ["CIF_1", "DATA_1", "EDIT_1"],
        ["CIF_2", "DATA_2", "EDIT_2"],
        ["CIF_3", "DATA_3", "EDIT_3"],
    ]

    main_window = QMainWindow()

    # Set up the QTableView
    table_view = CifTableView(main_window)
    model = CifTableModel(parent=main_window, data=data)
    table_view.setModel(model)

    main_window.setCentralWidget(table_view)
    main_window.show()

    app.exec_()


if __name__ == "__main__":
    main()