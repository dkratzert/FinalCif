from __future__ import annotations

import abc
import dataclasses
import enum
import itertools
import pathlib
import re
import sys
from collections import namedtuple
from collections.abc import Iterator
from contextlib import suppress
from math import sin, radians
from pathlib import Path
from typing import Any

from qtpy.QtWidgets import QApplication

from finalcif.cif.text import string_to_utf8
from finalcif.template.xsl.convert import xml_to_html
from finalcif.tools.dsrmath import my_isnumeric

# This is necessary, because if jinja crashes, we show an error dialog:
app = QApplication.instance()
if app is None:
    app = QApplication([])

from jinja2 import select_autoescape

import jinja2
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate, RichText, InlineImage, Subdoc
from shelxfile.atoms.atoms import Atom as SHXAtom

from finalcif import app_path
from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.dialogs import show_general_warning
from finalcif.report import references as ref, report_text
from finalcif.report.references import Reference
from finalcif.report.report_text import (math_to_word, gstr, format_radiation, _get_cooling_device)
from finalcif.report.symm import SymmetryElement
from finalcif.tools.misc import (isnumeric, this_or_quest, timessym, angstrom, protected_space,
                                 less_or_equal, halbgeviert, minus_sign, ellipsis_mid, angstrom_to_pm,
                                 angstrom_to_nanometers, do_nothing)
from finalcif.tools.options import Options
from finalcif.tools.space_groups import SpaceGroups

AdpWithMinus = namedtuple('AdpWithMinus', ('label', 'U11', 'U22', 'U33', 'U23', 'U13', 'U12'))

experiment_table_columns = ['axis', 'distance', 'theta', 'omega', 'phi', 'chi', 'width', 'images', 'time',
                            'wavelength', 'voltage', 'current', 'temperature']
TableRow = namedtuple('TableRow', experiment_table_columns)


class ReportFormat(enum.Enum):
    RICHTEXT = 'richtext'
    HTML = 'html'


@dataclasses.dataclass(frozen=True)
class Bond:
    atoms: str
    symm: str
    dist: str


@dataclasses.dataclass(frozen=True)
class Angle:
    atom1: str
    atom2: str
    symm1: str
    symm2: str
    angle: str


@dataclasses.dataclass(frozen=True)
class Torsion:
    atom1: str
    atom2: str
    atom3: str
    atom4: str
    symm1: str
    symm2: str
    symm3: str
    symm4: str
    angle: str


@dataclasses.dataclass(frozen=True)
class HydrogenBond:
    atoms: str
    dist_dh: str
    dist_ha: str
    dist_da: str
    angle_dha: str
    symm: str


class BondsAndAngles:
    def __init__(self, cif: CifContainer, without_h: bool):
        self.cif = cif
        self.without_h = without_h
        self._symmlist = {}
        # These can be used as strings for python-docx:
        self.bonds_as_string: list[Bond] = []
        self.angles_as_string: list[Angle] = []
        # These can be used as Richtext for python-docx-tpl:
        self.bonds_richtext: list[dict[str, RichText]] = self._get_bonds_list(without_h)
        self.angles_richtext: list[dict[str, RichText]] = self._get_angles_list(without_h)
        # The list of symmetry elements at the table end used for generated atoms:
        self.symminfo: str = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.bonds_richtext) + len(self.angles_richtext)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_bonds_list(self, without_h: bool) -> list[dict[str, RichText]]:
        bonds = []
        num = 1
        newsymms = {}
        symms = {}
        for at1, at2, dist, symm2 in self.cif.bonds(without_h):
            dist = dist.replace('-', minus_sign)
            if symm2 in ('.', '?'):
                symm2 = None
            num = symmsearch(self.cif, newsymms, num, symm2, symms)
            # Atom1 - Atom2:
            a = f'{at1}{halbgeviert}{at2}'
            symm = f'#{symms[symm2]!s}' if symm2 else ''
            atoms = RichText(a)
            atoms.add(symm, superscript=True)
            bonds.append({'atoms': atoms, 'dist': dist})
            self.bonds_as_string.append(Bond(atoms=a, symm=symm, dist=dist))
        self._symmlist.update(newsymms)
        return bonds

    def _get_angles_list(self, without_h: bool) -> list[dict[str, RichText]]:
        angles_list = []
        newsymms = {}
        symms = {}
        num = 1
        for ang in self.cif.angles(without_h):
            symm1 = ang.symm1
            symm2 = ang.symm2
            if symm1 in ('.', '?'):
                symm1 = None
            if symm2 in ('.', '?'):
                symm2 = None
            num = symmsearch(self.cif, newsymms, num, symm1, symms)
            num = symmsearch(self.cif, newsymms, num, symm2, symms)
            symm1_str = f'#{symms[symm1]!s}' if symm1 else ''
            symm2_str = f'#{symms[symm2]!s}' if symm2 else ''
            angle_val = ang.angle_val.replace('-', minus_sign)
            # atom1 symm1_str a symm2_str
            atoms = RichText(ang.label1)
            atoms.add(symm1_str, superscript=True)
            a = f'{halbgeviert}{ang.label2}{halbgeviert}{ang.label3}'
            atoms.add(a, superscript=False)
            atoms.add(symm2_str, superscript=True)
            angles_list.append({'atoms': atoms, 'angle': angle_val})
            self.angles_as_string.append(
                Angle(atom1=ang.label1, atom2=a, symm1=symm1_str, symm2=symm2_str, angle=angle_val))
        self._symmlist.update(newsymms)
        return angles_list


class TorsionAngles:

    def __init__(self, cif: CifContainer, without_h: bool):
        self.cif = cif
        self.without_h = without_h
        self._symmlist = {}
        self.torsion_angles_as_string: list[Torsion] = []
        self.torsion_angles_as_richtext = self._get_torsion_angles_list(without_h)
        # The list of symmetry elements at the table end used for generated atoms:
        self.symminfo: str = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.torsion_angles_as_richtext)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_torsion_angles_list(self, without_h: bool) -> list[dict[str, RichText]]:
        if self.cif.nangles(without_h) <= 0:
            return []
        symms = {}
        newsymms = {}
        num = 1
        torsion_angles = []
        for tors in self.cif.torsion_angles(without_h):
            symm1, symm2, symm3, symm4 = tors.symm1, tors.symm2, tors.symm3, tors.symm4
            if symm1 in ('.', '?'):
                symm1 = None
            if symm2 in ('.', '?'):
                symm2 = None
            if symm3 in ('.', '?'):
                symm3 = None
            if symm4 in ('.', '?'):
                symm4 = None
            num = symmsearch(self.cif, newsymms, num, symm1, symms)
            num = symmsearch(self.cif, newsymms, num, symm2, symms)
            num = symmsearch(self.cif, newsymms, num, symm3, symms)
            num = symmsearch(self.cif, newsymms, num, symm4, symms)
            symmstr1 = f'#{symms[symm1]!s}' if symm1 else ''
            symmstr2 = f'#{symms[symm2]!s}' if symm2 else ''
            symmstr3 = f'#{symms[symm3]!s}' if symm3 else ''
            symmstr4 = f'#{symms[symm4]!s}' if symm4 else ''
            atoms = RichText(tors.label1)
            atoms.add(symmstr1, superscript=True)
            atoms.add(halbgeviert)
            atoms.add(tors.label2)
            atoms.add(symmstr2, superscript=True)
            atoms.add(halbgeviert)
            atoms.add(tors.label3)
            atoms.add(symmstr3, superscript=True)
            atoms.add(halbgeviert)
            atoms.add(tors.label4)  # labels
            atoms.add(symmstr4, superscript=True)
            angle = tors.torsang.replace('-', minus_sign)
            torsion_angles.append({'atoms': atoms, 'angle': angle})
            self.torsion_angles_as_string.append(Torsion(atom1=tors.label1, atom2=tors.label2,
                                                         atom3=tors.label3, atom4=tors.label4,
                                                         symm1=symmstr1, symm2=symmstr2,
                                                         symm3=symmstr3, symm4=symmstr4,
                                                         angle=angle))
        self._symmlist = newsymms
        return torsion_angles


