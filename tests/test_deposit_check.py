from unittest import TestCase

from cif.cif_file_io import CifContainer
from cif.cod.deposit_check import DepositCheck


class TestDepositCheck(TestCase):
    def test_test_for_prepublication_one_missing_item(self):
        status = DepositCheck(CifContainer('test-data/1000007.cif')).list_missing_for_prepublication()
        self.assertEqual([], status)

    def test_test_for_prepublication_one_missing_item_bool(self):
        status = DepositCheck(CifContainer('test-data/1000007.cif')).is_complete_for_prepublication()
        self.assertEqual(True, status)

    def test_test_for_prepublication_one_missing_item_bool2(self):
        status = DepositCheck(CifContainer('test-data/1000006.cif')).is_complete_for_prepublication()
        self.assertEqual(False, status)

    def test_test_for_prepublication_no_missing_item_bool(self):
        status = DepositCheck(CifContainer('test-data/4060308.cif')).list_missing_for_prepublication()
        self.assertEqual([], status)