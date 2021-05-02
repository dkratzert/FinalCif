from unittest import TestCase

from cif.cod.deposit import COD_Deposit


class TestCOD_Deposit(TestCase):

    def setUp(self) -> None:
        pass
        # self.cod = COD_Deposit(None, CifContainer('tests/examples/1979688.cif'))

    def test__deposition_type_to_int_personal(self):
        self.assertEqual(0, COD_Deposit.deposition_type_to_int('personal'))

    def test__deposition_type_to_int_prepublication(self):
        self.assertEqual(1, COD_Deposit.deposition_type_to_int('prepublication'))

    def test__deposition_type_to_int_published(self):
        self.assertEqual(2, COD_Deposit.deposition_type_to_int('published'))

    def test__deposition_type_to_int_deposit(self):
        self.assertEqual(3, COD_Deposit.deposition_type_to_int('deposit'))
