import unittest

from equip_property.loop_templates import LoopTemplates
from tools.settings import FinalCifSettings


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = FinalCifSettings()

    def test_something(self):
        l = LoopTemplates('foo', self.settings)
        l.store_predefined_templates()
        t = self.settings.load_template('loops/' + 'Publication Details') or {}
        self.assertEqual(t, {'keys'  : ['_publ_author_name',
                                        '_publ_section_title',
                                        '_journal_name_full',
                                        '_journal_year',
                                        '_journal_volume',
                                        '_journal_issue',
                                        '_journal_page_first',
                                        '_journal_page_last',
                                        '_journal_paper_doi'],
                             'name'  : 'Publication Details',
                             'values': None})


if __name__ == '__main__':
    unittest.main()
