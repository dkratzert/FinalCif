import unittest

from finalcif.tools.sumformula import formula_str_to_dict, sum_formula_to_html


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


if __name__ == '__main__':
    unittest.main()
