import re
from enum import IntEnum
from typing import List

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QColor, QKeySequence, QBrush
from PyQt5.QtWidgets import QAbstractScrollArea, QTableWidget, \
    QTableWidgetItem, QWidget, QApplication, QShortcut, QHeaderView

from finalcif.cif.text import retranslate_delimiter
from finalcif.gui.combobox import MyComboBox
from finalcif.gui.dialogs import show_keyword_help
from finalcif.gui.mixins import ItemTextMixin
from finalcif.gui.plaintextedit import MyQPlainTextEdit

white = QColor(255, 255, 255)
light_green = QColor(217, 255, 201)
light_blue = QColor(220, 232, 247)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)  # #faf796


class Column(IntEnum):
    CIF = 0
    DATA = 1
    EDIT = 2
    BUTTON = 3


DEBUG = False


class MyCifTable(QTableWidget, ItemTextMixin):
    row_deleted = QtCore.pyqtSignal(str)
    textTemplate = QtCore.pyqtSignal(int)
    new_key = QtCore.pyqtSignal(str)

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setParent(parent)
        self.installEventFilter(self)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # item = MyTableWidgetItem()
        # self.setItemPrototype(item)
        del_shortcut = QShortcut(QKeySequence('Ctrl+Del'), self)
        del_shortcut.activated.connect(self.delete_row)
        self.vheaderitems: List[str] = []
        vheader = self.verticalHeader()
        vheader.setSectionsClickable(True)
        vheader.sectionClicked.connect(self.vheader_section_click)

    def setCellWidget(self, row: int, column: int, widget) -> None:
        widget.cif_key = self.vheaderitems[row]
        if (column == Column.CIF) or (column == Column.DATA):
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
        self.setCellWidget(row_num, Column.EDIT, combobox)
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

    def search(self, searchtext: str):
        # Clear current selection.
        self.setCurrentItem(None)
        if not searchtext:
            # Empty string, don't search and set all unhidden:
            for row in range(self.rowCount()):
                self.setRowHidden(row, False)
            return

        searchpattern = re.compile(f'.*{searchtext}.*', re.IGNORECASE)
        searched = [x for x in self.vheaderitems if searchpattern.match(x)]

        for row in range(self.rowCount()):
            if self.vheaderitems[row] in searched:
                self.setRowHidden(row, False)
            else:
                self.setRowHidden(row, True)

    def delete_content(self) -> None:
        """
        Deletes all content in the table.
        """
        self.setRowCount(0)
        # This deletes the header text and sets 1, 2, 3!!!
        # self.ui.cif_main_table.clear()
        self.clearContents()
        self.vheaderitems.clear()

    def vheader_section_click(self, section: int) -> None:
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
        self.setItem(row_num, Column.CIF, item1)
        self.setItem(row_num, Column.DATA, item2)
        self.setItem(row_num, Column.EDIT, item3)
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
        if row is None and key in self.vheaderitems:
            row = self.vheaderitems.index(key)
        elif row is None and key not in self.vheaderitems:
            row = 0
            raise IndexError
        if isinstance(self.cellWidget(row, column), MyComboBox):
            self.cellWidget(row, column).setText(txt)
            return
        if isinstance(self.cellWidget(row, column), MyQPlainTextEdit):
            widget = self.cellWidget(row, column)
            widget.setText(txt, color=color)
            # setting the CIF key here is important for the finding of row e.g. for clipboard copy
            widget.cif_key = key
        else:
            textedit = MyQPlainTextEdit(self)
            textedit.cif_key = key
            textedit.templateRequested.connect(self.goto_template_page)
            textedit.new_key.connect(lambda x: self.new_key.emit(x))
            self.setCellWidget(row, column, textedit)
            textedit.setText(txt, color=color)
            if (column == Column.CIF) or (column == Column.DATA):
                textedit.setUneditable()
        if color:
            self.cellWidget(row, column).setBackground(color)

    def goto_template_page(self, row):
        self.setCurrentCell(row, Column.EDIT)
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

    def copy_vhead_item(self):
        """
        Copies the content of a field.
        """
        row = self.currentRow()
        print(row, self.vheaderitems[row], '#')
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

    def vheader_text(self, row: int) -> str:
        vhead = self.model().headerData(row, Qt.Vertical)
        return str(vhead)

    def distribute_cif_main_table_columns_evenly(self) -> None:
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(Column.CIF, QHeaderView.Stretch)
        hheader.setSectionResizeMode(Column.DATA, QHeaderView.Stretch)
        hheader.setSectionResizeMode(Column.EDIT, QHeaderView.Stretch)
        hheader.setAlternatingRowColors(True)
        self.verticalHeader().setAlternatingRowColors(True)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, *args, **kwargs):
        # args and kwargs are essential here. Otherwise, the horizontal header text is missing!
        super().__init__(*args, **kwargs)

    def setUneditable(self) -> None:
        # noinspection PyTypeChecker
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)
        # noinspection PyTypeChecker
        self.setFlags(self.flags() | Qt.ItemIsSelectable)
