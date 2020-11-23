#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import unittest
from pathlib import Path

from datafiles.bruker_frame import BrukerFrameHeader


class TestBrukerFrame(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_str(self):
        sfrm = BrukerFrameHeader(basename='apex_frame', searchpath=Path('./test-data'))
        self.assertEqual("{ 'ANGLES'", str(sfrm)[:10])
