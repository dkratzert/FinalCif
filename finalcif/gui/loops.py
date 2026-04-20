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
from typing import TYPE_CHECKING

import gemmi

from finalcif.gui.custom_classes import light_blue, light_red
from finalcif.gui.plaintextedit import MyQPlainTextEdit
from finalcif.gui.validators import validators

with suppress(ImportError):
    import qtawesome
from qtpy import QtCore, QtWidgets, QtGui
from qtpy.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize, Signal, QEvent
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QTableView, QHeaderView, QMenu, QTabWidget
from gemmi import cif
from gemmi.cif import as_string, is_null

from finalcif.cif.text import retranslate_delimiter, utf8_to_str, quote
from finalcif.gui.dialogs import show_keyword_help
from finalcif.tools.dsrmath import my_isnumeric
from finalcif.tools.misc import cif_to_header_label, grouper

if TYPE_CHECKING:
    from finalcif.cif.cif_file_io import CifContainer


class Loop(QtCore.QObject):
    def __init__(self, tags: list[str], values: list[list[str]], parent, block):
        super().__init__(parent=parent)
        self._parent_widget = parent
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
    def display_help(self, header_section: int) -> None:
        from finalcif.cif.all_cif_dicts import cif_all_dict
        tag = self.tags[header_section]
        keyword_help = cif_all_dict.get(tag, None) or f'No help text found for {tag}.'
        if keyword_help:
            keyword_help = retranslate_delimiter(keyword_help, no_html_unescape=True)
            show_keyword_help(self._parent_widget, keyword_help, tag)

    def set_or_update_model(self, values: list[list[str]]) -> None:
        self.values = values
        self.model = LoopTableModel(self.tags, self.values)
        self.tableview.setModel(self.model)

    def save_new_cell_value_to_cif_block(self, row: int, col: int, value: str | int | float, header: list) -> None:
        """Save values of new table rows into cif loops."""
        if col >= 0:
            column = self.block.find_values(header[col])
            while len(column) < row + 1:
                loop = self.block.find_loop(header[col]).get_loop()
                loop.add_row(['.'] * len(header))
                column = self.block.find_values(header[col])
            column[row] = value if my_isnumeric(value) else quote(value)

    def delete_row(self, header: list[str], row: int) -> None:
        table: cif.Table = self.block.find(header)
        with suppress(IndexError):
            table.remove_row(row)

    def move_row(self, header: list[str], pos1: int, pos2: int):
        """Moves table row from pos1 to pos2"""
        table: cif.Table = self.block.find(header)
        with suppress(IndexError):
            table.move_row(pos1, pos2)

    def save_new_row_to_cif_block(self, header: list[str], data: list) -> None:
        """Save values of new table rows into cif loops."""
        table: cif.Table = self.block.find(header)
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
        """Creates the model and applies data to it."""
        self.set_or_update_model(self.values)
        header = self.tableview.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
            width = header.sectionSize(column) + 15
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
            header.resizeSection(column, width)

    def get_string_values(self, values: list[list[str]]) -> list[list[str]]:
        """Get data for a loop by tags."""
        data = []
        for v in values:
            data.append([x if is_null(x) else as_string(x) for x in v])
        return data


class MyQTableView(QTableView):
    rowChanged = Signal(list, list)
    row_moved = Signal(list, int, int)

    def __init__(self, parent):
        super().__init__(parent=parent)

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
        self.menu.popup(QCursor.pos())

    def _delete_row(self, event: QEvent) -> None:
        self.model().removeRow(self.currentIndex().row())
        self.model().modelReset.emit()

    def _add_row(self, event: QEvent) -> None:
        self.model().add_empty_row()
        self.model().modelReset.emit()

    def get_index_of_row(self, row_id):
        return self.model().index(row_id, 0)

    def _row_down(self, event: QEvent) -> None:
        """Moves the current row down a row."""
        row_id = self.currentIndex().row()
        if self.model().move_row_down(row_id):
            self.setCurrentIndex(self.get_index_of_row(row_id + 1))
            self.row_moved.emit(self.model().header, row_id, row_id + 1)

    def is_last_row(self, row_id):
        return row_id < (len(self.model().loop_data) - 1)

    def _row_up(self, event: QEvent) -> None:
        """Moves the current row up a row."""
        row_id = self.currentIndex().row()
        if self.model().move_row_up(row_id):
            self.setCurrentIndex(self.get_index_of_row(row_id - 1))
            self.row_moved.emit(self.model().header, row_id, row_id - 1)


class LoopItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_widget = parent
        self.color = None

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QPlainTextEdit(self._parent_widget)
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
    def header(self) -> list:
        return self._header

    @property
    def loop_data(self) -> list[list[str]]:
        return self._data

    def add_empty_row(self) -> None:
        """Appends a new empty row matching the current column count."""
        if len(self._data) > 0:
            rowlen = len(self._data[0])
            self._data.append([''] * rowlen)
            self._original.append([''] * rowlen)

    def move_row_down(self, row_id: int) -> bool:
        """Moves row at row_id one position down. Returns True if the move was performed."""
        if len(self._data) > 1 and row_id < len(self._data) - 1:
            rowdata = self._data.pop(row_id)
            self._data.insert(row_id + 1, rowdata)
            return True
        return False

    def move_row_up(self, row_id: int) -> bool:
        """Moves row at row_id one position up. Returns True if the move was performed."""
        if len(self._data) > 1 and row_id > 0:
            rowdata = self._data.pop(row_id)
            self._data.insert(row_id - 1, rowdata)
            return True
        return False

    def data(self, index: QModelIndex, role: int | None = None):
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == Qt.ItemDataRole.SizeHintRole:
            return QSize(120, 50)
        if role == Qt.ItemDataRole.BackgroundRole:
            if (row, col) in [(x['row'], x['column']) for x in self.modified] and self.validate_text(value, col):
                return light_blue
            if not self.validate_text(value, col):
                return light_red
            return None
        if role == QtCore.Qt.ItemDataRole.EditRole:
            return retranslate_delimiter(value)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return retranslate_delimiter(value)
        if role == Qt.ItemDataRole.ToolTipRole:
            key = self._header[col]
            if validators.get(key):
                return validators.get(key, None).help_text

    def headerData(self, section, orientation: Qt.Orientation = QtCore.Qt.Orientation.Horizontal, role=None):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            try:
                return str(self._header[section])
            except IndexError:
                return ''
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignVCenter + QtCore.Qt.AlignmentFlag.AlignLeft

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        if len(self._data) > 0:
            return len(self._data[0])
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
        return True

    def removeRow(self, row: int, parent: QModelIndex = None) -> bool:
        if len(self._data) > 0:
            del self._data[row]
        else:
            return False
        self.rowDeleted.emit(self._header, row)
        return True

    def revert(self) -> None:
        """Reverts the model to the state before editing."""
        self.beginResetModel()
        while self.modified:
            for p in self.modified:
                self._data[p['row']][p['column']] = p['previous']
            self.modified.pop(0)
        self.endResetModel()


