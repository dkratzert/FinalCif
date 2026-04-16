from __future__ import annotations

import re
from enum import IntEnum

from qtpy import QtCore, QtGui
from qtpy.QtCore import QEvent, QObject, Qt
from qtpy.QtGui import QColor, QKeySequence, QBrush
from qtpy.QtWidgets import (
    QAbstractScrollArea, QTableView, QWidget, QApplication,
    QHeaderView, QStyledItemDelegate, QStyleOptionViewItem,
)

from finalcif.cif.text import retranslate_delimiter
from finalcif.gui.cif_table_model import CifTableModel, blue
from finalcif.gui.combobox import MyComboBox
from finalcif.gui.dialogs import show_keyword_help
from finalcif.gui.plaintextedit import MyQPlainTextEdit

white = QColor(255, 255, 255)
light_green = QColor(217, 255, 201)
light_blue = QColor(244, 244, 249)
yellow = QColor(250, 247, 150)
light_red = QColor(254, 191, 189)


class Column(IntEnum):
    CIF = 0
    DATA = 1
    EDIT = 2


DEBUG = False


class SeparatorWidget(QWidget):
    """A simple widget that paints the blue diagonal cross pattern for the separator row."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QBrush(blue)
        brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
        painter.fillRect(self.rect(), brush)
        painter.end()


class CifTableDelegate(QStyledItemDelegate):
    """Delegate for painting separator rows and providing size hints."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option: QStyleOptionViewItem, index):
        model = index.model()
        if model:
            row_data = model.get_row_data(index.row())
            if row_data and row_data.is_separator:
                painter.save()
                brush = QBrush(blue)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                painter.fillRect(option.rect, brush)
                painter.restore()
                return
        super().paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index) -> QtCore.QSize:
        model = index.model()
        if model:
            row_data = model.get_row_data(index.row())
            if row_data and row_data.is_separator:
                return QtCore.QSize(100, 10)
        return super().sizeHint(option, index)


