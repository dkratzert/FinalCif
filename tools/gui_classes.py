from PyQt5.QtCore import Qt, QEvent
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

    def focusNextPrevChild(self, next: bool):
        # check if current column is the editable column
        if self.currentItem:
            currentColumn = self.currentColumn()
        else:
            currentColumn = -1
        if self.tabKeyNavigation() or currentColumn == 2:
            # Qt::Key_Down instead of Qt::Key_Tab and Qt::Key_Up instead of Qt::Key_Backtab
            self.keyPressEvent(QEvent.KeyPress, Qt.Key_Down)
            #if (event.isAccepted())
            return True
        return QTableWidget.focusNextPrevChild(next)