class HydrogenBonds:
    def __init__(self, cif: CifContainer):
        self.cif = cif
        self._symmlist = {}
        self.hydrogen_bonds_as_str: list[HydrogenBond] = []
        self.hydrogen_bonds = self._get_hydrogen_bonds()
        self.symminfo = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.hydrogen_bonds)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_hydrogen_bonds(self) -> list[dict]:
        symms = {}
        newsymms = {}
        num = 1
        atoms_list = []
        for h in self.cif.hydrogen_bonds():
            symm = h.symm
            if symm in ('.', '?'):
                symm = None
            num = symmsearch(self.cif, newsymms, num, symm, symms)
            symmval = f'#{symms[symm]!s}' if symm else ''
            a = h.label_d + halbgeviert + h.label_h + ellipsis_mid + h.label_a
            atoms = RichText(a)
            atoms.add(symmval, superscript=True)
            atoms_list.append({'atoms'  : atoms, 'dist_dh': h.dist_dh, 'dist_ha': h.dist_ha,
                               'dist_da': h.dist_da, 'angle_dha': h.angle_dha})
            self.hydrogen_bonds_as_str.append(HydrogenBond(atoms=a, dist_dh=h.dist_dh,
                                                           dist_ha=h.dist_ha, dist_da=h.dist_da,
                                                           angle_dha=h.angle_dha, symm=symmval))
        self._symmlist = newsymms
        return atoms_list


def get_card(cif: CifContainer, symm: str) -> list[str] | None:
    """
    Returns a symmetry card from the _space_group_symop_operation_xyz or _symmetry_equiv_pos_as_xyz list.
    :param cif: the cif file object
    :param symm: the symmetry number
    :return: ['x', ' y', ' z'] etc
    """
    try:
        card = cif.symmops[int(symm.split('_')[0]) - 1].split(',')
    except IndexError:
        return None
    return card


def get_symminfo(newsymms: dict[int, str]) -> str:
    """
    Adds text about the symmetry generators used in order to add symmetry generated atoms.
    """
    line = 'Symmetry transformations used to generate equivalent atoms:\n'
    nitems = len(newsymms)
    n = 0
    for key, value in newsymms.items():
        sep = ';'
        if n == nitems:
            sep = ''
        n += 1
        line += f"#{key}: {value}{sep}   "
    if newsymms:
        return line
    else:
        return ''


def symmsearch(cif: CifContainer, newsymms: dict[int, str], num: int,
               symm: str | None, symms_list: dict[str, int]) -> int:
    if symm and symm not in symms_list.keys():
        symms_list[symm] = num
        card = get_card(cif, symm)
        if card is None:
            num += 1
            return num
        s = SymmetryElement(card)
        s.translate(symm)
        newsymms[num] = s.toShelxl()
        num += 1
    return num


class Atoms:
    def __init__(self, cif: CifContainer):
        """
        Text for non-hydrogen atoms.
        """
        self.rt = RichText()
        self.cif = cif
        self.n_isotropic = self.number_of_isotropic_atoms(without_h=True)
        self.n_isotropic_with_h = self.number_of_isotropic_atoms(without_h=False)
        number = 'All'
        parameter_type = 'anisotropic'
        if 0 < self.n_isotropic < self.cif.natoms(without_h=True):
            number = (f'Some atoms ({self.n_isotropic}) were refined using isotropic displacement parameters. '
                      f'All other')
        if self.n_isotropic > 0 and self.n_isotropic > self.cif.natoms(without_h=True):
            number = (f'Most atoms ({self.n_isotropic}) were refined using isotropic displacement parameters. '
                      f'All other')
        if self.n_isotropic == self.cif.natoms(without_h=True):
            number = 'All'
            parameter_type = 'isotropic'
        non_h = 'non-hydrogen '
        sentence1 = (f"{number} {non_h if self.n_isotropic_with_h > 0 else ''}atoms were refined with {parameter_type} "
                     f"displacement parameters. ")
        self.rt.add(sentence1)

    def richtext(self) -> RichText:
        return self.rt

    def html(self):
        """
        Transforms XML to HTML using XSLT.
        """
        return xml_to_html(self.rt)

    def number_of_isotropic_atoms(self, without_h: bool = True) -> float | int:
        isotropic_count = 0
        for site in self.cif.atomic_struct.sites:
            if self.atom_is_isotropic(site, without_h):
                isotropic_count += 1
        return isotropic_count

    @staticmethod
    def atom_is_isotropic(site, without_h: bool) -> bool:
        if without_h:
            return not site.aniso.nonzero() and not site.element.is_hydrogen
        else:
            return not site.aniso.nonzero()


