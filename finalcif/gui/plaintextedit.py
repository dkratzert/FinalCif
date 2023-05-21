from contextlib import suppress
from functools import cache

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QEvent, QSize
from PyQt5.QtGui import QTextOption, QFontMetrics, QContextMenuEvent, QFont, QColor
from PyQt5.QtWidgets import QPlainTextEdit, QFrame, QApplication, QAbstractScrollArea

from finalcif.gui.new_key_dialog import NewKey

with suppress(ImportError):
    from finalcif.gui.custom_classes import MyCifTable


class MyQPlainTextEdit(QPlainTextEdit):
    """
    A special plaintextedit with convenient methods to set the background color and other things.
    """
    templateRequested = pyqtSignal(int)
    new_key = pyqtSignal(str)

    def __init__(self, parent=None, *args, **kwargs):
        """
        Plaintext edit field for most of the table cells.
        """
        super().__init__(parent, *args, **kwargs)
        self.setParent(parent)
        self.cif_key = ''
        font = QFont()
        font.setPointSize(self.document().defaultFont().pointSize() + 1)
        self.setFont(font)
        self.parent: 'MyCifTable' = parent
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WordWrap)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textChanged.connect(lambda: self.parent.resizeRowToContents(self.row))

    def __str__(self):
        return self.toPlainText()

    @property
    @cache
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

    def _add_cif_keys(self):
        new_key = NewKey(self)
        new_key.show()
        new_key.new_key_added.connect(lambda x: self.new_key.emit(x))

    def _on_create_template(self):
        self.templateRequested.emit(self.row)

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def copy_vhead_item(self, row):
        """
        Copies the content of a field.
        """
        if hasattr(self.parent, 'vheaderitems'):
            clipboard = QApplication.clipboard()
            clipboard.setText(self.cif_key)

    @property
    def row(self) -> int:
        return self.parent.vheaderitems.index(self.cif_key)

    def setBackground(self, color: QColor) -> None:
        """
        Set background color of the text field.
        """
        self.setStyleSheet("background-color: {};".format(str(color.name())))
        # No idea why this does not work
        # pal = self.palette()
        # pal.setColor(QPalette.Base, color)
        # self.setPalette(pal)

    def setUneditable(self):
        self.setReadOnly(True)

    def setText(self, text: str, color=None):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        if color:
            self.setBackground(color)
        self.setPlainText(text)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def getText(self):
        return self.toPlainText()

    def sizeHint(self) -> QSize:
        """Text field sizes are scaled to text length"""
        rect = self.fontmetric.boundingRect(self.contentsRect(), Qt.TextWordWrap, self.toPlainText())
        size = QSize(100, rect.height() + 14)
        if size.height() > 50:
            size = QSize(100, rect.height() + 24)
        if size.height() > 350:
            # Prevent extreme height for long text:
            size = QSize(100, 350)
        return size


class PlainTextEditTemplate(QPlainTextEdit):
    """
    A special plaintextedit for equipment and properties.
    """
    templateRequested = pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        """
        Plaintext edit field for most of the table cells.
        :param parent:
        :param minheight: minimum height of the widget.
        """
        super().__init__(parent, *args, **kwargs)
        self.setParent(parent)
        self.cif_key = ''
        self.parent = parent
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WordWrap)
        self.fontmetric = QFontMetrics(self.document().defaultFont())
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textChanged.connect(lambda: self.parent.resizeRowsToContents())

    def setText(self, text: str, color=None):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        if color:
            self.setBackground(color)
        self.setPlainText(text)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def getText(self):
        return self.toPlainText()

    def sizeHint(self) -> QSize:
        """Text field sizes are scaled to text length"""
        rect = self.fontmetric.boundingRect(self.contentsRect(), Qt.TextWordWrap, self.toPlainText())
        size = QSize(100, rect.height() + 14)
        if size.height() > 300:
            # Prevent extreme height for long text:
            size = QSize(100, 300)
        return size
