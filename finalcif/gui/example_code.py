# https://gist.github.com/Riateche/5984815

from PyQt5 import QtCore
from PyQt5.QtWidgets import QItemDelegate, QTableView, QWidget, QApplication, QVBoxLayout, QComboBox, QPushButton

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.ciftable_view import CifItemEditor
from finalcif.gui.table_model import CifTableModel


class TableModel(QtCore.QAbstractTableModel):
    """
    A simple 5x4 table model to demonstrate the delegates
    """

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 5

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        return f"{index.row():02d}"

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)

    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled


class ButtonDelegate(QItemDelegate):

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QPushButton(str(index.data()), parent)
        combo.clicked.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        # editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        print(self.sender(), '# sender() is the pushbutton')
        # self.sender().setText('#')
        # self.sender().setText(self.parent().model().data(index))
        self.commitData.emit(self.sender())


class ComboDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """

    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        li = []
        li.append("Zero")
        li.append("One")
        li.append("Two")
        li.append("Three")
        li.append("Four")
        li.append("Five")
        combo.addItems(li)
        combo.currentIndexChanged.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())

    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class TableView(QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the delegate for column 0 of our table
        # self.setItemDelegateForColumn(0, ButtonDelegate(self))
        #self.setItemDelegateForColumn(0, ComboDelegate(self))
        #self.setItemDelegateForColumn(1, ButtonDelegate(self))
        delegate = CifItemEditor(self)
        #delegate.heightChanged.connect(self.resizeRowToContents)
        self.setItemDelegateForColumn(0, delegate)


if __name__ == "__main__":
    from sys import argv, exit


    class Widget(QWidget):
        """
        A simple test widget to contain and own the model and table.
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            l = QVBoxLayout(self)
            c = CifContainer('tests/examples/1979688.cif')
            data = [[key, value, ''] for key, value in c.key_value_pairs()]
            self._tm = CifTableModel(self, data)
            self._tv = TableView(self)
            # self._tv.setGridStyle(QtCore.Qt.NoPen)
            self._tv.setShowGrid(False)
            self._tv.setAlternatingRowColors(True)
            self._tv.setModel(self._tm)
            #for row in range(0, self._tm.rowCount()):
            #    self._tv.openPersistentEditor(self._tm.index(row, 0))
            #    self._tv.openPersistentEditor(self._tm.index(row, 1))

            l.addWidget(self._tv)


    a = QApplication(argv)
    w = Widget()
    w.move(0, 0)
    w.resize(800, 600)
    w.show()
    w.raise_()
    exit(a.exec_())