class Hydrogens:
    def __init__(self, cif: CifContainer):
        """
        The hydrogen atoms were refined isotropically on calculated positions using
        a riding model with their Uiso values constrained to 1.5 times the Ueq of
        their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other
        carbon atoms.
        """
        rt = RichText()
        hatoms: list[SHXAtom] = [x for x in cif.shx.atoms.all_atoms if x.is_hydrogen]
        n_hatoms = len(hatoms)
        n_anisotropic_h = len([x for x in hatoms if sum([abs(y) for y in x.uvals[1:]]) > 0.0001])
        n_constr_h = len([x for x in hatoms if x.uvals[0] < -1.0])
        riding_atoms = [x for x in hatoms if x.afix]
        pivot_atoms = self.get_hydrogen_pivot_atoms(riding_atoms)
        n_riding = len(riding_atoms)
        n_non_riding = len(hatoms) - n_riding

        atom_type = "carbon"
        number = "The"
        sentence_isotropic = "isotropic"
        sentence_anisotropic = "anisotropic"

        if n_anisotropic_h == n_hatoms:
            # number = "All"
            utype = sentence_anisotropic
        elif n_anisotropic_h > 0 and n_anisotropic_h < n_hatoms:
            number = "Some"
            utype = sentence_isotropic + " and some with anisotropic "
        else:
            if all(self.pivot_atom_types(pivot_atoms)):
                number = "All"
            elif any(self.pivot_atom_types(pivot_atoms)):
                number = "All C-bound"
            else:
                number = "The heteroatom-bound"
            utype = sentence_isotropic
        sentence_riding = "on calculated positions using a riding model with their "
        sentence_free_pos = "freely"
        sentence_15 = " values constrained to 1.5 times the "  # Ueq
        sentence_pivot = " of their pivot atoms for terminal sp"  # 3
        # Adding dot later:
        sentence_12 = f" {atom_type} atoms and 1.2 times for all other {atom_type} atoms"

        if n_riding == n_hatoms:
            rt.add(f"{number} hydrogen atoms were refined {utype} ")
            riding = sentence_riding
            rt.add(riding)
            self.u_iso(rt)
            rt.add(sentence_15)
            self.u_eq(rt)
            rt.add(sentence_pivot)
            rt.add('3', superscript=True)
            rt.add(sentence_12)
        elif n_non_riding == n_hatoms:
            if n_constr_h == n_hatoms:
                rt.add(f"{number} hydrogen atoms were refined {sentence_free_pos}"
                       f" with their ")
            else:
                rt.add(f"{number} hydrogen atoms were refined {sentence_free_pos}"
                       f" with {utype} displacement parameters.")
            if n_constr_h == n_hatoms:
                self.u_iso(rt)
                rt.add(sentence_15)
                self.u_eq(rt)
                rt.add(sentence_pivot)
                rt.add('3', superscript=True)
                rt.add(sentence_12)
        else:
            rt.add(f"{number} hydrogen atoms were refined with {utype} displacement parameters. ")
            riding = f"Some of their coordinates were refined {sentence_free_pos} and some {sentence_riding}"
            rt.add(riding)
            self.u_iso(rt)
            rt.add(sentence_15)
            self.u_eq(rt)
            rt.add(sentence_pivot)
            rt.add('3', superscript=True)
            rt.add(sentence_12)
        rt.add('. ')  # End of paragraph
        self.rt = rt

    def pivot_atom_types(self, pivot_atoms):
        return [x.element == 'C' for x in pivot_atoms]

    def get_hydrogen_pivot_atoms(self, riding_atoms):
        pivot_atoms = []
        for at in riding_atoms:
            pivot_atoms.extend(at.find_atoms_around(dist=1.2))
        return pivot_atoms

    def u_eq(self, rt: RichText):
        rt.add('U', italic=True)
        rt.add('eq', subscript=True)

    def u_iso(self, rt: RichText):
        rt.add('U', italic=True)
        rt.add('iso', subscript=True)

    def richtext(self) -> RichText:
        return self.rt

    def html(self):
        """
        Transforms XML to HTML using XSLT.
        """
        return xml_to_html(self.rt)


class Disorder:
    def __init__(self, cif: CifContainer):
        self.rt = RichText()
        self.dsr_sentence = ''
        sentence1 = ("Disordered moieties were refined using bond lengths "
                     "restraints and displacement parameter restraints. ")
        self.rt.add(sentence1)
        if cif.dsr_used:
            dsr_sentence = "Some parts of the disorder model were introduced by the program DSR."
            self.rt.add(dsr_sentence)
            # reflist.append([references.DSRReference2015(), references.DSRReference2018()])

    def richtext(self) -> RichText:
        return self.rt

    def html(self):
        """
        Transforms XML to HTML using XSLT.
        """
        return xml_to_html(self.rt)


