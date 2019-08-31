from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QCursor
from PyQt5.QtWidgets import QTableWidget


class MyTableWidget(QTableWidget):
    """
    TODO: I think I have to subclass QPlainTextEdit also to get the correct behavior for the text fields
    """

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Tab:
            cursu = QCursor()
            #self.setCurrentCell(self.currentRow()+1, 1)
            self.setCurrentCell(self.currentRow(), 2)
            print(self.currentIndex().row())
            return
        super().keyPressEvent(event)

