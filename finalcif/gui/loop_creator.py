import re
from typing import List

from PyQt5.QtWidgets import QWidget

from finalcif.cif import all_cif_dicts
from finalcif.gui.loop_creator_ui import Ui_LoopCreator


class LoopCreator(QWidget, Ui_LoopCreator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.leftPushButton.clicked.connect(self.move_selected_key_to_left)
        self.rightPushButton.clicked.connect(self.move_selected_key_to_right)
        self.searchLineEdit.textChanged.connect(self.search)
        self.availableKeysListWidget.addItems(all_cif_dicts.cif_all_dict.keys())
        for num in range(self.availableKeysListWidget.count()):
            item = self.availableKeysListWidget.item(num)
            helptext = all_cif_dicts.cif_all_dict.get(item.text())
            item.setToolTip(helptext)

    @property
    def tags(self):
        return self.get_itemtexts_from_new_loop()

    def search(self, searchtext: str):
        self.availableKeysListWidget.clear()
        cif_keys = all_cif_dicts.cif_all_dict.keys()
        if searchtext:
            searchpattern = re.compile(f'.*{searchtext}.*', re.IGNORECASE)
            searched = [x for x in cif_keys if searchpattern.match(x)]
            self.availableKeysListWidget.addItems(searched)
        else:
            self.availableKeysListWidget.addItems(cif_keys)

    def move_selected_key_to_right(self):
        itemtexts = self.get_itemtexts_from_new_loop()
        item = self.availableKeysListWidget.currentItem()
        row = self.availableKeysListWidget.currentRow()
        if item and item.text() not in itemtexts:
            self.newLoopKeysListWidget.addItem(item.text())
            item.setHidden(True)
            if row <= self.availableKeysListWidget.count():
                self.availableKeysListWidget.setCurrentRow(row + 1)

    def get_itemtexts_from_new_loop(self) -> List[str]:
        itemtexts = []
        for num in range(self.newLoopKeysListWidget.count()):
            itemtext = self.newLoopKeysListWidget.item(num).text()
            itemtexts.append(itemtext)
        return itemtexts

    def move_selected_key_to_left(self):
        current_item = self.newLoopKeysListWidget.currentItem()
        if current_item:
            for num in range(self.availableKeysListWidget.count()):
                item = self.availableKeysListWidget.item(num)
                if item.text() == current_item.text():
                    item.setHidden(False)
            current_item.setHidden(True)
