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
    quoted = gemmi.cif.quote(textwrap.fill(string, width=wrapping))
    return quoted


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, file: Path):
        self.filename = file.absolute()
        self.fileobj = file
        self.cif_data = None
        self.block = None
        self.doc = None

    def save(self, filename):
        self.doc.write_file(filename, gemmi.cif.Style.Indent35)

    def open_cif_with_gemmi(self):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        # print('File opened:', self.filename)
        try:
            self.doc = gemmi.cif.read_file(str(self.filename))
        except RuntimeError as e:
            return e
        self.block = self.doc.sole_block()
        # print('Opened block:', self.block.name)
        self.cif_data = json.loads(self.doc.as_json())[self.block.name.lower()]

    def get_symmops(self):
        """
        >>> cif = CifContainer(Path('test-data/twin4.cif'))
        >>> cif.open_cif_with_gemmi()
        >>> cif.get_symmops()
        ['x, y, z', '-x, -y, -z']
        """
        xyz1 = self.block.find(("_symmetry_equiv_pos_as_xyz",))  # deprecated
        xyz2 = self.block.find(("_space_group_symop_operation_xyz",))  # New definition
        if xyz1:
            self.cif_data['_space_group_symop_operation_xyz'] = [i.str(0) for i in xyz1]
        else:
            self.cif_data['_space_group_symop_operation_xyz'] = [i.str(0) for i in xyz2]
        return self.cif_data['_space_group_symop_operation_xyz']

    @property
    def is_centrosymm(self):
        if '-x, -y, -z' in self.get_symmops():
            return True
        else:
            return False

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
        foo = high_prio_no_values + medium_prio_q + high_prio_with_values + medium_prio_with_values
        return foo

    def get_keys(self, inputkeys):
        """
        Returns the keys to be displayed in the main table.
        """
        questions = []
        # contains the answered keys:
        with_values = []
        for key in inputkeys:
            if key in self.non_centrosymm_keys and self.is_centrosymm:
                continue
            # try:
            value = self.block.find_value(key)
            # except (KeyError, TypeError):
            #    value = ''
            if not value or value == '?':
                questions.append([key, value])
            else:
                with_values.append([key, value])
        return questions, with_values

    non_centrosymm_keys = ('_chemical_absolute_configuration', '_refine_ls_abs_structure_Flack')
