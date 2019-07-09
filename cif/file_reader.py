#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

import json
import re
import textwrap
from pathlib import Path

import gemmi

from cif import cif_file_parser
from tools.misc import high_prio_keys, non_centrosymm_keys, to_float


def quote(string, wrapping=80):
    """
    Quotes a cif string and warppes it.
    """
    lines = '\n'
    for line in string.split('\n'):
        if len(line) > wrapping:
            line = textwrap.fill(line, width=wrapping)
            lines += line + '\n'
        else:
            lines += line + '\n'
    quoted = gemmi.cif.quote(lines.rstrip('\n'))
    return quoted


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    TODO: get _exptl_absorpt_process_details etc from cif file if it is there.
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
            self.block = self.doc.sole_block()
        except Exception as e:
            return e
        try:
            self.cif_data = json.loads(self.doc.as_json())[self.block.name.lower()]
        except Exception as e:
            return e

    @property
    def hkl_checksum_calcd(self):
        """
        Calculates the shelx checksum for the hkl file content of a cif file.

        >>> c = CifContainer(Path('test-data/DK_zucker2_0m.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.hkl_checksum_calcd
        69576
        >>> c = CifContainer(Path('test-data/4060310.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.hkl_checksum_calcd
        0
        """
        hkl = self.block.find_value('_shelx_hkl_file')
        if hkl:
            return self.calc_checksum(hkl[1:-1])
        else:
            return 0

    @property
    def res_checksum_calcd(self):
        """
        Calculates the shelx checksum for the res file content of a cif file.

        >>> c = CifContainer(Path('test-data/DK_zucker2_0m.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.res_checksum_calcd
        52593
        >>> c = CifContainer(Path('test-data/4060310.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.res_checksum_calcd
        0
        """
        res = self.block.find_value('_shelx_res_file')
        if res:
            return self.calc_checksum(res[1:-1])
        return 0

    def calc_checksum(self, input: str):
        """
        Calculates the shelx checksum a cif file.
        """
        sum = 0
        input = input.encode('ascii')
        for char in input:
            # print(char)
            if char > 32:  # space character
                sum += char
        sum %= 714025
        sum = sum * 1366 + 150889
        sum %= 714025
        sum %= 100000
        return sum

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
        result = self.block.find_value(item)
        return result if result else ''

    def atoms(self):
        # TODO: make this work
        labels = self.cif_data['_atom_site_label']
        types = self.cif_data['_atom_site_type_symbol']
        x = self.cif_data['_atom_site_fract_x']
        y = self.cif_data['_atom_site_fract_y']
        z = self.cif_data['_atom_site_fract_z']
        occ = self.cif_data['_atom_site_occupancy']
        part = self.cif_data['_atom_site_disorder_group']

    def atoms_in_asu(self, only_nh=False):
        summe = 0
        if '_atom_site_type_symbol' in self.cif_data and '_atom_site_occupancy' in self.cif_data:
            for n, at in enumerate(self.cif_data['_atom_site_type_symbol']):
                if only_nh:
                    if at in ['H', 'D']:
                        continue
                occ = self.cif_data['_atom_site_occupancy'][n]
                if isinstance(occ, str):
                    occ = to_float(occ)
                    if occ:
                        summe += occ
                else:
                        summe += occ
            return summe
        else:
            return None

    def atoms_in_cell(self, only_nh=False):
        summe = 0
        if '_atom_site_type_symbol' in self.cif_data:
            for at in self.cif_data['_chemical_formula_sum'].split():
                if only_nh:
                    if at[:2].strip('0123456789') in ['H', 'D']:
                        continue
                num = re.sub('\D', '', at)
                if num:
                    summe += float(num)
        return summe

    def cell(self):
        return self.cif_data.cell

    def set_pair_delimited(self, key, txt):
        """
        Converts special characters to their markup counterparts.
        """
        charcters = {'°': r'\%', '±': r'+-', 'ß': r'\&s', 'ü': r'u\"',
                     'ö': r'o\"', 'ä': r'a\"', 'é': '\'e', 'á': r'\'a',
                     'à': r'\`a', 'â': r'\^a', 'ç': r'\,c'}  # , r'\r\n': chr(10)}
        for char in txt:
            if char in charcters:
                txt = txt.replace(char, charcters[char])
        self.block.set_pair(key, quote(txt))

    def key_value_pairs(self):
        """
        Returns the key/value pairs of a cif file sorted by priority.

        >>> c = CifContainer(Path('test-data/P21c-final.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.key_value_pairs()[:2]
        [['_audit_contact_author_address', None], ['_audit_contact_author_email', None]]
        """
        high_prio_no_values, high_prio_with_values = self.get_keys(high_prio_keys)
        return high_prio_no_values + \
               [['These below are already in:', '---------------------'],
                ['', '']] + high_prio_with_values

    def get_keys(self, inputkeys):
        """
        Returns the keys to be displayed in the main table.
        """
        questions = []
        # contains the answered keys:
        with_values = []
        for key in inputkeys.keys():
            if key in non_centrosymm_keys and self.is_centrosymm:
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

    @property
    def crystal_system(self):
        return (self['_space_group_crystal_system'] or self['_symmetry_cell_setting']).strip("'\"; ")