class CifTableView(QTableView):
    """QTableView replacement for MyCifTable(QTableWidget).

    Provides a full compatibility API so that ``appwindow.py`` and other
    callers can keep using the same method names they used on the old
    ``MyCifTable`` (a QTableWidget subclass).
    """

    row_deleted = QtCore.Signal(str)
    textTemplate = QtCore.Signal(int)
    new_key = QtCore.Signal(str)

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent=parent)
        self._parent = parent
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        # Create and set the model
        self._model = CifTableModel(self)
        self.setModel(self._model)

        # Set the delegate for separator painting
        self._delegate = CifTableDelegate(self)
        self.setItemDelegate(self._delegate)

        # Configuration matching the old MyCifTable
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setShowGrid(True)
        self.setWordWrap(True)
        self.setSortingEnabled(False)

        # Ctrl+Del shortcut for deleting rows
        del_shortcut = QtGui.QShortcut(QKeySequence('Ctrl+Del'), self)
        del_shortcut.activated.connect(self._delete_current_row)

        # Vertical header: clickable for help display
        vheader = self.verticalHeader()
        vheader.setSectionsClickable(True)
        vheader.sectionClicked.connect(self.vheader_section_click)

        # Used by vheaderitems.insert() → insertRow() compatibility bridge
        self._pending_key: str | None = None

    # ---- vheaderitems compatibility ----

    @property
    def vheaderitems(self) -> _VHeaderItemsProxy:
        """Provides a mutable list-like proxy backed by the model.

        This keeps compatibility with code that does things like:
            self.ui.cif_main_table.vheaderitems[row]
            self.ui.cif_main_table.vheaderitems.index(key)
            self.ui.cif_main_table.vheaderitems.insert(pos, key)
            key in self.ui.cif_main_table.vheaderitems
        """
        return _VHeaderItemsProxy(self._model, self)

    # ---- Properties ----

    @property
    def rows_count(self) -> int:
        return self._model.rowCount()

    @property
    def columns_count(self) -> int:
        return self._model.columnCount()

    # ---- Compatibility: row/column count ----

    def rowCount(self) -> int:
        return self._model.rowCount()

    def insertRow(self, row: int) -> None:
        """Insert a new row (compatibility with QTableWidget.insertRow).

        The key for the row should have been set via ``vheaderitems.insert()``
        beforehand (same call order as the old code).
        """
        key = self._pending_key or ''
        self._pending_key = None
        self._model.add_row(key=key, position=row)

    def removeRow(self, row: int) -> None:
        self._model.remove_row(row)

    # ---- setCellWidget / cellWidget compatibility ----

    def setCellWidget(self, row: int, column: int, widget) -> None:
        """Set a persistent widget in the cell (uses setIndexWidget)."""
        keys = self._model.vheaderitems
        if row < len(keys):
            widget.cif_key = keys[row]
        if column in (Column.CIF, Column.DATA):
            widget.setUneditable()
        idx = self._model.index(row, column)
        self.setIndexWidget(idx, widget)

    def cellWidget(self, row: int, column: int) -> QWidget | None:
        """Get the persistent widget in the cell (uses indexWidget)."""
        idx = self._model.index(row, column)
        return self.indexWidget(idx)

    # ---- setItem / item compatibility ----

    def setItem(self, row: int, column: int, item) -> None:
        """Compatibility stub — stores item data in the model."""
        if item is not None:
            text = item.text() if hasattr(item, 'text') else ''
            self._model.set_cell_text(row, column, text)
            bg = item.background() if hasattr(item, 'background') else None
            if bg and bg.style() != Qt.BrushStyle.NoBrush:
                color = bg.color()
                self._model.set_cell_color(row, column, color)

    def item(self, row: int, column: int):
        """Returns a compatibility _FakeItem that reads from the model."""
        return _FakeItem(self._model, row, column)

    def itemFromKey(self, key: str, col: int):
        """Returns a compatibility item by CIF key lookup."""
        row = self._model.row_from_key(key)
        return _FakeItem(self._model, row, col)

    # ---- Vertical header compatibility ----

    def setVerticalHeaderItem(self, row: int, item) -> None:
        """Compatibility stub — the model already has the key as header."""
        pass

    def verticalHeaderItem(self, section: int):
        """Returns a compatibility object with .text() method."""
        return _FakeHeaderItem(self._model, section)

    # ---- setCurrentItem / setCurrentCell ----

    def setCurrentItem(self, item) -> None:
        """Clear selection (compatibility with QTableWidget.setCurrentItem(None))."""
        if item is None:
            self.clearSelection()
            self.setCurrentIndex(QtCore.QModelIndex())

    def setCurrentCell(self, row: int, column: int) -> None:
        idx = self._model.index(row, column)
        self.setCurrentIndex(idx)

    def currentRow(self) -> int:
        return self.currentIndex().row()

    # ---- Text access ----

    def setText(self, key: str, column: int, txt: str, row: int | None = None, color=None):
        """Set text in a table cell, creating a MyQPlainTextEdit widget if needed.

        This mirrors the old MyCifTable.setText() behavior exactly.
        """
        txt = retranslate_delimiter(txt)
        if row is None and self._model.has_key(key):
            row = self._model.row_from_key(key)
        elif row is None:
            row = 0
            raise IndexError(f'Key {key!r} not found in table')

        idx = self._model.index(row, column)
        existing_widget = self.indexWidget(idx)

        if isinstance(existing_widget, MyComboBox):
            existing_widget.setText(txt)
            return
        if isinstance(existing_widget, MyQPlainTextEdit):
            existing_widget.setText(txt, color=color)
            existing_widget.cif_key = key
        else:
            textedit = MyQPlainTextEdit(self)
            textedit.color = color
            textedit.cif_key = key
            textedit.templateRequested.connect(self.goto_template_page)
            textedit.new_key.connect(lambda x: self.new_key.emit(x))
            self.setCellWidget(row, column, textedit)
            textedit.setText(txt, color=color, column=column)
            if column in (Column.CIF, Column.DATA):
                textedit.setUneditable()

        if color:
            widget = self.indexWidget(idx)
            if widget and hasattr(widget, 'setBackground'):
                widget.setBackground(color)

        # Keep model data in sync
        self._model.set_cell_text(row, column, txt)
        if color:
            self._model.set_cell_color(row, column, color)

    def getText(self, row: int, col: int) -> str:
        return self.text(row, col)

    def text(self, row: int, column: int) -> str:
        """Returns the text from a cell, trying widget first, then model."""
        idx = self._model.index(row, column)
        widget = self.indexWidget(idx)
        if widget:
            if hasattr(widget, 'toPlainText'):
                txt = widget.toPlainText()
                if txt:
                    return txt
            if hasattr(widget, 'currentText'):
                txt = widget.currentText()
                if txt:
                    return txt
        return self._model.get_cell_text(row, column)

    def getTextFromKey(self, key: str, col: int) -> str:
        """Get text from field by CIF keyword."""
        row = self._model.row_from_key(key)
        return self.text(row, col)

    def row_from_key(self, key: str) -> int:
        return self._model.row_from_key(key)

    def widget_from_key(self, key: str, column: int) -> QWidget | None:
        row = self._model.row_from_key(key)
        return self.cellWidget(row, column)

    def vheader_text(self, row: int) -> str:
        header = self._model.headerData(row, Qt.Orientation.Vertical)
        return str(header) if header else ''

    # ---- Search ----

    def search(self, searchtext: str) -> None:
        """Filter rows by regex search against CIF keywords."""
        if not searchtext:
            for row in range(self._model.rowCount()):
                self.setRowHidden(row, False)
            return
        searchtext = searchtext.replace('.', '_')
        searchpattern = re.compile(f'.*{searchtext}.*', re.IGNORECASE)
        keys = self._model.vheaderitems
        searched = {x for x in keys if searchpattern.match(x)}
        for row in range(self._model.rowCount()):
            self.setRowHidden(row, keys[row] not in searched)

    # ---- Content management ----

    def delete_content(self) -> None:
        """Delete all content in the table."""
        self._model.clear_all()

    def delete_row(self, row: int | None = None) -> None:
        """Delete a row by index."""
        if row is None:
            row = self.currentRow()
        if row < 0 or row >= self._model.rowCount():
            return
        key = self._model.remove_row(row)
        if key:
            self.row_deleted.emit(key)

    def _delete_current_row(self) -> None:
        """Delete the currently selected row (Ctrl+Del shortcut)."""
        row = self.currentRow()
        if row >= 0:
            self.delete_row(row)

    def add_separation_line(self, row_num: int) -> None:
        """Mark the row at row_num as a separator line."""
        self._model.set_separator(row_num)
        # Place separator widgets to get the visual cross pattern
        for col in range(3):
            idx = self._model.index(row_num, col)
            sep = SeparatorWidget(self)
            self.setIndexWidget(idx, sep)
        self.resizeRowToContents(row_num)

    def add_property_combobox(self, data: list, row_num: int, key: str) -> None:
        """Adds a MyComboBox to the EDIT column with property values."""
        combobox = MyComboBox(self)
        combobox.cif_key = key
        combobox.textTemplate.connect(self.goto_template_page)
        self.setCellWidget(row_num, Column.EDIT, combobox)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        for num, value in data:
            try:
                combobox.addItem(retranslate_delimiter(value), num)
            except TypeError:
                print('Bad value in property:', value)
                if DEBUG:
                    raise
                continue
        combobox.setCurrentIndex(0)

    # ---- Navigation ----

    def goto_template_page(self, row: int) -> None:
        self.setCurrentCell(row, Column.EDIT)
        self.textTemplate.emit(self.currentRow())

    # ---- Vertical header help ----

    def vheader_section_click(self, section: int) -> None:
        from finalcif.cif.all_cif_dicts import cif_all_dict
        keys = self._model.vheaderitems
        if section >= len(keys):
            return
        itemtext = keys[section]
        keyword_help = cif_all_dict.get(itemtext, None)
        if keyword_help:
            keyword_help = retranslate_delimiter(keyword_help, no_html_unescape=True)
            show_keyword_help(self._parent, keyword_help, itemtext)
        elif itemtext.startswith('_vrf_'):
            helptxt = ('<pre><h2>Validation Response Form (VRF)</h2>\n'
                       'The Validation Response Form is supplied in the checkCIF report for '
                       'problems that have triggered Alerts. It '
                       'provides a field for the author to respond to the alert. '
                       'The response is clearly visible to the review process. \n'
                       'Usually, only level A or B alerts need a VRF.')
            show_keyword_help(self._parent, helptxt, itemtext)
        else:
            show_keyword_help(self._parent, 'No help available for this key.', '')

    # ---- Clipboard ----

    def copy_vhead_item(self) -> None:
        row = self.currentRow()
        keys = self._model.vheaderitems
        if 0 <= row < len(keys):
            clipboard = QApplication.clipboard()
            clipboard.setText(keys[row])

    def copy_item(self) -> None:
        idx = self.currentIndex()
        if idx.isValid():
            txt = self.text(idx.row(), idx.column())
            clipboard = QApplication.clipboard()
            clipboard.setText(txt)

    # ---- Column distribution ----

    def distribute_cif_main_table_columns_evenly(self) -> None:
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(Column.CIF, QHeaderView.ResizeMode.Stretch)
        hheader.setSectionResizeMode(Column.DATA, QHeaderView.ResizeMode.Stretch)
        hheader.setSectionResizeMode(Column.EDIT, QHeaderView.ResizeMode.Stretch)
        hheader.setAlternatingRowColors(True)
        self.verticalHeader().setAlternatingRowColors(True)

    # ---- Event handling ----

    def eventFilter(self, widget: QObject, event: QEvent):
        """Event filter for Tab/Shift+Tab navigation between rows."""
        if event.type() == QEvent.Type.KeyRelease and event.key() == QtCore.Qt.Key.Key_Backtab:
            row = self.currentRow()
            if row > 0:
                self.setCurrentCell(row - 1, 2)
            return True
        if event.type() == QEvent.Type.KeyRelease and event.key() == QtCore.Qt.Key.Key_Tab:
            row = self.currentRow()
            self.setCurrentCell(row, 2)
            return True
        if event.type() == QEvent.Type.Wheel:
            pass
        return QObject.eventFilter(self, widget, event)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        QtCore.QTimer(self).singleShot(0, self.resizeRowsToContents)
        super().resizeEvent(e)


