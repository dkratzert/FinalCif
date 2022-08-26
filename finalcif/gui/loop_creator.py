from PyQt5.QtWidgets import QWidget

from finalcif.gui.loop_creator_ui import Ui_LoopCreator


class LoopCreator(QWidget, Ui_LoopCreator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
