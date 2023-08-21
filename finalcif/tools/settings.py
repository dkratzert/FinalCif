#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from typing import List, Dict, Union, Tuple, Iterable, TYPE_CHECKING

from PyQt5.QtCore import QPoint, QSettings, QSize

if TYPE_CHECKING:
    pass

DEBUG = False


class FinalCifSettings():
    def __init__(self):
        self.software_name = 'FinalCif'
        self.organization = 'DK'
        self.settings = QSettings(self.organization, self.software_name)
        self.property_keys_and_values = self.load_property_keys_and_values()
        self.property_keys = self.load_cif_keys_of_properties()
        # print(self.settings.fileName())

    @property
    def property_items(self):
        return self.list_saved_items(property='property')

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
        maximized = self.settings.value('maximized')
        maxim = False
        if isinstance(maximized, str):
            if eval(maximized.capitalize()):
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
        self._save_settings_value(dir, 'dir', "WorkDir")

    def load_last_workdir(self) -> str:
        self.settings.beginGroup('WorkDir')
        lastdir = self.settings.value("dir", type=str)
        self.settings.endGroup()
        return lastdir

    def get_equipment_list(self) -> list:
        return sorted(self.list_saved_items('equipment'))

    def get_properties_list(self) -> list:
        return sorted(self.list_saved_items('property'))

    def load_property_keys_and_values(self) -> list:
        keylist = []
        for p in self.property_items:
            try:
                keylist.append(self.load_settings_list(property='property', item_name=p))
            except TypeError:
                pass
        return keylist

    def load_cif_keys_of_properties(self) -> List[str]:
        property_keys = [x[0] for x in self.load_property_keys_and_values()]
        return property_keys

    def load_property_values_by_key(self, cif_key: str):
        num_value_pairs = []
        if self.property_keys and cif_key in self.property_keys:
            keys_and_values = self.property_keys_and_values[self.property_keys.index(cif_key)]
            if len(keys_and_values) >= 1:
                property_values = keys_and_values[1]
            else:
                property_values = ['']
            for n, val in enumerate(property_values):
                num_value_pairs.append((n, val))
            return num_value_pairs
        return [(0, '')]

    def save_template_list(self, name: str, items: list):
        """
        Saves Equipment templates into the settings as list.
        """
        if DEBUG:
            print(f"Saving {name} {items}")
        self.settings.setValue(name, items)
        self.property_keys_and_values = self.load_property_keys_and_values()
        self.property_keys = self.load_cif_keys_of_properties()

    def save_key_value(self, name: str, item: Union[str, List, Tuple, Dict]):
        """
        Saves a single key/value pair.
        """
        self.settings.setValue(name, item)
        if DEBUG:
            print(f"Saving {name} {item}")

    def load_value_of_key(self, key: str) -> Union[object, Iterable, List]:
        """
        Load templates and return them as string.
        """
        return self.settings.value(key)

    def delete_template(self, property: str, name: str):
        """
        Deletes the currently seleted item.
        """
        self.settings.beginGroup(property)
        self.settings.remove(name)
        self.settings.endGroup()
        if property == 'equipment':
            deleted = self.load_value_of_key(key='deleted_templates') or []
            deleted.append(name)
            deleted = list(set(deleted))
            self.save_key_value(name='deleted_templates', item=deleted)

    @property
    def deleted_equipment(self):
        deleted = self.load_value_of_key(key='deleted_templates')
        return deleted or []

    def empty_deleted_list(self):
        self.save_key_value(name='deleted_templates', item=[])

    def load_options(self) -> dict:
        options = self.load_settings_dict('Options', "options")
        if not options:
            # These are the default values
            options = {'report_text'  : True,
                       'picture_width': 7.5,
                       'without_h'    : False,
                       'report_adp'   : True,
                       'track_changes': False,
                       'checkcif_url' : 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl',
                       }
        # self.settings.endGroup()
        # These are default values for now:
        options.update({'atoms_table'   : True,
                        'bonds_table'   : True,
                        'hydrogen_bonds': True,  # Wasserstoffbrückenbindungen
                        })
        return options

    def save_options(self, options: dict):
        self.save_settings_dict('Options', 'options', options)

    def load_settings_dict(self, property: str = '', item_name: str = '') -> Dict:
        settings = self._load_settings(property, item_name)
        return settings or {}

    def load_settings_list(self, property: str = '', item_name: str = '') -> List:
        settings = self._load_settings(property, item_name)
        return settings or []

    def load_settings_list_as_dict(self, property: str, item_name: str):
        setting = self.load_settings_list(property, item_name)
        keydict = {}
        for p in setting:
            try:
                keydict[p[0]] = p[1]
            except IndexError:
                continue
        return keydict

    def _load_settings(self, property: str, item_name: str):
        directory = self.list_saved_items(property)
        if directory and item_name in directory:
            self.settings.beginGroup(property)
            v = self.settings.value(item_name)
            self.settings.endGroup()
            return v

    def list_saved_items(self, property: str) -> list:
        self.settings.beginGroup(property)
        v = self.settings.allKeys()
        self.settings.endGroup()
        return v

    def save_settings_dict(self, property: str, name: str, items) -> None:
        self._save_settings_value(items, name, property)

    def _save_settings_value(self, items: Union[str, Dict[str, bool], List[str]], name: str, property: str) -> None:
        self.settings.beginGroup(property)
        self.settings.setValue(name, items)
        if DEBUG:
            print(f"Saving {name} {items}")
        self.settings.endGroup()

    def save_settings_list(self, property: str, name: str, items: List):
        self._save_settings_value(items, name, property)


if __name__ == '__main__':
    s = FinalCifSettings()
    # p = s.load_settings_dict(item_name='Daniel Kratzert')
    # print(p, '###ä###')
    print('load_property_by_key:', s.load_property_values_by_key(cif_key='_diffrn_ambient_environment'))
    print(s.load_cif_keys_of_properties())
