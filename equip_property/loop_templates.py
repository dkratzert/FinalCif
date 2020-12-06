from contextlib import suppress
from typing import Union

from cif.text import quote
from gui.loops import LoopTableModel, Loop
from tools.dsrmath import my_isnumeric
from tools.misc import cif_to_header_label

with suppress(ImportError):
    from appwindow import AppWindow
from PyQt5.QtWidgets import QListWidgetItem

from tools.settings import FinalCifSettings

predefined_loops = [{'name'  : 'Publication Details',
                     'keys'  : ['_publ_author_name',
                                '_publ_section_title',
                                '_journal_name_full',
                                '_journal_year',
                                '_journal_volume',
                                '_journal_issue',
                                '_journal_page_first',
                                '_journal_page_last',
                                '_journal_paper_doi',
                                ],
                     'values': [['', '', '', '', '', '', '', '', '']]
                     },
                    ]


class LoopTemplates():
    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings
        self.load_default_loops()
        # self.app.ui.LoopTemplatesListWidget.currentRowChanged.connect(self.load_selected_loop)
        self.app.ui.LoopTemplatesListWidget.clicked.connect(self.load_selected_loop)
        self.app.ui.SaveLoopButton.clicked.connect(self.save_current_loop)

    def save_current_loop(self):
        current_loop_tab_index = self.app.ui.LoopsTabWidget.currentIndex()
        loop_model: LoopTableModel = self.app.ui.LoopsTabWidget.widget(current_loop_tab_index).model()
        print('saving loop\n', loop_model.loop_data)
        new_loop = self.app.cif.block.init_loop('', loop_model._header)
        for row in loop_model.loop_data:
            print([quote(x) for x in row], '##')
            new_loop.add_row([quote(x) for x in row])

    def save_new_value_to_cif_block(self, row: int, col: int, value: Union[str, int, float], header: list):
        column = self.app.cif.block.find_values(header[col])
        if not column:
            # in this case, the loop is new and from the GUI
            self.save_current_loop()
            column = self.app.cif.block.find_values(header[col])
        column[row] = value if my_isnumeric(value) else quote(value)

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

    def load_selected_loop(self):
        self.app.ui.LoopTemplatesListWidget.blockSignals(True)
        print('selected loop name:', self.get_selected_loop_name())
        loopdata = self.settings.load_template('loops/' + self.get_selected_loop_name()) or {}
        keys = loopdata.get('keys')
        values = loopdata.get('values')
        print('#####')
        print(keys)
        print(values)
        loop = Loop(keys, values=values)
        self.app.ui.LoopsTabWidget.addTab(loop.tableview, cif_to_header_label.get(keys[0]) or keys[0])
        loop.model.modelChanged.connect(self.save_new_value_to_cif_block)
        self.app.ui.revertLoopsPushButton.clicked.connect(loop.model.revert)
        self.app.ui.LoopsTabWidget.setCurrentIndex(self.app.ui.LoopsTabWidget.count() - 1)
        self.app.ui.LoopTemplatesListWidget.blockSignals(False)
