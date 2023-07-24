#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import re
from collections import namedtuple
from contextlib import suppress
from functools import cache
from pathlib import Path
from typing import Dict, List, Tuple, Union, Generator, Type

import gemmi
from gemmi.cif import as_string, Document, Loop
from shelxfile import Shelxfile

from finalcif.cif.cif_order import order, special_keys
from finalcif.cif.hkl import HKL, Limit
from finalcif.cif.text import utf8_to_str, quote, retranslate_delimiter
from finalcif.datafiles.utils import DSRFind
from finalcif.tools.misc import essential_keys, non_centrosymm_keys, isnumeric, grouper, strip_finalcif_of_name


class GemmiError(Exception):
    pass


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, file: Union[Path, str], new_block: str = ''):
        """

        Args:
            file: CIF file to open
            new_block: Create a new block (new file) if a name is given. Otherwise, just
                       the existing document is opened.
        """
        if isinstance(file, str):
            self.fileobj = Path(file)
        elif isinstance(file, Path):
            self.fileobj = file
        else:
            raise TypeError('The file parameter must be string or Path object.')
        self.current_block = ''
        # I do this in small steps instead of gemmi.cif.read_file() in order to
        # leave out the check_for_missing_values. This way, gemmi reads cif files even
        # with missing values.
        if new_block:
            self.doc: Document = gemmi.cif.Document()
            self.doc.add_new_block(new_block)
        else:
            try:
                self.doc = self.read_file(self.fileobj)
            except Exception as e:
                raise GemmiError(e)
        # Starting with first block, but can use others with subsequent self._onload():
        self.block: gemmi.cif.Block = self.doc[0]
        self.shx = Shelxfile(verbose=True)
        self.shx.read_string(self.res_file_data[1:-1])
        self._on_load()

    @property
    def path_base(self) -> Path:
        """
        The absolute path of the current file without file name:
        /foo/bar/baz
        """
        return Path(self.doc.source).resolve().parent

    @property
    def filename(self) -> str:
        """
        The name of the current file without path:
        foo.cif
        """
        return Path(self.doc.source).name or self.fileobj.name

    @property
    def finalcif_file(self) -> Path:
        """
        The full path of the file with '-finalcif' attached to the end:
        foo/bar/baz-finalcif.cif
        """
        filename = self.finalcif_file_prefixed(prefix='', suffix='-finalcif.cif')
        return filename

    def finalcif_file_prefixed(self, prefix: str, suffix: str = '-finalcif.cif', force_strip=True) -> Path:
        """
        The full path of the file with a prefix and '-finalcif.cif' attached to the end.
        The suffix needs '-finalcif' in order to contain the finalcif ending.
        "foo/bar/baz-finalcif.cif"

        :param forece_strip: Forces to strip the filename also after the '-finalcif' string.
        """
        file_witout_finalcif = strip_finalcif_of_name(Path(self.filename).stem, till_name_ends=force_strip)
        filename = self.path_base.joinpath(Path(prefix + file_witout_finalcif + suffix))
        return filename

    def get_line_numbers_of_bad_characters(self, filepath: Path):
        line_numbers = []
        for num, line in enumerate(filepath.read_bytes().splitlines(keepends=True)):
            try:
                line.decode('ascii')
            except(UnicodeDecodeError):
                line_numbers.append(num)
        return line_numbers

    @property
    def is_multi_cif(self) -> bool:
        return True if len(self.doc) > 1 else False

    def load_this_block(self, index: int) -> None:
        self.block = self.doc[index]
        self.current_block = self.block.name
        self._on_load()

    def load_block_by_name(self, blockname: str) -> None:
        self.block = self.doc.find_block(blockname)
        self.current_block = self.block.name
        self._on_load()

    def _on_load(self) -> None:
        # will not ok with non-ascii characters in the res file:
        self.chars_ok = True
        self.doc.check_for_duplicates()
        self.order = order
        self.dsr_used = DSRFind(self.res_file_data).dsr_used
        self.atomic_struct: gemmi.SmallStructure = gemmi.make_small_structure_from_block(self.block)
        # A dictionary to convert Atom names like 'C1_2' or 'Ga3' into Element names like 'C' or 'Ga'
        self._name2elements = dict(
            zip([x.upper() for x in self.block.find_loop('_atom_site_label')],
                [x.upper() for x in self.block.find_loop('_atom_site_type_symbol')]))
        self.check_hkl_min_max()

    @property
    @cache
    def hkl_extra_info(self):
        return self._abs_hkl_details()

    def check_hkl_min_max(self) -> None:
        if not all([self['_diffrn_reflns_limit_h_min'], self['_diffrn_reflns_limit_h_max'],
                    self['_diffrn_reflns_limit_k_min'], self['_diffrn_reflns_limit_k_max'],
                    self['_diffrn_reflns_limit_l_min'], self['_diffrn_reflns_limit_l_max']]) and self.hkl_file:
            limits = self.min_max_diffrn_reflns_limit()
            self['_diffrn_reflns_limit_h_min'] = str(limits.h_min)
            self['_diffrn_reflns_limit_h_max'] = str(limits.h_max)
            self['_diffrn_reflns_limit_k_min'] = str(limits.k_min)
            self['_diffrn_reflns_limit_k_max'] = str(limits.k_max)
            self['_diffrn_reflns_limit_l_min'] = str(limits.l_min)
            self['_diffrn_reflns_limit_l_max'] = str(limits.l_max)

    def read_file(self, path: Path) -> gemmi.cif.Document:
        """
        Reads a cif file and returns a gemmi document object.
        """
        doc = gemmi.cif.Document()
        # support for platon squeeze files:
        if path.suffix == '.sqf':
            txt = path.read_text(encoding='ascii')
            txt = 'data_justrandomlkdsadflkmcn\n' + txt
            doc.parse_string(txt)
        else:
            doc.source = str(path.resolve())
            doc.parse_file(str(path.resolve()))
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
        if without_hkl:
            # return a copy, do not delete hkl from original:
            doc = gemmi.cif.Document()
            doc.parse_string(self.doc.as_string(style=gemmi.cif.Style.Indent35))
            for block in doc:
                if block.find_pair_item('_shelx_hkl_file'):
                    block.find_pair_item('_shelx_hkl_file').erase()
                if block.find_pair_item('_shelx_fcf_file'):
                    block.find_pair_item('_shelx_fcf_file').erase()
            return doc.as_string(style=gemmi.cif.Style.Indent35)
        else:
            return self.doc.as_string(style=gemmi.cif.Style.Indent35)

    def __getitem__(self, item: str) -> str:
        """
        This method returns an empty string when the item value is '?'
        """
        if self.block.find_value(item):
            return as_string(self.block.find_value(item))
        else:
            return ''

    def __setitem__(self, key: str, value: str) -> None:
        """Set a key value pair of the current block.
        Values are automatically encoded from utf-8 and delimited.
        """
        self.set_pair_delimited(key, value)

    def __delitem__(self, key: str) -> None:
        with suppress(AttributeError):
            self.block.find_pair_item(key).erase()

    def __contains__(self, item) -> bool:
        return bool(self.__getitem__(item))

    def __str__(self) -> str:
        return (f"CIF file: {str(self.fileobj.resolve())}\n"
                f"{len(self.doc)} Block(s): {', '.join([x.name for x in self.doc])}\n"
                f"Contains SHELX res file: {True if self.res_file_data else False}\n"
                f"Has {self.natoms()} atoms"
                f", {self.nbonds()} bonds"
                f", {self.nangles()} angles")

    def file_is_there_and_writable(self) -> bool:
        import os
        return self.fileobj.exists() and self.fileobj.is_file() and os.access(self.fileobj, os.W_OK)

    def set_pair_delimited(self, key: str, txt: str):
        """
        Converts special characters to their markup counterparts.
        """
        txt = utf8_to_str(txt)
        try:
            # bad hack to get the numbered values correct
            float(txt)
            self.block.set_pair(key, txt)
        except (TypeError, ValueError):
            # prevent _key '?' in cif:
            if txt == '?':
                self.block.set_pair(key, txt)
            else:
                self.block.set_pair(key, quote(txt))

    def save(self, filename: Union[Path, None] = None) -> None:
        """
        Saves the current cif file.
        :param filename:  Name to save cif file to.
        """
        if not filename:
            filename = self.finalcif_file
        if self.is_empty():
            print(f'File {filename} is empty.')
            return
        self.order_cif_keys()
        print('Saving to', Path(filename).resolve())
        self.doc.write_file(str(filename), gemmi.cif.Style.Indent35)

    def order_cif_keys(self) -> None:
        """
        Brings the current CIF in the specific order of the order list.
        """
        for block in self.doc:
            for key in reversed(self.order):
                try:
                    block.move_item(block.get_index(key), 0)
                except (RuntimeError, ValueError):
                    pass
                    # print('Not in list:', key)
            # make sure hkl file and res file are at the end if the cif file:
            for key in special_keys:
                try:
                    block.move_item(block.get_index(key), -1)
                except (RuntimeError, ValueError):
                    continue

    @property
    def res_file_data(self) -> str:
        try:
            if self['_shelx_res_file']:
                return self['_shelx_res_file']
            elif self['_iucr_refine_instructions_details']:
                return self['_iucr_refine_instructions_details']
            else:
                return ''
        except UnicodeDecodeError:
            # This is a fallback in case _shelx_res_file has non-ascii characters.
            print('File has non-ascii characters. Switching to compatible mode.')
            self.doc = self.read_string(self.fileobj.read_text(encoding='latin1', errors='ignore'))
            self.block = self.doc.sole_block()
            self.chars_ok = False
            return self.block.find_value('_shelx_res_file')

    @property
    def hkl_file(self) -> str:
        hkl_loop: Loop = self.get_loop('_diffrn_refln_index_h')
        if hkl_loop and hkl_loop.width() > 4:
            return self._hkl_from_cif_format(hkl_loop)
        else:
            # returns an empty string if no cif hkl was found:
            return self._hkl_from_shelx()

    def _hkl_from_cif_format(self, hkl_loop: Loop) -> str:
        hkl_list = []
        format_string = '{:>4}{:>4}{:>4}{:>8}{:>8}'
        if hkl_loop.width() == 6:
            format_string = '{:>4}{:>4}{:>4}{:>8}{:>8}{:>4}'
        for line in grouper(hkl_loop.values, hkl_loop.width()):
            hkl_list.append(format_string.format(*line[:6]))
        return '\n'.join(hkl_list)

    def _hkl_from_shelx(self) -> str:
        try:
            if self['_shelx_hkl_file']:
                return self['_shelx_hkl_file']
            elif self['_iucr_refine_reflections_details']:
                return self['_iucr_refine_reflections_details']
            elif self['_xd_hkl_file']:
                return self['_xd_hkl_file']
            else:
                return ''
        except Exception as e:
            print('No hkl data found in CIF!, {}'.format(e))
            return ''

    @property
    def hkl_as_cif(self):
        return HKL(self.hkl_file, self.block.name, hklf_type=self.hklf_number).hkl_as_cif

    @property
    def hklf_number(self) -> int:
        hklf = 4
        if self.res_file_data:
            hklf = self._hklf_number_from_shelxl_file()
        return hklf

    def min_max_diffrn_reflns_limit(self) -> Limit:
        return HKL(self.hkl_file, self.block.name, hklf_type=self.hklf_number).get_hkl_min_max()

    def _hklf_number_from_shelxl_file(self) -> int:
        if self.shx.hklf:
            return self.shx.hklf.n if self.shx.hklf.n != 0 else 4
        else:
            return 4

    @property
    def hkl_file_without_foot(self) -> str:
        """Returns a hkl file with no content after the 0 0 0 reflection"""
        zero_reflection_position = self._find_line_of_000(self.hkl_file)
        if zero_reflection_position:
            return '\n'.join(self.hkl_file.splitlines(keepends=False)[:zero_reflection_position + 1])
        else:
            return self.hkl_file

    @staticmethod
    def _find_line_of_000(lines: str):
        pattern = re.compile(r'^\s+0\s+0\s+0\s+0.*')
        for num, line in enumerate(lines.splitlines(keepends=False)):
            found = pattern.match(line)
            if found and num > 0:
                return num
        return 0

    def _abs_hkl_details(self) -> Dict[str, str]:
        """
        This method tries to determine the information witten at the end of a cif hkl file by sadabs.
        """
        hkl = None
        all_sadabs_items = {'_exptl_absorpt_process_details' : '',
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
            return all_sadabs_items
        # zero_reflection_position = self.normal_search(hkl)
        hkl_splitted = hkl.splitlines(keepends=False)
        zero_reflection_position = self.reversed_search(hkl_splitted)
        if not zero_reflection_position:
            return all_sadabs_items
        hkl = hkl.splitlines(keepends=False)[zero_reflection_position:]
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
            return all_sadabs_items
        for key in all_sadabs_items:
            val = hklblock.find_value(key)
            if val:
                all_sadabs_items[key] = gemmi.cif.as_string(val).strip()
        return all_sadabs_items

    def normal_search(self, hkl):
        pattern = re.compile(r'\s+0\s+0\s+0\s+0')
        found = pattern.search(hkl)
        if found:
            zero_reflection_position = found.start()
        else:
            zero_reflection_position = 0
        return zero_reflection_position

    def reversed_search(self, hkl_splitted: List):
        pattern = re.compile(r'\s+0\s+0\s+0\s+0')
        zero_reflection_position = 0
        for num, line in enumerate(reversed(hkl_splitted)):
            found = pattern.search(line)
            if num > 500:
                # A longer footer is not realistic
                break
            if found:
                zero_reflection_position = len(hkl_splitted) - num
        return zero_reflection_position

    def is_empty(self) -> bool:
        if len(self.keys()) + len(self.loops) == 0:
            return True
        return False

    def keys(self) -> List[str]:
        """
        Returns a plain list of keys that are really in this CIF.
        """
        return [x.pair[0] for x in self.block if x.pair is not None]

    def values(self):
        """
        Returns a plain list of keys that are really in this CIF.
        """
        return [x.pair[1] for x in self.block if x.pair is not None]

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

    def add_loop_to_cif(self, loop_tags: List[str], loop_values: Union[list, tuple]) -> gemmi.cif.Loop:
        gemmi_loop = self.init_loop(loop_tags)
        for row in list(grouper(loop_values, len(loop_tags))):
            gemmi_loop.add_row(row)
        return gemmi_loop

    @property
    def n_loops(self):
        return len(self.loops)

    def get_loop(self, key_in_loop: str) -> gemmi.cif.Loop:
        return self.block.find_loop(key_in_loop).get_loop()

    def get_loop_column(self, key_in_loop: str) -> List:
        return [retranslate_delimiter(as_string(x)) for x in self.block.find_loop(key_in_loop)]

    def init_loop(self, loop_keywords: List) -> gemmi.cif.Loop:
        return self.block.init_loop('', loop_keywords)

    @property
    def z_value(self):
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
    def absorpt_correction_t_max(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_correction_T_max']

    @property
    def absorpt_correction_t_min(self) -> str:
        return self.hkl_extra_info['_exptl_absorpt_correction_T_min']

    def _spgr(self) -> gemmi.SpaceGroup:
        if self.symmops and self.symmops != ['']:
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
        except (AttributeError, RuntimeError, ValueError):
            if self['_space_group_name_H-M_alt']:
                return gemmi.cif.as_string(self['_space_group_name_H-M_alt'])
            elif self['_symmetry_space_group_name_H-M']:
                return gemmi.cif.as_string(self['_symmetry_space_group_name_H-M'])
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
    def spgr_number(self) -> int:
        if self['_space_group_IT_number'] and isnumeric(self['_space_group_IT_number']):
            return int(self['_space_group_IT_number'])
        elif self['_symmetry_Int_Tables_number'] and isnumeric(self['_symmetry_Int_Tables_number']):
            return int(self['_symmetry_Int_Tables_number'])
        else:
            return self.spgr_number_from_symmops

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
        if self.hkl_file:
            return self.calc_checksum(self.hkl_file)
        else:
            return 0

    @property
    def res_checksum_calcd(self) -> int:
        """
        Calculates the shelx checksum for the res file content of a cif file.
        """
        if self.res_file_data:
            return self.calc_checksum(self.res_file_data)
        return 0

    @staticmethod
    def calc_checksum(input_str: str) -> int:
        """
        Calculates the shelx checksum of a cif file.
        The original algorithm was posted by Berthold Stöger on the Bruker Users Mailing list.
        """
        crc_sum = 0
        try:
            input_str = input_str.encode('cp1250', 'ignore')
        except Exception:
            input_str = input_str.encode('ascii', 'ignore')
        for char in input_str:
            # print(char)
            if char > 32:  # ascii 32 is space character
                crc_sum += char
        crc_sum %= 714025
        crc_sum = crc_sum * 1366 + 150889
        crc_sum %= 714025
        crc_sum %= 100000
        return crc_sum

    def rename_data_name(self, newname: str = ''):
        """
        Renames data_ tags to the newname. Also _vrf tags are renamed accordingly.
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
        if not self.symmops or self.symmops == ['']:
            # Do not crash without symmops
            return False
        ops = gemmi.GroupOps([gemmi.Op(o) for o in self.symmops])
        try:
            return ops.is_centric()
        except AttributeError:
            return ops.is_centrosymmetric()

    def atoms(self, without_h: bool = False) -> Generator:
        """
        Atoms from the CIF where values are returned as string like in the CIF with esds.
        """
        labels = self.block.find_loop('_atom_site_label')
        types = self.block.find_loop('_atom_site_type_symbol')
        x = self.block.find_loop('_atom_site_fract_x')
        y = self.block.find_loop('_atom_site_fract_y')
        z = self.block.find_loop('_atom_site_fract_z')
        part = self.block.find_loop('_atom_site_disorder_group')
        occ = self.block.find_loop('_atom_site_occupancy')
        u_eq = self.block.find_loop('_atom_site_U_iso_or_equiv')
        atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))
        for label, type, x, y, z, part, occ, u_eq in zip(labels, types, x, y, z,
                                                         part if part else ('0',) * len(labels),
                                                         occ if occ else ('1.000000',) * len(labels),
                                                         u_eq):
            if without_h and self.ishydrogen(label):
                continue
            #         0    1   2  3  4   5   6     7
            # yield label, type, x, y, z, part, occ, ueq
            yield atom(label=label, type=type, x=x, y=y, z=z, part=part, occ=occ, u_eq=u_eq)

    @property
    def atoms_fract(self) -> Generator:
        """Atoms with numbers as float values without esd."""
        for at in self.atomic_struct.sites:
            yield [at.label, at.type_symbol, at.fract.x, at.fract.y, at.fract.z, at.disorder_group, at.occ, at.u_iso]

    @property
    def atoms_orth(self) -> Generator:
        atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))
        cell = self.atomic_struct.cell
        for at in self.atomic_struct.sites:
            x, y, z = at.orth(cell)
            yield atom(label=at.label, type=at.type_symbol, x=x, y=y, z=z,
                       part=at.disorder_group, occ=at.occ, u_eq=at.u_iso)

    def displacement_parameters(self):
        """
        Yields the anisotropic displacement parameters.
        """
        labels = self.block.find_loop('_atom_site_aniso_label')
        u11 = self.block.find_loop('_atom_site_aniso_U_11')
        u22 = self.block.find_loop('_atom_site_aniso_U_22')
        u33 = self.block.find_loop('_atom_site_aniso_U_33')
        u23 = self.block.find_loop('_atom_site_aniso_U_23')
        u13 = self.block.find_loop('_atom_site_aniso_U_13')
        u12 = self.block.find_loop('_atom_site_aniso_U_12')
        adp = namedtuple('adp', ('label', 'U11', 'U22', 'U33', 'U23', 'U13', 'U12'))
        for label, u11, u22, u33, u23, u13, u12 in zip(labels, u11, u22, u33, u23, u13, u12):
            yield adp(label=label, U11=u11, U22=u22, U33=u33, U12=u12, U13=u13, U23=u23)

    @property
    def hydrogen_atoms_present(self) -> bool:
        for at in self.atomic_struct.sites:
            if at.type_symbol in ('H', 'D'):
                return True
        return False

    @property
    def disorder_present(self) -> bool:
        for at in self.atomic_struct.sites:
            if at.disorder_group:
                return True
        return False

    @property
    def cell(self) -> Type['cell']:
        c = self.atomic_struct.cell
        nt = namedtuple('cell', 'a, b, c, alpha, beta, gamma, volume')
        return nt(c.a, c.b, c.c, c.alpha, c.beta, c.gamma, c.volume)

    def ishydrogen(self, label: str) -> bool:
        """
        Determines if an atom with the name 'label' is a hydrogen atom.
        """
        hydrogen = ('H', 'D')
        if self._iselement(label) in hydrogen:
            return True
        else:
            return False

    def checksymm(self, symm):
        """Add translation of 555 to symmetry elements without translation"""
        if len(symm) == 1 and not (symm == '.' or symm == '?'):
            symm = symm + '_555'
        return symm

    def bonds(self, without_h: bool = False) -> Generator:
        """
        Yields a list of bonds in the cif file.
        """
        label1 = self.block.find_loop('_geom_bond_atom_site_label_1')
        label2 = self.block.find_loop('_geom_bond_atom_site_label_2')
        dist = self.block.find_loop('_geom_bond_distance')
        symm = self.block.find_loop('_geom_bond_site_symmetry_2')
        publ_loop = self.block.find_loop('_geom_bond_publ_flag')
        bond = namedtuple('Bond', ('label1', 'label2', 'dist', 'symm'))
        for label1, label2, dist, symm, publ in zip(label1, label2, dist, symm, publ_loop):
            if without_h and (self.ishydrogen(label1) or self.ishydrogen(label2)) or \
                    self.yes_not_set(publ, self._has_publ_flag_set(publ_loop)):
                continue
            else:
                yield bond(label1=label1, label2=label2, dist=dist, symm=self.checksymm(symm))

    def _has_publ_flag_set(self, publ_loop: gemmi.cif.Column) -> bool:
        return any([x[0].lower() == 'y' for x in list(publ_loop) if x])

    def angles(self, without_H: bool = False) -> Generator:
        label1 = self.block.find_loop('_geom_angle_atom_site_label_1')
        label2 = self.block.find_loop('_geom_angle_atom_site_label_2')
        label3 = self.block.find_loop('_geom_angle_atom_site_label_3')
        angle_val = self.block.find_loop('_geom_angle')
        symm1 = self.block.find_loop('_geom_angle_site_symmetry_1')
        symm2 = self.block.find_loop('_geom_angle_site_symmetry_3')
        publ_loop = self.block.find_loop('_geom_angle_publ_flag')
        angle = namedtuple('Angle', ('label1', 'label2', 'label3', 'angle_val', 'symm1', 'symm2'))
        for label1, label2, label3, angle_val, symm1, symm2, publ in \
                zip(label1, label2, label3, angle_val, symm1, symm2, publ_loop):
            if without_H and (
                    self.ishydrogen(label1) or self.ishydrogen(label2) or self.ishydrogen(label3)) or \
                    self.yes_not_set(publ, self._has_publ_flag_set(publ_loop)):
                continue
            else:
                yield angle(label1=label1, label2=label2, label3=label3, angle_val=angle_val,
                            symm1=self.checksymm(symm1), symm2=self.checksymm(symm2))

    def _iselement(self, name: str) -> str:
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

    def torsion_angles(self, without_h: bool = False) -> Generator:
        label1 = self.block.find_loop('_geom_torsion_atom_site_label_1')
        label2 = self.block.find_loop('_geom_torsion_atom_site_label_2')
        label3 = self.block.find_loop('_geom_torsion_atom_site_label_3')
        label4 = self.block.find_loop('_geom_torsion_atom_site_label_4')
        torsang = self.block.find_loop('_geom_torsion')
        symm1 = self.block.find_loop('_geom_torsion_site_symmetry_1')
        symm2 = self.block.find_loop('_geom_torsion_site_symmetry_2')
        symm3 = self.block.find_loop('_geom_torsion_site_symmetry_3')
        symm4 = self.block.find_loop('_geom_torsion_site_symmetry_4')
        publ_loop = self.block.find_loop('_geom_torsion_publ_flag')
        tors = namedtuple('Torsion',
                          ('label1', 'label2', 'label3', 'label4', 'torsang', 'symm1', 'symm2', 'symm3', 'symm4'))
        for label1, label2, label3, label4, torsang, symm1, symm2, symm3, symm4, publ in zip(label1, label2, label3,
                                                                                             label4,
                                                                                             torsang, symm1, symm2,
                                                                                             symm3,
                                                                                             symm4, publ_loop):
            if without_h and (self.ishydrogen(label1) or self.ishydrogen(label2)
                              or self.ishydrogen(label3) or self.ishydrogen(label3)) or \
                    self.yes_not_set(publ, self._has_publ_flag_set(publ_loop)):
                continue
            yield tors(label1=label1, label2=label2, label3=label3, label4=label4, torsang=torsang,
                       symm1=self.checksymm(symm1),
                       symm2=self.checksymm(symm2),
                       symm3=self.checksymm(symm3),
                       symm4=self.checksymm(symm4))

    def hydrogen_bonds(self) -> Generator:
        label_d = self.block.find_loop('_geom_hbond_atom_site_label_D')
        label_h = self.block.find_loop('_geom_hbond_atom_site_label_H')
        label_a = self.block.find_loop('_geom_hbond_atom_site_label_A')
        dist_dh = self.block.find_loop('_geom_hbond_distance_DH')
        dist_ha = self.block.find_loop('_geom_hbond_distance_HA')
        dist_da = self.block.find_loop('_geom_hbond_distance_DA')
        angle_dha = self.block.find_loop('_geom_hbond_angle_DHA')
        symm = self.block.find_loop('_geom_hbond_site_symmetry_A')
        publ_loop = self.block.find_loop('_geom_hbond_publ_flag')
        hydr = namedtuple('HydrogenBond', ('label_d', 'label_h', 'label_a', 'dist_dh', 'dist_ha', 'dist_da',
                                           'angle_dha', 'symm'))
        for label_d, label_h, label_a, dist_dh, dist_ha, dist_da, angle_dha, symm, publ in \
                zip(label_d, label_h, label_a, dist_dh, dist_ha, dist_da, angle_dha, symm, publ_loop):
            if self.yes_not_set(publ, self._has_publ_flag_set(publ_loop)):
                continue
            yield hydr(label_d, label_h, label_a, dist_dh, dist_ha, dist_da, angle_dha, self.checksymm(symm))

    def yes_not_set(self, publ: str, publ_flag):
        return publ_flag and publ not in {'y', 'yes'} or publ in {'n', 'no'}

    def key_value_pairs(self) -> List[Tuple[str, str]]:
        """
        Returns the key/value pairs of a cif file sorted by priority.
        """
        keys_without_values, keys_with_values = self.keys_with_essentials()
        return keys_without_values + [('These below are already in:', '---------------------')] + keys_with_values

    def _is_centrokey(self, key) -> bool:
        """
        Is True if the kurrent key is only valid
        for non-centrosymmetric structures
        """
        return self.is_centrosymm and key in non_centrosymm_keys

    def keys_with_essentials(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """
        Returns the keys to be displayed in the main table as two separate lists.
        """
        questions = []
        # contains the answered keys:
        with_values = []
        for item in self.block:
            if item.pair is not None:
                key, value = item.pair
                if key.startswith('_shelx'):
                    # No-one should edit shelx values:
                    continue
                if key == '_iucr_refine_instructions_details':
                    continue
                if self._is_centrokey(key):
                    continue
                if not value or value == '?' or value == "'?'":
                    questions.append((key, value))
                else:
                    with_values.append((key, value))
        all_keys = [x[0] for x in with_values] + [x[0] for x in questions]
        self.check_for_missing_essential_keys(all_keys, questions)
        return sorted(questions), sorted(with_values)

    def check_for_missing_essential_keys(self, all_keys: List[Tuple[str, str]],
                                         questions: List[Tuple[str, str]]) -> None:
        """
        Check if there are keys not in the cif but in essential_keys and append them if so.
        """
        for key in essential_keys:
            if key not in all_keys:
                if self._is_centrokey(key):
                    continue
                questions.append((key, '?'))
                self.block.set_pair(key, '?')

    def test_res_checksum(self) -> bool:
        """
        A method to check whether the checksums in the cif file fit to the content.
        """
        cif_res_ckecksum = 0
        res_checksum_calcd = self.res_checksum_calcd
        if res_checksum_calcd > 0:
            cif_res_ckecksum = self['_shelx_res_checksum'] or -1
            try:
                cif_res_ckecksum = int(cif_res_ckecksum)
            except ValueError:
                cif_res_ckecksum = -1
        if cif_res_ckecksum > 0 and cif_res_ckecksum != res_checksum_calcd:
            return False
        else:
            return True

    def test_hkl_checksum(self) -> bool:
        """
        A method to check whether the checksums in the cif file fit to the content.
        """
        cif_hkl_ckecksum = 0
        hkl_checksum_calcd = self.hkl_checksum_calcd
        if hkl_checksum_calcd > 0:
            cif_hkl_ckecksum = self['_shelx_hkl_checksum'] or -1
            try:
                cif_hkl_ckecksum = int(cif_hkl_ckecksum)
            except ValueError:
                cif_hkl_ckecksum = -1
        if cif_hkl_ckecksum > 0 and cif_hkl_ckecksum != hkl_checksum_calcd:
            return False
        else:
            return True


if __name__ == '__main__':
    # c = CifContainer('../41467_2015.cif')
    # c = CifContainer('test-data/p21c.cif')
    from pprint import pp

    c = CifContainer('test-data/DK_Zucker2_0m.cif')
    c.load_this_block(len(c.doc) - 1)
    pp(list(c.torsion_angles()))
    # pp(c.hkl_extra_info)
    # print(c.hkl_file)
    # print(c.hkl_as_cif)
    # print(c.test_hkl_checksum())
    # s = Shelxfile()
    # print(c.res_file_data)
    # s.read_string(c.res_file_data)
    # print(s.hklf.n)

    # print(CifContainer('tests/examples/1979688.cif').hkl_as_cif[-250:])

    """
    import n#umpy as np
    mtz = gemmi.Mtz(with_base=True)
    data = [x.split() for x in c.hkl_file.splitlines()]
    mtz.add_column('I', 'I')
    mtz.add_column('SIGI', 'Q')
    mtz.set_data(data)
    mtz.set_cell_for_all(gemmi.UnitCell(c.cell.a, c.cell.b, c.cell.c, c.cell.alpha, c.cell.beta, c.cell.gamma))
    mtz.spacegroup = gemmi.find_spacegroup_by_name(c.space_group)
    mtz.update_reso()
    size = mtz.get_size_for_hkl()
    np.seterr(divide='ignore', invalid='ignore')
    ios =  intensity.array / sigma.array
    
    doc = gemmi.cif.read('tests/examples/1979688-finalcif.fcf')
    rblock = gemmi.hkl_cif_as_refln_block(doc[0])
    """
