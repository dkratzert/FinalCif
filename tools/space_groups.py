#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path

import gemmi

from testing2 import spgrps
from tools.misc import isnumeric


class SpaceGroups():

    def __init__(self):
        self.spgrps = spgrps

    def to_mathml(self, space_group: str) -> str:
        pass

    def to_html(self, space_group: str, number: str) -> str:
        txt = self._to_html_without_body(space_group)
        return '<body style="">{} &thinsp;({})</body>'.format(txt, number)

    def to_plain_text(self, space_group: str) -> str:
        return ''.join([x[0] for x in self.spgrps[space_group]])

    def _to_html_without_body(self, space_group: str) -> str:
        html = ''
        if not space_group:
            return ''
        for word in self.spgrps[space_group][0]:
            char, format = word
            if format == 'italic':
                html = html + '<i>{}</i>'.format(char)
            elif format == 'regular':
                html = html + char
            elif format == 'sub':
                html = html + '<sub>{}</sub>'.format(char)
            elif format == 'overline':
                html = html + '<span style=" text-decoration: overline;">{}</span>'.format(char)
            else:
                print('##############', char)
        return html

    def old_to_html(self, number):
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

    def get_screw(self, symbol: str):
        sub = '{}<sub>{}</sub>'.format(symbol[0], symbol[1])
        return {'21': sub, '31': sub, '32': sub, '41': sub, '42': sub, '43': sub,
                '61': sub, '62': sub, '63': sub, '64': sub, '65': sub, }.get(symbol)

    def get_screw_format(self, symbol: str):
        sub = '("{}", "regular"), \n("{}", "sub"),\n'.format(symbol[0], symbol[1])
        return {'21': sub, '31': sub, '32': sub, '41': sub, '42': sub, '43': sub,
                '61': sub, '62': sub, '63': sub, '64': sub, '65': sub, }.get(symbol)

    def test_htmlout(self):
        # special: P 21212(a)
        htxt = ''
        for s in gemmi.spacegroup_table():
            s: gemmi.SpaceGroup
            html = []
            splitted_s = s.xhm().split(' ')
            html.append(str(s.number) + s.qualifier + ' ->')
            print('{}:{}'.format(s.number, s.qualifier), s.short_name(), splitted_s)
            html.append('<i>{}</i>'.format(splitted_s.pop(0)))
            if s.short_name() == 'P21212(a)':
                # This one is differently formated as the others in gemmi:
                html.append('2<sub>1</sub>2<sub>1</sub>2<sub>1</sub>2 (a)')
                # print('{}:{}'.format(s.number, s.qualifier), s.short_name(), splitted_s)
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
                    if len(c) == 2 and self.get_screw(c):
                        html.append(self.get_screw(c))
                    if len(c) == 2 and not self.get_screw(c):
                        if c.startswith('-'):
                            html.append('<span style=" text-decoration: overline;">{}</span>'.format(c[-1]))
                        else:
                            self.italize_chars(c, html)
                    if len(c) > 2:
                        txt = []
                        if self.get_screw(c[:2]):
                            html.append(self.get_screw(c[:2]))
                            c = c[2:]
                        for char in c:
                            self.make_italic(char, txt)
                        html.append(''.join(txt))
            # print(len(splitted_s) + 1 - len(html))
            print(html)
            htxt = htxt + ''.join(html) + '<br>\n'
            Path('testing.html').write_text(htxt)
            print('---------------\n')

    def myshort(self, s):
        return ''.join([x for x in s.xhm().split(' ') if x != '1']).split(':')[0]

    def test_generalout(self):
        # special: P 21212(a)
        htxt = 'spgrps = {\n'
        for s in gemmi.spacegroup_table():
            s: gemmi.SpaceGroup
            html = []
            splitted_s = s.xhm().split(' ')
            # html.append(str(s.number)+ s.qualifier + ' ->')
            if s.short_name() == self.myshort(s):
                splitted_s = [x for x in s.xhm().split(':')[0].split(' ') if x != '1']
                print('short:', s.short_name(), self.myshort(s))
            else:
                pass
            # print('{}:"{}"'.format(s.number, s.ext), s.short_name(), splitted_s, s.xhm(), '#'+s.ext)
            html.append('"{}": (\n(("{}", "italic"),\n'.format(s.xhm(), splitted_s.pop(0)))
            if s.short_name() == 'P21212(a)':
                # This one is differently formated as the others in gemmi:
                html.append('("2", "regular"),\n ("1" ,"sub"),\n ("2", "regular"),\n ("1", "sub"),\n ("2", "regular"),'
                            '\n ("1", "sub"),\n ("2(a)", "regular"),\n')
                # print('{}:{}'.format(s.number, s.qualifier), s.short_name(), splitted_s)
            else:
                for num, c in enumerate(splitted_s):
                    if ':' in c:
                        c, append = c.split(':')
                        if c.startswith('-'):
                            html.append('({}, "overline"),\n'.format(c[-1]))
                        else:
                            self.italize_chars_format(c, html)
                        self.italize_chars_format(':' + append, html)
                        continue
                    if len(c) == 1:
                        if isnumeric(c):
                            html.append("('{}', 'regular'),\n".format(c))
                        else:
                            html.append('("{}", "italic"),\n'.format(c))
                    if len(c) == 2 and self.get_screw(c):
                        html.append(self.get_screw_format(c))
                    if len(c) == 2 and not self.get_screw(c):
                        if c.startswith('-'):
                            html.append('("{}", "overline"),\n'.format(c[-1]))
                        else:
                            self.italize_chars_format(c, html)
                    if len(c) > 2:
                        txt = []
                        if self.get_screw(c[:2]):
                            html.append(self.get_screw_format(c[:2]))
                            c = c[2:]
                        for char in c:
                            self.make_italic_format(char, txt)
                        html.append("{}".format(''.join(txt)))
                    # html.append(',\n')
            # print(len(splitted_s) + 1 - len(html))
            # print(html)
            htxt = htxt + ''.join(html) + "),\n {{'itnumber': {}, 'crystal_system': '{}', " \
                                          "'hm':'{}', 'short-hm':'{}', 'is_reference':{}}},\n),\n".format(s.number,
                                                                                                          s.crystal_system_str(),
                                                                                                          s.hm,
                                                                                                          s.short_name(),
                                                                                                          s.is_reference_setting(),
                                                                                                          )
            Path('testing2.py').write_text(htxt + '\n}')
            print('---------------')

    def italize_chars(self, c, html):
        txt = []
        for char in c:
            self.make_italic(char, txt)
        html.append(''.join(txt))

    def italize_chars_format(self, c, html):
        txt = []
        for char in c:
            self.make_italic_format(char, txt)
        html.append(''.join(txt))

    def make_italic_format(self, char, txt):
        if char.isalpha():
            txt.append('("{}", "italic"),\n'.format(char))
        else:
            txt.append("('{}', 'regular'),\n".format(char))

    def make_italic(self, char, txt):
        if char.isalpha():
            txt.append('<i>{}</i>'.format(char))
        else:
            txt.append(char)


if __name__ == '__main__':
    sp = SpaceGroups()
    # s.test_generalout()

    # p = s.to_html(gemmi.find_spacegroup_by_name('P-1').xhm())
    # print(p)
    txt = ''
    # for n in range(1, 331):
    #    txt = txt + s.iucr_num_to_html(n) + '<br>\n'

    # Path('testing.html').write_text(txt)

    for s in gemmi.spacegroup_table():
        p = sp.to_html(s.xhm(), s.number)
        print(p)
        txt = txt + p + '<br>\n'

    Path('testing.html').write_text(txt)
