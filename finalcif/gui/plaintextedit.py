from enum import IntEnum
from typing import TYPE_CHECKING

from qtpy import QtCore, QtGui
from qtpy.QtCore import Signal, Qt, QObject, QEvent, QSize
from qtpy.QtGui import QTextOption, QFontMetrics, QContextMenuEvent, QFont, QColor
from qtpy.QtWidgets import QPlainTextEdit, QFrame, QAbstractScrollArea, QWidget

from finalcif.gui.edit_button import FloatingButtonWidget
from finalcif.gui.new_key_dialog import NewKey
from finalcif.gui.validators import validators

if TYPE_CHECKING:
    from finalcif.gui.custom_classes import MyCifTable

light_red = QColor(254, 191, 189)


class Column(IntEnum):
    CIF = 0
    DATA = 1
    EDIT = 2


class MyQPlainTextEdit(QPlainTextEdit):
    """
    A special plaintextedit with convenient methods to set the background color and other things.
    """
    templateRequested = Signal(int)
    new_key = Signal(str)
    to_be_shortened = {'_shelx_hkl_file', '_shelx_res_file', '_shelx_fab_file', '_shelx_fcf_file',
                       '_iucr_refine_instructions_details', '_iucr_refine_fcf_details'}

    def __init__(self, parent=None, *args):
        """
        Plaintext edit field for most of the table cells.
        """
        super().__init__(parent, *args)
        self.color = None
        self.cif_key = ''
        self.edit_button = None
        self.default_palette = self.palette()
        # self.increse_font_size()
        self.parent: MyCifTable = parent
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.textChanged.connect(lambda: self.parent.resizeRowToContents(self.row))

    def increse_font_size(self):
        font = QFont()
        font.setPointSize(self.document().defaultFont().pointSize() + 1)
        self.setFont(font)

    def __str__(self):
        return self.toPlainText()

    @property
    def fontmetric(self):
        return QFontMetrics(self.document().defaultFont())

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.createStandardContextMenu(event.pos())
        action_copy_vhead = menu.addAction("Copy CIF Keyword")
        deleterow = menu.addAction("Delete Row")
        menu.addSeparator()
        action_template = menu.addAction("Text Template")
        new_key = menu.addAction('Add new CIF keys')
        action_copy_vhead.triggered.connect(self.copy_vhead_item)
        action_template.triggered.connect(self._on_create_template)
        deleterow.triggered.connect(self._delete_row)
        new_key.triggered.connect(self._add_cif_keys)
        menu.exec(event.globalPos())

    def _add_cif_keys(self) -> None:
        new_key = NewKey(self)
        new_key.show()
        new_key.new_key_added.connect(lambda x: self.new_key.emit(x))

    def _on_create_template(self) -> None:
        self.templateRequested.emit(self.row)

    def _delete_row(self) -> None:
        self.parent.delete_row(self.row)

    def copy_vhead_item(self, row):
        """
        Copies the content of a field.
        """
        from qtpy import QtWidgets
        if hasattr(self.parent, 'vheaderitems'):
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self.cif_key)

    @property
    def row(self) -> int:
        return self.parent.indexAt(self.pos()).row()

    @property
    def column(self) -> int:
        return self.parent.indexAt(self.pos()).column()

    def setBackground(self, color: QColor) -> None:
        """
        Set background color of the text field.
        """
        # self.setStyleSheet("background-color: {};".format(str(color.name())))
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Base, color)
        #palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, color)
        self.setPalette(palette)
        self.default_palette = palette

    def getBackgroundColor(self) -> QtGui.QColor:
        palette = self.palette()
        background_color = palette.color(QtGui.QPalette.ColorRole.Base)
        return background_color

    def setUneditable(self):
        self.setReadOnly(True)

    def setText(self, text: str, color: QColor = None, column: int | None = None):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        if color:
            self.setBackground(color)
        if not text:
            return
        if column == Column.CIF and self.cif_key in self.to_be_shortened:
            self.setPlainText(f'{text[:300]} [...]')
        else:
            self.setPlainText(text)

    def eventFilter(self, widget: QWidget, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Type.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.edit_button and self.column == Column.EDIT:
            self.edit_button.update_position()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        if self.column == Column.EDIT:
            if not self.edit_button:
                self.edit_button = FloatingButtonWidget(parent=self)
                self.edit_button.floatingButtonClicked.connect(self._on_create_template)
                self.edit_button.update_position()
            self.edit_button.show()

    def event(self, e: QtCore.QEvent):
        if e.type() == QtCore.QEvent.Type.InputMethodQuery:
            self.parent.setCurrentCell(self.row, self.column)
        return super().event(e)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super().keyPressEvent(event)
        if self.column == Column.EDIT:
            self.validate_text(self.toPlainText())

    def validate_text(self, text: str):
        validator = validators.get(self.cif_key, None)
        if validator and not validator.valid(text):
            self.setBadStyle()
            self.setToolTip(validator.help_text)
        else:
            self.setToolTip('')
            self.setRegularStyle()

    def setBadStyle(self) -> None:
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Base, light_red)
        self.setPalette(palette)

    def setRegularStyle(self) -> None:
        self.setPalette(self.default_palette)

    def leaveEvent(self, a0: QEvent) -> None:
        super().leaveEvent(a0)
        if self.edit_button and self.column == Column.EDIT:
            self.edit_button.hide()

    def getText(self):
        return self.toPlainText()

    def sizeHint(self) -> QSize:
        """Text field sizes are scaled to text length"""
        max_size = QSize(100, 350)
        if len(self.toPlainText()) > 500:
            return max_size
        rect = self.fontmetric.boundingRect(self.contentsRect(), Qt.TextFlag.TextWordWrap, self.toPlainText())
        size = QSize(100, rect.height() + 14)
        if size.height() > 50:
            size = QSize(100, rect.height() + 24)
        if size.height() > 350:
            # Prevent extreme height for long text:
            size = max_size
        return size


