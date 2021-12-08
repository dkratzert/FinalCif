#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

from contextlib import suppress
from pathlib import Path

import gemmi

from finalcif.tools.misc import isnumeric
from finalcif.tools.spgr_format import spgrps


class SpaceGroups():

    def __init__(self):
        self.spgrps = spgrps

    def to_mathml(self, space_group: str) -> str:
        """
        Uses the general format dictionary to format a space group as mathml:

        '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                    '<mi>P</mi>'
                    '<mover>'
                    '<mn>6</mn>'
                    '<mo stretchy="false">&#x0305;</mo>'
                    '</mover>'
                    '<mn>c</mn>'
                    '<mn>2</mn>'
                    '</math>'
        """
        if not space_group:
            return ''
        xml = '<math xmlns="http://www.w3.org/1998/Math/MathML">\n'
        sp = self.spgrps[space_group][0]
        overline = False
        sub = False
        for n, word in enumerate(sp):
            char, spgr_format = word
            if len(sp) >= n + 1:
                with suppress(Exception):
                    if sp[n][1] == 'overline':
                        overline = True
                    if sp[n + 1][1] == 'sub':
                        sub = True
                        xml = xml + '<msub>\n'
            if overline:
                overline = False
                xml = xml + '<mover>\n<mn>{}</mn>\n<mo stretchy="false">&#x0305;</mo>'.format(char)
            if not overline and spgr_format == 'overline':
                xml = xml + '\n</mover>\n'
            if spgr_format == 'regular':
                xml = xml + '<mn>{}</mn>\n'.format(char)
            if spgr_format == 'italic':
                xml = xml + '<mi>{}</mi>\n'.format(char)
            if sub and spgr_format == 'sub':
                xml = xml + '<mn>{}</mn>\n</msub>\n'.format(char)
        xml = xml + '</math>\n'
        return xml

    def to_html(self, space_group: str) -> str:
        if not space_group:
            return ''
        txt = self._to_html_without_body(space_group)
        return '<body style="">{} &thinsp;({})</body>'.format(txt, self.spgrps[space_group][1].get('itnumber'))

    def to_plain_text(self, space_group: str) -> str:
        """
        Uses the general format dictionary to format a space group as plain text.
        """
        if not space_group:
            return ''
        return ''.join([x[0] for x in self.spgrps[space_group][0]])

    def _to_html_without_body(self, space_group: str) -> str:
        """
        Uses the general format dictionary in order to output a space group as html.
        """
        html = ''
        if not space_group:
            return ''
        for word in self.spgrps[space_group][0]:
            char, space_group_format = word
            if space_group_format == 'italic':
                html = html + '<i>{}</i>'.format(char)
            elif space_group_format == 'regular':
                html = html + char
            elif space_group_format == 'sub':
                html = html + '<sub>{}</sub>'.format(char)
            elif space_group_format == 'overline':
                html = html + '<span style=" text-decoration: overline;">{}</span>'.format(char)
            else:
                print('##############', char)
        return html

    def _general_format_out(self):
        """
        Writes out a python file with a dictionary of a general format definition of all space groups.
        """
        Path('testing2.py').unlink(missing_ok=True)
        htxt = 'spgrps = {\n'
        for space_group_obj in gemmi.spacegroup_table():
            space_group_obj: gemmi.SpaceGroup
            html = []
            splitted_spgr = space_group_obj.xhm().split(' ')
            if space_group_obj.short_name() == self._myshort(space_group_obj):
                splitted_spgr = self.remove_setting(space_group_obj)
            html.append("    '{}'         : (\n        (('{}', 'italic'),\n".format(space_group_obj.xhm(),
                                                                                    splitted_spgr.pop(0)))
            if space_group_obj.short_name() == 'P21212(a)':
                self.handle_p21212a_specially(html)
            else:
                for num, chars in enumerate(splitted_spgr):
                    if ':' in chars:
                        chars, append = chars.split(':')
                        if chars.startswith('-'):
                            html.append("            ({}, 'overline'),\n".format(chars[-1]))
                        else:
                            self._italize_chars_format(chars, html)
                        self._italize_chars_format(':' + append, html)
                        continue
                    if len(chars) == 1:
                        if isnumeric(chars):
                            html.append("         ('{}', 'regular'),\n".format(chars))
                        else:
                            html.append("         ('{}', 'italic'),\n".format(chars))
                    if len(chars) == 2 and self._get_screw(chars):
                        html.append(self._get_screw_format(chars))
                    if len(chars) == 2 and not self._get_screw(chars):
                        if chars.startswith('-'):
                            html.append("         ('{}', 'overline'),\n".format(chars[-1]))
                        else:
                            self._italize_chars_format(chars, html)
                    if len(chars) > 2:
                        txt = []
                        if self._get_screw(chars[:2]):
                            html.append(self._get_screw_format(chars[:2]))
                            chars = chars[:]
                        for chars in chars:
                            self._make_italic_format(chars, txt)
                        html.append("{}".format(''.join(txt)))
            htxt = htxt + ''.join(html) \
                   + "         ), {{'itnumber': {}, 'crystal_system': '{}', " \
                     "'short-hm': '{}', 'is_reference': {}}},\n    ),\n".format(space_group_obj.number,
                                                                                space_group_obj.crystal_system_str(),
                                                                                space_group_obj.short_name(),
                                                                                space_group_obj.is_reference_setting(),
                                                                                )
        Path('testing2.py').write_text(htxt + '\n}')

    def remove_setting(self, space_group_obj):
        return [x for x in space_group_obj.xhm().split(':')[0].split(' ') if x != '1']

    def handle_p21212a_specially(self, html):
        # This one is differently formated as the others in gemmi:
        html.append("('2', 'regular'),\n ('1' ,'sub'),\n ('2', 'regular'),\n ('1', 'sub'),\n ('2', 'regular'),"
                    "\n ('1', 'sub'),\n ('2(a)', 'regular'),\n")

    def _screw(self, sub_format, symbol):
        return {'21': sub_format, '31': sub_format, '32': sub_format, '41': sub_format, '42': sub_format,
                '43': sub_format, '61': sub_format, '62': sub_format, '63': sub_format, '64': sub_format,
                '65': sub_format, }.get(symbol)

    def _get_screw(self, symbol: str):
        sub = '{}<sub>{}</sub>'.format(symbol[0], symbol[1])
        return self._screw(sub, symbol)

    def _get_screw_format(self, symbol: str):
        sub = "         ('{}', 'regular'), \n         ('{}', 'sub'),\n".format(symbol[0], symbol[1])
        return self._screw(sub, symbol)

    def _myshort(self, s):
        return ''.join([x for x in s.xhm().split(' ') if x != '1']).split(':')[0]

    def _italize_chars(self, c, html):
        txt = []
        for char in c:
            self._make_italic(char, txt)
        html.append(''.join(txt))

    def _make_italic(self, char, txt):
        if char.isalpha():
            txt.append('<i>{}</i>'.format(char))
        else:
            txt.append(char)

    def _italize_chars_format(self, c, html):
        txt = []
        for char in c:
            self._make_italic_format(char, txt)
        html.append(''.join(txt))

    def _make_italic_format(self, char, txt):
        if char.isalpha():
            txt.append("         ('{}', 'italic'),\n".format(char))
        else:
            txt.append("         ('{}', 'regular'),\n".format(char))


##########################
# For testing purposes:

def wite_xml():
    sp = SpaceGroups()
    txt = ''
    for s in gemmi.spacegroup_table():
        print(s.number, s.short_name())
        p = sp.to_mathml(s.xhm())
        print(p)
        txt = txt + '{} {}\n'.format(s.number, s.short_name())
        txt = txt + p + '\n'
    Path('testing_xml.html').write_text(txt)


def write_html():
    s = SpaceGroups()
    txt = ''
    for sp in gemmi.spacegroup_table():
        txt = txt + s.to_html(sp.xhm()) + '<br>\n'
    Path('testing.html').write_text(txt)


if __name__ == '__main__':
    s = SpaceGroups()
    s._general_format_out()

    # write_html()
    # wite_xml()
