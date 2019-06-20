from PyQt5.QtCore import QSettings, QPoint
from PyQt5.QtWidgets import QMainWindow


class FinalCifSettings():
    def __init__(self, window: QMainWindow):
        self.window = window
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)

    def save_window_position(self, position: QPoint):
        self.settings.setValue("FinalCifWindow/position", position)

    def load_window_position(self):
        pos = self.settings.value("FinalCifWindow/position", type=QPoint)
        self.window.move(pos)
