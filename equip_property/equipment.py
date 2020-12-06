from contextlib import suppress
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from gemmi import cif

from cif.core_dict import cif_all_dict
from cif.text import retranslate_delimiter, set_pair_delimited
from gui.custom_classes import COL_CIF, COL_DATA, light_green, COL_EDIT
from gui.dialogs import show_general_warning, cif_file_open_dialog, cif_file_save_dialog
from tools import misc
from tools.misc import include_equipment_imports
from tools.settings import FinalCifSettings
with suppress(ImportError):
    from appwindow import AppWindow

class Equipment:

    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.app.ui.EquipmentEditTableWidget.verticalHeader().hide()
        self.signals_and_slots()
        self.load_default_equipment()

    def signals_and_slots(self):
        ## equipment
        self.app.ui.EquipmentTemplatesListWidget.doubleClicked.connect(self.edit_equipment_template)
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
        self.app.ui.EquipmentTemplatesListWidget.currentRowChanged.connect(self.load_selected_equipment)
        self.app.ui.EquipmentTemplatesListWidget.clicked.connect(self.load_selected_equipment)

    def show_equipment(self):
        self.app.ui.EquipmentTemplatesListWidget.clear()
        for eq in self.settings.get_equipment_list():
            if eq:
                item = QListWidgetItem(eq)
                self.app.ui.EquipmentTemplatesListWidget.addItem(item)

    def load_selected_equipment(self) -> None:
        """
        Loads equipment data to be shown in the main Cif table.
        Not for template edititng!
        """
        listwidget = self.app.ui.EquipmentTemplatesListWidget
        selected_row_text = listwidget.currentIndex().data()
        if not selected_row_text:
            return None
        equipment = self.settings.load_equipment_template_as_dict(selected_row_text)
        if self.app.ui.cif_main_table.vheaderitems:
            for key in equipment:
                if key not in self.app.ui.cif_main_table.vheaderitems:
                    # Key is not in the main table:
                    self.app.add_row(key, equipment[key])
                else:
                    # Key is already there:
                    self.app.ui.cif_main_table.setText(key, COL_CIF,
                                                       txt=self.app.ui.cif_main_table.getTextFromKey(key, COL_CIF))
                    self.app.ui.cif_main_table.setText(key, COL_DATA, txt=equipment[key], color=light_green)
                    self.app.ui.cif_main_table.setText(key, COL_EDIT, txt=equipment[key])
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
        self.settings.delete_template('equipment/' + selected_template_text)
        equipment_list = self.settings.settings.value('equipment_list') or []
        try:
            equipment_list.remove(selected_template_text)
        except ValueError:
            pass
        self.settings.save_template('equipment_list', equipment_list)
        # now make it invisible:
        self.app.ui.EquipmentTemplatesListWidget.takeItem(index.row())
        self.cancel_equipment_template()
        # I do these both to clear the list:
        self.load_default_equipment()

    def load_default_equipment(self):
        self.store_predefined_templates()
        self.show_equipment()

    def store_predefined_templates(self):
        equipment_list = self.settings.settings.value('equipment_list') or []
        for item in misc.predef_equipment_templ:
            if not item['name'] in equipment_list:
                equipment_list.append(item['name'])
                newlist = [x for x in list(set(equipment_list)) if x]
                # this list keeps track of the equipment items:
                self.settings.save_template('equipment_list', newlist)
                self.settings.save_template('equipment/' + item['name'], item['items'])

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
        listwidget = self.app.ui.EquipmentTemplatesListWidget
        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_template('equipment/' + selected_row_text)
        # first load the previous values:
        if table_data:
            for key, value in table_data:
                if not key or not value:
                    continue
                table.add_equipment_row(key, retranslate_delimiter(value))
        else:
            # new empty equipment:
            for _ in range(8):
                table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(1)
        table.resizeRowsToContents()
        table.blockSignals(False)

    def save_equipment_template(self) -> None:
        """
        Saves the currently selected equipment template to the config file.
        """
        selected_template_text, table_data = self.get_equipment_entry_data()
        # warn if key is not official:
        for key, _ in table_data:
            if key not in cif_all_dict:
                if not key.startswith('_'):
                    show_general_warning('"{}" is not a valid keyword! '
                                         '\nChange the name in order to save.\n'
                                         'Keys must start with an underscore.'.format(key))
                    return
                show_general_warning('"{}" is not an official CIF keyword!'.format(key))
        self.settings.save_template('equipment/' + selected_template_text, table_data)
        self.settings.append_to_equipment_list(selected_template_text)
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
        try:
            doc = cif.read_file(filename)
        except RuntimeError as e:
            show_general_warning(str(e))
            return
        block = doc.sole_block()
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
        self.settings.save_template('equipment/' + name, table_data)
        self.settings.append_to_equipment_list(name)
        self.show_equipment()

    def get_equipment_entry_data(self) -> Tuple[str, list]:
        """
        Returns the string of the currently selected entry and the table data behind it.
        """
        table = self.app.ui.EquipmentEditTableWidget
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        selected_template_text = self.app.ui.EquipmentTemplatesListWidget.currentIndex().data()
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
        return selected_template_text, table_data

    def export_equipment_template(self, filename: str = None) -> None:
        """
        Exports the currently selected equipment entry to a file.

        I order to export, we have to run self.edit_equipment_template() first!
        """
        selected_template, table_data = self.get_equipment_entry_data()
        if not selected_template:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_template.split())
        block = doc.add_new_block(blockname)
        for key, value in table_data:
            set_pair_delimited(block, key, value.strip('\n\r '))
        if not filename:
            filename = cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

    def cancel_equipment_template(self) -> None:
        """
        Cancel Equipment editing.
        """
        table = self.app.ui.EquipmentEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('cancelled equipment')
