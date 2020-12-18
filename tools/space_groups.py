#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

import gemmi

from tools.misc import isnumeric


class SpaceGroups():
    def iucrNumberToMathml(self, number: Union[int, str]) -> str:
        number = str(number)
        return self.spgrps[number][0]

    def iucrNumberToPlainText(self, number: Union[int, str]) -> str:
        number = str(number)
        return self.spgrps[number][1]

    def _to_html_without_body(self, number: Union[int, str]) -> str:
        """
        Retrurns the space group als html formated for rich-text Qt text fields. Overlined numbers seem
        not to be possible...

        >>> SpaceGroups().iucr_num_to_html(14)
        '<body><i>P</i>2<sub>1</sub>/c</body>'
        """
        num = str(number)
        mxml = self.spgrps.get(num)[0]
        root = ET.fromstring(mxml)
        txt = ''
        for root_element in root:
            substart = False
            if root_element.text:
                if root_element.tag.endswith('mi'):
                    txt = txt + "<i>{}</i>".format(root_element.text)
                elif root_element.tag.endswith('mn'):
                    if isnumeric(root_element.text) or root_element.text == '/':
                        txt = txt + root_element.text
                    else:
                        txt = txt + "<i>{}</i>".format(root_element.text)
            for sub_element in root_element:
                if sub_element.text:
                    if sub_element.tag.endswith('mo'):
                        # I do this shift, because the overline shifts from right to left ofer the number:
                        txt = '{}<span style=" text-decoration: overline;">{}</span>'.format(txt[:-1], txt[-1])
                    elif sub_element.tag.endswith('mn') and sub_element.text in ['1', '2', '3'] \
                        and root_element.tag.endswith('msub') and substart:
                        txt = txt + "<sub>{}</sub>".format(sub_element.text)
                    else:
                        txt = txt + sub_element.text
                        if root_element.tag.endswith('msub') and not substart:
                            substart = True
        return txt

    def iucr_num_to_html(self, number: Union[int, str]) -> str:
        txt = self._to_html_without_body(number)
        return '<body style="">{} &thinsp;({})</body>'.format(txt, number)

    def is_screw(self, symbol: str):
        sub = '{}<sub>{}</sub>'.format(symbol[0], symbol[1])
        return {'21': sub, '31': sub, '32': sub, '41': sub, '42': sub, '43': sub,
                '61': sub, '62': sub, '63': sub, '64': sub, '65': sub, }.get(symbol)

    def test_new(self):
        # special: P 21212(a)
        htxt = ''
        for s in gemmi.spacegroup_table():
            s: gemmi.SpaceGroup
            html = []
            splitted_s = s.xhm().split(' ')
            html.append(str(s.number)+ s.qualifier + ' ->')
            print('{}:{}'.format(s.number, s.qualifier), s.short_name(), splitted_s)
            html.append('<i>{}</i>'.format(splitted_s.pop(0)))
            if s.short_name() == 'P21212(a)':
                html.append('2<sub>1</sub>2<sub>1</sub>2<sub>1</sub>2 (a)')
                #print('{}:{}'.format(s.number, s.qualifier), s.short_name(), splitted_s)
            else:
                for num, c in enumerate(splitted_s):
                    if ':' in c:
                        c, append = c.split(':')
                        if c.startswith('-'):
                            html.append('<span style=" text-decoration: overline;">{}</span>'.format(c[-1]))
                        else:
                            self.italize_chars(c, html)
                        self.italize_chars(':' + append, html)
                        continue
                    if len(c) == 1:
                        if isnumeric(c):
                            html.append(c)
                        else:
                            html.append('<i>{}</i>'.format(c))
                    if len(c) == 2 and self.is_screw(c):
                        html.append(self.is_screw(c))
                    if len(c) == 2 and not self.is_screw(c):
                        if c.startswith('-'):
                            html.append('<span style=" text-decoration: overline;">{}</span>'.format(c[-1]))
                        else:
                            self.italize_chars(c, html)
                    if len(c) > 2:
                        txt = []
                        if self.is_screw(c[:2]):
                            html.append(self.is_screw(c[:2]))
                            c = c[2:]
                        for char in c:
                            self.make_italic(char, txt)
                        html.append(''.join(txt))
            #print(len(splitted_s) + 1 - len(html))
            print(html)
            htxt = htxt + ''.join(html) + '<br>\n'
            Path('testing.html').write_text(htxt)
            print('---------------\n')

    def italize_chars(self, c, html):
        txt = []
        for char in c:
            self.make_italic(char, txt)
        html.append(''.join(txt))

    def make_italic(self, char, txt):
        if char.isalpha():
            txt.append('<i>{}</i>'.format(char))
        else:
            txt.append(char)


if __name__ == '__main__':
    s = SpaceGroups()
    s.test_new()
    # txt = ''
    # for n in range(1, 331):
    #    txt = txt + s.iucr_num_to_html(n) + '<br>\n'

    # Path('testing.html').write_text(txt)
