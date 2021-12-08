from html.parser import HTMLParser
from typing import List, Dict, Union


class MyCODStructuresParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._table_row = 0
        self._table_body = False
        self._tag = ''
        self._structure = self.init_structure()
        self.structures: List = []
        self._column = 0
        self.token = ''

    def __repr__(self):
        txt = ''
        for st in self.structures:
            txt = txt + 'https://www.crystallography.net/cod/information_card.php?id={0}&CODSESSION={1}\n' \
                .format(st['number'], self.token)
        return txt

    def init_structure(self) -> Dict[str, Union[str, None]]:
        return {'number': None, 'date': None, 'time': None}

    def handle_starttag(self, tag: str, attrs: str):
        # print("Encountered a start tag:", tag, '->', attrs)
        attr = ''
        if len(attrs) > 0 and len(attrs[0]) > 1:
            attr = attrs[0][1]
        attrs_have_session_id = (tag == 'a' and 'CODSESSION' in attr and 'manage_depositions' in attr)
        if attrs_have_session_id:
            self.token = attr.split('=')[-1]
        if tag == 'tr' and self._table_body:
            self._table_row += 1
        if self._table_row > 0 and tag == 'td':
            self._tag = 'td'
        if tag == 'tbody':
            self._table_body = True

    def handle_endtag(self, tag: str):
        # end of table row, reset parser:
        table_row_ends = (tag == 'tr' and self._table_row > 0 and self._table_body)
        if table_row_ends:
            self.structures.append(self._structure)
            self._tag = ''
            self._column = 0
            self._structure = self.init_structure()

    def handle_data(self, data: str):
        data_is_from_table_row = (self._tag == 'td' and self._table_row > 0)
        if data_is_from_table_row:
            if self._column == 0:
                self._structure['date'] = data
                self._column += 1
                return
            if self._column == 1:
                self._structure['time'] = data
                self._column += 1
                return
            if self._column == 2:
                self._structure['number'] = data
                self._column += 1
