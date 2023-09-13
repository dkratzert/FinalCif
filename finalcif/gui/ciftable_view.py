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

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        return MyQPlainTextEdit(parent)

    def setEditorData(self, editor: MyQPlainTextEdit, index):
        editor.setPlainText(index.data())

    def setModelData(self, editor: MyQPlainTextEdit, model, index):
        model.setData(index, editor.toPlainText(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor: MyQPlainTextEdit, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex):
        print(editor.toPlainText())
        print(editor.sizeHint())
        editor.setGeometry(option.rect)

    # def itemEditorFactory(self) -> QItemEditorFactory:
    #    factory = QItemEditorFactory()
    #    factory.registerEditor(Qt.EditRole, MyQPlainTextEdit)
    #    return factory

    # def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
    #    editor.setPlainText(index.data(role=Qt.EditRole))

    # def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
    #    print(editor)
    #    print(option)
    #    pass

    # def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
    #    print(editor, model)
    #    pass


class CifTableView(QtWidgets.QTableView):
    save_excel_triggered = pyqtSignal()

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent)
        #self.setModel(CifTableModel(self))
        delegate = CifItemEditor(self)
        self.setItemDelegate(delegate)
        # self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
        # self._on_data_changed()
        super().changeEvent(a0)

    def _on_save_excel(self, event: QtGui.QContextMenuEvent):
        self.save_excel_triggered.emit()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.RightButton:
            pass
        super().mousePressEvent(e)