class Formatter(abc.ABC):
    def __init__(self, options: Options, cif: CifContainer) -> None:
        self.literature: dict[str, Reference] = {'finalcif'   : ref.FinalCifReference(),
                                                 'ccdc'       : ref.CCDCReference(),
                                                 'absorption' : ref.DummyReference(),
                                                 'solution'   : ref.DummyReference(),
                                                 'refinement' : ref.DummyReference(),
                                                 'integration': ref.DummyReference(),
                                                 'dsr'        : ref.DummyReference(),
                                                 }
        self._bonds_angles = BondsAndAngles(cif, without_h=options.without_h)
        self._torsions = TorsionAngles(cif, without_h=options.without_h)
        self._hydrogens = HydrogenBonds(cif)

    @abc.abstractmethod
    def get_bonds(self):
        ...

    @abc.abstractmethod
    def get_angles(self):
        ...

    @abc.abstractmethod
    def get_torsion_angles(self) -> list[dict[str, RichText]] | list[Torsion]:
        ...

    @abc.abstractmethod
    def get_hydrogen_bonds(self) -> list[dict[str, RichText]] | list[HydrogenBond]:
        ...

    def get_bonds_angles_symminfo(self) -> str:
        return self._bonds_angles.symminfo

    def get_torsion_symminfo(self) -> str:
        return self._torsions.symminfo

    def get_hydrogen_symminfo(self) -> str:
        return self._hydrogens.symminfo

    def get_crystallization_method(self, cif: CifContainer) -> str:
        return string_to_utf8(gstr(cif['_exptl_crystal_recrystallization_method']))

    @abc.abstractmethod
    def get_radiation(self, cif: CifContainer) -> str | RichText:
        ...

    def get_wavelength(self, cif: CifContainer) -> str:
        try:
            return cif['_diffrn_radiation_wavelength'] if not cif.picometer else angstrom_to_pm(
                cif['_diffrn_radiation_wavelength'])
        except ValueError:
            return ''

    @abc.abstractmethod
    def hkl_index_limits(self, cif: CifContainer) -> str:
        ...

    def make_3d(self, cif: CifContainer, options: Options) -> str:
        raise NotImplementedError

    def space_group_formatted(self, cif: CifContainer, tpl_doc: DocxTemplate):
        raise NotImplementedError

    def make_picture(self, options: Options, picfile: Path, tpl_doc: DocxTemplate):
        raise NotImplementedError

    @abc.abstractmethod
    def format_sum_formula(self, sum_formula: str) -> str:
        ...

    def hydrogen_atoms_refinement(self, cif: CifContainer) -> RichText | str:
        """
        Returns the text describing the refinement of hydrogen atoms.
        """
        raise NotImplementedError

    def atoms_refinement(self, cif: CifContainer) -> RichText | str:
        """
        Returns the text describing the refinement of all non-hydrogen atoms.
        """
        raise NotImplementedError

    def disorder_description(self, cif: CifContainer) -> str:
        raise NotImplementedError

    @staticmethod
    def get_from_to_theta_range(cif: CifContainer) -> str:
        theta_min = cif['_diffrn_reflns_theta_min']
        theta_max = cif['_diffrn_reflns_theta_max']
        radiation_wavelength = cif['_diffrn_radiation_wavelength']
        try:
            resolution_angst = float(radiation_wavelength) / (2 * sin(radians(float(theta_max))))
            if cif.picometer:
                d_max = f' ({angstrom_to_pm(str(resolution_angst)):.2}{protected_space}pm)'
            else:
                d_max = f' ({resolution_angst:.2f}{protected_space}{angstrom})'
            # 2theta range:
            return f"{2 * float(theta_min):.2f} to {2 * float(theta_max):.2f}{d_max}"
        except ValueError:
            return '? to ?'

    @staticmethod
    def get_diff_density_min(cif: CifContainer) -> str:
        try:
            diff_density_min = f"{float(cif['_refine_diff_density_min']):.2f}"
        except ValueError:
            diff_density_min = '?'
        return diff_density_min

    @staticmethod
    def get_diff_density_max(cif: CifContainer) -> str:
        try:
            diff_density_max = f"{float(cif['_refine_diff_density_max']):.2f}"
        except ValueError:
            diff_density_max = '?'
        return diff_density_max

    @staticmethod
    def get_exti(cif: CifContainer) -> str:
        exti = cif['_refine_ls_extinction_coef']
        if exti not in ['.', "'.'", '?', '']:
            return exti
        else:
            return ''

    @staticmethod
    def get_flackx(cif: CifContainer) -> str:
        if not cif.is_centrosymm:
            return cif['_refine_ls_abs_structure_Flack'] or '?'
        else:
            return ''

    def get_integration_program(self, cif: CifContainer) -> str:
        integration = gstr(cif['_computing_data_reduction']) or ''
        integration_prog = '[No _computing_data_reduction given]'
        if 'SAINT' in integration:
            saintversion = ''
            integration_prog = 'SAINT'
            if len(integration.split()) > 1:
                saintversion = integration.split()[1]
                integration_prog += " " + saintversion
            self.literature['integration'] = ref.SAINTReference('SAINT', saintversion)
        if 'CrysAlisPro'.lower() in integration.lower():
            regex = r"(CrysAlisPro)\s{0,2}(\d+\.\d+\.\d+\.\d+.*)\((.*),\s?(\d+)\)"
            year = 'unknown version'
            version = ''
            match = re.match(regex, integration, re.MULTILINE | re.IGNORECASE | re.ASCII)
            if match:
                year = match.group(4).strip()
                version = match.group(2).strip()
                integration_prog = match.group(1).strip()
            else:
                integration_prog = 'CrysAlisPro'
            self.literature['integration'] = ref.CrysalisProReference(version=version, year=year)
            self.literature['absorption'] = ref.CrysalisProReference(version=version, year=year)
        if 'XDS' in integration:
            self.literature['integration'] = ref.XDSReference()
            integration_prog = 'XDS'
        if 'STOE X-RED'.lower() in integration.lower():
            integration_prog = 'STOE X-RED'
            self.literature['integration'] = ref.XRedReference('X-RED', '[unknown version]')
        return integration_prog

    def get_refinement_gui(self, cif: CifContainer) -> str:
        refined = gstr(cif['_computing_structure_refinement'])
        gui_reference = ref.DummyReference()
        refinement_gui = ''
        if 'shelxle' in refined.lower() or 'shelxle' in cif['_computing_molecular_graphics'].lower():
            gui_reference = ref.ShelXleReference()
            refinement_gui = 'ShelXle'
        elif 'olex' in refined.lower() or 'olex' in cif['_computing_molecular_graphics'].lower():
            gui_reference = ref.Olex2Reference()
            refinement_gui = 'Olex2'
        else:
            refinement_gui = '[Unknown program in _computing_structure_refinement]'
        self.literature['gui'] = gui_reference
        return string_to_utf8(refinement_gui)

    def _get_scaling_program(self, absdetails: str) -> tuple[str, str]:
        scale_prog = ''
        version = ''
        if 'SADABS' in absdetails.upper() or 'TWINABS' in absdetails.upper():
            if len(absdetails.split()) > 1:
                version = absdetails.split()[1]
            else:
                version = 'unknown version'
            if 'SADABS' in absdetails:
                scale_prog = 'SADABS'
            else:
                scale_prog = 'TWINABS'
            self.literature['absorption'] = ref.SadabsTwinabsReference()
        return scale_prog, version

    def get_absortion_correction_program(self, cif: CifContainer) -> str:
        absdetails = cif['_exptl_absorpt_process_details'].replace('-', ' ').replace(':', '')
        bruker_scaling = cif['_computing_bruker_data_scaling'].replace('-', ' ').replace(':', '')
        scale_prog, version = self._get_scaling_program(absdetails)
        if not scale_prog:
            scale_prog, version = self._get_scaling_program(bruker_scaling)
        if 'SORTAV' in absdetails.upper():
            scale_prog = 'SORTAV'
            self.literature['absorption'] = ref.SORTAVReference()
        if 'crysalis' in absdetails.lower():
            scale_prog = 'SCALE3 ABSPACK'
            # see above also
        if 'STOE X-RED'.lower() in scale_prog.lower():
            version = 'unknown version'
            scale_prog = 'STOE X-RED'
            self.literature['absorption'] = ref.XRedReference('X-RED', 'unknown version')
        scale_prog += " " + version
        return string_to_utf8(scale_prog)

    def solution_method(self, cif: CifContainer) -> str:
        solution_method = gstr(cif['_atom_sites_solution_primary']) or '??'
        return solution_method.strip('\n\r').strip()

    def refinement_prog(self, cif: CifContainer) -> Reference | str:
        refined = gstr(cif['_computing_structure_refinement']) or '??'
        if 'SHELXL' in refined.upper() or 'XL' in refined.upper():
            self.literature['refinement'] = ref.SHELXLReference()
        if 'OLEX' in refined.upper():
            self.literature['refinement'] = ref.Olex2Reference()
        if ('NOSPHERA2' in refined.upper() or 'NOSPHERA2' in cif['_refine_special_details'].upper() or
            'NOSPHERAT2' in cif['_olex2_refine_details'].upper()):
            self.literature['refinement'] = ref.Nosphera2Reference()
        return string_to_utf8(refined.split('(')[0]).strip()

    def solution_program(self, cif: CifContainer) -> str:
        solution_prog = gstr(cif['_computing_structure_solution']) or '??'
        if solution_prog.upper().startswith(('SHELXT', 'XT')):
            self.literature['solution'] = ref.SHELXTReference()
        if 'SHELXS' in solution_prog.upper():
            self.literature['solution'] = ref.SHELXSReference()
        if 'SHELXD' in solution_prog.upper():
            self.literature['solution'] = ref.SHELXDReference()
        return string_to_utf8(solution_prog.split('(')[0]).strip()

    def t_minvalue(self, cif: CifContainer) -> str:
        t_min = cif['_exptl_absorpt_correction_T_min']
        with suppress(ValueError):
            return f'{float(t_min):.4f}'
        return '?'

    def t_maxvalue(self, cif: CifContainer) -> str:
        t_max = cif['_exptl_absorpt_correction_T_max']
        with suppress(ValueError):
            return f'{float(t_max) :.4f}'
        return '?'

    def get_atomic_coordinates(self, cif: CifContainer) -> tuple[dict[str, str], ...]:
        coords = []
        for at in cif.atoms(without_h=False):
            coords.append({
                'label': at.label,
                'type' : at.type,
                'x'    : at.x.replace('-', minus_sign),
                'y'    : at.y.replace('-', minus_sign),
                'z'    : at.z.replace('-', minus_sign),
                'part' : at.part.replace('-', minus_sign),
                'occ'  : at.occ.replace('-', minus_sign),
                'u_eq' : at.u_eq.replace('-', minus_sign)
            })
        return tuple(coords)

    def get_displacement_parameters(self, cif: CifContainer) -> tuple[AdpWithMinus, ...]:
        """
        Returns anisotropic displacement parameters with hyphens replaced by minus signs.
        """
        return tuple(AdpWithMinus(label=label,
                                  U11=u11.replace('-', minus_sign),
                                  U22=u22.replace('-', minus_sign),
                                  U33=u33.replace('-', minus_sign),
                                  U12=u12.replace('-', minus_sign),
                                  U13=u13.replace('-', minus_sign),
                                  U23=u23.replace('-', minus_sign))
                     for label, u11, u22, u33, u23, u13, u12 in cif.displacement_parameters())

    def get_completeness(self, cif: CifContainer) -> str:
        try:
            completeness = f"{float(cif['_diffrn_measured_fraction_theta_full']) * 100:.1f}"
        except ValueError:
            completeness = cif['_diffrn_measured_fraction_theta_full']
        return completeness

    def format_experiment_table(self, cif: CifContainer):
        result = []
        table = cif.block.find('_bruker_diffrn_runs_', experiment_table_columns)
        for row in table:
            result.append(TableRow(axis=row['axis'] if not row['axis'] == '?' else minus_sign,
                                   distance=self._value_format(row['distance'], '{:.2f}'),
                                   theta=self._value_format(row['theta'], '{:.2f}', multiply=True),
                                   omega=self._value_format(row['omega'], '{:.2f}'),
                                   phi=self._value_format(row['phi'], '{:.2f}'),
                                   chi=self._value_format(row['chi'], '{:.2f}'),
                                   width=self._value_format(row['width'], '{:.2f}'),
                                   images=row['images'],
                                   time=self._value_format(row['time'], '{:.2f}'),
                                   wavelength=self._value_format(row['wavelength'], '{:.5f}'),
                                   voltage=self._value_format(row['voltage'], '{:.0f}'),
                                   current=self._value_format(row['current'], '{:.1f}'),
                                   temperature=self._value_format(row['temperature'], '{:.1f}'),
                                   )
                          )
        return result

    def _value_format(self, value: str, string_format: str, multiply: bool = False) -> str:
        if value is None:
            value = 0.0
        if my_isnumeric(value):
            value = float(value)
            if multiply:
                value *= 2
            return string_format.format(value).replace('-', minus_sign)
        else:
            return str(value).replace('-', minus_sign)

    def get_number_of_collected_images(self, cif: CifContainer) -> str:
        try:
            return str(sum([int(x) for x in cif.block.find_values('_bruker_diffrn_runs_images')]))
        except (ValueError, SyntaxError):
            return 'n/a'

    def get_experiment_time(self, cif: CifContainer) -> str:
        if exptime := cif['cif._diffrn_measurement_bruker_total_exposure_time']:
            with suppress(ValueError):
                return f'{float(exptime) / 3600.0:.2f}'
        images = cif.block.find_values('_bruker_diffrn_runs_images')
        times = cif.block.find_values('_bruker_diffrn_runs_time')
        axes = cif.block.find_values('_bruker_diffrn_runs_axis')
        try:
            seconds = sum([(images is not None and time is not None and int(images) * float(time)) or 0.0
                           for axis, images, time in zip(axes, images, times, strict=False) if axis], 0.0)
        except ValueError:
            seconds = 0
        if seconds > 0.0001:
            return f'{seconds / 3600.0:.2f}'
        return 'n/a'

    def get_angstrom_resolution(self, cif: CifContainer):
        wavelen = cif['_diffrn_radiation_wavelength']
        thetamax = cif['_diffrn_reflns_theta_max']
        try:
            d = float(wavelen) / (2 * sin(radians(float(thetamax))))
        except(ZeroDivisionError, TypeError, ValueError):
            return ''
        return f'{d:.2f}'

    def get_redundancy(self, cif):
        if twinabs := cif['_diffrn_reflns_bruker_twinabs_number']:
            n_refl = twinabs
        else:
            n_refl = cif['_diffrn_reflns_number']
        n_all = cif['_reflns_number_total']
        try:
            redundancy = float(n_refl) / float(n_all)
        except(ZeroDivisionError, TypeError, ValueError):
            return ''
        return f'{redundancy:.2f}'

    def get_data_to_param(self, cif):
        n_refl = cif['_refine_ls_number_reflns']
        n_param = cif['_refine_ls_number_parameters']
        try:
            redundancy = float(n_refl) / float(n_param)
        except(ZeroDivisionError, TypeError, ValueError):
            return ''
        return f'{redundancy:.2f}'

    def refinement_details(self, cif):
        details = ' '.join(cif['_refine_special_details'].splitlines(keepends=False)).strip()
        return string_to_utf8(details)


