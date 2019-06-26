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

    def property_name_by_key(self, key):
        """
        Returns the name in the PropertiesTemplatesListWidget that belongs to the cif keyword.
        """
        plist = self.settings.value('property_list')
        for p in plist:
            try:
                val = self.settings.value('property/' + p)[0]
            except TypeError:
                continue
            if p == key:
                return val

    def load_property_keys(self):
        """
        Returns a list of keys like _exptl_crystal_colour from all properties.
        """
        keylist = []
        plist = self.settings.value('property_list')
        for p in plist:
            try:
                keylist.append(self.settings.value('property/'+p)[0])
            except TypeError:
                pass
        return keylist

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

    def load_equipment_template_as_dict(self, name: str) -> dict:
        """
        """
        keydict = {}
        plist = self.load_template('equipment/' + name) or []
        for p in plist:
            try:
                keydict[p[0]] = p[1]
            except IndexError:
                continue
        return keydict

    def delete_template(self, name: str):
        """
        Deletes the currently seleted item.
        """
        self.settings.remove(name)

    def load_property_by_key(self, key):
        keylist = self.load_property_keys()
        plist = self.settings.value('property_list')
        templ = None
        for (p, k) in zip(plist, keylist):
            if k == key:
                templ = self.load_template('property/' + p)
        return [(n, x) for n, x in enumerate(templ[1])]

if __name__ == '__main__':
    sett = QSettings('foo', 'bar')
    sett.setValue('a property', {'key': 'value', 'another': 'yetmore'})
    print(sett.value('a property'))
