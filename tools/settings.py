from PyQt5.QtCore import QPoint, QSettings
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

    def save_template(self, name: str, items: list):
        """
        Saves Equipment templates into the settings.
        :param name: is the name of the template.
        :param items: List of key value pairs
        """
        for item in items:
            key, value = item
            self.settings.setValue("Equipment/{}".format(key), value)

    def load_template(self, name):

