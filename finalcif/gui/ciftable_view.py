from typing import Iterable

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem, QHeaderView

from finalcif.gui.plaintextedit import MyQPlainTextEdit

"""
textedit = MyQPlainTextEdit(self)
            textedit.cif_key = key
            textedit.templateRequested.connect(self.goto_template_page)
            self.setCellWidget(row, column, textedit)
            textedit.setText(txt, color=color)
"""


class CifItemEditor(QtWidgets.QStyledItemDelegate):
    text_changed = pyqtSignal(object)

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

    # def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
    #    return MyQPlainTextEdit(parent)
    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        text = index.model().data(index, Qt.EditRole)
        #if len(text) > 20:
        editor = MyQPlainTextEdit(parent)
        #editor = QtWidgets.QPlainTextEdit(parent)
        return editor

    """def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> bool:
        print(event, index.row())
        self.text_changed.emit(index)
        return super().editorEvent(event, model, option, index)"""

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.EditRole)
        if isinstance(editor, QtWidgets.QPlainTextEdit):
            editor.setPlainText(text)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QtWidgets.QPlainTextEdit):
            model.setData(index, editor.toPlainText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    """def updateEditorGeometry(self, editor: MyQPlainTextEdit, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex):
        print(editor.toPlainText())
        print(editor.sizeHint())
        editor.setGeometry(option.rect)"""

    # def itemEditorFactory(self) -> QItemEditorFactory:
    #    factory = QItemEditorFactory()
    #    factory.registerEditor(Qt.EditRole, MyQPlainTextEdit)
    #    return factory

    # def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
    #    editor.setPlainText(index.data(role=Qt.EditRole))

    """def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        print(editor)
        print(option)
        pass"""

    # def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
    #    print(editor, model)
    #    pass
    def displayText(self, value, locale: QtCore.QLocale) -> str:
        #self.parent.resizeRowToContents(self.parent.currentIndex().row())
        return super().displayText(value, locale)

class CifTableView(QtWidgets.QTableView):
    save_excel_triggered = pyqtSignal()

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent)
        # self.setModel(CifTableModel(self))
        delegate = CifItemEditor(self)
        self.setItemDelegate(delegate)
        delegate.text_changed.connect(lambda index: self.resizeRowToContents(index.row()))
        # self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setEnabled(True)

    def on_data_changed(self, topLeft, bottomRight, roles):
        for row in range(topLeft.row(), bottomRight.row() + 1):
            self.resizeRowToContents(row)

    @property
    def rows_count(self):
        return self.model().rowCount()

    @property
    def columns_count(self):
        return self.model().columnCount()

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        context_menu = QtWidgets.QMenu(self)
        save_excel = context_menu.addAction("Save as Excel File")
        save_excel.triggered.connect(lambda: self._on_save_excel(event))
        context_menu.addAction(save_excel)
        context_menu.popup(QCursor.pos())

    def changeEvent(self, a0: QtCore.QEvent) -> None:
        self.resizeRowsToContents()
        print('changeevent')
        self.model().dataChanged.connect(self.on_data_changed)
        # self._on_data_changed()
        super().changeEvent(a0)

    def _on_save_excel(self, event: QtGui.QContextMenuEvent):
        self.save_excel_triggered.emit()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.RightButton:
            pass
        super().mousePressEvent(e)

    def resizeRowToContents(self, row: int) -> None:
        super().resizeRowToContents(row)

    """def resizeRowsToContents(self):
        for row in range(self.model().rowCount()):
            max_text_length = max([self.model().data(self.model().index(row, col), Qt.DisplayRole)
                                   for col in range(self.model().columnCount())], key=len, default="")

            # Here, you can adjust the value '20' and the multiplier as per your requirement.
            row_height = 20 + (len(max_text_length) // 50) * 20
            self.setRowHeight(row, row_height)"""

    def dataChanged(self, topLeft: QtCore.QModelIndex, bottomRight: QtCore.QModelIndex,
                    roles: Iterable[int] = None) -> None:
        self.resizeRowsToContents()
        super().dataChanged(topLeft, bottomRight, roles)