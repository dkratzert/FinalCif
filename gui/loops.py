#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import copy
from typing import Union, List, Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize, QVariant, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableView, QHeaderView
from gemmi.cif import as_string

from cif.cif_file_io import CifContainer


class Loop():
    def __init__(self, tags: List[str], values: List[List[str]], table: QTableView):
        self.table = table
        self.values = values
        self.tags = tags
        self.model: Union[TableModel, None] = None

    def make_model(self, ) -> None:
        """
        Creates the model and applies data to it
        """
        self.model = TableModel(self.get_string_values(), self.tags)
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        # Format the header sizes:
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width = header.sectionSize(column) + 10
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width)

    def get_string_values(self) -> List[List[str]]:
        """
        Get data for a loop by tags
        """
        data = []
        for v in self.values:
            # as_string() would make . and ? to empty strings otherwise: 
            data.append([x if x in ('.', '?') else as_string(x) for x in v])
        return data


class TableModel(QAbstractTableModel):
    modelChanged = pyqtSignal(int, int, 'PyQt_PyObject', list)

    def __init__(self, data, header):
        super(TableModel, self).__init__()
        self._data = data
        self._original = copy.deepcopy(data)
        self._header = header
        self.modified = []  # a list of modified table items 

    def data(self, index: QModelIndex, role: int = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.SizeHintRole:
            return QSize(120, 50)
        if role == Qt.TextAlignmentRole:
            pass
            # if isnumeric(value):
            #    return Qt.AlignVCenter + Qt.AlignVertical_Mask
        if role == Qt.BackgroundColorRole:
            if (row, col) in [(x['row'], x['column']) for x in self.modified]:
                return QVariant(QColor("#facaca"))
        if role == Qt.EditRole:
            return value
        if role == Qt.DisplayRole:
            return value

    def headerData(self, section, orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._header[section])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignLeft

    def rowCount(self, parent=None, *args, **kwargs):
        """
        The length of the outer list.
        """
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Tkes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        return len(self._data[0])

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        row, col = index.row(), index.column()
        previous = self._original[row][col]
        if not index:
            return False
        if index.isValid() and role == Qt.EditRole and value != previous:
            self._data[row][col] = value
            self.modified.append({'row': row, 'column': col, 'previous': previous})
            self.modelChanged.emit(row, col, value, self._header)
            return True
        return False

    def revert(self) -> None:
        """Reverts the model to the state before editing"""
        self.beginResetModel()
        while self.modified:
            for p in self.modified:
                self._data[p.get('row')][p.get('column')] = p.get('previous')
            self.modified.pop(0)
        self.endResetModel()
