#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import re
from collections import namedtuple
from math import sin, cos, sqrt
from pathlib import Path
from typing import Dict, List, Tuple, Union

import gemmi

from cif.cif_order import order, special_keys
from datafiles.utils import DSRFind
from tools.dsrmath import mean
from tools.misc import essential_keys, non_centrosymm_keys, get_error_from_value


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, file: Union[Path, str]):
        self.fileobj: Path
        if isinstance(file, str):
            self.fileobj = Path(file)
        elif isinstance(file, Path):
            self.fileobj = file
        else:
            raise TypeError('The file parameter must be string or Path object.')
        # I do this in small steps instead of gemmi.cif.read_file() in order to
        # leave out the check_for_missing_values. This was gemmi reads cif files
        # with missing values.
        self.doc = self.read_file(str(self.fileobj.absolute()))
        self.block = self.doc.sole_block()
        # will not ok with non-ascii characters in the res file:
        self.chars_ok = True
        d = DSRFind(self.res_file_data)
        self.doc.check_for_duplicates()
        self.hkl_extra_info = self.abs_hkl_details()
        self.order = order
        self.dsr_used = d.dsr_used
        self.atomic_struct = gemmi.make_small_structure_from_block(self.block)
        # A dictionary to convert Atom names like 'C1_2' or 'Ga3' into Element names like 'C' or 'Ga'
        self._name2elements = dict(
            zip([x.upper() for x in self.block.find_loop('_atom_site_label')],
                [x.upper() for x in self.block.find_loop('_atom_site_type_symbol')]))

    def read_file(self, path: str) -> gemmi.cif.Document:
        """
        Reads a cif file and returns a gemmi document object.
        """
        doc = gemmi.cif.Document()
        # support for platon squeeze files:
        if path.endswith('.sqf'):
            txt = Path(path).read_text(encoding='ascii')
            txt = 'data_justrandomlkdsadflkmcn\n' + txt
            doc.parse_string(txt)
        else:
            doc.source = path
            doc.parse_file(path)
        return doc

    def read_string(self, cif_string: str) -> gemmi.cif.Document:
        """
        Reads a cif file from a string and returns a gemmi cif docment.
        :param cif_string: cif as string
        :return: gemmi document
        """
        doc = gemmi.cif.Document()
        doc.parse_string(cif_string)
        return doc

    def cif_as_string(self, without_hkl=False) -> str:
        if not without_hkl:
            return self.doc.as_string(style=gemmi.cif.Style.Indent35)
        else:
            doc = gemmi.cif.Document()
            doc.parse_string(self.doc.as_string(style=gemmi.cif.Style.Indent35))
            block = doc.sole_block()
            block.find_pair_item('_shelx_hkl_file').erase()
            return doc.as_string(style=gemmi.cif.Style.Indent35)

    def __str__(self):
        return str(self.fileobj.absolute())

    def __getitem__(self, item: str) -> str:
        result = self.block.find_value(item)
        if result:
            if result == '?' or result == "'?'":
                return ''
            # can I do this? No:
            # return retranslate_delimiter(result)
            return gemmi.cif.as_string(result)
        else:
            return ''

    def __setitem__(self, key: str, value: str) -> None:
        """Set a key value pair of the current block"""
        self.block.set_pair(key, value)

    def __delitem__(self, key: str):
        self.block.find_pair_item(key).erase()

    def save(self, filename: str = None) -> None:
        """
        Saves the current cif file.
        :param filename:  Name to save cif file to.
        """
        if not filename:
            filename = str(self.fileobj.absolute())
        self.order_cif_keys()
        self.doc.write_file(filename, gemmi.cif.Style.Indent35)
        # Path(filename).write_text(self.doc.as_string(gemmi.cif.Style.Indent35))

    def order_cif_keys(self):
        """
        Brings the current CIF in the specific order of the order list.
        """
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

    @property
    def res_file_data(self) -> str:
        try:
            return self.block.find_value('_shelx_res_file')
        except UnicodeDecodeError:
            # This is a fallback in case _shelx_res_file has non-ascii characters.
            print('File has non-ascii characters. Switching to compatible mode.')
            self.doc = self.read_string(self.fileobj.read_text(encoding='cp1250', errors='ignore'))
            self.block = self.doc.sole_block()
            self.chars_ok = False
            return self.block.find_value('_shelx_res_file')

    @property
    def hkl_file(self) -> str:
        try:
            return self.block.find_value('_shelx_hkl_file')
        except Exception as e:
            print('No hkl data found in CIF!, {}'.format(e))
            return ''

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
            hkl = self.hkl_file
        except Exception:
            pass
        if not hkl:
            return all
        hkl = hkl[hkl.find('  0   0   0    0'):].splitlines(keepends=False)[1:-1]
        # html-embedded cif has ')' instead of ';':
        hkl = [';' if x[:1] == ')' else x for x in hkl]
        # the keys have a blank char in front:
        hkl = [re.sub(r'^ _', '_', x) for x in hkl]
        hkl = 'data_hkldat\n' + '\n'.join(hkl)
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
    def loops(self) -> List[gemmi.cif.Loop]:
        """
        Returns a list of loops contained in the current block.
        """
        loops = []
        for b in self.block:
            if b.loop:
                loops.append(b.loop)
        return loops

    @property
    def n_loops(self):
        return len(self.loops)

    def import_loops(self, imp_cif: 'CifContainer'):
        """
        Import all loops from the CifContainer imp_cif to the current block.
        """
        for loop in imp_cif.loops:
            new_loop = self.block.init_loop('', loop.tags)
            for row in imp_cif.block.find(loop.tags):
                new_loop.add_row([x for x in row])

    @property
    def Z_value(self):
        return self.atomic_struct.cell.volume / self.atomic_struct.cell.volume_per_image()

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

    @property
    def bond_precision(self):
        """
        This method is unfinished and might result in wrong numbers!
        """
        a, aerror = get_error_from_value(self['_cell_length_a'])
        b, berror = get_error_from_value(self['_cell_length_b'])
        c, cerror = get_error_from_value(self['_cell_length_c'])
        alpha, sigalpha = get_error_from_value(self['_cell_angle_alpha'])
        beta, sigbeta = get_error_from_value(self['_cell_angle_beta'])
        gamma, siggamma = get_error_from_value(self['_cell_angle_gamma'])
        A1 = aerror / a
        A2 = berror / b
        A3 = cerror / c
        # B1 = sin(alpha) * (cos(alpha) - cos(beta) * cos(gamma)) * sigalpha
        # B2 = sin(beta) * (cos(beta) - cos(alpha) * cos(gamma)) * sigbeta
        # B3 = sin(gamma) * (cos(gamma) - cos(alpha) * cos(beta)) * siggamma
        name2coords = dict([(x[0], (x[2], x[3], x[4])) for x in self.atoms()])
        name2part = dict([(x[0], x[5]) for x in self.atoms()])
        count = 0
        bonderrors = []
        bb = 0.0
        pair = ('C')
        for bond in self.bonds(without_h=True):
            atom1 = bond[0]
            atom2 = bond[1]
            if 'B' in atom1 or 'B' in atom2:
                continue
            if name2part[atom1] != '.' or name2part[atom2] != '.':
                continue
            if self.iselement(atom1) in pair and self.iselement(atom2) in pair:
                dist, error = get_error_from_value(bond[2])
                x1, sig_x1 = get_error_from_value(name2coords[atom1][0])
                y1, sig_y1 = get_error_from_value(name2coords[atom1][1])
                z1, sig_z1 = get_error_from_value(name2coords[atom1][2])
                x2, sig_x2 = get_error_from_value(name2coords[atom2][0])
                y2, sig_y2 = get_error_from_value(name2coords[atom2][1])
                z2, sig_z2 = get_error_from_value(name2coords[atom2][2])
                delta1 = a * (x1 - x2)
                delta2 = b * (y1 - y2)
                delta3 = c * (z1 - z2)
                sigd = (
                               (delta1 + delta2 * cos(gamma) + delta3 * cos(beta)) ** 2 * (
                               delta1 ** 2 * A1 ** 2 + a ** 2 * (sig_x1 ** 2 + sig_x2 ** 2))
                               + (delta1 * cos(gamma) + delta2 + delta3 * cos(alpha)) ** 2 * (
                                       delta2 ** 2 * A2 ** 2 + b ** 2 * (sig_y1 ** 2 + sig_y2 ** 2))
                               + (delta1 * cos(beta) + delta2 * cos(alpha) + delta3) ** 2 * (
                                       delta3 ** 2 * A3 ** 2 + c ** 2 * (sig_z1 ** 2 + sig_z2 ** 2))
                               + ((delta1 * delta2 * siggamma * sin(gamma)) ** 2 +
                                  (delta1 * delta3 * sigbeta * sin(beta)) ** 2 +
                                  (delta2 * delta3 * sigalpha * sin(alpha)) ** 2)) / dist ** 2
                # The error is too large:
                sigd = sqrt(sigd)
                bb += sigd
                if sigd > 0.0001:
                    count += 1
                    # print(atom1, atom2, dist, round(error, 5), round(sigd, 4), round(bb, 5), count)
                    # print('------ dist - sigma - calcsig - sum - num')
                    bonderrors.append(sigd)
        if len(bonderrors) > 2:
            return round(mean(bonderrors), 5)
        else:
            return 0.0

    def _spgr(self) -> gemmi.SpaceGroup:
        if self.symmops:
            symm_ops = self.symmops
        else:
            symm_ops = self.symmops_from_spgr
        return gemmi.find_spacegroup_by_ops(gemmi.GroupOps([gemmi.Op(o) for o in symm_ops]))

    @property
    def space_group(self) -> str:
        """
        Returns the space group from the symmetry operators.
        spgr.short_name() gives the short name.
        """
        try:
            return self._spgr().xhm()
        except (AttributeError, RuntimeError):
            if self['_space_group_name_H-M_alt']:
                return gemmi.cif.as_string(self['_space_group_name_H-M_alt'])
            else:
                return ''

    @property
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

    @property
    def spgr_number_from_symmops(self) -> int:
        return self._spgr().number

    @property
    def crystal_system(self) -> str:
        if not self._spgr():
            return ''
        return self._spgr().crystal_system_str()

    @property
    def hall_symbol(self) -> str:
        return self._spgr().hall

    @property
    def hkl_checksum_calcd(self) -> int:
        """
        Calculates the shelx checksum for the hkl file content of a cif file.
        """
        hkl = self.hkl_file
        if hkl:
            return self.calc_checksum(hkl[1:-1])
        else:
            return 0

    @property
    def res_checksum_calcd(self) -> int:
        """
        Calculates the shelx checksum for the res file content of a cif file.
        """
        res = self.res_file_data
        if res:
            return self.calc_checksum(self.res_file_data[1:-1])
        return 0

    @staticmethod
    def calc_checksum(input_str: str) -> int:
        """
        Calculates the shelx checksum of a cif file.
        """
        sum = 0
        try:
            input_str = input_str.encode('cp1250', 'ignore')
        except Exception:
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

    def rename_data_name(self, newname: str = ''):
        """
        Reanmes data_ tags to the newname. Also _vrf tags are renamed accordingly.
        http://journals.iucr.org/services/cif/checking/checkfaq.html
        """
        # Have to use ord(), because Python 3.6 has not str.isascii():
        newname = ''.join([i for i in newname if ord(i) < 127])
        self.block.name = newname
        for item in self.block:
            if item.pair is not None:
                key, value = item.pair
                if key.startswith('_vrf'):
                    newkey = '_' + '_'.join(key.split('_')[1:3]) + '_' + newname
                    self.block.find_pair_item(key).erase()
                    self.block.set_pair(newkey, value)

    @property
    def symmops(self) -> List[str]:
        """
        Reads the symmops from the cif file.
        """
        xyz1 = self.block.find(("_symmetry_equiv_pos_as_xyz",))  # deprecated
        xyz2 = self.block.find(("_space_group_symop_operation_xyz",))  # New definition
        if xyz1:
            return [i.str(0) for i in xyz1]
        elif xyz2:
            return [i.str(0) for i in xyz2]
        else:
            return self.symmops_from_spgr

    @property
    def is_centrosymm(self) -> bool:
        """
        Whether a structuere is centro symmetric or not.
        """
        ops = gemmi.GroupOps([gemmi.Op(o) for o in self.symmops])
        return ops.is_centric()

    def atoms(self, without_h: bool = False) -> Tuple[str, str, str, str, str, str, str, str]:
        labels = self.block.find_loop('_atom_site_label')
        types = self.block.find_loop('_atom_site_type_symbol')
        x = self.block.find_loop('_atom_site_fract_x')
        y = self.block.find_loop('_atom_site_fract_y')
        z = self.block.find_loop('_atom_site_fract_z')
        part = self.block.find_loop('_atom_site_disorder_group')
        occ = self.block.find_loop('_atom_site_occupancy')
        u_eq = self.block.find_loop('_atom_site_U_iso_or_equiv')
        for label, type, x, y, z, part, occ, ueq in zip(labels, types, x, y, z, part, occ, u_eq):
            if without_h and self.ishydrogen(label):
                continue
            #         0    1   2  3  4   5   6     7
            #yield label, type, x, y, z, part, occ, ueq
            atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))
            yield atom(label=label, type=type, x=x, y=y, z=z, part=part, occ=occ, u_eq=u_eq)

    @property
    def atoms_fract(self) -> List:
        for at in self.atomic_struct.sites:
            yield [at.label, at.type_symbol, at.fract.x, at.fract.y, at.fract.z, at.disorder_group, at.occ, at.u_iso]

    @property
    def atoms_orth(self):
        cell = self.atomic_struct.cell
        for at in self.atomic_struct.sites:
            x, y, z = at.orth(cell)
            yield [at.label, at.type_symbol, x, y, z, at.disorder_group, at.occ, at.u_iso]

    @property
    def hydrogen_atoms_present(self) -> bool:
        for at in self.atomic_struct.sites:
            if at.type_symbol in ('H', 'D'):
                return True
        else:
            return False

    @property
    def disorder_present(self) -> bool:
        for at in self.atomic_struct.sites:
            if at.disorder_group:
                return True
        else:
            return False

    @property
    def cell(self) -> tuple:
        c = self.atomic_struct.cell
        return c.a, c.b, c.c, c.alpha, c.beta, c.gamma, c.volume

    def ishydrogen(self, label: str) -> bool:
        """
        Determines if an atom with the name 'label' is a hydrogen atom.
        """
        hydrogen = ('H', 'D')
        if self.iselement(label) in hydrogen:
            return True
        else:
            return False

    def bonds(self, without_h: bool = False):
        """
        Yields a list of bonds in the cif file.
        """
        label1 = self.block.find_loop('_geom_bond_atom_site_label_1')
        label2 = self.block.find_loop('_geom_bond_atom_site_label_2')
        dist = self.block.find_loop('_geom_bond_distance')
        symm = self.block.find_loop('_geom_bond_site_symmetry_2')
        for label1, label2, dist, symm in zip(label1, label2, dist, symm):
            if without_h and (self.ishydrogen(label1) or self.ishydrogen(label2)):
                continue
            else:
                yield (label1, label2, dist, symm)

    def angles(self, without_H: bool = False):
        label1 = self.block.find_loop('_geom_angle_atom_site_label_1')
        label2 = self.block.find_loop('_geom_angle_atom_site_label_2')
        label3 = self.block.find_loop('_geom_angle_atom_site_label_3')
        angle = self.block.find_loop('_geom_angle')
        symm1 = self.block.find_loop('_geom_angle_site_symmetry_1')
        symm2 = self.block.find_loop('_geom_angle_site_symmetry_3')
        for label1, label2, label3, angle, symm1, symm2 in zip(label1, label2, label3, angle, symm1, symm2):
            if without_H and (self.ishydrogen(label1) or self.ishydrogen(label2) or self.ishydrogen(label3)):
                continue
            else:
                yield (label1, label2, label3, angle, symm1, symm2)

    def iselement(self, name: str) -> str:
        return self._name2elements[name.upper()]

    def natoms(self, without_h: bool = False) -> int:
        return len(tuple(self.atoms(without_h)))

    def nbonds(self, without_h: bool = False) -> int:
        """
        Number of bonds in the cif object, with and without hydrogen atoms.
        """
        return len(tuple(self.bonds(without_h)))

    def nangles(self, without_h: bool = False) -> int:
        """
        Number of bond angles in the cif object, with and without hydrogen atoms.
        """
        return len(tuple(self.angles(without_h)))

    def ntorsion_angles(self, without_h: bool = False) -> int:
        """
        Number of torsion angles in the cif object, with and without hydrogen atoms.
        """
        return len(tuple(self.torsion_angles(without_h)))

    def torsion_angles(self, without_h: bool = False):
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
            if without_h and (self.ishydrogen(label1) or self.ishydrogen(label2)
                              or self.ishydrogen(label3) or self.ishydrogen(label3)):
                continue
            yield label1, label2, label3, label4, torsang, symm1, symm2, symm3, symm4

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

    def key_value_pairs(self) -> List[Tuple[str, str]]:
        """
        Returns the key/value pairs of a cif file sorted by priority.
        """
        keys_without_values, keys_with_values = self.get_keys()
        return keys_without_values + [('These below are already in:', '---------------------')] + keys_with_values

    def is_centrokey(self, key) -> bool:
        """
        Is True if the kurrent key is only valid 
        for non-centrosymmetric structures
        """
        return self.is_centrosymm and key in non_centrosymm_keys

    def get_keys(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
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
                    # No-one should edit shelx values:
                    continue
                if self.is_centrokey(key):
                    continue
                if not value or value == '?' or value == "'?'":
                    questions.append((key, value))
                else:
                    with_values.append((key, value))
        all_keys = [x[0] for x in with_values] + [x[0] for x in questions]
        # check if there are keys not in the cif but in essential_keys:
        for key in essential_keys:
            if key not in all_keys:
                if self.is_centrokey(key):
                    continue
                questions.append((key, '?'))
                missing_keys.append(key)
        for k in missing_keys:
            if self.is_centrokey(k):
                continue
            self.block.set_pair(k, '?')
        return sorted(questions), sorted(with_values)

    def test_res_checksum(self) -> bool:
        """
        A method to check whether the checksums in the cif file fit to the content.
        """
        cif_res_ckecksum = 0
        if self.res_checksum_calcd > 0:
            cif_res_ckecksum = self['_shelx_res_checksum'] or -1
            try:
                cif_res_ckecksum = int(cif_res_ckecksum)
            except ValueError:
                cif_res_ckecksum = -1
        if cif_res_ckecksum > 0 and cif_res_ckecksum != self.res_checksum_calcd:
            return False
        else:
            return True

    def test_hkl_checksum(self) -> bool:
        """
        A method to check whether the checksums in the cif file fit to the content.
        """
        cif_hkl_ckecksum = 0
        if self.hkl_checksum_calcd > 0:
            cif_hkl_ckecksum = self['_shelx_hkl_checksum'] or -1
            try:
                cif_hkl_ckecksum = int(cif_hkl_ckecksum)
            except ValueError:
                cif_hkl_ckecksum = -1
        if cif_hkl_ckecksum > 0 and cif_hkl_ckecksum != self.hkl_checksum_calcd:
            return False
        else:
            return True
