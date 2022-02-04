from contextlib import suppress
from textwrap import wrap
from typing import List

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, QObject, Qt, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QTextOption, QKeySequence, QContextMenuEvent, QBrush, QFontMetrics
from PyQt5.QtWidgets import QAbstractScrollArea, QAction, QComboBox, QFrame, QPlainTextEdit, QSizePolicy, QTableWidget, \
    QTableWidgetItem, QWidget, QApplication, QShortcut, QStackedWidget

from finalcif.cif.text import retranslate_delimiter
from finalcif.gui.dialogs import show_keyword_help

light_green = QColor(217, 255, 201)
light_blue = QColor(173, 216, 230)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)  # #faf796

[COL_CIF,
 COL_DATA,
 COL_EDIT
 ] = range(3)

DEBUG = False


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
    textTemplate = QtCore.pyqtSignal(int)

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)
        self.setParent(parent)
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        item = MyTableWidgetItem()
        self.setItemPrototype(item)
        self.actionDeletePair = QAction("Delete Row", self)
        self.actionCopy = QAction("Copy", self)
        self.actionCopyVhead = QAction("Copy CIF Keyword", self)
        self.templateAction = QAction("Text Template", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.actionDeletePair)
        self.addAction(self.actionCopy)
        self.addAction(self.actionCopyVhead)
        self.addAction(QAction('-----', self))
        self.addAction(self.templateAction)
        self.templateAction.triggered.connect(self.goto_template_page)
        self.actionDeletePair.triggered.connect(self.delete_row)
        self.actionCopy.triggered.connect(self.copy_item)
        self.actionCopyVhead.triggered.connect(self.copy_vhead_item)
        del_shortcut = QShortcut(QKeySequence('Ctrl+Del'), self)
        del_shortcut.activated.connect(self.delete_row)
        self.vheaderitems: list = []
        # This is the index number of the vheader that got clicked last:
        # vertical header click:
        vheader = self.verticalHeader()
        vheader.setSectionsClickable(True)
        # noinspection PyUnresolvedReferences
        vheader.sectionClicked.connect(self.vheader_section_click)

    # @cache
    # def _vheaderitems(self, row: int) -> str:
    #    return self.vheaderitems[row]

    def setCellWidget(self, row: int, column: int, widget) -> None:
        widget.cif_key = self.vheaderitems[row]
        if (column == COL_CIF) or (column == COL_DATA):
            # noinspection PyUnresolvedReferences
            widget.setUneditable()
        super(MyCifTable, self).setCellWidget(row, column, widget)

    @property
    def rows_count(self):
        return self.model().rowCount()

    @property
    def columns_count(self):
        return self.model().columnCount()

    def add_property_combobox(self, data: List, row_num: int, key: str) -> None:
        """
        Adds a QComboBox to the cif_main_table with the content of special_fields or property templates.
        """
        combobox = MyComboBox(self)
        combobox.cif_key = key
        combobox.textTemplate.connect(self.goto_template_page)
        # print('special:', row_num, miss_data)
        self.setCellWidget(row_num, COL_EDIT, combobox)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for num, value in data:
            try:
                combobox.addItem(retranslate_delimiter(value), num)
            except TypeError:
                print('Bad value in property:', value)
                if DEBUG:
                    raise
                continue
        combobox.setCurrentIndex(0)

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
        from finalcif.cif.all_cif_dicts import cif_all_dict
        item = self.verticalHeaderItem(section)
        itemtext = item.text()
        keyword_help = cif_all_dict.get(itemtext, None)
        if keyword_help:
            keyword_help = retranslate_delimiter(keyword_help, no_html_unescape=True)
            show_keyword_help(self.parent, keyword_help, itemtext)
        elif itemtext.startswith('_vrf_'):
            helptxt = '<pre><h2>Validation Response Form (VRF)</h2>\n' \
                      'The Validation Response Form is supplied in the checkCIF report for ' \
                      'problems that have triggered Alerts. It ' \
                      'provides a field for the author to respond to the alert. ' \
                      'The response is clearly visible to the review process. \n' \
                      'Usually, only level A or B alerts need a VRF.'
            show_keyword_help(self.parent, helptxt, itemtext)
        else:
            show_keyword_help(self.parent, 'No help available for this key.', '')

    def add_separation_line(self, row_num: int) -> None:
        """
        Adds a blue separation line between cif content and empty cif keywords.
        """
        # The blue line in the table:
        item_vhead = MyTableWidgetItem('These below are already in:')
        item1 = MyTableWidgetItem('')
        item2 = MyTableWidgetItem('')
        item3 = MyTableWidgetItem('')
        diag = QBrush(blue)
        diag.setStyle(Qt.DiagCrossPattern)
        item_vhead.setBackground(diag)
        item1.setBackground(diag)
        item1.setUneditable()
        item2.setBackground(diag)
        item2.setUneditable()
        item3.setBackground(diag)
        item3.setUneditable()
        self.setVerticalHeaderItem(row_num, item_vhead)
        self.setItem(row_num, COL_CIF, item1)
        self.setItem(row_num, COL_DATA, item2)
        self.setItem(row_num, COL_EDIT, item3)
        self.resizeRowToContents(row_num)

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

    def setText(self, key: str, column: int, txt: str, row: int = None, color=None):
        """
        Set text in current table cell regardless of the containing item.
        """
        txt = retranslate_delimiter(txt)
        if row is None:
            row = self.vheaderitems.index(key)
        if isinstance(self.cellWidget(row, column), MyComboBox):
            self.cellWidget(row, column).setText(txt)
            return
        # item = MyTableWidgetItem(txt)
        # self.setItem(row, column, item)
        #lentext = max([len(txt), len(self.getText(0, row)), len(self.getText(1, row))])
        # This is a regular table cell:
        # if not (key in text_field_keys) and (lentext < 35):
        #    item.setText(txt)
        #    if (column == COL_CIF) or (column == COL_DATA):
        #        # noinspection PyUnresolvedReferences
        #        item.setUneditable()
        #    if color:
        #        item.setBackground(color)
        # else:
        # This is a text field:
        if isinstance(self.cellWidget(row, column), MyQPlainTextEdit):
            self.cellWidget(row, column).setText(txt, color=color)
        else:
            textedit = MyQPlainTextEdit(self)
            textedit.cif_key = key
            textedit.templateRequested.connect(self.goto_template_page)
            self.setCellWidget(row, column, textedit)
            textedit.setText(txt, color=color)
            if (column == COL_CIF) or (column == COL_DATA):
                textedit.setUneditable()
        if color:
            self.cellWidget(row, column).setBackground(color)

    def goto_template_page(self, row):
        self.setCurrentCell(row, COL_EDIT)
        self.parent.parent().go_to_text_template_page()
        self.textTemplate.emit(self.currentRow())

    def getText(self, row: int, col: int):
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

    def row_from_key(self, key: str) -> int:
        return self.vheaderitems.index(key)

    def itemFromKey(self, key: str, col: int) -> QTableWidgetItem:
        """Returns the tableitem of the cell by key and column"""
        row = self.vheaderitems.index(key)
        return self.item(row, col)

    def widget_from_key(self, key: str, column: int) -> QWidget:
        row = self.vheaderitems.index(key)
        return self.cellWidget(row, column)

    """    
    def setBackground(self, key: str, column: int, color: QColor):
        row = self.vheaderitems.index(key)
        self.setCurrentCell(row, column)
        item = self.currentItem()
        if item:
            item.setBackground(color)
            if column == COL_DATA:
                item.setUneditable()
        else:
            widget = self.cellWidget(row, column)
            if widget:
                with suppress(Exception):
                    widget.setBackground(color)"""

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
    templateRequested = pyqtSignal(int)

    def __init__(self, parent=None, minheight: int = 80, *args, **kwargs):
        """
        Plaintext edit field for most of the table cells.
        :param parent:
        :param minheight: minimum height of the widget.
        """
        super().__init__(parent, *args, **kwargs)
        self.setParent(parent)
        self.cif_key = ''
        #self.minheight = minheight
        self.parent: MyCifTable = parent
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.fontmetric = QFontMetrics(self.document().defaultFont())
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def __str__(self):
        return self.toPlainText()

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.createStandardContextMenu(event.pos())
        action_copy_vhead = menu.addAction("Copy CIF Keyword")
        deleterow = menu.addAction("Delete Row")
        menu.addSeparator()
        action_template = menu.addAction("Text Template")
        action_copy_vhead.triggered.connect(self.copy_vhead_item)
        action_template.triggered.connect(self._on_create_template)
        deleterow.triggered.connect(self._delete_row)
        choosed_action = menu.exec(event.globalPos())

    def _on_create_template(self):
        self.templateRequested.emit(self.row)

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def copy_vhead_item(self, row):
        """
        Copies the content of a field.
        """
        if hasattr(self.parent, 'vheaderitems'):
            row = self.parent.currentRow()
            clipboard = QApplication.clipboard()
            clipboard.setText(self.parent.vheaderitems[row])

    @property
    def row(self) -> int:
        return self.parent.vheaderitems.index(self.cif_key)

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

    def setText(self, text: str, color=None):
        """
        Set text of a Plaintextfield with lines wrapped at newline characters.
        """
        if color:
            self.setBackground(color)
        txtlst = text.split(r'\n')
        # special treatment for text fields in order to get line breaks:
        for txt in txtlst:
            self.setPlainText(txt)
        self.textChanged.connect(lambda: self.parent.resizeRowsToContents())

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

    def getText(self):
        return self.toPlainText()

    def sizeHint(self) -> QSize:
        """Text field sizes are scaled to text length"""
        # if not self.getText().strip():
        #    return QSize(self.width(), self.minheight)
        # else:
        rect = self.fontmetric.boundingRect(self.contentsRect(), Qt.TextWordWrap, self.toPlainText())
        size =  QSize(100, rect.height() + 14)
        # if len(self.getText().splitlines()) < 4:
        #    size = QSize(100, int(0.5 * len(self.getText()) + 26))
        # else:
        #    size = QSize(self.width(), int(fm.height() * len(self.getText().splitlines()) + 3) + 16)
        # size = QSize(self.width(), int(15 * (len(self.getText().splitlines()) +
        #                                     (len(self.getText()) / 30)
        #                                     ) + 15))
        #
        if size.height() > 300:
            # Prevent extreme height for long text:
            size = QSize(100, 300)
        return size


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """
    textTemplate = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: MyCifTable = parent
        self.setParent(parent)
        self.cif_key = ''
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setEditable(True)  # only editable as new template
        self.installEventFilter(self)
        self.actionDelete = QAction("Delete Row", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.actionDelete)
        self.actionDelete.triggered.connect(self._delete_row)
        action_template = QAction("Text Template", self)
        self.addAction(action_template)
        action_template.triggered.connect(self._on_create_template)

    def __str__(self):
        return self.currentText()

    @property
    def row(self) -> int:
        return self.parent.vheaderitems.index(self.cif_key)

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def _on_create_template(self):
        self.textTemplate.emit(self.row)

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

    def __init__(self, *args, **kwargs):
        # args and kwargs are essential here. Otherwise, the horizontal header text is missing!
        super().__init__(*args, **kwargs)

    def setUneditable(self):
        # noinspection PyTypeChecker
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)
        # noinspection PyTypeChecker
        self.setFlags(self.flags() | Qt.ItemIsSelectable)


class MyEQTableWidget(QTableWidget, ItemTextMixin):
    """
    A table widget for the equipment list.
    """

    def __init__(self, parent: QTableWidget = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.setParent(parent)
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
        key_item = MyQPlainTextEdit(parent=self)
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

    def delete_row(self, row: int = None):
        if not row:
            row = self.currentRow()
        self.removeRow(row)
        self.set_row_numbers()

    def set_row_numbers(self):
        for row in range(self.rowCount()):
            self.setCurrentCell(row, 1)
            for col in range(self.columnCount()):
                try:
                    self.cellWidget(row, col).row = row
                except ValueError:
                    print('Row or Column of MyEQTableWidget does not exist.')


class MyPropTableWidget(QTableWidget):
    """
    A table widget for the properties table.
    """

    def __init__(self, parent: MyQPlainTextEdit, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

    def delete_row(self, row: int = None):
        if not row:
            row = self.currentRow()
        self.removeRow(row)
        # I need to set the row numbers again because one was deleted.
        self.set_row_numbers()

    def set_row_numbers(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.setCurrentCell(row, col)
                try:
                    self.cellWidget(row, col).row = row
                except ValueError:
                    print('Row or Column of MyEQTableWidget does not exist.')


class MyMainStackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setParent(parent)

    def got_to_main_page(self):
        self.setCurrentIndex(0)

    def go_to_cif_text_page(self):
        self.setCurrentIndex(1)

    def go_to_info_page(self):
        self.setCurrentIndex(2)

    def go_to_data_sources_page(self):
        self.setCurrentIndex(3)

    def go_to_options_page(self):
        self.setCurrentIndex(4)

    def go_to_loops_page(self):
        self.setCurrentIndex(5)

    def on_loops_page(self):
        return self.currentIndex() == 5

    def go_to_checkcif_page(self):
        self.setCurrentIndex(6)

    def got_to_cod_page(self):
        self.setCurrentIndex(7)

    def go_to_text_template_page(self):
        self.setCurrentIndex(8)

    @property
    def current_page(self):
        return self.currentIndex()

    def on_checkcif_page(self):
        return self.current_page == 6
