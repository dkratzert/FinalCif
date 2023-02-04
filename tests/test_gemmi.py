import unittest

import gemmi
from packaging import version


class MyGemmiTestsForAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.doc: gemmi.cif.Document = gemmi.cif.Document()
        self.doc.add_new_block('block1')
        self.doc.add_new_block('block2')

    def test_blocks_in_doc(self):
        self.assertEqual('<gemmi.cif.Block block1>', str(self.doc.find_block('block1')))  # add assertion here
        self.assertEqual('[<gemmi.cif.Block block1>, <gemmi.cif.Block block2>]', str(list(self.doc)))  # add assertion here
        self.assertTrue('block2' in [x.name for x in self.doc])
        if version.parse(gemmi.__version__) > version.parse('0.5.7'):
            self.assertTrue('block2' in self.doc)


if __name__ == '__main__':
    unittest.main()