class LoopsPage(QtWidgets.QWidget):
    """
    Self-contained widget that owns a QTabWidget for displaying and editing CIF loops.

    Embed this in a layout, then call load(cif) whenever a new CIF is opened.
    To add the Author Editor tab (which lives in the main .ui file), call
    set_author_editor_tab(widget) once after ui.setupUi().

    Signals
    -------
    new_loop_requested
        Emitted when the user navigates to the "Create Loops" page; AppWindow
        should respond by hiding the revert/new/delete buttons.
    """
    new_loop_requested = Signal()

    def __init__(self, parent=None, *, cif: 'CifContainer | None' = None):
        super().__init__(parent=parent)
        self._cif = cif
        self._loops: list[Loop] = []
        self._has_author_tab: bool = False
        self._loopcreate = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)

        if cif is not None:
            self.load(cif)

    def set_author_editor_tab(self, widget: QtWidgets.QWidget) -> None:
        """Insert the Author Editor widget as the first (index 0) tab."""
        self.tab_widget.insertTab(0, widget, 'Author Editor')
        self._has_author_tab = True

    def load(self, cif: 'CifContainer') -> None:
        """Store the CIF container and rebuild all loop tabs."""
        self._cif = cif
        self.make_loops_tables()

    def make_loops_tables(self) -> None:
        """Remove all loop tabs (keeping Author Editor at 0 if present) and rebuild."""
        first_loop_index = 1 if self._has_author_tab else 0
        while self.tab_widget.count() > first_loop_index:
            self.tab_widget.removeTab(first_loop_index)
        self._loops.clear()
        if self._cif and self._cif.loops:
            self._add_loops_tables()

    def _add_loops_tables(self) -> None:
        for num, loop in enumerate(self._cif.loops):
            tags = loop.tags
            if not tags:
                continue
            self._new_loop_tab(loop, num, tags)
        if self._cif.res_file_data:
            self._add_res_file_to_loops()

    def _new_loop_tab(self, loop: gemmi.cif.Loop, num: int, tags: list[str]) -> None:
        loop_obj = Loop(tags, values=grouper(loop.values, loop.width()),
                        parent=self.tab_widget, block=self._cif.block)
        self._loops.append(loop_obj)
        self.tab_widget.addTab(loop_obj.tableview, cif_to_header_label.get(tags[0]) or tags[0])
        self.tab_widget.setTabToolTip(self.tab_widget.count() - 1, tags[0])

    def _add_res_file_to_loops(self) -> None:
        fixfont = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        textedit = QtWidgets.QPlainTextEdit()
        self.tab_widget.addTab(textedit, 'SHELX res file')
        textedit.setPlainText(self._cif.res_file_data[1:-1])
        textedit.document().setDefaultFont(fixfont)
        textedit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        textedit.setReadOnly(True)

    def revert_all_loops(self) -> None:
        """Revert every loop model to its state before editing."""
        for loop in self._loops:
            loop.model.revert()

    def go_to_new_loop_page(self) -> None:
        """Add a LoopCreator tab and emit new_loop_requested so AppWindow can hide buttons."""
        from finalcif.gui.loop_creator import LoopCreator
        self._loopcreate = LoopCreator(parent=self, cif=self._cif)
        self.tab_widget.addTab(self._loopcreate, 'Create Loops')
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        self._loopcreate.saveLoopPushButton.clicked.connect(self._save_new_loop_to_cif)
        self.new_loop_requested.emit()

    def on_delete_current_loop(self) -> None:
        """Delete the CIF loop shown in the currently active tab."""
        current_tab_index = self.tab_widget.currentIndex()
        current_table_view = self.tab_widget.widget(current_tab_index)
        try:
            header_model: LoopTableModel = current_table_view.horizontalHeader().model()
        except AttributeError:
            return  # Not a QTableView (e.g. Author Editor or SHELX tab)
        header_item = header_model.header[0]
        loop: gemmi.cif.Loop = self._cif.block.find_loop(header_item).get_loop()
        table: gemmi.cif.Table = self._cif.block.find(loop.tags)
        table.erase()
        self.tab_widget.removeTab(current_tab_index)

    def _save_new_loop_to_cif(self) -> None:
        if self._loopcreate is None:
            return
        loop = self._loopcreate.save_new_loop_to_cif()
        self._new_loop_tab(loop=loop, num=self.tab_widget.count(), tags=self._loopcreate.tags)
        self.tab_widget.removeTab(self.tab_widget.count() - 2)
        self._loopcreate.deleteLater()
        self._loopcreate = None
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)


if __name__ == '__main__':
    import sys
    from pathlib import Path
    from qtpy.QtWidgets import QApplication, QMainWindow
    from finalcif.cif.cif_file_io import CifContainer

    _app = QApplication.instance() or QApplication(sys.argv)

    _cif_path = Path(__file__).parent.parent.parent / 'tests' / 'examples' / '1979688_small.cif'
    _cif = CifContainer(_cif_path)

    _win = QMainWindow()
    _win.setWindowTitle('LoopsPage — manual test')
    _win.resize(1200, 700)

    _page = LoopsPage(cif=_cif, parent=_win)
    _win.setCentralWidget(_page)
    _win.show()

    sys.exit(_app.exec())
