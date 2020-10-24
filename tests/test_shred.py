import unittest
from pathlib import Path

from cif.cif_file_io import CifContainer
from tools.shred import ShredCIF


class TestShedCif(unittest.TestCase):

    def setUp(self) -> None:
        self.cif = CifContainer(Path('../test-data/p21c.cif'))
        self.shred = ShredCIF(self.cif, ui=None)

    def test_shred(self):
        self.shred.