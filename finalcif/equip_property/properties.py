from contextlib import suppress
from pathlib import Path
from typing import List, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QTableWidget, QListWidget, QStackedWidget
from gemmi import cif

from finalcif.cif.text import retranslate_delimiter, utf8_to_str
from finalcif.equip_property.tools import read_document_from_cif_file
from finalcif.gui.dialogs import cif_file_open_dialog, show_general_warning, cif_file_save_dialog
from finalcif.gui.plaintextedit import PlainTextEditTemplate
from finalcif.tools.misc import predef_prop_templ
from finalcif.tools.settings import FinalCifSettings

with suppress(ImportError):
    from finalcif.appwindow import AppWindow


class Properties:
    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        if app:
            self.signals_and_slots()
            self.app.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)
            self.app.ui.PropertiesEditTableWidget.verticalHeader().hide()
            self.store_predefined_templates()
            self.show_properties()

    def signals_and_slots(self):
        ## properties
        self.app.ui.EditPropertyTemplateButton.clicked.connect(self.edit_property_template)
        self.app.ui.SavePropertiesButton.clicked.connect(self.save_property_template)
        self.app.ui.CancelPropertiesButton.clicked.connect(self.cancel_property_template)
        self.app.ui.DeletePropertiesButton.clicked.connect(self.delete_property)
        ## properties
        self.app.ui.PropertiesEditTableWidget.itemSelectionChanged.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.cellPressed.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.itemEntered.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.cellChanged.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.currentItemChanged.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.itemActivated.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.itemPressed.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.itemClicked.connect(self.add_property_row_if_needed)
        self.app.ui.PropertiesEditTableWidget.itemChanged.connect(self.add_property_row_if_needed)
        self.app.ui.NewPropertyTemplateButton.clicked.connect(self.new_property)
        self.app.ui.ImportPropertyTemplateButton.clicked.connect(self.import_property_from_file)
        self.app.ui.ExportPropertyButton.clicked.connect(self.export_property_template)

    def show_properties(self) -> None:
        """
        Display saved items in the properties lists.
        """
        self.app.ui.PropertiesTemplatesListWidget.clear()
        property_list = self.settings.get_properties_list()
        for pr in property_list:
            if pr:
                item = QListWidgetItem(pr)
                self.app.ui.PropertiesTemplatesListWidget.addItem(item)

    def new_property(self) -> None:
        item = QListWidgetItem('')
        self.app.ui.PropertiesTemplatesListWidget.addItem(item)
        self.app.ui.PropertiesTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.app.ui.PropertiesTemplatesListWidget.editItem(item)
        self.app.ui.cifKeywordLineEdit.clear()

    def add_property_row_if_needed(self) -> None:
        """
        Adds an empty row at the bottom of either the PropertiesEditTableWidget.
        """
        table = self.app.ui.PropertiesEditTableWidget
        rowcount = table.rowCount()
        cont = 0
        for row in range(rowcount):
            key = ''
            with suppress(AttributeError, TypeError):
                key = table.item(row, 0).text()
            with suppress(AttributeError, TypeError):
                key = table.cellWidget(row, 0).getText()
            if key:  # don't count empty key rows
                cont += 1
        diff = rowcount - cont
        if diff < 4:
            table.insertRow(rowcount)

    # The properties templates:

    def delete_property(self) -> None:
        # First delete the list entries
        index = self.app.ui.PropertiesTemplatesListWidget.currentIndex()
        property_name = index.data()
        self.settings.delete_template('property', property_name)
        # now make it invisible:
        self.app.ui.PropertiesTemplatesListWidget.takeItem(index.row())
        self.cancel_property_template()
        # I do these both to clear the list:
        self.store_predefined_templates()
        self.show_properties()
        self.app.refresh_combo_boxes()

    def edit_property_template(self) -> None:
        """
        Edit the Property table.
        """
        # make sure the current item doesnt get lost:
        it = self.app.ui.PropertiesTemplatesListWidget.currentItem()
        self.app.ui.PropertiesTemplatesListWidget.setCurrentItem(None)
        self.app.ui.PropertiesTemplatesListWidget.setCurrentItem(it)
        self.app.ui.CancelEquipmentButton.click()
        self.load_property_from_settings()

    def save_property_template(self) -> None:
        table = self.app.ui.PropertiesEditTableWidget
        stackedwidget = self.app.ui.PropertiesTemplatesStackedWidget
        listwidget = self.app.ui.PropertiesTemplatesListWidget
        keyword = self.app.ui.cifKeywordLineEdit.text()
        self.save_property(table, stackedwidget, listwidget, keyword)
        self.app.refresh_combo_boxes()

    def store_predefined_templates(self) -> None:
        property_list = self.settings.get_properties_list() or []
        for item in predef_prop_templ:
            if item['name'] not in property_list:
                self.settings.save_settings_list('property', item['name'], item['values'])

    def export_property_template(self, filename: str = '') -> None:
        """
        Exports the currently selected property entry to a file.
        """
        if not self.selected_template_name():
            return
        prop_data = self.settings.load_settings_list('property', self.selected_template_name())
        table_data = []
        cif_key = ''
        if prop_data:
            cif_key = prop_data[0]
            with suppress(Exception):
                table_data = prop_data[1]
        if not cif_key:
            return
        doc = cif.Document()
        blockname = '__'.join(self.selected_template_name().split())
        block = doc.add_new_block(blockname)
        try:
            loop = block.init_loop(cif_key, [''])
        except RuntimeError:
            # Not a valid loop key
            show_general_warning('"{}" is not a valid cif keyword.'.format(cif_key))
            return
        for value in table_data:
            if value:
                loop.add_row([cif.quote(utf8_to_str(value))])
        if not filename:
            filename = cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).resolve()))

    def selected_template_name(self):
        return self.app.ui.PropertiesTemplatesListWidget.currentIndex().data()

    def import_property_from_file(self, filename: str = '') -> None:
        """
        Imports a cif file as entry of the property templates list.
        """
        if not filename:
            filename = cif_file_open_dialog(filter="CIF file (*.cif)")
        if not filename:
            return
        doc = read_document_from_cif_file(filename)
        if not doc:
            return
        for block in doc:
            self._import_block(block)
        self.show_properties()

    def _import_block(self, block: cif.Block) -> None:
        property_list = self.settings.settings.value('property_list')
        if not property_list:
            property_list = ['']
        template_list = []
        loop_column_name = ''
        for i in block:
            if i.loop is not None:
                if len(i.loop.tags) > 0:
                    loop_column_name = i.loop.tags[0]
                for n in range(i.loop.length()):
                    value = i.loop.val(n, 0)
                    template_list.append(retranslate_delimiter(cif.as_string(value).strip("\n\r ;")))
        block_name = block.name.replace('__', ' ')
        # This is the list shown in the Main menu:
        property_list.append(block_name)
        table = self.app.ui.PropertiesEditTableWidget
        table.setRowCount(0)
        self.app.ui.cifKeywordLineEdit.setText(loop_column_name)
        newlist = [x for x in list(set(property_list)) if x]
        newlist.sort()
        # this list keeps track of the property items:
        self.settings.save_template_list('property_list', newlist)
        template_list.insert(0, '')
        template_list = list(set(template_list))
        # save as dictionary for properties to have "_cif_key : itemlist"
        # for a table item as dropdown menu in the main table.
        table_data = [loop_column_name, template_list]
        self.settings.save_template_list('property/' + block_name, table_data)

    def load_property_from_settings(self) -> None:
        """
        Load/Edit the value list of a property entry.
        """
        table = self.app.ui.PropertiesEditTableWidget
        listwidget = self.app.ui.PropertiesTemplatesListWidget
        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            # self.app.ui.PropertiesEditTableWidget.blockSignals(False)
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_settings_list('property', selected_row_text)
        if table_data:
            cif_key = table_data[0]
            with suppress(Exception):
                table_data = table_data[1]
            self.app.ui.cifKeywordLineEdit.setText(cif_key)
        if not table_data:
            table_data = ['', '', '']
        for value in table_data:
            try:
                self.add_propeties_row(table, retranslate_delimiter(str(value)))
            except TypeError:
                print('Bad value in property table')
                continue
        self.add_propeties_row(table, '')
        self.app.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(1)
        table.blockSignals(False)
        # table.setWordWrap(False)
        table.resizeRowsToContents()

    def export_raw_data(self) -> List[Dict]:
        properties_list = []
        for property in self.settings.get_properties_list():
            if property:
                property_name, property_data  = self.settings.load_settings_list('property', item_name=property)
                properties_list.append({'name': property_name, 'data': property_data})
        return properties_list

    def import_raw_data(self, properties_list: List[Dict]) -> None:
        for property in properties_list:
            self.settings.save_settings_list('property', property.get('name'), property.get('data'))
        self.show_properties()

    @staticmethod
    def add_propeties_row(table: QTableWidget, value: str = '') -> None:
        """
        Add a new row with a value to the Property table.
        """
        # Create a empty row at bottom of table
        row_num = table.rowCount()
        table.insertRow(row_num)
        # Add cif key and value to the row:
        # item_val = MyTableWidgetItem(value)
        # table.setItem(row_num, 0, item_val)
        key_item = PlainTextEditTemplate(parent=table)
        key_item.textChanged.connect(lambda: table.resizeRowsToContents())
        key_item.setPlainText(value)
        ## This is critical, because otherwise the add_row_if_needed does not work as expected:
        # key_item.textChanged.connect(self.add_row_if_needed)
        table.setCellWidget(row_num, 0, key_item)

    def save_property(self, table: QTableWidget,
                      stackwidget: QStackedWidget,
                      listwidget: QListWidget,
                      keyword: str = '') -> None:
        """
        Saves the currently selected Property template to the config file.
        """
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        selected_template_text = listwidget.currentIndex().data()
        table_data = []
        ncolumns = table.rowCount()
        for rownum in range(ncolumns):
            try:
                # only one column!
                value = table.cellWidget(rownum, 0).getText()
            except AttributeError:
                value = ''
            if value:
                table_data.append(value)
        # make sure to have always a blank item first:
        table_data.insert(0, '')
        if keyword:
            # save as dictionary for properties to have "_cif_key : itemlist"
            # for a table item as dropdown menu in the main table.
            table_data = [keyword, table_data]
        self.settings.save_template_list('property/' + selected_template_text, table_data)
        stackwidget.setCurrentIndex(0)
        print('saved')

    def cancel_property_template(self) -> None:
        """
        Cancel editing of the current template.
        """
        table = self.app.ui.PropertiesEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.app.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)


if __name__ == '__main__':
    l = Properties(None, FinalCifSettings())
    for line in l.export_raw_data():
        print(f"{line}")
