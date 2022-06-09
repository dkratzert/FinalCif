from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QTableWidget

from finalcif.cif.text import retranslate_delimiter
from finalcif.gui.mixins import ItemTextMixin
from finalcif.gui.plaintextedit import PlainTextEditTemplate


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
        key_item = PlainTextEditTemplate(parent=self)
        key_item.setPlainText(key_text)
        # This is critical, because otherwise the add_row_if_needed does not work as expected:
        key_item.textChanged.connect(self.add_row_if_needed)
        self.setCellWidget(row_num, 0, key_item)
        tab_item = PlainTextEditTemplate(self)
        tab_item.textChanged.connect(lambda: self.resizeRowsToContents())
        tab_item.setPlainText(retranslate_delimiter(value_text))
        self.setCellWidget(row_num, 1, tab_item)

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
