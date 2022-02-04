from PyQt5.QtWidgets import QTableWidget

from finalcif.gui.plaintextedit import MyQPlainTextEdit


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