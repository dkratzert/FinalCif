import unittest
from pathlib import Path
from unittest import TestCase

from finalcif.tools.misc import to_int, to_float, this_or_quest, flatten, strip_finalcif_of_name, next_path, \
    get_error_from_value, grouper, distance, sha512_checksum_of_file, isnumeric, \
    is_database_number


class TestMisc(unittest.TestCase):

    def test_toint(self):
        self.assertEqual(1, to_int('1'))
        self.assertEqual(1, to_int('1(4)'))
        self.assertEqual(1, to_int('1.124(4)'))
        self.assertEqual(3, to_int('3.0'))
        self.assertEqual([2, 3], to_int(['1', '2', '3']))
        self.assertEqual([2, 3], to_int([1, 2, 3]))

    def test_tofloat(self):
        self.assertEqual(1.0, to_float('1'))
        self.assertEqual(1.0, to_float('1(4)'))
        self.assertEqual(1.124, to_float('1.124(4)'))
        self.assertEqual(3.0, to_float('3.0'))
        self.assertEqual([2.123, 3.0], to_float(['1', '2.123', '3']))
        self.assertEqual([2.0, 3.0], to_float([1, 2, 3]))

    def test_this_or_quest_integer(self):
        self.assertEqual(12, this_or_quest(12))

    def test_this_or_quest_None(self):
        self.assertEqual('?', this_or_quest(None))

    def test_this_or_quest_zero(self):
        self.assertEqual(0, this_or_quest(0))

    def test_this_or_quest_stringzero(self):
        self.assertEqual('0', this_or_quest('0'))

    def test_this_or_quest_emptystring(self):
        self.assertEqual('?', this_or_quest(''))

    def test_this_or_quest_zeropzero(self):
        self.assertEqual(0.0, this_or_quest(0.0))

    def test_flatten(self):
        tofl = flatten([['wer', 234, 'brdt5'], ['dfg'], [[21, 34, 5, [1, 2, 3]], ['fhg', 4]]])
        fl = ['wer', 234, 'brdt5', 'dfg', 21, 34, 5, 1, 2, 3, 'fhg', 4]
        self.assertEqual(fl, tofl)
        self.assertEqual(fl, tofl)

    def test_strip_finalcif(self):
        stripped = strip_finalcif_of_name(Path('406-0308-finalcif.cif').stem)
        self.assertEqual('406-0308', stripped)
        self.assertEqual('foobar', strip_finalcif_of_name('foobar'))

    def test_strip_finalcif_till_end(self):
        self.assertEqual('cu_BruecknerJK_153F40_0m', strip_finalcif_of_name('cu_BruecknerJK_153F40_0m-finalcif'))
        self.assertEqual('cu_BruecknerJK_153F40_0m-finalcif_changes', strip_finalcif_of_name('cu_BruecknerJK_153F40_0m-finalcif_changes'))
        self.assertEqual('cu_BruecknerJK_153F40_0m', strip_finalcif_of_name('cu_BruecknerJK_153F40_0m-finalcif_changes', till_name_ends=True))

    def test_isnumeric_true(self):
        self.assertEqual(True, isnumeric('1.234'))
        self.assertEqual(True, isnumeric('234'))
        self.assertEqual(True, isnumeric('0'))
        self.assertEqual(True, isnumeric('0.234(12)'))
        self.assertEqual(True, isnumeric('0.234(?)'))

    def test_isnumeric_false(self):
        self.assertEqual(False, isnumeric('foo'))
        self.assertEqual(False, isnumeric('!0'))

    def test_grouper(self):
        self.assertEqual([(1, 2, 3), (4, 5, None)], list(grouper([1, 2, 3, 4, 5], n=3)))
        self.assertEqual([(1, 2, 3), (4, 5, '!')], list(grouper([1, 2, 3, 4, 5], n=3, fillvalue='!')))
        self.assertEqual([(1, 2), (3, 4), (5, 6)], list(grouper([1, 2, 3, 4, 5, 6], n=2)))
        self.assertEqual([(1,), (2,), (3,), (4,), (5,), (6,)], list(grouper([1, 2, 3, 4, 5, 6], n=1)))

    def test_distance(self):
        self.assertEqual(1.7320508075688772, distance(1, 1, 1, 2, 2, 2))
        self.assertEqual(1.0, distance(1, 0, 0, 2, 0, 0))


class TestSha512(unittest.TestCase):
    def setUp(self) -> None:
        Path('testfile').write_bytes(b'foobarbaz!1234')

    def tearDown(self) -> None:
        Path('testfile').unlink(missing_ok=True)

    def test_sha512(self):
        self.assertEqual(
            'c2ef738518857a9360893420c7ead3d44b4e15d2b1b25ab870d6bdfbf4542e369e337a6546b5fa5fe0d6d0554c2c72a09fef5e997d2724256d62c03d9be1e18b',
            sha512_checksum_of_file('testfile'))


class TestErrorFromValue(unittest.TestCase):
    def test_get_error_from_value_with_space(self):
        self.assertEqual((0.0123, 0.0023), get_error_from_value("0.0123 (23)"))

    def test_get_error_from_value_below_unity(self):
        self.assertEqual((0.0123, 0.0023), get_error_from_value("0.0123(23)"))

    def test_get_error_from_value_noerror(self):
        self.assertEqual((0.0123, 0.0), get_error_from_value('0.0123'))

    def test_get_error_from_value_float(self):
        self.assertEqual((250.0123, 0.0023), get_error_from_value("250.0123(23)"))

    def test_get_error_from_value_onlyint(self):
        self.assertEqual((123.0, 25.0), get_error_from_value("123(25)"))

    def test_get_error_from_value_missing_last_bracket(self):
        self.assertEqual((123.0, 25.0), get_error_from_value("123(25"))

    def test_get_error_from_value_missing_error(self):
        self.assertEqual((123.0, 0), get_error_from_value("123()"))
        self.assertEqual((12.323, 0), get_error_from_value("12.323()"))
        self.assertEqual((12.323, 0), get_error_from_value("12.323 ()"))
        self.assertEqual((12.323, 0), get_error_from_value("12.323 ( )"))


class TestNextpath(unittest.TestCase):
    def setUp(self) -> None:
        Path('./foobar.txt').touch()
        Path('./foobar-1.txt').touch()

    def tearDown(self) -> None:
        Path('./foobar.txt').unlink(missing_ok=True)
        Path('./foobar-1.txt').unlink(missing_ok=True)
        Path('./foobar-2.txt').unlink(missing_ok=True)

    def test_nextpath(self):
        self.assertEqual('./foobar-2.txt', next_path('./foobar-%s.txt'))


class TestDatabaseNumber(TestCase):
    def test_is_database_number_str_true(self):
        self.assertEqual(True, is_database_number('1234567'))

    def test_is_database_number_str_false(self):
        self.assertEqual(False, is_database_number('123456'))

    def test_is_database_number_str_false_long(self):
        self.assertEqual(False, is_database_number('12345678'))

    def test_is_database_number_int_true(self):
        self.assertEqual(True, is_database_number(1234567))

    def test_is_database_number_int_false(self):
        self.assertEqual(False, is_database_number(123456))
