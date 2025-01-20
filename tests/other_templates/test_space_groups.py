#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import unittest

from finalcif.tools.space_groups import SpaceGroups


class TestSpaceGroups(unittest.TestCase):

    def setUp(self) -> None:
        self.s = SpaceGroups()

    def test_to_string(self):
        self.assertEqual('P1', self.s.to_plain_text('P 1'))

    def test_to_string2(self):
        self.assertEqual('I2/a', self.s.to_plain_text('I 1 2/a 1'))

    def test_to_html(self):
        self.assertEqual('<i>P</i>1', self.s.to_html('P 1'))

    def test_to_html2(self):
        self.assertEqual('<i>I</i>2/<i>a</i>', self.s.to_html('I 1 2/a 1'))

    def test_to_html_overline(self):
        self.assertEqual('<i>R</i><span style=" text-decoration: overline;">3</span><i>c</i>:<i>H</i>',
                         self.s.to_html('R -3 c:H'))

    def test_to_mathml(self):
        self.assertEqual('''<math xmlns="http://www.w3.org/1998/Math/MathML">\n<mi>P</mi>\n<mn>1</mn>\n</math>\n''',
                         self.s.to_mathml('P 1'))

    def test_to_mathml_21(self):
        self.assertEqual(
            '''<math xmlns="http://www.w3.org/1998/Math/MathML">\n<mi>P</mi>\n<msub>\n<mn>2</mn>\n<mn>1</mn>\n</msub>\n</math>\n''',
            self.s.to_mathml('P 1 21 1'))

    def test_to_mathml_overline(self):
        self.assertEqual('<math xmlns="http://www.w3.org/1998/Math/MathML">\n<mi>R</mi>\n<mover>\n<mn>3</mn>\n'
                         '<mo stretchy="false">&#x0305;</mo>\n</mover>\n<mi>c</mi>\n<mn>:</mn>\n<mi>H</mi>\n</math>\n',
                         self.s.to_mathml('R -3 c:H'))

    def test_empty_spgr_txt(self):
        self.assertEqual('', self.s.to_plain_text(''))

    def test_empty_spgr_html(self):
        self.assertEqual('', self.s.to_html(''))

    def test_empty_spgr_mathml(self):
        self.assertEqual('', self.s.to_mathml(''))


if __name__ == '__main__':
    unittest.main()
