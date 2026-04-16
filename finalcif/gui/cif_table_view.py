from __future__ import annotations

import re

from qtpy import QtCore, QtGui
from qtpy.QtCore import QEvent, QObject, Qt
from qtpy.QtGui import QColor, QKeySequence, QBrush
from qtpy.QtWidgets import (
    QAbstractScrollArea, QTableView, QWidget, QApplication,
    QHeaderView, QStyledItemDelegate, QStyleOptionViewItem,
)

from finalcif.cif.text import retranslate_delimiter
from finalcif.gui.cif_table_model import CifTableModel, Column, blue
from finalcif.gui.combobox import MyComboBox
from finalcif.gui.dialogs import show_keyword_help
from finalcif.gui.plaintextedit import MyQPlainTextEdit

DEBUG = False


class SeparatorWidget(QWidget):
    """A simple widget that paints the blue diagonal cross pattern for the separator row."""

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QBrush(blue)
        brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
        painter.fillRect(self.rect(), brush)
        painter.end()


class CifTableDelegate(QStyledItemDelegate):
    """Delegate for painting separator rows and providing size hints."""

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
    """QTableView-based main CIF table, replacing MyCifTable(QTableWidget).

    Uses a :class:`CifTableModel` as its data store and persistent
    :class:`MyQPlainTextEdit` / :class:`MyComboBox` widgets placed via
    ``setIndexWidget()`` for each cell.
    """

    row_deleted = QtCore.Signal(str)
    textTemplate = QtCore.Signal(int)
    new_key = QtCore.Signal(str)

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent=parent)
        self._parent = parent
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        # Model & delegate
        self._model = CifTableModel(self)
        self.setModel(self._model)
        self.setItemDelegate(CifTableDelegate(self))

        # Visual config
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setShowGrid(True)
        self.setWordWrap(True)
        self.setSortingEnabled(False)

        # Shortcuts
        del_shortcut = QtGui.QShortcut(QKeySequence('Ctrl+Del'), self)
        del_shortcut.activated.connect(self._delete_current_row)

        # Vertical header
        vheader = self.verticalHeader()
        vheader.setSectionsClickable(True)
        vheader.sectionClicked.connect(self._vheader_section_click)

    # ------------------------------------------------------------------
    # Row / column counts
    # ------------------------------------------------------------------

    @property
    def rows_count(self) -> int:
        return self._model.rowCount()

    @property
    def columns_count(self) -> int:
        return self._model.columnCount()

    @property
    def vheaderitems(self) -> list[str]:
        """List of CIF keywords in row order."""
        return self._model.vheaderitems

    def rowCount(self) -> int:  # noqa: N802 – keep old name
        return self._model.rowCount()

    # ------------------------------------------------------------------
    # Row management
    # ------------------------------------------------------------------

    def add_row(self, key: str, position: int | None = None) -> int:
        """Insert a new row into the model. Returns the row index."""
        return self._model.add_row(key=key, position=position)

    def delete_row(self, row: int | None = None) -> None:
        if row is None:
            row = self.currentIndex().row()
        if row < 0 or row >= self._model.rowCount():
            return
        key = self._model.remove_row(row)
        if key:
            self.row_deleted.emit(key)

    def _delete_current_row(self) -> None:
        self.delete_row()

    def delete_content(self) -> None:
        """Remove all rows."""
        self._model.clear_all()

    def has_key(self, key: str) -> bool:
        return self._model.has_key(key)

    def row_from_key(self, key: str) -> int:
        return self._model.row_from_key(key)

    def add_separation_line(self, row_num: int) -> None:
        """Mark *row_num* as the blue diagonal-cross separator."""
        self._model.set_separator(row_num)
        for col in range(3):
            idx = self._model.index(row_num, col)
            self.setIndexWidget(idx, SeparatorWidget(self))
        self.resizeRowToContents(row_num)

    # ------------------------------------------------------------------
    # Cell widgets
    # ------------------------------------------------------------------

    def cellWidget(self, row: int, column: int) -> QWidget | None:
        return self.indexWidget(self._model.index(row, column))

    def setCellWidget(self, row: int, column: int, widget) -> None:
        keys = self._model.vheaderitems
        if row < len(keys):
            widget.cif_key = keys[row]
        if column in (Column.CIF, Column.DATA):
            widget.setUneditable()
        self.setIndexWidget(self._model.index(row, column), widget)

    def widget_from_key(self, key: str, column: int) -> QWidget | None:
        return self.cellWidget(self._model.row_from_key(key), column)

    # ------------------------------------------------------------------
    # Text access
    # ------------------------------------------------------------------

    def setText(self, key: str, column: int, txt: str,
                row: int | None = None, color: QColor | None = None) -> None:
        """Set text in a cell, creating a :class:`MyQPlainTextEdit` if needed."""
        if txt:
            txt = retranslate_delimiter(txt)

        if row is None:
            row = self._model.row_from_key(key)

        idx = self._model.index(row, column)
        existing = self.indexWidget(idx)

        if isinstance(existing, MyComboBox):
            existing.setText(txt)
            return

        if isinstance(existing, MyQPlainTextEdit):
            existing.setText(txt, color=color, column=column)
            existing.cif_key = key
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

        widget = self.indexWidget(idx)

        if color:
            if widget and hasattr(widget, 'setBackground'):
                widget.setBackground(color)

        # Keep model in sync — store the widget's actual display text so that
        # the delegate's sizeHint (which reads from the model) matches the
        # truncated content shown for large values like HKL files.
        if widget and hasattr(widget, 'toPlainText'):
            self._model.set_cell_text(row, column, widget.toPlainText())
        else:
            self._model.set_cell_text(row, column, txt)
        if color:
            self._model.set_cell_color(row, column, color)

        # Resize explicitly — widget signals are blocked during setText to avoid
        # per-keystroke resizes during programmatic population.
        # Skip when updates are disabled (bulk loading) — the caller resizes at the end.
        if self.updatesEnabled():
            self.resizeRowToContents(row)

    def text(self, row: int, column: int) -> str:
        """Read text from a cell, preferring the live widget content."""
        widget = self.indexWidget(self._model.index(row, column))
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

    def getText(self, row: int, col: int) -> str:  # noqa: N802
        return self.text(row, col)

    def getTextFromKey(self, key: str, col: int) -> str:  # noqa: N802
        return self.text(self._model.row_from_key(key), col)

    def vheader_text(self, row: int) -> str:
        h = self._model.headerData(row, Qt.Orientation.Vertical)
        return str(h) if h else ''

    # ------------------------------------------------------------------
    # Combobox helper
    # ------------------------------------------------------------------

    def add_property_combobox(self, data: list, row_num: int, key: str) -> None:
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

    # ------------------------------------------------------------------
    # Navigation / selection
    # ------------------------------------------------------------------

    def setCurrentCell(self, row: int, column: int) -> None:  # noqa: N802
        self.setCurrentIndex(self._model.index(row, column))

    def currentRow(self) -> int:  # noqa: N802
        return self.currentIndex().row()

    def goto_template_page(self, row: int) -> None:
        self.setCurrentCell(row, Column.EDIT)
        self.textTemplate.emit(self.currentRow())

    # ------------------------------------------------------------------
    # Search / filter
    # ------------------------------------------------------------------

    def search(self, searchtext: str) -> None:
        if not searchtext:
            for row in range(self._model.rowCount()):
                self.setRowHidden(row, False)
            return
        searchtext = searchtext.replace('.', '_')
        pattern = re.compile(f'.*{searchtext}.*', re.IGNORECASE)
        keys = self._model.vheaderitems
        matched = {k for k in keys if pattern.match(k)}
        for row in range(self._model.rowCount()):
            self.setRowHidden(row, keys[row] not in matched)

    # ------------------------------------------------------------------
    # Clipboard
    # ------------------------------------------------------------------

    def copy_vhead_item(self) -> None:
        row = self.currentIndex().row()
        keys = self._model.vheaderitems
        if 0 <= row < len(keys):
            QApplication.clipboard().setText(keys[row])

    # ------------------------------------------------------------------
    # Vertical header help
    # ------------------------------------------------------------------

    def _vheader_section_click(self, section: int) -> None:
        from finalcif.cif.all_cif_dicts import cif_all_dict
        keys = self._model.vheaderitems
        if section >= len(keys):
            return
        itemtext = keys[section]
        keyword_help = cif_all_dict.get(itemtext)
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

    # ------------------------------------------------------------------
    # Column layout
    # ------------------------------------------------------------------

    def distribute_cif_main_table_columns_evenly(self) -> None:
        hh = self.horizontalHeader()
        for col in (Column.CIF, Column.DATA, Column.EDIT):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        hh.setAlternatingRowColors(True)
        self.verticalHeader().setAlternatingRowColors(True)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def eventFilter(self, widget: QObject, event: QEvent):
        if event.type() == QEvent.Type.KeyRelease:
            if event.key() == QtCore.Qt.Key.Key_Backtab:
                row = self.currentIndex().row()
                if row > 0:
                    self.setCurrentCell(row - 1, 2)
                return True
            if event.key() == QtCore.Qt.Key.Key_Tab:
                self.setCurrentCell(self.currentIndex().row(), 2)
                return True
        return QObject.eventFilter(self, widget, event)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        QtCore.QTimer(self).singleShot(0, self.resizeRowsToContents)
        super().resizeEvent(e)
