from contextlib import suppress
from textwrap import wrap

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QColor, QTextOption, QKeySequence, QContextMenuEvent
from PyQt5.QtWidgets import QAbstractScrollArea, QAction, QComboBox, QFrame, QPlainTextEdit, QSizePolicy, QTableWidget, \
    QTableWidgetItem, QWidget, QApplication, QShortcut

from cif.text import retranslate_delimiter
from tools.misc import essential_keys, text_field_keys

light_green = QColor(217, 255, 201)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)  # #faf796

[COL_CIF,
 COL_DATA,
 COL_EDIT
 ] = range(3)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        # gives a black line:
        # self.setFrameShadow(QFrame.Plain)
        self.setFrameShadow(QFrame.Raised)


# noinspection PyUnresolvedReferences
class ItemTextMixin:

    def text(self, row: int, column: int) -> str:
        """
        Returns the text inside a table cell.
        """
        try:
            txt = self.item(row, column).text()
        except AttributeError:
            txt = ''
        if not txt:
            try:
                txt = self.item(row, column).data(0)
            except AttributeError:
                txt = ''
        if not txt:
            try:
                # for QPlaintextWidgets:
                txt = self.cellWidget(row, column).toPlainText()
            except AttributeError:
                txt = ''
        if not txt:
            # for comboboxes:
            try:
                txt = self.cellWidget(row, column).currentText()
            except AttributeError:
                txt = ''
        return txt


class MyCifTable(QTableWidget, ItemTextMixin):
    row_deleted = QtCore.pyqtSignal(str)

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #item = MyTableWidgetItem()
        self.setItemPrototype(MyTableWidgetItem())
        self.actionDeletePair = QAction("Delete Row", self)
        self.actionCopy = QAction("Copy", self)
        self.actionCopyVhead = QAction("Copy CIF Keyword", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.actionDeletePair)
        self.addAction(self.actionCopy)
        self.addAction(self.actionCopyVhead)
        self.actionDeletePair.triggered.connect(self.delete_row)
        self.actionCopy.triggered.connect(self.copy_item)
        self.actionCopyVhead.triggered.connect(self.copy_vhead_item)
        del_shortcut = QShortcut(QKeySequence('Ctrl+Del'), self)
        del_shortcut.activated.connect(self.delete_row)
        self.vheaderitems = list()
        # This is the index number of the vheader that got clicked last:
        self.vheader_clicked = -1
        # vertical header click:
        vheader = self.verticalHeader()
        vheader.setSectionsClickable(True)
        # noinspection PyUnresolvedReferences
        vheader.sectionClicked.connect(self.vheader_section_click)

    def setCellWidget(self, row: int, column: int, widget) -> None:
        widget.row = row
        if (column == COL_CIF) or (column == COL_DATA):
            widget.setUneditable()
        super(MyCifTable, self).setCellWidget(row, column, widget)

    @property
    def rows_count(self):
        return self.model().rowCount()

    @property
    def columns_count(self):
        return self.model().columnCount()

    def delete_content(self):
        """
        Deletes all content in the table.
        """
        self.setRowCount(0)
        # This deletes the header text and sets 1, 2, 3!!!
        # self.ui.cif_main_table.clear()
        self.clearContents()
        self.vheaderitems.clear()

    def vheader_section_click(self, section):
        item = self.verticalHeaderItem(section)
        itemtext = item.text()
        # be sure not to get vheader with name of last click:
        if section != self.vheader_clicked and self.vheader_clicked > -1:
            self.restore_vertical_header()
            self.vheader_clicked = -1
            return
            # get back previous name
        if self.vheader_clicked > -1:
            item.setText(self.vheaderitems[self.vheader_clicked])
            self.vheader_clicked = -1
            return
        try:
            txt = essential_keys[itemtext]
            if txt:
                # item.setText('\n'.join(wrap(txt, 20)))
                item.setText(txt)
            self.vheader_clicked = section
            return
        except KeyError:
            pass

    def restore_vertical_header(self):
        for row_num, key in enumerate(self.vheaderitems):
            item_key = MyTableWidgetItem(key)
            self.setVerticalHeaderItem(row_num, item_key)

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
        if event.type() == QEvent.Wheel:
            pass
        return QObject.eventFilter(self, widget, event)

    def setText(self, key: str, column: int, txt: str, row: int = None):
        """
        Set text in current table cell regardless of the containing item.
        """
        txt = retranslate_delimiter(txt)
        if row is None:
            row = self.vheaderitems.index(key)
        self.setCurrentCell(row, column)
        item = self.currentItem()
        if item:
            item.setText(txt)
        else:
            if (key in text_field_keys) or (len(txt) > 60):
                textedit = MyQPlainTextEdit(self)
                self.setCellWidget(row, column, textedit)
                textedit.setText(txt)
                if (column == COL_CIF) or (column == COL_DATA):
                    textedit.setUneditable()
                return
            # in this case, we have a combobox
            if isinstance(self.cellWidget(row, column), MyComboBox):
                # noinspection PyUnresolvedReferences
                self.cellWidget(row, column).setText(txt)
            else:
                # No item in table cell:
                item = MyTableWidgetItem(txt)
                self.setItem(row, column, item)
        if (column == COL_CIF) or (column == COL_DATA):
            item.setUneditable()

    def getText(self, col: int, row: int):
        return self.text(row, col)

    def getTextFromKey(self, key: str, col: int):
        """
        Get text from field by cif keyword.
        :param key: CIF keyword like _chemical_formula_moiety
        :param col: column number to get text from.
        :return: text
        """
        row = self.vheaderitems.index(key)
        return self.text(row, col)

    def itemFromKey(self, key: str, col: int):
        """Returns the tableitem of the cell by key and column"""
        row = self.vheaderitems.index(key)
        return self.item(row, col)

    def setBackground(self, key: str, column: int, color: QColor):
        row = self.vheaderitems.index(key)
        self.setCurrentCell(row, column)
        item = self.currentItem()
        if item:
            item.setBackground(color)
        else:
            widget = self.cellWidget(row, column)
            if widget:
                with suppress(Exception):
                    widget.setBackground(color)

    def copy_vhead_item(self):
        """
        Copies the content of a field.
        """
        row = self.currentRow()
        clipboard = QApplication.clipboard()
        clipboard.setText(self.vheaderitems[row])

    def copy_item(self):
        """
        Copies the content of a field.
        """
        text = self.currentItem().text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def delete_row(self, row: int = None):
        """
        Deletes the current row, but gemmi can not delete items from the block at the moment!
        """
        if not row:
            row = self.currentRow()
        key = self.vheaderitems[row]
        del self.vheaderitems[row]
        self.removeRow(row)
        self.row_deleted.emit(key)

    def vheader_text(self, row):
        vhead = self.model().headerData(row, Qt.Vertical)
        return str(vhead)


