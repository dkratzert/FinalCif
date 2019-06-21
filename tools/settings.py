from PyQt5.QtCore import QPoint, QSettings, QSize
from PyQt5.QtWidgets import QMainWindow


class FinalCifSettings():
    def __init__(self, window: QMainWindow):
        self.window = window
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)
        print(self.settings.fileName())

    def save_window_position(self, position: QPoint, size: QSize):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("position", position)
        self.settings.setValue("size", size)
        self.settings.endGroup()

    def load_window_position(self):
        self.settings.beginGroup("MainWindow")
        pos = self.settings.value("position", type=QPoint)
        self.window.move(pos)
        try:
            size = QSize(self.settings.value("size"))
            self.window.resize(size)
        except TypeError:
            pass
        self.settings.endGroup()

    def save_template(self, name: str, items: list):
        """
        Saves Equipment templates into the settings.
        :param name: is the name of the template.
        :param items: List of key value pairs
        """
        self.settings.beginWriteArray(name)
        for num, item in enumerate(items):
            key, value = item
            self.settings.setArrayIndex(num)
            self.settings.setValue(key, value)
        self.settings.endArray()

    def load_template(self, name):
        pass
