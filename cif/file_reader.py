import json
import textwrap
from pathlib import Path

import gemmi
from cif import cif_file_parser
from tools.misc import high_prio_keys, medium_prio_keys


def quote(string, wrapping=80):
    """
    Quotes a cif string and warppes it.
    """
    return gemmi.cif.quote(textwrap.fill(string, width=wrapping))

class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, filename: Path):
        self.filename = filename.absolute()
        self.cif_data = None
        self.block = None
        self.doc = None

    def save(self, filename):
        filename = Path(filename.parts[-1][:-4] + '-final.cif').name
        self.doc.write_file(filename, gemmi.cif.Style.Indent35)

    def open_cif_with_gemmi(self):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        print('File opened:', self.filename)
        try:
            self.doc = gemmi.cif.read_file(str(self.filename))
        except RuntimeError as e:
            return str(e)
        self.block = self.doc.sole_block()
        print('Opened block:', self.block.name)
        self.cif_data = json.loads(self.doc.as_json())[self.block.name.lower()]

    def open_cif_with_fileparser(self):
        """
        """
        if self.cif_data:
            raise RuntimeError
        try:
            self.cif_data = cif_file_parser.Cif(self.filename)
        except AttributeError:
            print('Filename has to be a Path instance.')
        except IsADirectoryError:
            print('Filename can not be a directory.')

    def __getitem__(self, item):
        return self.cif_data[item.lower()] if self.cif_data[item.lower()] else ''

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
        high_prio_no_values, high_prio_with_values = self.get_keys(high_prio_keys)
        medium_prio_q, medium_prio_with_values = self.get_keys(medium_prio_keys)
        # low_prio_q, low_prio_with_values = self.get_keys(low_prio_keys)
        medium_prio_q += [['These are already in:', '---------------------'], ['', '']]
        return high_prio_no_values + medium_prio_q + high_prio_with_values + medium_prio_with_values

    def get_keys(self, inputkeys):
        """
        Returns the keys to be displayed in the main table.
        """
        questions = []
        # contains the answered keys:
        with_values = []
        for k in inputkeys:
            try:
                value = self.cif_data[k.lower()]
                if not value:
                    questions.append([k, value])
                else:
                    with_values.append([k, value])
            except Exception as e:
                #print(e)
                pass
        return questions, with_values
