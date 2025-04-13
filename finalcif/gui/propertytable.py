from PySide6.QtWidgets import QTableWidget, QWidget


class MyPropTableWidget(QTableWidget):
    """
    A table widget for the properties table.
    """

    def __init__(self, parent: QWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

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