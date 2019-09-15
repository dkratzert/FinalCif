#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from typing import List

from PyQt5.QtCore import QPoint, QSettings, QSize
from PyQt5.QtWidgets import QMainWindow

from gui.finalcif_gui import Ui_FinalCifWindow


class FinalCifSettings():
    def __init__(self, window: QMainWindow):
        self.window = window
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)
        self.settings.setDefaultFormat(QSettings.IniFormat)
        #print(self.settings.fileName())

    def save_window_position(self, position: QPoint, size: QSize, maximized: bool):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("position", position)
        self.settings.setValue("size", size)
        self.settings.setValue('maximized', maximized)
        self.settings.endGroup()

    def save_favorite_template(self, app: Ui_FinalCifWindow):
        last_equipment = app.EquipmentTemplatesListWidget.currentRow()
        self.settings.beginGroup('LastEquipment')
        self.settings.setValue('last', last_equipment)
        self.settings.endGroup()

    def append_to_equipment_list(self, selected_template_text):
        equipment_list = self.settings.value('equipment_list')
        if not equipment_list:
            equipment_list = ['']
        equipment_list.sort()
        equipment_list.append(selected_template_text)
        newlist = [x for x in list(set(equipment_list)) if x]
        # this list keeps track of the equipment items:
        self.save_template('equipment_list', newlist)

    def get_equipment_list(self):
        equipment_list = self.settings.value('equipment_list')
        if not equipment_list:
            equipment_list = ['']
        return equipment_list

    def load_last_equipment(self):
        self.settings.beginGroup('LastEquipment')
        last = self.settings.value("last", type=int)
        self.settings.endGroup()
        return last

    def load_window_position(self):
        self.settings.beginGroup("MainWindow")
        try:
            pos = self.settings.value("position", type=QPoint)
        except TypeError:
            pos = QPoint(20, 20)
        try:
            size = QSize(self.settings.value("size"))
            self.window.resize(size)
        except TypeError:
            print('Unable to set window size.')
        self.window.move(pos)
        max = self.settings.value('maximized')
        if isinstance(max, str):
            if bool(eval(max.capitalize())):
                self.window.showMaximized()
        elif max:
            self.window.showMaximized()
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
                keylist.append(self.settings.value('property/' + p)[0])
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
            if k.lower() == key.lower():
                templ = self.load_template('property/' + p)
        if not templ:
            return [('', '')]
        return [(n, x) for n, x in enumerate(templ[1]) if templ and len(templ) > 0]


if __name__ == '__main__':
    sett = QSettings('foo', 'bar')
    sett.setValue('a property', {'key': 'value', 'another': 'yetmore'})
    print(sett.value('a property'))
