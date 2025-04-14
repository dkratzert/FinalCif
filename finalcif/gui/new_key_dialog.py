import re

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Signal, Qt

from finalcif.cif import all_cif_dicts
from finalcif.gui.new_key_dialog_ui import Ui_AddKeyWindow


class NewKey(QtWidgets.QMainWindow, Ui_AddKeyWindow):
    new_key_added = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.searchLineEdit.textChanged.connect(self.search)
        self.addKeyPushButton.clicked.connect(self.add_keys)
        self.cancelPushButton.clicked.connect(lambda: self.close())
        self.keysListWidget.addItems(['', *list(all_cif_dicts.cif_all_dict.keys())])
        self.keysListWidget.item(0).setFlags(
            QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
        self.keysListWidget.item(0).setText('Double-click to add custom key.')
        self.keysListWidget.item(0).setForeground(QtGui.QBrush(QtGui.QColor("gray")))
        self.keysListWidget.itemDoubleClicked.connect(self.item_clicked)
        for num in range(self.keysListWidget.count()):
            item = self.keysListWidget.item(num)
            helptext = all_cif_dicts.cif_all_dict.get(item.text())
            item.setToolTip(helptext)

    def item_clicked(self, item: QtWidgets.QListWidgetItem):
        if self.keysListWidget.row(item) == 0:
            self.keysListWidget.item(0).setText('')
            self.keysListWidget.item(0).setForeground(QtGui.QBrush(QtGui.QColor("black")))

    def add_keys(self):
        for item in self.keysListWidget.selectedItems():
            if item.text() and item.text().startswith('_') and len(item.text()) > 2:
                self.new_key_added.emit(item.text())

    def search(self, searchtext: str):
        self.keysListWidget.clear()
        cif_keys = all_cif_dicts.cif_all_dict.keys()
        if searchtext:
            searchpattern = re.compile(f'.*{searchtext}.*', re.IGNORECASE)
            searched = [x for x in cif_keys if searchpattern.match(x)]
            self.keysListWidget.addItems(searched)
        else:
            self.keysListWidget.addItems(cif_keys)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    nk = NewKey()
    nk.show()
    sys.exit(app.exec())
