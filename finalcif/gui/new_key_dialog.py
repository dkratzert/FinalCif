import re

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from finalcif.cif import all_cif_dicts
from finalcif.gui.new_key_dialog_ui import Ui_AddKeyWindow


class NewKey(QtWidgets.QMainWindow, Ui_AddKeyWindow):
    new_key_added = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.searchLineEdit.textChanged.connect(self.search)
        self.addKeyPushButton.clicked.connect(self.add_keys)
        self.cancelPushButton.clicked.connect(lambda: self.close())
        self.keysListWidget.addItems(all_cif_dicts.cif_all_dict.keys())
        for num in range(self.keysListWidget.count()):
            item = self.keysListWidget.item(num)
            helptext = all_cif_dicts.cif_all_dict.get(item.text())
            item.setToolTip(helptext)

    def add_keys(self):
        for item in self.keysListWidget.selectedItems():
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
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    nk = NewKey()
    nk.show()
    sys.exit(app.exec_())
