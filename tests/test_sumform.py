import unittest

from tools.sumformula import formula_str_to_dict, sum_formula_to_html


class MyTestCase(unittest.TestCase):

    def test_sumform1(self):
        self.assertEqual({'S': '', 'Sn': ''}, formula_str_to_dict("SSn"))

    def test_sumform2(self):
        self.assertEqual({'S': '1', 'Cl': ''}, formula_str_to_dict("S1Cl"))

    def test_sumform3(self):
        self.assertEqual({'C': '12', 'H': '6', 'O': '3', 'Mn': '7'}, formula_str_to_dict("C12H6O3Mn7"))

    def test_sumform4(self):
        self.assertEqual({'C': '12', 'H': '60', 'O': '3', 'Mn': '7'}, formula_str_to_dict("C12 H60 O3 Mn7"))

    def test_sumform5(self):
        self.assertEqual({'C': '12', 'H': '60', 'O': '3', 'Mn': '7'}, formula_str_to_dict("C12 H60 O3  Mn 7"))

    def test_sumform6(self):
        self.assertEqual({'C': '13', 'Cs': '12', 'H': '60', 'O': '3', 'Mn': '7'},
                         formula_str_to_dict("C13Cs12 H60 O3  Mn 7"))

    def test_sumform7(self):
        self.assertEqual({'C': '', 'H': '', 'Mn': ''}, formula_str_to_dict("CHMn\n"))

    def test_sumform8(self):
        with self.assertRaises(KeyError):
            formula_str_to_dict("Hallo")

    def test_sumform9(self):
        with self.assertRaises(KeyError):
            formula_str_to_dict("H3O+")

    def test_sumform10(self):
        self.assertEqual({'C': '4', 'H': '2.91', 'Al': '0.12', 'F': '4.36', 'Ni': '0.12', 'O': '0.48'},
                         formula_str_to_dict('C4 H2.91 Al0.12 F4.36 Ni0.12 O0.48'))

    def test_sumform11(self):
        with self.assertRaises(KeyError):
            formula_str_to_dict('C4H6O1*5H2O')


class TestSumformHTLM(unittest.TestCase):

    def test_sumform_to_html(self):
        self.assertEqual('<html><body>C<sub>12 </sub>H<sub>6 </sub>O<sub>3 </sub>Mn<sub>7 </sub></body></html>',
                         sum_formula_to_html({'C': 12, 'H': 6, 'O': 3, 'Mn': 7}))


if __name__ == '__main__':
    unittest.main()
