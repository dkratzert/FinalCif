#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

import textwrap
from pathlib import Path

import gemmi

from datafiles.utils import DSRFind
from tools.misc import find_line, high_prio_keys, non_centrosymm_keys


def quote(string: str, wrapping=80):
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


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, file: Path):
        self.fileobj = file
        self.cif_data = None
        self.block = None
        self.doc = None
        self.cif_file_text = ''
        self.atomic_struct = None
        self.missing_keys = []
        self.open_cif_with_gemmi()
        self.symmops = self._get_symmops()
        self.hkl_extra_info = self.abs_hkl_details()
        self.resdata = self.block.find_value('_shelx_res_file')
        d = DSRFind(self.resdata)
        self.dsr_used = d.dsr_used

    def save(self, filename=None):
        if not filename:
            filename = self.fileobj.absolute()
        self.doc.write_file(filename, gemmi.cif.Style.Indent35)

    def open_cif_with_gemmi(self):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        # print('File opened:', self.filename)
        self.cif_file_text = self.fileobj.read_text(encoding='utf-8', errors='ignore')
        try:
            self.doc = gemmi.cif.read_string(self.cif_file_text)
            self.block = self.doc.sole_block()
        except Exception as e:
            print('Unable to read file:', e)
            raise
        try:
            self.atomic_struct = gemmi.make_atomic_structure_from_block(self.block)
        except Exception as e:
            print('Unable to read atomic structure:', e)
            raise

    def open_cif_by_string(self):
        self.doc = gemmi.cif.read_string(self.cif_file_text)
        self.block = self.doc.sole_block()
        self.atomic_struct = gemmi.make_atomic_structure_from_block(self.block)

    def abs_hkl_details(self):
        """
        This method tries to determine the information witten at the end of a cif hkl file by sadabs.
        """
        hkl = self.block.find_value('_shelx_hkl_file')
        all = {'_exptl_absorpt_process_details' : '',
               '_exptl_absorpt_correction_type' : '',
               '_exptl_absorpt_correction_T_max': '',
               '_exptl_absorpt_correction_T_min': '',
               }
        if not hkl:
            return all
        abs = False
        details = ''
        for line in hkl.splitlines():
            if line.startswith(' _exptl_absorpt_process_details'):
                abs = True
                continue
            if abs and not line.startswith(')'):
                details += line
                continue
            if line.startswith(')') and details:
                all['_exptl_absorpt_process_details'] = details.lstrip()
                abs = False
                continue
            if line.startswith(' _exptl_absorpt_correction_type'):
                all['_exptl_absorpt_correction_type'] = line.split()[1]
            if line.startswith(' _exptl_absorpt_correction_T_max'):
                all['_exptl_absorpt_correction_T_max'] = line.split()[1]
            if line.startswith(' _exptl_absorpt_correction_T_min'):
                all['_exptl_absorpt_correction_T_min'] = line.split()[1]
        return all

    @property
    def absorpt_process_details(self):
        return self.hkl_extra_info['_exptl_absorpt_process_details']

    @property
    def absorpt_correction_type(self):
        return self.hkl_extra_info['_exptl_absorpt_correction_type']

    @property
    def absorpt_correction_T_max(self):
        return self.hkl_extra_info['_exptl_absorpt_correction_T_max']

    @property
    def absorpt_correction_T_min(self):
        return self.hkl_extra_info['_exptl_absorpt_correction_T_min']

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

    def calc_checksum(self, input_str: str):
        """
        Calculates the shelx checksum a cif file.
        """
        sum = 0
        input_str = input_str.encode('ascii')
        for char in input_str:
            # print(char)
            if char > 32:  # space character
                sum += char
        sum %= 714025
        sum = sum * 1366 + 150889
        sum %= 714025
        sum %= 100000
        return sum

    def _get_symmops(self):
        """
        Reads the symmops from the cif file.

        >>> cif = CifContainer(Path('test-data/twin4.cif'))
        >>> cif.open_cif_with_gemmi()
        >>> cif._get_symmops()
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
    def is_centrosymm(self):
        if '-x, -y, -z' in self.symmops:
            return True
        else:
            return False

    def __getitem__(self, item):
        result = self.block.find_value(item)
        return result if result else ''

    def atoms(self):
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
    def hydrogen_atoms_present(self):
        for at in self.atomic_struct.sites:
            if at.type_symbol in ('H', 'D'):
                return True
        else:
            return False

    @property
    def disorder_present(self):
        for at in self.atoms():
            if at[6] == '.':
                continue
            if int(at[6]) > 0:
                return True
        else:
            return False


    @property
    def cell(self):
        c = self.atomic_struct.cell
        return c.a, c.b, c.c, c.alpha, c.beta, c.gamma, c.volume

    def bonds(self):
        label1 = self.block.find_loop('_geom_bond_atom_site_label_1')
        label2 = self.block.find_loop('_geom_bond_atom_site_label_2')
        dist = self.block.find_loop('_geom_bond_distance')
        symm = self.block.find_loop('_geom_bond_site_symmetry_2')
        publ = self.block.find_loop('_geom_bond_publ_flag')
        for label1, label2, dist, symm in zip(label1, label2, dist, symm):
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
        try:
            # bad hack to get the numbered values correct
            float(txt)
            self.block.set_pair(key, txt)
        except (TypeError, ValueError):
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
            if not value:
                # these are not in the cif file
                self.missing_keys.append(key)
            # except (KeyError, TypeError):
            #    value = ''
            if not value or value == '?':
                questions.append([key, value])
            else:
                with_values.append([key, value])
        cif = self.cif_file_text.splitlines()
        data_position = find_line(cif, '^data_')
        for k in self.missing_keys:
            if k in non_centrosymm_keys and self.is_centrosymm:
                continue
            cif.insert(data_position + 1, k + ' ' * (31 - len(k)) + '    ?')
        self.cif_file_text = "\n".join(cif)
        self.open_cif_by_string()
        return questions, with_values

    @property
    def crystal_system(self):
        return (self['_space_group_crystal_system'] or self['_symmetry_cell_setting']).strip("'\"; ")