class HtmlFormatter(Formatter):

    def __init__(self, options: Options, cif: CifContainer) -> None:
        super().__init__(options, cif)

    def get_bonds(self) -> list[Bond]:
        return self._bonds_angles.bonds_as_string

    def get_angles(self) -> list[Angle]:
        return self._bonds_angles.angles_as_string

    def get_torsion_angles(self) -> list[Torsion]:
        return self._torsions.torsion_angles_as_string

    def get_hydrogen_bonds(self) -> list[HydrogenBond]:
        return self._hydrogens.hydrogen_bonds_as_str

    def _format_symminfo(self, txt: str) -> str:
        return (txt.replace('#1:', '<br>#1:')
                .replace(', ', ',&nbsp;')
                .replace(': ', ':&nbsp;')
                .replace('-', minus_sign))

    def get_bonds_angles_symminfo(self) -> str:
        return self._format_symminfo(self._bonds_angles.symminfo)

    def get_torsion_symminfo(self) -> str:
        return self._format_symminfo(self._torsions.symminfo)

    def get_hydrogen_symminfo(self) -> str:
        return self._format_symminfo(self._hydrogens.symminfo)

    def make_3d(self, cif: CifContainer, options: Options) -> str:
        return '[3D representation of the structure in html/javascript not implemented]'

    def space_group_formatted(self, cif: CifContainer, _: None) -> str:
        s = SpaceGroups()
        try:
            spgrxml = s.to_html(cif.space_group)
            # Mathml doesn't work well in pyQt
            # spgrxml = s.to_mathml(cif.space_group)
        except KeyError:
            spgrxml = '<math xmlns="http://www.w3.org/1998/Math/MathML">?</math>'
        try:
            number = cif.spgr_number
        except AttributeError:
            return '?'
        return f'{spgrxml} ({number})'

    def make_picture(self, options: Options, picfile: Path, _: None) -> str:
        picture_path = ''
        if options.report_text and picfile and picfile.exists():
            picture_path = str(picfile.resolve())
        return picture_path  # (f'<img src="{picture_path}" '
        # f'alt="Structure View" style="width:20%;height:20%;">')

    def format_sum_formula(self, sum_formula: str) -> str:
        sum_formula_group = [''.join(x[1]) for x in itertools.groupby(sum_formula, lambda x: x.isalpha())]
        html_text = ''
        if sum_formula_group:
            for _, word in enumerate(sum_formula_group):
                if isnumeric(word):
                    html_text += f'<sub>{word}</sub>'
                elif ')' in word:
                    html_text += f"<sub>{word.split(')')[0]}</sub>)"
                elif ']' in word:
                    html_text += f"<sub>{word.split(']')[0]}</sub>)"
                else:
                    html_text += word
                    if word == ',':
                        html_text += ';&nbsp;'
            return html_text
        else:
            return 'no formula'

    def hydrogen_atoms_refinement(self, cif: CifContainer) -> str:
        return Hydrogens(cif).html()

    def atoms_refinement(self, cif: CifContainer) -> str:
        return Atoms(cif).html()

    def disorder_description(self, cif: CifContainer) -> str:
        self.literature['dsr'] = ref.DSRReference2018()
        return Disorder(cif).html()

    def get_radiation(self, cif: CifContainer) -> str:
        rad_element, radtype, radline = format_radiation(cif['_diffrn_radiation_type'])
        radiation = f'{rad_element}<i>{radtype}</i><i><sub>{radline}</sub></i>'
        return radiation

    def hkl_index_limits(self, cif: CifContainer) -> str:
        limit_h_min = cif['_diffrn_reflns_limit_h_min']
        limit_h_max = cif['_diffrn_reflns_limit_h_max']
        limit_k_min = cif['_diffrn_reflns_limit_k_min']
        limit_k_max = cif['_diffrn_reflns_limit_k_max']
        limit_l_min = cif['_diffrn_reflns_limit_l_min']
        limit_l_max = cif['_diffrn_reflns_limit_l_max']
        return (f'{minus_sign if limit_h_min != "0" else ""}{limit_h_min.replace("-", "")} '
                f'{less_or_equal} h {less_or_equal} {limit_h_max}<br>'
                f'{minus_sign if limit_k_min != "0" else ""}{limit_k_min.replace("-", "")} '
                f'{less_or_equal} k {less_or_equal} {limit_k_max}<br>'
                f'{minus_sign if limit_l_min != "0" else ""}{limit_l_min.replace("-", "")} '
                f'{less_or_equal} l {less_or_equal} {limit_l_max}')


