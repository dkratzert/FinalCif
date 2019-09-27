from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QColor, QPalette, QTextOption
from PyQt5.QtWidgets import QAbstractScrollArea, QComboBox, QFrame, QPlainTextEdit, QSizePolicy, QTableWidget, \
    QTableWidgetItem, QWidget

from cif.cif_file_io import retranslate_delimiter

light_green = QColor(217, 255, 201)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)

# noinspection PyUnresolvedReferences
class ItemTextMixin:

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


class MyCifTable(QTableWidget, ItemTextMixin):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

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

    def adjustToContents(self):
        pass

    def setText(self, row, column, txt):
        """
        Set text in current table cell regardless of the containing item.
        """
        self.setCurrentCell(row, column)
        item = self.currentItem()
        if item:
            item.setText(txt)
        else:
            try:
                # in this case, we have a combobox
                self.cellWidget(row, column).setText(txt)
            except AttributeError:
                pass

    def setBackground(self, row: int, column: int, color: QColor):
        self.setCurrentCell(row, column)
        item = self.currentItem()
        if item:
            item.setBackground(color)
        else:
            widget = self.cellWidget(row, column)
            if widget:
                widget.setBackground(color)


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
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

    def setBackground(self, color):
        """
        Set background color of the text field.
        """
        self.setStyleSheet("QPlainTextEdit {{background-color: {};}}".format(str(color.name())))
        # No idea why tis does not work
        #pal = self.palette()
        #pal.setColor(QPalette.Base, color)
        #self.setPalette(pal)

    def set_uneditable(self):
        self.setReadOnly(True)

    def setText(self, text: str):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        txtlst = text.split(r'\n')
        # special treatment for text fields in order to get line breaks:
        for txt in txtlst:
            self.setPlainText(txt)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)


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
        if event.type() == QEvent.Wheel:  # and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def set_uneditable(self):
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def setText(self, txt: str):
        self.setEditText(txt)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_uneditable(self):
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)


class MyEQTableWidget(QTableWidget, ItemTextMixin):
    """
    A table widget for the equipment list.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWordWrap(QTextOption.WrapAtWordBoundaryOrAnywhere)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        """
        return QObject.eventFilter(self, widget, event)

    def add_row_if_needed(self):
        rowcount = self.rowCount()
        cont = 0
        for row in range(rowcount):
            key = ''
            try:
                key = self.text(row, 0)
            except (AttributeError, TypeError) as e:
                pass
                # print(e)
            if key:  # don't count empty key rows
                cont += 1
        diff = rowcount - cont
        if diff < 2:
            self.add_equipment_row()

    def add_equipment_row(self, key_text: str = '', value_text: str = ''):
        """
        Add a new row with content to the table (Equipment or Property).
        """
        if not isinstance(value_text, str):
            return
        if not isinstance(key_text, str):
            return
        # Create a empty row at bottom of table
        row_num = self.rowCount()
        self.insertRow(row_num)
        key_item = MyQPlainTextEdit(self)
        key_item.setPlainText(key_text)
        # This is critical, because otherwise the add_row_if_needed does not work as expected:
        key_item.textChanged.connect(self.add_row_if_needed)
        self.setCellWidget(row_num, 0, key_item)
        # if len(value) > 38:
        tab_item = MyQPlainTextEdit(self)
        tab_item.setPlainText(retranslate_delimiter(value_text))
        self.setCellWidget(row_num, 1, tab_item)

    def adjustToContents(self):
        # print('adjust')
        self.resizeRowsToContents()



