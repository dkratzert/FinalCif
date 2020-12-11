#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from typing import List, Dict

from PyQt5.QtCore import QPoint, QSettings, QSize


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

    def save_to_equipment_list(self, selected_template_text: str, templ_type: str = 'equipment_list/') -> None:
        equipment_list = self.settings.value(templ_type)
        if not equipment_list:
            equipment_list = ['']
        equipment_list.sort()
        equipment_list.append(selected_template_text)
        newlist = [x for x in list(set(equipment_list)) if x]
        # this list keeps track of the equipment items:
        self.save_template(templ_type, newlist)

    def get_equipment_list(self, equipment='equipment_list') -> list:
        equipment_list = self.settings.value(equipment)
        if not equipment_list:
            equipment_list = ['']
        return sorted(equipment_list)

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
        Saves Equipment templates into the settings as list.
        """
        self.settings.setValue(name, items)

    def load_template(self, name: str) -> List[List]:
        """
        Load templates and return them as list of lists.
        """
        return self.settings.value(name)

    def load_loop_template(self, name: str) -> Dict:
        """
        Load templates and return them as list of lists.
        """
        return self.settings.value('authors_list/' + name)

    def save_loop_template(self, name: str, items: dict):
        """
        Saves Equipment templates into the settings as list.
        """
        if not isinstance(name, str):
            print('name was no string')
            return
        self.settings.setValue('authors_list/' + name, items)

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
                       'without_h'    : False,
                       'checkcif_url' : 'https://checkcif.iucr.org/cgi-bin/checkcif_with_hkl',
                       }
        self.settings.endGroup()
        # These are default values for now:
        options.update({'atoms_table'   : True,
                        'bonds_table'   : True,
                        'hydrogen_bonds': True,  # Wasserstoffbrückenbindungen
                        })
        return options

    def save_options(self, options: dict):
        self.settings.beginGroup('Options')
        self.settings.setValue('options', options)
        self.settings.endGroup()


if __name__ == '__main__':
    sett = QSettings('foo', 'bar')
    sett.setValue('a property', {'key': 'value', 'another': 'yetmore'})
    print(sett.value('a property'))
