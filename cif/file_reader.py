from pathlib import Path
from runpy import _get_main_module_details

import gemmi
from cif import file_parser
from tools.misc import high_prio_keys


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, filename: Path):
        self.filename = filename.absolute()
        self.cif_data = None

    def open_cif_with_gemmi(self):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        doc = gemmi.cif.read_file(self.filename)
        return doc

    def open_cif_with_fileparser(self):
        """
        """
        if self.cif_data:
            raise RuntimeError
        try:
            self.cif_data = file_parser.Cif(self.filename)
        except AttributeError:
            print('Filename has to be a Path instance.')
        except IsADirectoryError:
            print('Filename can not be a directory.')

    def __getitem__(self, item):
        return self.cif_data[item] if self.cif_data[item] else ''

    def atoms(self):
        return self.cif_data.atoms

    def cell(self):
        return self.cif_data.cell

    def key_value_pairs(self):
        """
        Returns the key/value pairs of a cif file sorted by priority.

        >>> c = CifContainer(Path('test-data/P21c-final.cif'))
        >>> c.open_cif_with_fileparser()
        >>> c.key_value_pairs()

        """
        pairs = []
        for k in high_prio_keys:
            try:
                pairs.append([k, self.cif_data[k]])
            except:
                pass
        return pairs
