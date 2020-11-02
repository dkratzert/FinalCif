#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from contextlib import suppress
from typing import List

from PyQt5.QtCore import QPoint, QSettings, QSize

with suppress(Exception):
    from gui.finalcif_gui import Ui_FinalCifWindow


class FinalCifSettings():
    def __init__(self):
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)
        self.settings.setDefaultFormat(QSettings.IniFormat)
        # print(self.settings.fileName())

    def save_window_position(self, position: QPoint, size: QSize, maximized: bool) -> None:
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("position", position)
        self.settings.setValue("size", size)
        # print('save:', maximized)
        self.settings.setValue('maximized', maximized)
        self.settings.endGroup()

    def load_window_position(self) -> dict:
        """
        Loads window position information and sets default values if no configuration exists.
        """
        self.settings.beginGroup("MainWindow")
        pos = self.settings.value("position", type=QPoint)
        size = self.settings.value("size", type=QSize)
        size = size if size.width() > 0 else QSize(900, 850)
        pos = pos if pos.x() > 0 else QSize(20, 20)
        max = self.settings.value('maximized')
        maxim = False
        if isinstance(max, str):
            if bool(eval(max.capitalize())):
                maxim = True
            else:
                maxim = False
        self.settings.endGroup()
        return {'size': size, 'position': pos, 'maximized': maxim}

    def save_current_dir(self, dir: str) -> None:
        """
        Saves the current work directory of the Program.
        :param dir: Directory as string
        """
        self.settings.beginGroup("WorkDir")
        self.settings.setValue('dir', dir)
        self.settings.endGroup()

    def load_last_workdir(self) -> str:
        self.settings.beginGroup('WorkDir')
        lastdir = self.settings.value("dir", type=str)
        self.settings.endGroup()
        return lastdir

    def save_favorite_template(self, app: 'Ui_FinalCifWindow') -> None:
        """
        Saves the last used equipment. I curently do not use it.
        :param app: Appwindow instance
        """
        last_equipment = app.EquipmentTemplatesListWidget.currentRow()
        self.settings.beginGroup('LastEquipment')
        self.settings.setValue('last', last_equipment)
        self.settings.endGroup()

    def append_to_equipment_list(self, selected_template_text) -> None:
        equipment_list = self.settings.value('equipment_list')
        if not equipment_list:
            equipment_list = ['']
        equipment_list.sort()
        equipment_list.append(selected_template_text)
        newlist = [x for x in list(set(equipment_list)) if x]
        # this list keeps track of the equipment items:
        self.save_template('equipment_list', newlist)

    def get_equipment_list(self) -> list:
        equipment_list = self.settings.value('equipment_list')
        if not equipment_list:
            equipment_list = ['']
        return sorted(equipment_list)

    def load_last_equipment(self) -> int:
        self.settings.beginGroup('LastEquipment')
        last = self.settings.value("last", type=int)
        self.settings.endGroup()
        return last

    def property_name_by_key(self, key) -> str:
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

    def load_property_keys(self) -> list:
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

    def load_options(self) -> dict:
        self.settings.beginGroup('Options')
        options = self.settings.value("options", type=dict)
        if not options:
            options = {'report_text'  : True,
                       'picture_width': 7.5,
                       'without_H'    : False,
                       'checkcif_url' : 'https://checkcif.iucr.org/cgi-bin/checkcif_with_hkl'
                       }
        self.settings.endGroup()
        return options

    def save_options(self, options: dict):
        self.settings.beginGroup('Options')
        self.settings.setValue('options', options)
        self.settings.endGroup()


if __name__ == '__main__':
    sett = QSettings('foo', 'bar')
    sett.setValue('a property', {'key': 'value', 'another': 'yetmore'})
    print(sett.value('a property'))