class RichTextFormatter(Formatter):

    def __init__(self, options: Options, cif: CifContainer) -> None:
        super().__init__(options, cif)

    def get_bonds(self) -> list[dict[str, RichText]]:
        return self._bonds_angles.bonds_richtext

    def get_angles(self) -> list[dict[str, RichText]]:
        return self._bonds_angles.angles_richtext

    def get_torsion_angles(self) -> list[dict[str, RichText]]:
        return self._torsions.torsion_angles_as_richtext

    def get_hydrogen_bonds(self) -> list[dict[str, RichText]]:
        return self._hydrogens.hydrogen_bonds

    def get_bonds_angles_symminfo(self) -> RichText:
        return RichText(self._bonds_angles.symminfo.replace('\n', '\a'), style='table foot')

    def get_torsion_symminfo(self) -> RichText:
        return RichText(self._torsions.symminfo.replace('\n', '\a'), style='table foot')

    def get_hydrogen_symminfo(self) -> RichText:
        return RichText(self._hydrogens.symminfo.replace('\n', '\a'), style='table foot')

    def make_3d(self, cif: CifContainer, options: Options) -> str:
        return '[3D representation not implemented for .docx files]'

    def format_sum_formula(self, sum_formula: str) -> RichText:
        sum_formula_group = [''.join(x[1]) for x in itertools.groupby(sum_formula, lambda x: x.isalpha())]
        richtext = RichText('')
        if sum_formula_group:
            for _, word in enumerate(sum_formula_group):
                if isnumeric(word):
                    richtext.add(word, subscript=True)
                elif ')' in word:
                    richtext.add(word.split(')')[0], subscript=True)
                    richtext.add(')')
                elif ']' in word:
                    richtext.add(word.split(']')[0], subscript=True)
                    richtext.add(']')
                else:
                    richtext.add(word)
                    if word == ',':
                        richtext.add(' ')
            return richtext
        else:
            return RichText('no formula')

    def hydrogen_atoms_refinement(self, cif: CifContainer) -> RichText:
        return Hydrogens(cif).richtext()

    def atoms_refinement(self, cif: CifContainer) -> RichText:
        return Atoms(cif).richtext()

    def disorder_description(self, cif: CifContainer) -> RichText:
        self.literature['dsr'] = ref.DSRReference2018()
        return Disorder(cif).richtext()

    def space_group_formatted(self, cif: CifContainer, tpl_doc: DocxTemplate) -> Subdoc:
        """
        Generates a Subdoc subdocument with the xml code for a math element in MSWord.
        """
        s = SpaceGroups()
        try:
            spgrxml = s.to_mathml(cif.space_group)
        except KeyError:
            spgrxml = '<math xmlns="http://www.w3.org/1998/Math/MathML">?</math>'
        spgr_word = math_to_word(spgrxml)
        # I have to create a subdocument in order to add the xml:
        sd = tpl_doc.new_subdoc()
        p: Paragraph = sd.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        p._element.append(spgr_word)
        try:
            p.add_run(f' ({cif.spgr_number})')
        except AttributeError:
            pass
        return sd

    def get_radiation(self, cif: CifContainer) -> RichText:
        rad_element, radtype, radline = format_radiation(cif['_diffrn_radiation_type'])
        radiation = RichText(rad_element)
        radiation.add(radtype, italic=True)
        radiation.add(radline, italic=True, subscript=True)
        return radiation

    def make_picture(self, options: Options, picfile: Path, tpl_doc: DocxTemplate) -> InlineImage | None:
        if options.report_text and picfile and picfile.exists():
            return InlineImage(tpl_doc, str(picfile.resolve()), width=Cm(options.picture_width))
        return None

    def hkl_index_limits(self, cif: CifContainer) -> str:
        limit_h_min = cif['_diffrn_reflns_limit_h_min']
        limit_h_max = cif['_diffrn_reflns_limit_h_max']
        limit_k_min = cif['_diffrn_reflns_limit_k_min']
        limit_k_max = cif['_diffrn_reflns_limit_k_max']
        limit_l_min = cif['_diffrn_reflns_limit_l_min']
        limit_l_max = cif['_diffrn_reflns_limit_l_max']
        return (f'{minus_sign if limit_h_min != "0" else ""}{limit_h_min.replace("-", "")} '
                f'{less_or_equal} h {less_or_equal} {limit_h_max}\n'
                f'{minus_sign if limit_k_min != "0" else ""}{limit_k_min.replace("-", "")} '
                f'{less_or_equal} k {less_or_equal} {limit_k_max}\n'
                f'{minus_sign if limit_l_min != "0" else ""}{limit_l_min.replace("-", "")} '
                f'{less_or_equal} l {less_or_equal} {limit_l_max}')


