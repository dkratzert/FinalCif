from pathlib import Path
from unittest import TestCase

from finalcif.cif.cod.website_parser import MyCODStructuresParser


class TestMyCODStructuresParser(TestCase):
    def setUp(self) -> None:
        # Imagine we have a web page from the COD with a list of structures in it
        html = Path('tests/statics/cod_struct_list.html').read_text()
        # The pasrer gets initilized
        self.parser = MyCODStructuresParser()
        # And we feed the parser with data
        self.parser.feed(html)

    def test_parse_structures_list_number(self):
        self.assertEqual(self.parser.structures[0]['number'], '3000277')
        self.assertEqual(self.parser.structures[1]['number'], '3000282')

    def test_parse_structures_list_date(self):
        self.assertEqual(self.parser.structures[0]['date'], '2020-08-20')
        self.assertEqual(self.parser.structures[1]['date'], '2020-12-11')

    def test_parse_structures_list_time(self):
        self.assertEqual(self.parser.structures[0]['time'], '13:48:46')
        self.assertEqual(self.parser.structures[1]['time'], '09:03:03')

    def test_parse_token(self):
        self.assertEqual(self.parser.token, 'foo')
