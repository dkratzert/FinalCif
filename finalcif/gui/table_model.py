from contextlib import suppress
from typing import Any, List, Union, Tuple, Dict

import gemmi.cif
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class CifTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.horizontalHeaders = ['CIF data', 'Sources', 'Own Data']
        self.verticalHeaders = []
        self._data = []
        self.dataChanged.connect(self.foo)

    def foo(self, *args, **kwargs):
        print('foo', args, kwargs)

    def resetInternalData(self) -> None:
        self._data.clear()

    def setCifData(self, data: List[Union[List, Tuple]]):
        self._data = [(gemmi.cif.as_string(x[1]), '', '') for x in data]
        self.verticalHeaders = [x[0] for x in data]

    def data(self, index: QModelIndex, role: int = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.DisplayRole:
            if isinstance(value, bytes):
                return value.decode('utf-8')
            else:
                return value
        #if role == Qt.EditRole:
        #    return value


    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            with suppress(IndexError):
                self.horizontalHeaders[section] = data
        if orientation == Qt.Vertical and role in (Qt.DisplayRole, Qt.EditRole):
            with suppress(IndexError):
                self.verticalHeaders[section] = data
        #self.headerDataChanged.emit(orientation, section, section)
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
        if len(self._data) > 0:
            return len(self._data[0])
        else:
            return 0

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        row, col = index.row(), index.column()
        if not index:
            return False
        if index.isValid() and role == Qt.EditRole:
            self._data[row][col] = value
            #self.dataChanged.emit(index, index, role)
            return True
        return super(CifTableModel, self).setData(index, value, role)

    def clear(self):
        self.resetInternalData()

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=True if order == Qt.DescendingOrder else False)
        #self._data, self.verticalHeaders = zip(*sorted(zip(self._data, self.verticalHeaders), key=lambda x: x[column]))
        self.layoutChanged.emit()
        # super(TableModel, self).sort(column, order)