def text_factory(options: Options, cif: CifContainer) -> dict[ReportFormat, Formatter]:
    factory = {
        ReportFormat.RICHTEXT: RichTextFormatter(options, cif),
        ReportFormat.HTML    : HtmlFormatter(options, cif),
        # 'plaintext': StringFormatter(),
    }
    return factory


class TemplatedReport:
    def __init__(self, format: ReportFormat, options: Options, cif: CifContainer) -> None:
        self.format = format
        self.cif = cif
        self.options = options
        self.text_formatter = text_factory(options, cif)[self.format]
        self.references = {}

    def count_reference(self, ref):
        if self.references:
            count = max(self.references.keys()) + 1
        else:
            count = 1
        self.references[count] = ref
        ref.count = count
        return count

    def reference_long(self, ref):
        return ref.richtext

    def reference_short(self, ref: Reference):
        return ref.short_ref

    def reference_text(self, ref: Reference):
        return ref.text

    def reference_html(self, ref: Reference):
        return ref.html

    def make_templated_docx_report(self,
                                   output_filename: str,
                                   picfile: Path | None,
                                   template_path: Path) -> bool:
        tpl_doc = DocxTemplate(template_path)
        context, tpl_doc = self.prepare_report_data(self.cif, self.options, picfile, tpl_doc)
        # Filter definition for {{foobar|filter}} things:
        jinja_env = jinja2.Environment()
        jinja_env.globals.update(zip=zip)
        jinja_env.globals.update(strip=str.strip)
        jinja_env.filters['utf8'] = report_text.utf8
        jinja_env.filters['inv_article'] = report_text.get_inf_article
        jinja_env.filters['to_pm'] = angstrom_to_pm if self.options.use_picometers else do_nothing
        jinja_env.filters['to_nm'] = angstrom_to_nanometers if self.options.use_picometers else do_nothing
        jinja_env.filters['float_num'] = report_text.format_float_with_decimal_places
        # foo[1,2] bar[3]:
        jinja_env.filters['ref_num'] = self.count_reference
        # foo(Kratzert, 2015):
        jinja_env.filters['ref_short'] = self.reference_short
        # richtext formatted full reference:
        jinja_env.filters['ref_long'] = self.reference_long
        # plain text full reference:
        jinja_env.filters['ref_txt'] = self.reference_text
        try:
            tpl_doc.render(context, jinja_env=jinja_env, autoescape=True)
            tpl_doc.save(output_filename)
            return True
        except PermissionError:
            # raise
            show_general_warning(parent=None, window_title='Warning',
                                 warn_text=f'The document {output_filename} could not be opened to write the report.\n'
                                           f'Is the file already opened?')
            return False
        except Exception as e:
            show_general_warning(parent=None, window_title='Warning', warn_text='Document generation failed',
                                 info_text=str(e))
            print(e)
            raise
            return False

    def make_templated_html_report(self,
                                   output_filename: str = 'test.html',
                                   picfile: Path | None = None,
                                   template_path: Path = Path('.'),
                                   template_file: str = "report.tmpl") -> bool:
        context = self.get_context(self.cif, self.options, picfile, None)
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=template_path.resolve()),
                                       autoescape=select_autoescape(['html', 'htm', 'xml']))
        # Add zip() method to global namespace of the template:
        jinja_env.globals.update(zip=zip)
        jinja_env.globals.update(strip=str.strip)
        jinja_env.filters['to_pm'] = angstrom_to_pm if self.options.use_picometers else do_nothing
        jinja_env.filters['to_nm'] = angstrom_to_nanometers if self.options.use_picometers else do_nothing
        jinja_env.filters['inv_article'] = report_text.get_inf_article
        jinja_env.filters['utf8'] = report_text.utf8
        jinja_env.filters['float_num'] = report_text.format_float_with_decimal_places
        jinja_env.filters['ref_num'] = self.count_reference
        # foo(Kratzert, 2015):
        jinja_env.filters['ref_short'] = self.reference_short
        # richtext formatted full reference:
        jinja_env.filters['ref_long'] = self.reference_long
        # plain text full reference:
        jinja_env.filters['ref_txt'] = self.reference_text
        # html reference:
        jinja_env.filters['ref_html'] = self.reference_html
        template = jinja_env.get_template(template_file)
        try:
            with open(output_filename, encoding='utf-8', mode='w+t') as f:
                outputText = template.render(context)
                f.write(outputText)
        except Exception as e:
            show_general_warning(parent=None, window_title='Warning', warn_text='Document generation failed',
                                 info_text=str(e))
            raise
            return False
        return True

    def prepare_report_data(self, cif: CifContainer,
                            options: Options,
                            picfile: Path | None,
                            tpl_doc: DocxTemplate | None) -> tuple[dict[str, Any], DocxTemplate]:
        maincontext = {}
        if not cif.is_multi_cif:
            maincontext = self.get_context(cif, options, picfile, tpl_doc)
        else:
            current_block = cif.block.name
            current_file = cif.fileobj
            maincontext.update(self.get_context(cif, options, picfile, tpl_doc))
            block_list = []
            blocks = {}
            for block in cif.doc:
                cif2 = CifContainer(file=current_file)
                cif2.load_block_by_name(block.name)
                context = self.get_context(cif2, options, picfile, tpl_doc)
                block_list.append(context)
                blocks[block.name] = context
            maincontext['blocklist'] = block_list
            maincontext['block'] = blocks
            cif.load_block_by_name(current_block)
        return maincontext, tpl_doc

    def get_context(self, cif: CifContainer, options: Options, picfile: Path, tpl_doc: DocxTemplate = None):
        context = {'options'                : options,
                   'cif'                    : cif,
                   'name'                   : cif.block.name,
                   'space_group'            : self.text_formatter.space_group_formatted(cif, tpl_doc),
                   'structure_figure'       : self.text_formatter.make_picture(options, picfile,
                                                                               tpl_doc) if options else '',
                   'crystal_video'          : self.text_formatter.make_picture(options, options.video_image,
                                                                               tpl_doc) if options else '',
                   '3d_structure'           : self.text_formatter.make_3d(cif, options) if options else '',
                   'crystallization_method' : self.text_formatter.get_crystallization_method(cif),
                   'sum_formula'            : self.text_formatter.format_sum_formula(
                       cif['_chemical_formula_sum'].replace(" ", "")),
                   'moiety_formula'         : self.text_formatter.format_sum_formula(
                       cif['_chemical_formula_moiety'].replace(" ", "")),
                   'itnum'                  : cif['_space_group_IT_number'],
                   'crystal_size'           : this_or_quest(cif['_exptl_crystal_size_min']) + timessym +
                                              this_or_quest(cif['_exptl_crystal_size_mid']) + timessym +
                                              this_or_quest(cif['_exptl_crystal_size_max']),
                   'crystal_colour'         : string_to_utf8(this_or_quest(cif['_exptl_crystal_colour'])),
                   'crystal_shape'          : string_to_utf8(cif['_exptl_crystal_description']),
                   'radiation'              : self.text_formatter.get_radiation(cif),
                   'wavelength'             : self.text_formatter.get_wavelength(cif),
                   'theta_range'            : self.text_formatter.get_from_to_theta_range(cif),
                   'diffr_type'             : gstr(cif['_diffrn_measurement_device_type'])
                                              or '[No _diffrn_measurement_device_type given]',
                   'diffr_device'           : string_to_utf8(gstr(cif['_diffrn_measurement_device'])
                                                             or '[No _diffrn_measurement_device given]'),
                   'diffr_source'           : gstr(cif['_diffrn_source']).strip('\n\r')
                                              or '[No _diffrn_source given]',
                   'monochromator'          : gstr(cif['_diffrn_radiation_monochromator']) \
                                              or '[No _diffrn_radiation_monochromator given]',
                   'detector'               : gstr(cif['_diffrn_detector_type']) \
                                              or '[No _diffrn_detector_type given]',
                   'lowtemp_dev'            : _get_cooling_device(cif),
                   'index_ranges'           : self.text_formatter.hkl_index_limits(cif),
                   'indepentent_refl'       : this_or_quest(cif['_reflns_number_total']),
                   'r_int'                  : this_or_quest(cif['_diffrn_reflns_av_R_equivalents']),
                   'r_sigma'                : this_or_quest(cif['_diffrn_reflns_av_unetI/netI']),
                   'completeness'           : self.text_formatter.get_completeness(cif),
                   'theta_full'             : cif['_diffrn_reflns_theta_full'],
                   'resolution_angstrom'    : self.text_formatter.get_angstrom_resolution(cif),
                   'redundancy'             : self.text_formatter.get_redundancy(cif),
                   'data'                   : this_or_quest(cif['_refine_ls_number_reflns']),
                   'restraints'             : this_or_quest(cif['_refine_ls_number_restraints']),
                   'parameters'             : this_or_quest(cif['_refine_ls_number_parameters']),
                   'goof'                   : this_or_quest(cif['_refine_ls_goodness_of_fit_ref']),
                   't_min'                  : self.text_formatter.t_minvalue(cif),
                   't_max'                  : self.text_formatter.t_maxvalue(cif),
                   'ls_R_factor_gt'         : this_or_quest(cif['_refine_ls_R_factor_gt']),
                   'ls_wR_factor_gt'        : this_or_quest(cif['_refine_ls_wR_factor_gt']),
                   'ls_R_factor_all'        : this_or_quest(cif['_refine_ls_R_factor_all']),
                   'ls_wR_factor_ref'       : this_or_quest(cif['_refine_ls_wR_factor_ref']),
                   'diff_dens_min'          : self.text_formatter.get_diff_density_min(cif).replace('-', minus_sign),
                   'diff_dens_max'          : self.text_formatter.get_diff_density_max(cif).replace('-', minus_sign),
                   'exti'                   : self.text_formatter.get_exti(cif),
                   'flack_x'                : self.text_formatter.get_flackx(cif),
                   'integration_progr'      : string_to_utf8(self.text_formatter.get_integration_program(cif)),
                   'abstype'                : gstr(cif['_exptl_absorpt_correction_type']) or 'Not applied',
                   'abs_details'            : self.text_formatter.get_absortion_correction_program(cif),
                   'solution_method'        : self.text_formatter.solution_method(cif),
                   'solution_program'       : self.text_formatter.solution_program(cif),
                   'refinement_details'     : self.text_formatter.refinement_details(cif),
                   'refinement_prog'        : self.text_formatter.refinement_prog(cif),
                   'refinement_gui'         : self.text_formatter.get_refinement_gui(cif),
                   'atomic_coordinates'     : self.text_formatter.get_atomic_coordinates(cif),
                   'displacement_parameters': self.text_formatter.get_displacement_parameters(cif),
                   'hydrogen_atoms'         : self.text_formatter.hydrogen_atoms_refinement(cif),
                   'atoms_refinement'       : self.text_formatter.atoms_refinement(cif),
                   'disorder_descr'         : self.text_formatter.disorder_description(cif),
                   'dist_unit'              : report_text.get_distance_unit(self.cif.picometer),
                   'vol_unit'               : report_text.get_volume_unit(self.cif.picometer),
                   'bonds'                  : self.text_formatter.get_bonds(),
                   'angles'                 : self.text_formatter.get_angles(),
                   'ba_symminfo'            : self.text_formatter.get_bonds_angles_symminfo(),
                   'torsions'               : self.text_formatter.get_torsion_angles(),
                   'torsion_symminfo'       : self.text_formatter.get_torsion_symminfo(),
                   'hydrogen_bonds'         : self.text_formatter.get_hydrogen_bonds(),
                   'hydrogen_symminfo'      : self.text_formatter.get_hydrogen_symminfo(),
                   'literature'             : self.text_formatter.literature,
                   'number_of_images'       : self.text_formatter.get_number_of_collected_images(cif),
                   'references'             : self.references,
                   'experiment_table'       : self.text_formatter.format_experiment_table(cif),
                   'experiment_time'        : self.text_formatter.get_experiment_time(cif),
                   'bootstrap_css'          : (app_path.application_path /
                                               'template/bootstrap/bootstrap.min.css').read_text(encoding='utf-8'),

                   }
        return context


