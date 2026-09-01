import unittest

from finalcif.tools.sumformula import (formula_str_to_dict, formula_to_html, sum_formula_to_html,
                                       with_solvent_marker)


class MyTestCase(unittest.TestCase):

    def test_sumform1(self):
        self.assertEqual({'S': 1.0, 'Sn': 1.0}, formula_str_to_dict("SSn"))

    def test_sumform2(self):
        self.assertEqual({'Cl': 1.0, 'S': 1.0}, formula_str_to_dict("S1Cl"))

    def test_sumform3(self):
        self.assertEqual({'C': 12.0, 'H': 6.0, 'Mn': 7.0, 'O': 3.0}, formula_str_to_dict("C12H6O3Mn7"))

    def test_sumform4(self):
        self.assertEqual({'C': 12.0, 'H': 60.0, 'Mn': 7.0, 'O': 3.0}, formula_str_to_dict("C12 H60 O3 Mn7"))

    def test_sumform5(self):
        self.assertEqual({'C': 12.0, 'H': 60.0, 'Mn': 7.0, 'O': 3.0}, formula_str_to_dict("C12 H60 O3  Mn 7"))

    def test_sumform6(self):
        self.assertEqual({'C': 13.0, 'Cs': 12.0, 'H': 60.0, 'Mn': 7.0, 'O': 3.0},
                         formula_str_to_dict("C13Cs12 H60 O3  Mn 7"))

    def test_sumform7(self):
        self.assertEqual({'C': 1.0, 'H': 1.0, 'Mn': 1.0}, formula_str_to_dict("CHMn\n"))

    def test_sumform8(self):
        self.assertEqual({'Hallo': 1.0}, formula_str_to_dict("Hallo"))

    def test_sumform9(self):
        self.assertEqual({'+': 1.0, 'H': 3.0, 'O': 1.0}, formula_str_to_dict("H3O+"))

    def test_sumform10(self):
        self.assertEqual({'Al': 0.12, 'C': 4.0, 'F': 4.36, 'H': 2.91, 'Ni': 0.12, 'O': 0.48},
                         formula_str_to_dict('C4 H2.91 Al0.12 F4.36 Ni0.12 O0.48'))

    def test_sumform11(self):
        self.assertEqual({'C': 4.0, 'H': 8.0, 'O': 2.0}, formula_str_to_dict('C4H6O*5(H2O)'))

    def test_sumform12(self):
        self.assertEqual({'B': 1.0, 'C': 15.0, 'F': 2.0, 'H': 23.0, 'N': 2.0, 'O': 1.0, 'Si': 2.0},
                         formula_str_to_dict('C15 H23 B F2 N2 O Si2'))

    def test_sumform13(self):
        self.assertEqual({'B': 1.0, 'C': 15.0, 'F': 2.0, 'H': 23.0, 'N': 2.0, 'O': 1.0, 'Si': 1.0},
                         formula_str_to_dict('C15 H23 B F2 N2 O Si'))

    def test_sumform14(self):
        self.assertEqual({'B': 1.0, 'C': 15.0, 'F': 2.0, 'H': 23.0, 'I': 1.0, 'N': 2.0, 'Os': 1.0},
                         formula_str_to_dict('C15 H23 B F2 N2 Os I'))


class TestSumformHTLM(unittest.TestCase):

    def test_sumform_to_html(self):
        self.assertEqual('<html><body>C<sub>12</sub>H<sub>6</sub>O<sub>3</sub>Mn<sub>7</sub></body></html>',
                         sum_formula_to_html({'C': 12, 'H': 6, 'O': 3, 'Mn': 7}))

    def test_sumform_to_html_with_difficult_elements(self):
        self.assertEqual(
            '<html><body>C<sub>15</sub>H<sub>23</sub>BF<sub>2</sub>N<sub>2</sub>OSi<sub>2</sub></body></html>',
            sum_formula_to_html(formula_str_to_dict('C15H23BF2N2OSi2')))


class TestSqueezedSolventMarker(unittest.TestCase):
    """The '[+ solvent]' marker is prose and must not be parsed as chemistry."""

    SUM = 'C126 H111.89 Al2 B2 F73.11 N6 O9 P [+ solvent]'

    def test_marker_is_ignored_when_parsing(self):
        parsed = formula_str_to_dict(self.SUM)
        self.assertEqual(126.0, parsed['C'])
        self.assertNotIn('S', parsed)
        self.assertNotIn('V', parsed)

    def test_marker_is_appended_as_plain_text(self):
        html = with_solvent_marker(sum_formula_to_html(formula_str_to_dict(self.SUM)), self.SUM)
        self.assertTrue(html.startswith('<html><body>C<sub>126</sub>'))
        self.assertTrue(html.endswith(' [+ solvent]</body></html>'))

    def test_no_marker_is_added_without_one(self):
        formula = 'C15H23BF2N2OSi2'
        html = sum_formula_to_html(formula_str_to_dict(formula))
        self.assertEqual(html, with_solvent_marker(html, formula))

    def test_moiety_html_keeps_the_marker_unformatted(self):
        html = formula_to_html('2(C16 Al F36 O4), 1.889(C6 H6) [+ solvent]')
        self.assertEqual('<html><body>2(C<sub>16</sub>AlF<sub>36</sub>O<sub>4</sub>), '
                         '1.889(C<sub>6</sub>H<sub>6</sub>) [+ solvent]</body></html>', html)

    def test_moiety_html_normalises_a_wrapped_marker(self):
        self.assertEqual('<html><body>C<sub>6</sub>H<sub>6</sub> [+ solvent]</body></html>',
                         formula_to_html('C6 H6 [+ \nsolvent]'))


if __name__ == '__main__':
    unittest.main()