class _VHeaderItemsProxy:
    """A mutable list-like proxy so that ``table.vheaderitems`` behaves like
    the old ``list[str]`` attribute but is backed by the model.

    Supports: indexing, ``in``, ``.index()``, ``.insert()``, ``.clear()``,
    ``len()``, ``del``, iteration, and max(…, key=len).
    """

    def __init__(self, model: CifTableModel, view: CifTableView):
        self._model = model
        self._view = view

    def __getitem__(self, index):
        return self._model.vheaderitems[index]

    def __len__(self):
        return len(self._model.vheaderitems)

    def __contains__(self, item):
        return item in self._model.vheaderitems

    def __iter__(self):
        return iter(self._model.vheaderitems)

    def index(self, key: str) -> int:
        return self._model.row_from_key(key)

    def insert(self, position: int, key: str) -> None:
        """Record the key so the next ``insertRow()`` can use it."""
        self._view._pending_key = key

    def clear(self) -> None:
        """Clearing is handled by model.clear_all() in delete_content()."""
        pass


class _FakeItem:
    """Lightweight compatibility object returned by ``item(row, col)``
    so that existing code like ``item.text()``, ``item.background()`` and
    ``item.setUneditable()`` still works without a real QTableWidgetItem.
    """

    def __init__(self, model: CifTableModel, row: int, col: int):
        self._model = model
        self._row = row
        self._col = col

    def text(self) -> str:
        return self._model.get_cell_text(self._row, self._col)

    def data(self, role=0) -> str:
        return self._model.get_cell_text(self._row, self._col)

    def background(self) -> QBrush:
        row_data = self._model.get_row_data(self._row)
        if row_data:
            if row_data.is_separator:
                brush = QBrush(blue)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                return brush
            color = None
            if self._col == 0:
                color = row_data.cif_color
            elif self._col == 1:
                color = row_data.data_color
            elif self._col == 2:
                color = row_data.edit_color
            if color:
                return QBrush(color)
        return QBrush()

    def setBackground(self, brush: QBrush) -> None:
        self._model.set_cell_color(self._row, self._col, brush.color() if brush else None)

    def setUneditable(self) -> None:
        pass

    def flags(self):
        return self._model.flags(self._model.index(self._row, self._col))

    def setFlags(self, flags):
        pass


class _FakeHeaderItem:
    """Compatibility object returned by ``verticalHeaderItem(section)``."""

    def __init__(self, model: CifTableModel, section: int):
        self._model = model
        self._section = section

    def text(self) -> str:
        header = self._model.headerData(self._section, Qt.Orientation.Vertical)
        return str(header) if header else ''

    def background(self) -> QBrush:
        row_data = self._model.get_row_data(self._section)
        if row_data and row_data.is_separator:
            brush = QBrush(blue)
            brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
            return brush
        return QBrush()
