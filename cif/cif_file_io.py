#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import re
import textwrap
from pathlib import Path
# noinspection PyUnresolvedReferences
from typing import Dict, List, Tuple

import gemmi

from cif.cif_order import order, special_keys
from datafiles.utils import DSRFind
from tools.misc import essential_keys, non_centrosymm_keys


def quote(string: str, wrapping=80) -> str:
    """
    Quotes a cif string and wrapps it. The shorter strings are directly handled by cif.quote().
    """
    if len(string) < 80:
        return gemmi.cif.quote(string)
    lines = '\n'
    for line in string.split('\n'):
        if len(line) > wrapping:
            line = textwrap.fill(line, width=wrapping)
            lines += line + '\n'
        else:
            lines += line + '\n'
    quoted = gemmi.cif.quote(lines.rstrip('\n'))
    return quoted


charcters = {'°'      : r'\%',
             '±'      : r'+-',
             'ß'      : r'\&s',
             'ü'      : r'u\"',
             'ö'      : r'o\"',
             'ä'      : r'a\"',
             'é'      : r"\'e",
             'è'      : r'\`e',
             'ó'      : r"\'o",
             'ò'      : r'\`o',
             u'\u022F': r'\.o',
             'á'      : r'\'a',
             'à'      : r'\`a',
             'â'      : r'\^a',
             'ê'      : r'\^e',
             'î'      : r'\^i',
             'ô'      : r'\^o',
             'û'      : r'\^u',
             'ç'      : r'\,c',
             u"\u03B1": r'\a',
             u"\u03B2": r'\b',
             u"\u03B3": r'\g',
             u"\u03B4": r'\d',
             u"\u03B5": r'\e',
             u"\u03B6": r'\z',
             u"\u03B7": r'\h',
             u"\u03B8": r'\q',
             u"\u03B9": r'\i',
             u"\u03BA": r'\k',
             u"\u03BB": r'\l',
             u"\u03BC": r'\m',
             u"\u03BD": r'\n',
             u"\u03BE": r'\x',
             u"\u03BF": r'\o',
             u"\u03C0": r'\p',
             u"\u03C1": r'\r',
             u"\u03C3": r'\s',
             u"\u03C4": r'\t',
             u"\u03C5": r'\u',
             u"\u03C6": r'\F',
             u"\u03C9": r'\w',
             u"\u03A9": r'\W',
             u"\u03D5": r'\f',
             }  # , r'\r\n': chr(10)}


def set_pair_delimited(block, key: str, txt: str):
    """
    Converts special characters to their markup counterparts.
    """
    for char in txt:
        if char in charcters:
            txt = txt.replace(char, charcters[char])
    try:
        # bad hack to get the numbered values correct
        float(txt)
        block.set_pair(key, txt)
    except (TypeError, ValueError):
        # prevent _key '?' in cif:
        if txt == '?':
            block.set_pair(key, txt)
        else:
            block.set_pair(key, quote(txt))


