from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QTableWidget


class MyTableWidget(QTableWidget):

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Tab:
            self.setCurrentCell(self.currentRow(), 2)
            return
        super().keyPressEvent(event)
