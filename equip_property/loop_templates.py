#from appwindow import AppWindow
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
                     'values': None
                     },
                    ]


class LoopTemplates():
    def __init__(self, app: 'AppWindow', settings: FinalCifSettings):
        self.app = app
        self.settings = settings

    def load_default_loops(self):
        self.store_predefined_templates()
        #self.show_loops()

    def store_predefined_templates(self):
        loops_list = self.settings.settings.value('loops_list') or []
        for item in predefined_loops:
            if not item['name'] in loops_list:
                loops_list.append(item['name'])
                newlist = [x for x in list(set(loops_list)) if x]
                # this list keeps track of the loop items:
                self.settings.save_template('loops_list', newlist)
                self.settings.save_loop_template('loops/' + item['name'], item)

    def load_selected_loop(self):
        plist = self.settings.load_template('loops/' + 'Publication Details') or {}
        print(plist)