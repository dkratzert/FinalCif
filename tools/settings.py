from typing import List

from PyQt5.QtCore import QPoint, QSettings, QSize
from PyQt5.QtWidgets import QMainWindow


class FinalCifSettings():
    def __init__(self, window: QMainWindow):
        self.window = window
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)
        self.settings.setDefaultFormat(QSettings.IniFormat)
        print(self.settings.setFallbacksEnabled(False))
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
        Saves Equipment templates into the settings as dictionary.
        :param name: is the name of the template.
        :param items: List of key value pairs
        """
        self.settings.setValue(name, items)

    def load_template(self, name: str) -> List[list]:
        """
        Load templates abnd return them as list of lists.
        """
        return self.settings.value(name)


if __name__ == '__main__':
    sett = QSettings('foo', 'bar')
    sett.setValue('a property', {'key': 'value', 'another': 'yetmore'})
    print(sett.value('a property'))