class MyQPlainTextEdit(QPlainTextEdit):
    """
    A special plaintextedit with convenient methods to set the background color and other things.
    """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.row: int = -1
        self.parent: MyCifTable = parent
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setTabChangesFocus(True)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.createStandardContextMenu(event.pos())
        actionCopyVhead = menu.addAction("Copy CIF Keyword")
        deleterow = menu.addAction("Delete Row")
        actionCopyVhead.triggered.connect(self.copy_vhead_item)
        deleterow.triggered.connect(self._delete_row)
        choosedAction = menu.exec(event.globalPos())

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def copy_vhead_item(self, row):
        """
        Copies the content of a field.
        """
        row = self.parent.currentRow()
        clipboard = QApplication.clipboard()
        clipboard.setText(self.parent.vheaderitems[row])

    def setBackground(self, color):
        """
        Set background color of the text field.
        """
        self.setStyleSheet("QPlainTextEdit {{background-color: {};}}".format(str(color.name())))
        # No idea why tis does not work
        # pal = self.palette()
        # pal.setColor(QPalette.Base, color)
        # self.setPalette(pal)

    def setUneditable(self):
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
        # if event.type() == QEvent.MouseButtonPress:
        #    self.cell_clicked.emit(event.)
        return QObject.eventFilter(self, widget, event)


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: MyCifTable = parent
        self.row: int = -1
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setEditable(True)  # only editable as new template
        self.installEventFilter(self)
        self.actionDelete = QAction("Delete Row", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.actionDelete)
        self.actionDelete.triggered.connect(self._delete_row)

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel:  # and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def setUneditable(self):
        # noinspection PyUnresolvedReferences
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def setText(self, txt: str):
        self.setEditText('\n'.join(wrap(txt, width=30)))

    def addItem(self, *__args):
        text = '\n'.join(wrap(__args[0], width=60))
        super().addItem(text, __args[1])


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, parent=None, *args, **kwargs):
        # args and kwargs are essentiel here. Otherwise, the horizontal header text is missing!
        super().__init__(parent, *args, **kwargs)

    def setUneditable(self):
        # noinspection PyTypeChecker
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)
        # noinspection PyTypeChecker
        self.setFlags(self.flags() | Qt.ItemIsSelectable)


class MyEQTableWidget(QTableWidget, ItemTextMixin):
    """
    A table widget for the equipment list.
    """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
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
