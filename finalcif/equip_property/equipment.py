from bisect import bisect
from contextlib import suppress
from pathlib import Path
from typing import List, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from gemmi import cif

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.text import retranslate_delimiter, string_to_utf8
from finalcif.equip_property.tools import read_document_from_cif_file
from finalcif.gui.custom_classes import Column, light_green
from finalcif.gui.dialogs import show_general_warning, cif_file_open_dialog, cif_file_save_dialog
from finalcif.tools import misc
from finalcif.tools.misc import include_equipment_imports
from finalcif.tools.settings import FinalCifSettings

with suppress(ImportError):
    from finalcif.appwindow import AppWindow


class Equipment:

    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        if app:
            self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
            self.app.ui.EquipmentEditTableWidget.verticalHeader().hide()
            self.signals_and_slots()
            self.load_default_equipment()

    def signals_and_slots(self):
        ## equipment
        self.app.ui.EditEquipmentTemplateButton.clicked.connect(self.edit_equipment_template)
        self.app.ui.SaveEquipmentButton.clicked.connect(self.save_equipment_template)
        self.app.ui.CancelEquipmentButton.clicked.connect(self.cancel_equipment_template)
        self.app.ui.DeleteEquipmentButton.clicked.connect(self.delete_equipment)
        self.app.ui.ExportEquipmentButton.clicked.connect(self.export_equipment_template)
        self.app.ui.ImportEquipmentTemplateButton.clicked.connect(self.import_equipment_from_file)
        ## equipment
        self.app.ui.EquipmentEditTableWidget.cellPressed.connect(self.app.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.app.ui.EquipmentEditTableWidget.itemSelectionChanged.connect(
            self.app.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.app.ui.EquipmentEditTableWidget.itemEntered.connect(self.app.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.app.ui.EquipmentEditTableWidget.cellChanged.connect(self.app.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.app.ui.EquipmentEditTableWidget.currentItemChanged.connect(
            self.app.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.app.ui.NewEquipmentTemplateButton.clicked.connect(self.new_equipment)
        self.app.ui.EquipmentTemplatesListWidget.doubleClicked.connect(self.load_selected_equipment)

    def show_equipment(self):
        self.app.ui.EquipmentTemplatesListWidget.clear()
        deleted = self.settings.load_value_of_key(key='deleted_templates') or []
        for eq in self.settings.get_equipment_list():
            if eq and eq not in deleted:
                item = QListWidgetItem(eq)
                self.app.ui.EquipmentTemplatesListWidget.addItem(item)

    def load_selected_equipment(self) -> None:
        """
        Loads equipment data to be shown in the main Cif table.
        Not for template edititng!
        """
        if not self.selected_template_name():
            return None
        equipment = self.settings.load_settings_list_as_dict(property='equipment',
                                                             item_name=self.selected_template_name())
        if self.app.ui.cif_main_table.vheaderitems:
            for key in equipment:
                if key not in self.app.ui.cif_main_table.vheaderitems:
                    # Key is not in the main table:
                    self.app.add_row(key, equipment[key], at_start=False,
                                     position=bisect(self.app.ui.cif_main_table.vheaderitems, key))
                # Key is already there:
                self.app.ui.cif_main_table.setText(key, Column.CIF, txt='?')
                self.app.ui.cif_main_table.setText(key, Column.DATA, txt=equipment[key], color=light_green)
                self.app.ui.cif_main_table.setText(key, Column.EDIT, txt=equipment[key])
        else:
            print('Empty main table!')

    def new_equipment(self) -> None:
        item = QListWidgetItem('')
        self.app.ui.EquipmentTemplatesListWidget.addItem(item)
        self.app.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.app.ui.EquipmentTemplatesListWidget.editItem(item)

    def delete_equipment(self) -> None:
        # First delete the list entries
        index = self.app.ui.EquipmentTemplatesListWidget.currentIndex()
        selected_template_text = index.data()
        self.settings.delete_template('equipment', selected_template_text)
        # now make it invisible:
        self.app.ui.EquipmentTemplatesListWidget.takeItem(index.row())
        self.cancel_equipment_template()
        # I do these both to clear the list:
        self.load_default_equipment()

    def export_raw_data(self) -> List[Dict]:
        equipment_list = []
        for equipment_name in self.settings.get_equipment_list():
            if equipment_name:
                equipment = self.settings.load_settings_list(property='equipment', item_name=equipment_name)
                equipment_list.append({'name'   : equipment_name, 'data': equipment,
                                       'deleted': self.settings.deleted_equipment})
        return equipment_list

    def import_raw_data(self, equipment_list: List[Dict]) -> None:
        deleted = self.settings.deleted_equipment
        for eq in equipment_list:
            name = eq.get('name')
            if name in deleted and name not in (eq.get('deleted') or []):
                deleted.remove(name)
            self.settings.save_settings_list('equipment', name, eq.get('data'))
        self.settings.save_key_value(name='deleted_templates', item=deleted)
        self.show_equipment()

    def load_default_equipment(self):
        self.store_predefined_templates()
        self.show_equipment()

    def store_predefined_templates(self):
        equipment_list = self.settings.get_equipment_list() or []
        for item in misc.predefined_equipment_templates:
            if item['name'] not in equipment_list:
                self.settings.save_settings_list('equipment', item['name'], item['items'])

    def edit_equipment_template(self) -> None:
        """Gets called when 'edit equipment' button was clicked."""
        it = self.app.ui.EquipmentTemplatesListWidget.currentItem()
        self.app.ui.EquipmentTemplatesListWidget.setCurrentItem(None)
        self.app.ui.EquipmentTemplatesListWidget.setCurrentItem(it)
        self.app.ui.CancelPropertiesButton.click()
        self.load_equipment_to_edit()

    def load_equipment_to_edit(self) -> None:
        """
        Load/Edit the key/value list of an equipment entry.
        """
        table = self.app.ui.EquipmentEditTableWidget
        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(0)
        if not self.selected_template_name():
            return
        self.undelete_equipment(self.selected_template_name())
        table_data = self.settings.load_settings_list(property='equipment', item_name=self.selected_template_name())
        # first load the previous values:
        if table_data:
            for data in table_data:
                if len(data) != 2:
                    continue
                key, value = data
                table.add_equipment_row(key, string_to_utf8(value))
        else:
            # new empty equipment:
            for _ in range(8):
                table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(1)
        table.resizeRowsToContents()
        table.blockSignals(False)

    def undelete_equipment(self, equipment_name: str) -> None:
        deleted = self.settings.deleted_equipment or []
        if equipment_name in deleted:
            del deleted[deleted.index(equipment_name)]
            self.settings.save_key_value(name='deleted_templates', item=deleted)

    def save_equipment_template(self) -> None:
        """
        Saves the currently selected equipment template to the config file.
        """
        # Local import for faster startup
        from finalcif.cif.all_cif_dicts import cif_all_dict
        table_data = self.get_equipment_entry_data()
        # warn if key is not official:
        for key, _ in table_data:
            if key not in cif_all_dict.keys():
                if not key.startswith('_'):
                    show_general_warning('"{}" is not a valid keyword! '
                                         '\nChange the name in order to save.\n'
                                         'Keys must start with an underscore.'.format(key))
                    return
                show_general_warning('"{}" is not an official CIF keyword!'.format(key))
        self.settings.save_settings_list('equipment', self.selected_template_name(), table_data)
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('saved')

    def import_equipment_from_file(self, filename='') -> None:
        """
        Import an equipment entry from a cif file.
        """
        if not filename:
            filename = cif_file_open_dialog(filter="CIF file (*.cif  *.cif_od *.cfx)")
        if not filename:
            print('No file given')
            return
        doc = read_document_from_cif_file(filename)
        if not doc:
            return
        for block in doc:
            self._import_block(block, filename)
        self.show_equipment()

    def _import_block(self, block: cif.Block, filename: str) -> None:
        table_data = []
        for item in block:
            if item.pair is not None:
                key, value = item.pair
                if filename.endswith('.cif_od') and key not in include_equipment_imports:
                    continue
                table_data.append([key, retranslate_delimiter(cif.as_string(value).strip('\n\r ;'))])
        if filename.endswith('.cif_od'):
            name = Path(filename).stem
        else:
            name = block.name.replace('__', ' ')
        self.undelete_equipment(equipment_name=name)
        self.settings.save_settings_list('equipment', name, table_data)

    def get_equipment_entry_data(self) -> list:
        """
        Returns the string of the currently selected entry and the table data behind it.
        """
        table = self.app.ui.EquipmentEditTableWidget
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        table_data = []
        ncolumns = table.rowCount()
        for rownum in range(ncolumns):
            key = ''
            try:
                key = table.text(rownum, 0)
                value = table.text(rownum, 1).strip('\n\r ')
            except AttributeError:
                value = ''
            if key and value:
                table_data.append([key, value])
        return table_data

    def selected_template_name(self) -> str:
        return self.app.ui.EquipmentTemplatesListWidget.currentIndex().data()

    def export_equipment_template(self, filename: str = None) -> None:
        """
        Exports the currently selected equipment entry to a file.

        In order to export, we have to run self.edit_equipment_template() first!
        """
        selected_template = self.selected_template_name()
        if not selected_template:
            return
        table_data = self.get_equipment_entry_data()
        blockname = '__'.join(selected_template.split())
        if not filename:
            filename = cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        equipment_cif = CifContainer(filename, new_block=blockname)
        for key, value in table_data:
            equipment_cif[key] = value.strip('\n\r ')
        try:
            equipment_cif.save(Path(filename))
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).resolve()))

    def cancel_equipment_template(self) -> None:
        """
        Cancel Equipment editing.
        """
        table = self.app.ui.EquipmentEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('cancelled equipment')


if __name__ == '__main__':
    l = Equipment(None, FinalCifSettings())
    for line in l.export_raw_data():
        print(f"{line}")
