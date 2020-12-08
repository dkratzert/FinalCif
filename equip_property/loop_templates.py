from contextlib import suppress
from typing import Union

from PyQt5.QtCore import Qt

from cif.text import quote
from gui.loops import LoopTableModel, Loop
from tools.dsrmath import my_isnumeric

with suppress(ImportError):
    from appwindow import AppWindow
from PyQt5.QtWidgets import QListWidgetItem

from tools.settings import FinalCifSettings

"""
TODO: Completely different idea:
- add hard-wired form with author names, journal, etc. to start of loops page
- add a "save as template button"
- add a "delete loop" button to every loop page
- the save loop button creates a new line in the templates listwidget and asks for a name
- a click on a template entry in the listwidget fills all data into the form (and the respective loop)
- 
"""

predefined_loops = [{'name'  : 'Publication Details',
                     'keys'  : [
                         '_publ_contact_author_name',
                         '_publ_contact_author_address',
                         '_publ_contact_author_email',
                         '_publ_contact_author_phone',
                         '_publ_contact_letter',
                         '_publ_requested_journal',
                         '_publ_section_title',
                         '_publ_section_title_footnote',
                         '_publ_author_name',
                         '_publ_author_footnote',
                         '_publ_author_address',
                         '_publ_section_synopsis',
                         '_publ_section_abstract',
                         '_journal_name_full',
                         '_journal_year',
                         '_journal_volume',
                         '_journal_issue',
                         '_journal_page_first',
                         '_journal_page_last',
                         '_journal_paper_doi',
                     ],
                     'values': [['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]
                     },
                    ]


# print(len(predefined_loops[0].get('keys')), len(predefined_loops[0].get('values')[0]))


class LoopTemplates():
    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        self.load_default_loops()
        # self.app.ui.LoopTemplatesListWidget.currentRowChanged.connect(self.load_selected_loop)
        self.app.ui.LoopTemplatesListWidget.clicked.connect(self.load_selected_loop)
        self.app.ui.SaveLoopButton.clicked.connect(self.save_current_loop)
        self.app.ui.DeleteLoopButton.clicked.connect(self.delete_loop)
        self.app.ui.NewLoopTemplateButton.clicked.connect(self.new_loop)
        self.app.ui.AddRowPushButton.clicked.connect(self.add_row)
        self.app.ui.AddColumnPushButton.clicked.connect(self.add_column)

    def add_row(self):
        current_loop_tab_index = self.app.ui.LoopsTabWidget.currentIndex()
        loop_model: LoopTableModel = self.app.ui.LoopsTabWidget.widget(current_loop_tab_index).model()
        data = loop_model.loop_data
        if len(data) > 0:
            print(data)
            data.append(['',]*len(data[0]))
            loop_model._data = data

    def add_column(self):
        pass

    def delete_loop(self) -> None:
        # First delete the list entries
        index = self.app.ui.LoopTemplatesListWidget.currentIndex()
        selected_template_text = index.data()
        self.settings.delete_template('loops/' + selected_template_text)
        loops_list = self.settings.settings.value('loops_list') or []
        try:
            loops_list.remove(selected_template_text)
        except ValueError:
            pass
        self.settings.save_template('loops_list', loops_list)
        self.app.ui.LoopTemplatesListWidget.takeItem(index.row())
        self.load_default_loops()

    def save_current_loop(self):
        current_loop_tab_index = self.app.ui.LoopsTabWidget.currentIndex()
        loop_model: LoopTableModel = self.app.ui.LoopsTabWidget.widget(current_loop_tab_index).model()
        print('saving loop\n', loop_model.loop_data, loop_model._header)
        new_loop = self.app.cif.block.init_loop('', loop_model._header)
        # TODO: finish this
        loop = {'name'  : 'Publication Details',
                'keys'  : [loop_model._header],
                'values': ['']}
        # Saves loop to cif file:
        for row in loop_model.loop_data:
            print([quote(x) for x in row], '##')
            new_loop.add_row([quote(x) for x in row])
        # Saves loop to Template:
        self.settings.save_loop_template('loops/' + self.get_selected_loop_name()
                                         , loop)

    def new_loop(self) -> None:
        item = QListWidgetItem('')
        self.app.ui.LoopTemplatesListWidget.addItem(item)
        self.app.ui.LoopTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.app.ui.LoopTemplatesListWidget.editItem(item)

    def save_new_value_to_cif_block(self, row: int, col: int, value: Union[str, int, float], header: list):
        column = self.app.cif.block.find_values(header[col])
        if not column:
            # in this case, the loop is new and from the GUI
            self.save_current_loop()
            column = self.app.cif.block.find_values(header[col])
        column[row] = value if my_isnumeric(value) else quote(value) #if value else '.'

    def load_default_loops(self):
        self.store_predefined_templates()
        self.show_loops()

    def show_loops(self):
        l = self.settings.get_loops_list()
        for loop in l:
            if loop:
                item = QListWidgetItem(loop)
                self.app.ui.LoopTemplatesListWidget.addItem(item)

    def store_predefined_templates(self):
        loops_list = self.settings.settings.value('loops_list') or []
        for item in predefined_loops:
            if not item.get('values'):
                continue
            if not item['name'] in loops_list:
                loops_list.append(item['name'])
                newlist = [x for x in list(set(loops_list)) if x]
                # this list keeps track of the loop items:
                self.settings.save_template('loops_list', newlist)
                self.settings.save_loop_template('loops/' + item['name'], item)

    def get_selected_loop_name(self) -> str:
        listwidget = self.app.ui.LoopTemplatesListWidget
        selected_row_text = listwidget.currentIndex().data()
        if not selected_row_text:
            return ''
        return selected_row_text

    def _get_tabwidget_headers(self):
        headers = []
        num_headers = self.app.ui.LoopsTabWidget.count()
        for i in range(num_headers):
            tabtext = self.app.ui.LoopsTabWidget.tabText(i)
            headers.append(tabtext)
        return headers

    def load_selected_loop(self):
        headers = self._get_tabwidget_headers()
        self.app.ui.LoopTemplatesListWidget.blockSignals(True)
        print('selected loop name:', self.get_selected_loop_name())
        loopdata = self.settings.load_template('loops/' + self.get_selected_loop_name()) or {
            'name'  : self.get_selected_loop_name(),
            'keys'  : ['', ],
            'values': [['', ]]
        }
        keys = loopdata.get('keys')
        values = loopdata.get('values')
        tab_header = self.get_selected_loop_name()
        # print('#####')
        # print(keys)
        # print(values)
        if tab_header in headers:
            # Do not add loops twice
            return
        loop = Loop(keys, values=values)
        self.app.ui.LoopsTabWidget.addTab(loop.tableview, tab_header)
        loop.model.modelChanged.connect(self.save_new_value_to_cif_block)
        self.app.ui.revertLoopsPushButton.clicked.connect(loop.model.revert)
        self.app.ui.LoopsTabWidget.setCurrentIndex(self.app.ui.LoopsTabWidget.count() - 1)
        self.app.ui.LoopTemplatesListWidget.blockSignals(False)
