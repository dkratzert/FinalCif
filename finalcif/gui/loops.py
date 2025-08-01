from __future__ import annotations
#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import copy
from contextlib import suppress
from typing import Any

import gemmi

from finalcif.gui.custom_classes import light_blue, light_red
from finalcif.gui.plaintextedit import MyQPlainTextEdit
from finalcif.gui.validators import validators

with suppress(ImportError):
    import qtawesome
from qtpy import QtCore, QtWidgets, QtGui
from qtpy.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize, Signal, QEvent
from qtpy.QtGui import QCursor, QColor
from qtpy.QtWidgets import QTableView, QHeaderView, QMenu
from gemmi import cif
from gemmi.cif import as_string, is_null
from packaging import version

from finalcif.cif.text import retranslate_delimiter, utf8_to_str, quote
from finalcif.gui.dialogs import show_keyword_help
from finalcif.tools.dsrmath import my_isnumeric


class Loop(QtCore.QObject):
    def __init__(self, tags: list[str], values: list[list[str]], parent, block):
        super().__init__(parent=parent)
        self.parent = parent
        self.block = block
        self.tableview = MyQTableView(parent)
        self._values: list[list[str]] = self.get_string_values(values)
        self.tags = tags
        self.model: LoopTableModel | None = None
        self.make_model()
        self.tableview.horizontalHeader().sectionClicked.connect(self.display_help)
        self.model.modelChanged.connect(self.save_new_cell_value_to_cif_block)
        self.tableview.rowChanged.connect(self.save_new_row_to_cif_block)
        self.tableview.row_moved.connect(self.move_row)
        self.model.rowDeleted.connect(self.delete_row)

    @QtCore.Slot(int)
    def display_help(self, header_section: int):
        from finalcif.cif.all_cif_dicts import cif_all_dict
        tag = self.tags[header_section]
        keyword_help = cif_all_dict.get(tag, None) or f'No help text found for {tag}.'
        if keyword_help:
            keyword_help = retranslate_delimiter(keyword_help, no_html_unescape=True)
            show_keyword_help(self.parent, keyword_help, tag)

    def set_or_update_model(self, values: list[list[str]]):
        self.values = values
        self.model = LoopTableModel(self.tags, self.values)
        self.tableview.setModel(self.model)

    def save_new_cell_value_to_cif_block(self, row: int, col: int, value: str | int | float, header: list):
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

    def delete_row(self, header: list[str], row: int):
        table: cif.Table = self.block.find(header)
        with suppress(IndexError):
            table.remove_row(row)

    def move_row(self, header: list[str], pos1: int, pos2: int):
        """Moves table row from pos1 to pos2"""
        table: cif.Table = self.block.find(header)
        table.move_row(pos1, pos2)

    def save_new_row_to_cif_block(self, header: list[str], data: list):
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
    def values(self, values) -> None:
        self._values = self.get_string_values(values)

    def make_model(self) -> None:
        """
        Creates the model and applies data to it
        """
        self.set_or_update_model(self.values)
        header = self.tableview.horizontalHeader()
        # Format the header sizes:
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
            width = header.sectionSize(column) + 15
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
            header.resizeSection(column, width)

    def get_string_values(self, values: list[list[str]]) -> list[list[str]]:
        """
        Get data for a loop by tags
        """
        data = []
        for v in values:
            # as_string() would make . and ? to empty strings otherwise: 
            data.append([x if is_null(x) else as_string(x) for x in v])
        return data


class MyQTableView(QTableView):
    rowChanged = Signal(list, list)
    row_moved = Signal(list, int, int)

    def __init__(self, parent):
        super().__init__(parent=parent)
        # self.setItemDelegate(LoopItemDelegate(self))

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        add_action = QtGui.QAction('Add Row', self)
        del_action = QtGui.QAction('Delete Row', self)
        down_action = QtGui.QAction('Move row down', self)
        up_action = QtGui.QAction('Move row up', self)
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

    def _delete_row(self, event: QEvent) -> None:
        self.model().removeRow(self.currentIndex().row())
        self.model().modelReset.emit()

    def _add_row(self, event: QEvent) -> None:
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


class LoopItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.color = None

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QPlainTextEdit(self.parent)
        editor.color = self.color
        editor.cif_key = ''
        return editor

    def setEditorData(self, editor: MyQPlainTextEdit, index):
        value = index.model().data(index, QtCore.Qt.ItemDataRole.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor: MyQPlainTextEdit, model, index):
        value = editor.getText()
        model.setData(index, value, QtCore.Qt.ItemDataRole.EditRole)


class LoopTableModel(QAbstractTableModel):
    modelChanged = Signal(int, int, object, list)
    rowDeleted = Signal(list, int)

    def __init__(self, header, data):
        super().__init__()
        self._data = data
        self._original = copy.deepcopy(data)
        self._header = header
        self.modified = []  # a list of modified table items

    @property
    def loop_data(self) -> list[list[str]]:
        return self._data

    def data(self, index: QModelIndex, role: int | None = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.ItemDataRole.SizeHintRole:
            return QSize(120, 50)
        # if role == Qt.TextAlignmentRole:
        #    pass
        # if isnumeric(value):
        #    return QtCore.Qt.AlignmentFlag.AlignVCenter + Qt.AlignVertical_Mask
        if (role == Qt.ItemDataRole.BackgroundRole and
                (row, col) in [(x['row'], x['column']) for x in self.modified] and self.validate_text(value, col)):
            return light_blue
        elif role == Qt.ItemDataRole.BackgroundRole and not self.validate_text(value, col):
            return light_red
        else:
            QColor(255, 255, 255)
        if role == QtCore.Qt.ItemDataRole.EditRole:
            return retranslate_delimiter(value)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return retranslate_delimiter(value)
        if role == Qt.ItemDataRole.ToolTipRole:
            key = self._header[col]
            if validators.get(key):
                return validators.get(key, None).help_text

    def headerData(self, section, orientation: Qt.Orientation = QtCore.Qt.Orientation.Horizontal, role=None):
        # section is the index of the column/row.
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            try:
                return str(self._header[section])
            except IndexError:
                return ''
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignVCenter + QtCore.Qt.AlignmentFlag.AlignLeft

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

    def flags(self, index: QModelIndex) -> Qt.ItemFlag | None:
        if index.isValid():
            return (QAbstractTableModel.flags(self, index) | QtCore.Qt.ItemFlag.ItemIsEditable |
                    QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)

    def setData(self, index: QModelIndex, value: str | int | float, role: int | None = None) -> bool:
        row, col = index.row(), index.column()
        previous = self._original[row][col]
        if not index:
            return False
        if index.isValid() and role == QtCore.Qt.ItemDataRole.EditRole:
            self._data[row][col] = value
            self.modified.append({'row': row, 'column': col, 'previous': previous})
            self.modelChanged.emit(row, col, utf8_to_str(value), self._header)
            return True
        return False

    def validate_text(self, text: str, col: int) -> bool:
        validator = validators.get(self._header[col], None)
        if validator and not validator.valid(text):
            return False
        else:
            return True

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
