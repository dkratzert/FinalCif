from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem, QItemEditorFactory, QHeaderView
from finalcif.gui.plaintextedit import MyQPlainTextEdit
from finalcif.gui.table_model import Column

"""
textedit = MyQPlainTextEdit(self)
            textedit.cif_key = key
            textedit.templateRequested.connect(self.goto_template_page)
            self.setCellWidget(row, column, textedit)
            textedit.setText(txt, color=color)
"""


class CifItemEditor(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        return MyQPlainTextEdit(parent)

    # def itemEditorFactory(self) -> QItemEditorFactory:
    #    factory = QItemEditorFactory()
    #    factory.registerEditor(Qt.EditRole, )


class CifTableView(QtWidgets.QTableView):
    save_excel_triggered = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        delegate = CifItemEditor(self)
        self.setItemDelegate(delegate)
        # self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        context_menu = QtWidgets.QMenu(self)
        save_excel = context_menu.addAction("Save as Excel File")
        save_excel.triggered.connect(lambda: self._on_save_excel(event))
        context_menu.addAction(save_excel)
        context_menu.popup(QCursor.pos())

    def changeEvent(self, a0: QtCore.QEvent) -> None:
        self.resizeRowsToContents()
        print('changeevent')
        # self._on_data_changed()
        super().changeEvent(a0)

    def _on_save_excel(self, event: QtGui.QContextMenuEvent):
        self.save_excel_triggered.emit()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.RightButton:
            pass
        super().mousePressEvent(e)