def retranslate_delimiter(txt: str) -> str:
    """
    Translates delimited cif characters back to unicode characters.
    >>> retranslate_delimiter("Crystals were grown from thf at -20 \%C.")
    'Crystals were grown from thf at -20 °C.'
    """
    inv_map = {v: k for k, v in charcters.items()}
    for char in inv_map.keys():
        txt = txt.replace(char, inv_map[char])
    return txt


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, file: Path):
        self.fileobj = file
        self.block = None
        self.doc = None
        self.cif_file_text = self.fileobj.read_text(encoding='utf-8', errors='ignore')
        self.open_cif_with_gemmi()
        self.hkl_extra_info = self.abs_hkl_details()
        self.resdata = self.block.find_value('_shelx_res_file')
        d = DSRFind(self.resdata)
        self.order = order
        self.dsr_used = d.dsr_used

    def __getitem__(self, item: str) -> str:
        result = self.block.find_value(item)
        if result:
            if result == '?' or result == "'?'":
                return ''
            return result
        else:
            return ''

    def __delitem__(self, key):
        # TODO: ask if delitem could be possible:
        self.block.set_pair(key, '?')

    def save(self, filename: str = None) -> None:
        """
        Saves the current cif file in the specific order of the order list.
        :param filename:  Name to save cif file to.
        """
        if not filename:
            filename = self.fileobj.absolute()
        for key in reversed(self.order):
            try:
                self.block.move_item(self.block.get_index(key), 0)
            except RuntimeError:
                pass
                # print('Not in list:', key)
        # make sure hkl file and res file are at the end if the cif file:
        for key in special_keys:
            try:
                self.block.move_item(self.block.get_index(key), -1)
            except RuntimeError:
                continue
        # self.doc.write_file(filename, gemmi.cif.Style.Indent35)
        Path(filename).write_text(self.doc.as_string(gemmi.cif.Style.Indent35))

    def open_cif_with_gemmi(self) -> None:
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        try:
            self.doc = gemmi.cif.read_string(self.cif_file_text)
            # self.doc = gemmi.cif.read_file(str(self.fileobj.absolute()))
            self.block = self.doc.sole_block()
        except Exception as e:
            print('Unable to read file:', e)
            raise

    def open_cif_by_string(self) -> None:
        self.doc = gemmi.cif.read_string(self.cif_file_text)
        self.block = self.doc.sole_block()

    @property
    def atomic_struct(self):
        return gemmi.make_atomic_structure_from_block(self.block)

    def abs_hkl_details(self) -> Dict[str, str]:
        """
        This method tries to determine the information witten at the end of a cif hkl file by sadabs.
        """
        hkl = None
        all = {'_exptl_absorpt_process_details' : '',
               '_exptl_absorpt_correction_type' : '',
               '_exptl_absorpt_correction_T_max': '',
               '_exptl_absorpt_correction_T_min': '',
               '_computing_structure_solution'  : '',
               }
        try:
            hkl = self.block.find_value('_shelx_hkl_file')[:-1]
        except Exception:
            pass
        if not hkl:
            return all
        hkl = hkl[hkl.find('  0   0   0    0'):].split('\n')[1:]
        hkl = 'data_hkldat\n' + '\n'.join(hkl)
        # in-html cif has ')' instead of ';':
        hkl = [re.sub(r'^\)', ';', x) for x in hkl.split('\n')]
        # the keys have a blank char in front:
        hkl = [re.sub(r'^ _', '_', x) for x in hkl]
        hkl = '\n'.join(hkl)
        try:
            hkldoc = gemmi.cif.read_string(hkl)
            hklblock = hkldoc.sole_block()
        except Exception as e:
            print('Unable to get information from hkl foot.')
            print(e)
            return all
        for key in all:
            val = hklblock.find_value(key)
            if val:
                all[key] = gemmi.cif.as_string(val).strip()
        return all

    @property
    def solution_program_details(self) -> str:
        return self.hkl_extra_info['_computing_structure_solution']

    @property
    def absorpt_process_details(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_process_details']

    @property
    def absorpt_correction_type(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_correction_type']

    @property
    def absorpt_correction_T_max(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_correction_T_max']

    @property
    def absorpt_correction_T_min(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_correction_T_min']

    def _spgr(self) -> gemmi.SpaceGroup:
        if self.symmops:
            symm_ops = self.symmops
        else:
            symm_ops = self.symmops_from_spgr()
        return gemmi.find_spacegroup_by_ops(gemmi.GroupOps([gemmi.Op(o) for o in symm_ops]))

    def space_group(self) -> str:
        """
        Returns the space group from the symmetry operators.
        spgr.short_name() gives the short name.
        """
        return self._spgr().xhm()

    def symmops_from_spgr(self) -> List[str]:
        # _symmetry_space_group_name_Hall
        space_group = None
        if self['_space_group_name_H-M_alt']:
            space_group = self['_space_group_name_H-M_alt']
        if self['_symmetry_space_group_name_H-M']:
            space_group = self['_symmetry_space_group_name_H-M']
        if not space_group:
            return []
        ops = [op.triplet() for op in
               gemmi.find_spacegroup_by_name(gemmi.cif.as_string(space_group)).operations()]
        return ops

    def spgr_number_from_symmops(self) -> int:
        return self._spgr().number

    def crystal_system(self) -> str:
        return self._spgr().crystal_system_str()

    def hall_symbol(self) -> str:
        return self._spgr().hall

    @property
    def hkl_checksum_calcd(self) -> int:
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
    def res_checksum_calcd(self) -> int:
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

    def calc_checksum(self, input_str: str) -> int:
        """
        Calculates the shelx checksum of a cif file.
        """
        sum = 0
        input_str = input_str.encode('ascii', 'ignore')
        for char in input_str:
            # print(char)
            if char > 32:  # ascii 32 is space character
                sum += char
        sum %= 714025
        sum = sum * 1366 + 150889
        sum %= 714025
        sum %= 100000
        return sum

    @property
    def symmops(self) -> List[str]:
        """
        Reads the symmops from the cif file.

        >>> cif = CifContainer(Path('test-data/twin4.cif'))
        >>> cif.symmops
        ['x, y, z', '-x, -y, -z']
        """
        xyz1 = self.block.find(("_symmetry_equiv_pos_as_xyz",))  # deprecated
        xyz2 = self.block.find(("_space_group_symop_operation_xyz",))  # New definition
        if xyz1:
            return [i.str(0) for i in xyz1]
        elif xyz2:
            return [i.str(0) for i in xyz2]
        else:
            return []

    @property
    def is_centrosymm(self) -> bool:
        if '-x, -y, -z' in self.symmops:
            return True
        else:
            return False

    def atoms(self) -> Tuple[str, str, str, str, str, str, str, str]:
        labels = self.block.find_loop('_atom_site_label')
        types = self.block.find_loop('_atom_site_type_symbol')
        x = self.block.find_loop('_atom_site_fract_x')
        y = self.block.find_loop('_atom_site_fract_y')
        z = self.block.find_loop('_atom_site_fract_z')
        occ = self.block.find_loop('_atom_site_occupancy')
        part = self.block.find_loop('_atom_site_disorder_group')
        u_eq = self.block.find_loop('_atom_site_U_iso_or_equiv')
        for label, type, x, y, z, occ, part, ueq in zip(labels, types, x, y, z, occ, part, u_eq):
            #  0    1    2  3  4   5    6     7
            yield label, type, x, y, z, occ, part, ueq

    def atoms_from_sites(self):
        for at in self.atomic_struct.sites:
            yield at.label, at.type_symbol, at.fract.x, at.fract.y, at.fract.z

    def atoms_orthogonal(self):
        for at in self.atomic_struct.sites:
            yield [self.atomic_struct.cell.orthogonalize(at.fract).x,
                   self.atomic_struct.cell.orthogonalize(at.fract).y,
                   self.atomic_struct.cell.orthogonalize(at.fract).z]

    @property
    def hydrogen_atoms_present(self) -> bool:
        for at in self.atomic_struct.sites:
            if at.type_symbol in ('H', 'D'):
                return True
        else:
            return False

    @property
    def disorder_present(self) -> bool:
        for at in self.atoms():
            if at[6] == '.':
                continue
            if int(at[6]) > 0:
                return True
        else:
            return False

    @property
    def cell(self) -> tuple:
        c = self.atomic_struct.cell
        return c.a, c.b, c.c, c.alpha, c.beta, c.gamma, c.volume

    def bonds(self, without_H: bool = False):
        """
        Yields a list of bonds in the cif file.
        """
        label1 = self.block.find_loop('_geom_bond_atom_site_label_1')
        label2 = self.block.find_loop('_geom_bond_atom_site_label_2')
        dist = self.block.find_loop('_geom_bond_distance')
        symm = self.block.find_loop('_geom_bond_site_symmetry_2')
        publ = self.block.find_loop('_geom_bond_publ_flag')
        hat = ('H', 'D')
        for label1, label2, dist, symm in zip(label1, label2, dist, symm):
            if without_H and (label1[0] in hat or label2[0] in hat):
                continue
            else:
                yield (label1, label2, dist, symm)

    def angles(self):
        label1 = self.block.find_loop('_geom_angle_atom_site_label_1')
        label2 = self.block.find_loop('_geom_angle_atom_site_label_2')
        label3 = self.block.find_loop('_geom_angle_atom_site_label_3')
        angle = self.block.find_loop('_geom_angle')
        symm1 = self.block.find_loop('_geom_angle_site_symmetry_1')
        symm2 = self.block.find_loop('_geom_angle_site_symmetry_3')
        # publ = self.block.find_loop('_geom_angle_publ_flag')
        for label1, label2, label3, angle, symm1, symm2 in zip(label1, label2, label3, angle, symm1, symm2):
            yield (label1, label2, label3, angle, symm1, symm2)

    def torsion_angles(self):
        label1 = self.block.find_loop('_geom_torsion_atom_site_label_1')
        label2 = self.block.find_loop('_geom_torsion_atom_site_label_2')
        label3 = self.block.find_loop('_geom_torsion_atom_site_label_3')
        label4 = self.block.find_loop('_geom_torsion_atom_site_label_4')
        torsang = self.block.find_loop('_geom_torsion')
        symm1 = self.block.find_loop('_geom_torsion_site_symmetry_1')
        symm2 = self.block.find_loop('_geom_torsion_site_symmetry_2')
        symm3 = self.block.find_loop('_geom_torsion_site_symmetry_3')
        symm4 = self.block.find_loop('_geom_torsion_site_symmetry_4')
        # publ = self.block.find_loop('_geom_torsion_publ_flag')
        for label1, label2, label3, label4, torsang, symm1, symm2, symm3, symm4 in zip(label1, label2, label3, label4,
                                                                                       torsang, symm1, symm2, symm3,
                                                                                       symm4):
            yield (label1, label2, label3, label4, torsang, symm1, symm2, symm3, symm4)

    def hydrogen_bonds(self):
        label_d = self.block.find_loop('_geom_hbond_atom_site_label_D')
        label_h = self.block.find_loop('_geom_hbond_atom_site_label_H')
        label_a = self.block.find_loop('_geom_hbond_atom_site_label_A')
        dist_dh = self.block.find_loop('_geom_hbond_distance_DH')
        dist_ha = self.block.find_loop('_geom_hbond_distance_HA')
        dist_da = self.block.find_loop('_geom_hbond_distance_DA')
        angle_dha = self.block.find_loop('_geom_hbond_angle_DHA')
        symm = self.block.find_loop('_geom_hbond_site_symmetry_A')
        # publ = self.block.find_loop('_geom_hbond_publ_flag')
        for label_d, label_h, label_a, dist_dh, dist_ha, dist_da, angle_dha, symm in zip(label_d, label_h, label_a,
                                                                                         dist_dh, dist_ha, dist_da,
                                                                                         angle_dha, symm):
            yield label_d, label_h, label_a, dist_dh, dist_ha, dist_da, angle_dha, symm

    def key_value_pairs(self):
        """
        Returns the key/value pairs of a cif file sorted by priority.

        >>> c = CifContainer(Path('test-data/P21c-final.cif'))
        >>> c.open_cif_with_gemmi()
        >>> c.key_value_pairs()[:2]
        [['_audit_contact_author_address', None], ['_audit_contact_author_email', None]]
        """
        high_prio_no_values, high_prio_with_values = self.get_keys()
        return high_prio_no_values + [['These below are already in:', '---------------------']] + high_prio_with_values

    def is_centrokey(self, key):
        """
        Is True if the kurrent key is only valid 
        for non-centrosymmetric structures
        """
        return self.is_centrosymm and key in non_centrosymm_keys

    def get_keys(self):
        """
        Returns the keys to be displayed in the main table as two separate lists.
        """
        questions = []
        # contains the answered keys:
        with_values = []
        # holds keys that are not in the cif file but in essential_keys:
        missing_keys = []
        for item in self.block:
            if item.pair is not None:
                key, value = item.pair
                if len(value) > 1000:
                    # do not include res and hkl file:
                    continue
                if key.startswith('_shelx'):
                    continue
                if self.is_centrokey(key):
                    continue
                if not value or value == '?' or value == "'?'":
                    questions.append([key, value])
                else:
                    with_values.append([key, value])
        all_keys = [x[0] for x in with_values] + [x[0] for x in questions]
        # check if there are keys not in the cif but in essential_keys:
        for key in essential_keys:
            if key not in all_keys:
                if self.is_centrokey(key):
                    continue
                questions.append([key, '?'])
                missing_keys.append(key)
        for k in missing_keys:
            if self.is_centrokey(k):
                continue
            self.block.set_pair(k, '?')
        return sorted(questions), sorted(with_values)

    def add_to_cif(self, key: str, value: str = '?'):
        """
        Add an additional key value pair to the cif block.
        """
        self.block.set_pair(key, value)
