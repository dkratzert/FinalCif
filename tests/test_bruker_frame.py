#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import unittest
from pathlib import Path

from finalcif.datafiles.bruker_frame import BrukerFrameHeader


class TestBrukerFrame(unittest.TestCase):
    """
    BrukerFrameHeader searches for *basename*.sfrm files in searchpath.
    Then, the newest found file is used to gather the machine information.
    """

    def setUp(self) -> None:
        self.test_data = Path('./test-data')
        self.example_data = Path('tests/examples/')

    def test_str(self):
        sfrm = BrukerFrameHeader(basename='apex_frame',
                                 searchpath=self.test_data)
        self.assertEqual("{ 'ANGLES'", str(sfrm)[:10])

    def test_radiation_type(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual('Mo', sfrm.radiation_type)

    def test_radiation_type_in_work_folder(self):
        # check if a basename without cu_ prefix leads to a found .sfrm file:
        sfrm = BrukerFrameHeader(basename='BruecknerJK_153F40', searchpath=self.example_data / 'work')
        self.assertEqual('Cu', sfrm.radiation_type)
        sfrm = BrukerFrameHeader(basename='cu_BruecknerJK_153F40', searchpath=self.example_data / 'work')
        self.assertEqual('Cu', sfrm.radiation_type)

    def test_radiation_type_in_work_folder_and_wrong_prefix(self):
        with self.assertRaises(FileNotFoundError):
            BrukerFrameHeader(basename='mo_BruecknerJK_153F40', searchpath=self.example_data / 'work')

    def test_measure_date(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual('15-Apr-2019 13:32:45', sfrm.measure_date)

    def test_program(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual('BIS V6.2.10/2018-10-02', sfrm.program)

    def test_kilovolts_milliamps(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual(50.0, sfrm.kilovolts)
        self.assertEqual(1.4, sfrm.milliamps)

    def test_kilovolts_milliamps_work_folder(self):
        sfrm = BrukerFrameHeader(basename='BruecknerJK_153F40', searchpath=self.example_data / 'work')
        self.assertEqual(50.0, sfrm.kilovolts)
        self.assertEqual(1.1, sfrm.milliamps)

    def test_radiation_type_temperature(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual(100.0, sfrm.temperature)

    def test_detector_type(self):
        sfrm = BrukerFrameHeader(basename='mo_DK_Zucker2', searchpath=self.test_data)
        self.assertEqual('CMOS-PHOTONII', sfrm.detector_type)
