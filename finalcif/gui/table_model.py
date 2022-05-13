from typing import Any

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, structures=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.horizontalHeaders = ['Id', 'Data Name', 'File Name', 'Last Modified', 'Path']
        self._data = structures or []

    def data(self, index: QModelIndex, role: int = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.DisplayRole:
            if isinstance(value, bytes):
                return value.decode('utf-8')
            else:
                return value

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except IndexError:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except IndexError:
                pass
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
            return True
        return False

    def clear(self):
        self.resetInternalData()

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=True if order == Qt.DescendingOrder else False)
        self.layoutChanged.emit()
        # super(TableModel, self).sort(column, order)