def save_docx_to_pdf(docx_file: Path):
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(str(docx_file))
    try:
        doc.SaveAs(str(docx_file.with_suffix('.pdf')), FileFormat=17)
    except Exception:
        raise
    finally:
        pass
        # closes the Word document previously opened by subprocess:
        # doc.Close(0)
    # Quits all word applications!
    # word.Quit()


if __name__ == '__main__':

    import subprocess

    html = True

    data = Path('tests')
    testcif = Path(data / 'examples/1979688.cif').absolute()
    testcif = Path(r'test-data/p31c.cif').absolute()
    testcif = Path(r"D:\Downloads\9008564.cif").absolute()
    cif = CifContainer(testcif)

    pic = pathlib.Path("screenshots/finalcif_checkcif.png")

    options = Options()
    # Set options with leading underscore without settings parameter in Options:
    options._bonds_table = True
    # options._report_adp = True
    options._without_h = False
    # options._report_text = False
    options._hydrogen_bonds = True
    # options._picture_width = '300'

    work = Path('work').resolve()
    work.mkdir(exist_ok=True)
    template_path = app_path.application_path / 'template'

    if html:
        output = work / 'test.html'
        t = TemplatedReport(format=ReportFormat.HTML, options=options, cif=cif)
        ok = t.make_templated_html_report(output_filename=str(output), picfile=pic, template_path=template_path)
    else:
        output = work / 'test.docx'
        t = TemplatedReport(format=ReportFormat.RICHTEXT, options=options, cif=cif)
        ok = t.make_templated_docx_report(template_path=Path('finalcif/template/template_text.docx'),
                                          output_filename=str(output), picfile=pic)
    if ok:
        print('report successfully generated')
        if sys.platform == 'darwin':
            subprocess.call(['open', output])
        else:
            subprocess.Popen(['explorer', output], shell=True)
            # save_docx_to_pdf(output)
    else:
        print('HTML report failed')
