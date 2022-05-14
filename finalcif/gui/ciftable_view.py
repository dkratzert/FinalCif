from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor


class CifTableView(QtWidgets.QTableView):
    save_excel_triggered = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    """def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        context_menu = QtWidgets.QMenu(self)
        save_excel = context_menu.addAction("Save as Excel File")
        save_excel.triggered.connect(lambda: self._on_save_excel(event))
        context_menu.addAction(save_excel)
        context_menu.popup(QCursor.pos())

    def _on_save_excel(self, event: QtGui.QContextMenuEvent):
        self.save_excel_triggered.emit()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.RightButton:
            pass
        super().mousePressEvent(e)"""
