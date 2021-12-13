#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import copy
from typing import Union, List, Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize, QVariant, pyqtSignal, QEvent
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QTableView, QHeaderView, QMenu, QAction
from gemmi.cif import as_string, is_null

from finalcif.cif.text import retranslate_delimiter, utf8_to_str


class MyQTableView(QTableView):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        delAction = QAction('Delete Row', self)
        delAction.triggered.connect(lambda: self._delete_row(event))
        addAction = QAction('Add Row', self)
        addAction.triggered.connect(lambda: self._add_row(event))
        self.menu.addAction(addAction)
        self.menu.addAction(delAction)
        # add other required actions
        self.menu.popup(QCursor.pos())

    def _delete_row(self, event: QEvent):
        self.model().removeRow(self.currentIndex().row())
        self.model().modelReset.emit()

    def _add_row(self, event: QEvent):
        if len(self.model()._data) > 0:
            rowlen = len(self.model()._data[0])
            self.model()._data.append(['', ] * rowlen)
            self.model()._original.append(['', ] * rowlen)
            self.model().modelReset.emit()


class Loop():
    def __init__(self, tags: List[str], values: List[List[str]]):
        self.tableview = MyQTableView()
        self._values: List[List[str]] = self.get_string_values(values)
        # print(self._values, '#_values')
        self.tags = tags
        self.model: Union[LoopTableModel, None] = None
        self.make_model()

    def set_or_update_model(self, values: List[List[str]]):
        self.values = values
        self.model = LoopTableModel(self.tags, self.values)
        self.tableview.setModel(self.model)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = self.get_string_values(values)

    def make_model(self) -> None:
        """
        Creates the model and applies data to it
        """
        self.set_or_update_model(self.values)
        header = self.tableview.horizontalHeader()
        # Format the header sizes:
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width = header.sectionSize(column) + 15
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width)

    def get_string_values(self, values: List[List[str]]) -> List[List[str]]:
        """
        Get data for a loop by tags
        """
        data = []
        for v in values:
            # as_string() would make . and ? to empty strings otherwise: 
            data.append([x if is_null(x) else as_string(x) for x in v])
        return data


class LoopTableModel(QAbstractTableModel):
    modelChanged = pyqtSignal(int, int, 'PyQt_PyObject', list)

    def __init__(self, header, data):
        super(LoopTableModel, self).__init__()
        self._data = data
        self._original = copy.deepcopy(data)
        self._header = header
        self.modified = []  # a list of modified table items

    @property
    def loop_data(self) -> List[List[str]]:
        return self._data

    def data(self, index: QModelIndex, role: int = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.SizeHintRole:
            return QSize(120, 50)
        #if role == Qt.TextAlignmentRole:
        #    pass
            # if isnumeric(value):
            #    return Qt.AlignVCenter + Qt.AlignVertical_Mask
        if role == Qt.BackgroundColorRole and \
            (row, col) in [(x['row'], x['column']) for x in self.modified]:
            return QVariant(QColor("#facaca"))
        if role == Qt.EditRole:
            return retranslate_delimiter(value)
        if role == Qt.DisplayRole:
            return retranslate_delimiter(value)

    def headerData(self, section, orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            try:
                return str(self._header[section])
            except IndexError:
                return ''
        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignLeft

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
            self.modelChanged.emit(row, col, utf8_to_str(value), self._header)
            return True
        return False

    def removeRow(self, row: int, parent: QModelIndex = None) -> bool:
        if len(self._data) > 0:
            del self._data[row]
        else:
            return False
        self.modelChanged.emit(row, -1, '', self._header)
        return True

    def revert(self) -> None:
        """Reverts the model to the state before editing"""
        self.beginResetModel()
        while self.modified:
            for p in self.modified:
                row = p.get('row')
                col = p.get('column')
                value = p.get('previous')
                self._data[row][col] = value
            self.modified.pop(0)
        self.endResetModel()
