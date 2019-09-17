from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QComboBox, QFrame, QPlainTextEdit, QSizePolicy, QTableWidget, QWidget, QTableWidgetItem


class MyCifTable(QTableWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.installEventFilter(self)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter for tab down on third column.
        """
        if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Backtab:
            row = self.currentRow()
            if row > 0:
                self.setCurrentCell(row - 1, 2)
            return True
        if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Tab:
            row = self.currentRow()
            self.setCurrentCell(row, 2)
            return True
        return QObject.eventFilter(self, widget, event)

    def text(self, row: int, column: int) -> str:
        """
        Returns the text inside a table cell.
        """
        try:
            txt = self.item(row, column).text()
        except AttributeError:
            txt = None
        if not txt:
            try:
                txt = self.item(row, column).data(0)
            except AttributeError:
                txt = None
        if not txt:
            try:
                # for QPlaintextWidgets:
                txt = self.cellWidget(row, column).toPlainText()
            except AttributeError:
                txt = None
        if not txt:
            # for comboboxes:
            try:
                txt = self.cellWidget(row, column).currentText()
            except AttributeError:
                txt = None
        return txt


class MyQPlainTextEdit(QPlainTextEdit):
    """
    A special plaintextedit with convenient methods to set the background color and other things.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setTabChangesFocus(True)

    def setColor(self, color):
        pal = self.palette()
        pal.setColor(QPalette.Base, color)
        self.setPalette(pal)

    def set_uneditable(self):
        self.setReadOnly(True)


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setEditable(True)  # only editable as new template
        self.installEventFilter(self)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def set_uneditable(self):
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_uneditable(self):
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