class PlainTextEditTemplate(QPlainTextEdit):
    """
    A special plaintextedit for equipment and properties.
    """
    templateRequested = Signal(int)

    def __init__(self, parent=None, *args, **kwargs):
        """
        Plaintext edit field for most of the table cells.
        :param parent:
        :param minheight: minimum height of the widget.
        """
        super().__init__(parent, *args, **kwargs)
        self.cif_key = ''
        self.parent = parent
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.fontmetric = QFontMetrics(self.document().defaultFont())
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.textChanged.connect(lambda: self.parent.resizeRowsToContents())

    def setText(self, text: str, color=None):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        if color:
            self.setBackground(color)
        self.setPlainText(text)

    def eventFilter(self, widget: QWidget, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Type.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def getText(self):
        return self.toPlainText()

    def sizeHint(self) -> QSize:
        """Text field sizes are scaled to text length"""
        rect = self.fontmetric.boundingRect(self.contentsRect(), Qt.TextFlag.TextWordWrap, self.toPlainText())
        size = QSize(100, rect.height() + 14)
        if size.height() > 300:
            # Prevent extreme height for long text:
            size = QSize(100, 300)
        return size


if __name__ == '__main__':
    import sys
    import random
    from qtpy.QtWidgets import QApplication, QTableWidget

    app = QApplication(sys.argv)
    window = QTableWidget()
    window.setColumnCount(3)
    window.setRowCount(10)
    # stretch the last table colum:
    window.horizontalHeader().setStretchLastSection(True)
    window.setHorizontalHeaderLabels(['CIF', 'Data', 'Edit'])
    for row in range(10):
        for col in range(3):
            window.setCellWidget(row, col, MyQPlainTextEdit(window))
            w = window.cellWidget(row, col)
            if col == 2:
                w.setText(f'Hello World {random.randint(0, 10000)} {random.randint(0, 10000)}')
            w.setMinimumHeight(50)
            w.setMinimumWidth(150)
    window.resizeRowsToContents()
    window.resizeColumnsToContents()
    window.show()
    window.setMinimumSize(600, 400)

    sys.exit(app.exec())
