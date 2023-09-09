#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import copy
from contextlib import suppress
from typing import Union, List, Any

import gemmi
import qtawesome
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize, QVariant, pyqtSignal, QEvent
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QTableView, QHeaderView, QMenu, QAction
from gemmi import cif
from gemmi.cif import as_string, is_null
from packaging import version

from finalcif.cif.text import retranslate_delimiter, utf8_to_str, quote
from finalcif.gui.dialogs import show_keyword_help
from finalcif.tools.dsrmath import my_isnumeric


class Loop(QtCore.QObject):
    def __init__(self, tags: List[str], values: List[List[str]], parent, block):
        super(Loop, self).__init__(parent=parent)
        self.parent = parent
        self.block = block
        self.tableview = MyQTableView(parent)
        self._values: List[List[str]] = self.get_string_values(values)
        self.tags = tags
        self.model: Union[LoopTableModel, None] = None
        self.make_model()
        self.tableview.horizontalHeader().sectionClicked.connect(self.display_help)
        self.model.modelChanged.connect(self.save_new_cell_value_to_cif_block)
        self.tableview.rowChanged.connect(self.save_new_row_to_cif_block)
        self.tableview.row_moved.connect(self.move_row)
        self.model.rowDeleted.connect(self.delete_row)

    @QtCore.pyqtSlot(int)
    def display_help(self, header_section: int):
        from finalcif.cif.all_cif_dicts import cif_all_dict
        tag = self.tags[header_section]
        keyword_help = cif_all_dict.get(tag, None)
        if keyword_help:
            keyword_help = retranslate_delimiter(keyword_help, no_html_unescape=True)
            show_keyword_help(self.parent, keyword_help, tag)

    def set_or_update_model(self, values: List[List[str]]):
        self.values = values
        self.model = LoopTableModel(self.tags, self.values)
        self.tableview.setModel(self.model)

    def save_new_cell_value_to_cif_block(self, row: int, col: int, value: Union[str, int, float], header: list):
        """
        Save values of new table rows into cif loops.
        """
        if col >= 0:
            column = self.block.find_values(header[col])
            while len(column) < row + 1:
                # fill table fields with values until last new row reached
                loop = self.block.find_loop(header[col]).get_loop()
                loop.add_row(['.'] * len(header))
                column = self.block.find_values(header[col])
            column[row] = value if my_isnumeric(value) else quote(value)

    def delete_row(self, header: List[str], row: int):
        table: cif.Table = self.block.find(header)
        with suppress(IndexError):
            table.remove_row(row)

    def move_row(self, header: List[str], pos1: int, pos2: int):
        """Moves table row from pos1 to pos2"""
        table: cif.Table = self.block.find(header)
        table.move_row(pos1, pos2)

    def save_new_row_to_cif_block(self, header: List[str], data: list):
        """
        Save values of new table rows into cif loops.
        """
        table: cif.Table = self.block.find(header)
        # There is no reordering currently, so I have to delete and subsequently append the new rows:
        while len(table) > 0:
            table.remove_row(0)
        for row in data:
            table.append_row([x if is_null(x) else quote(x) for x in row])

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


class MyQTableView(QTableView):
    rowChanged = pyqtSignal(list, list)
    row_moved = pyqtSignal(list, int, int)

    def __init__(self, parent):
        super().__init__(parent=parent)

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        add_action = QAction('Add Row', self)
        del_action = QAction('Delete Row', self)
        down_action = QAction('Move row down', self)
        up_action = QAction('Move row up', self)
        add_action.triggered.connect(lambda: self._add_row(event))
        del_action.triggered.connect(lambda: self._delete_row(event))
        up_action.triggered.connect(lambda: self._row_up(event))
        down_action.triggered.connect(lambda: self._row_down(event))
        with suppress(Exception):
            up_action.setIcon(qtawesome.icon('mdi.arrow-up'))
            down_action.setIcon(qtawesome.icon('mdi.arrow-down'))
            del_action.setIcon(qtawesome.icon('mdi.trash-can-outline'))
            add_action.setIcon(qtawesome.icon('mdi.table-row-plus-after'))
        self.menu.addAction(add_action)
        self.menu.addAction(del_action)
        self.menu.addSeparator()
        self.menu.addAction(up_action)
        self.menu.addAction(down_action)
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

    def get_index_of_row(self, row_id):
        return self.model().index(row_id, 0)

    def _row_down(self, event: QEvent) -> None:
        """Moves the current row down a row"""
        row_id = self.currentIndex().row()
        # Should have data and not be the last row:
        if len(self.model()._data) > 1 and self.is_last_row(row_id):
            rowdata = self.model()._data.pop(row_id)
            self.model()._data.insert(row_id + 1, rowdata)
            self.setCurrentIndex(self.get_index_of_row(row_id + 1))
            if version.parse(gemmi.__version__) > version.parse('0.5.1'):
                self.row_moved.emit(self.model()._header, row_id, row_id + 1)
            else:
                self.rowChanged.emit(self.model()._header, self.model()._data)

    def is_last_row(self, row_id):
        return row_id < (len(self.model()._data) - 1)

    def _row_up(self, event: QEvent) -> None:
        """Moves the current row up a row"""
        row_id = self.currentIndex().row()
        if len(self.model()._data) > 1 and row_id > 0:
            rowdata = self.model()._data.pop(row_id)
            self.model()._data.insert(row_id - 1, rowdata)
            self.setCurrentIndex(self.get_index_of_row(row_id - 1))
            if version.parse(gemmi.__version__) > version.parse('0.5.1'):
                self.row_moved.emit(self.model()._header, row_id, row_id - 1)
            else:
                self.rowChanged.emit(self.model()._header, self.model()._data)


class LoopTableModel(QAbstractTableModel):
    modelChanged = pyqtSignal(int, int, 'PyQt_PyObject', list)
    rowDeleted = pyqtSignal(list, int)

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
        # if role == Qt.TextAlignmentRole:
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
        self.rowDeleted.emit(self._header, row)
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
