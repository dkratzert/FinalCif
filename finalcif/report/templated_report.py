import itertools
import re
from collections import namedtuple
from math import sin, radians
from pathlib import Path
from typing import List, Dict, Union

import jinja2
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate, RichText, InlineImage, Subdoc

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.text import retranslate_delimiter
from finalcif.report.references import SAINTReference, SHELXLReference, SadabsTwinabsReference, SHELXTReference, \
    SHELXSReference, SHELXDReference, SORTAVReference, FinalCifReference, CCDCReference, \
    CrysalisProReference, Nosphera2Reference, Olex2Reference
from finalcif.report.report_text import math_to_word, gstr, format_radiation, get_inf_article, MachineType
from finalcif.report.symm import SymmetryElement
from finalcif.tools.misc import isnumeric, this_or_quest, timessym, angstrom, protected_space, less_or_equal, \
    halbgeviert, \
    minus_sign, ellipsis_mid, remove_line_endings
from finalcif.tools.options import Options
from finalcif.tools.space_groups import SpaceGroups


class BondsAndAngles():
    def __init__(self, cif: CifContainer, without_h: bool):
        self.cif = cif
        self.without_h = without_h
        self._symmlist = {}
        # These can be used as strings for python-docx:
        self.bonds_as_string: List[Dict[str:str]] = []
        self.angles_as_string: List[Dict[str:str]] = []
        # These can be used as Richtext for python-docx-tpl:
        self.bonds: List[dict] = self._get_bonds_list(without_h)
        self.angles: List[dict] = self._get_angles_list(without_h)
        # The list of symmetry elements at the table end used for generated atoms:
        self.symminfo: str = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.bonds) + len(self.angles)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_bonds_list(self, without_h):
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
            symm = '#' + str(symms[symm2]) if symm2 else ''
            atoms = RichText(a)
            atoms.add(symm, superscript=True)
            bonds.append({'atoms': atoms, 'dist': dist})
            self.bonds_as_string.append({'atoms': a, 'symm': symm, 'dist': dist})
        self._symmlist.update(newsymms)
        return bonds

    def _get_angles_list(self, without_h):
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
            symm1_str = '#' + str(symms[symm1]) if symm1 else ''
            symm2_str = '#' + str(symms[symm2]) if symm2 else ''
            angle_val = ang.angle_val.replace('-', minus_sign)
            # atom1 symm1_str a symm2_str
            atoms = RichText(ang.label1)
            atoms.add(symm1_str, superscript=True)
            a = f'{halbgeviert}{ang.label2}{halbgeviert}{ang.label3}'
            atoms.add(a, superscript=False)
            atoms.add(symm2_str, superscript=True)
            angles_list.append({'atoms': atoms, 'angle': angle_val})
            self.angles_as_string.append({'atom1': ang.label1,
                                          'atom2': a,
                                          'symm1': symm1_str,
                                          'symm2': symm2_str,
                                          'angle': angle_val})
        self._symmlist.update(newsymms)
        return angles_list


class TorsionAngles():

    def __init__(self, cif: CifContainer, without_h: bool):
        self.cif = cif
        self.without_h = without_h
        self._symmlist = {}
        self.torsion_angles_as_string: List[Dict[str:str]] = []
        self.torsion_angles = self._get_torsion_angles_list(without_h)
        # The list of symmetry elements at the table end used for generated atoms:
        self.symminfo: str = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.torsion_angles)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_torsion_angles_list(self, without_h: bool):
        if not self.cif.nangles(without_h) > 0:
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
            symmstr1 = '#' + str(symms[symm1]) if symm1 else ''
            symmstr2 = '#' + str(symms[symm2]) if symm2 else ''
            symmstr3 = '#' + str(symms[symm3]) if symm3 else ''
            symmstr4 = '#' + str(symms[symm4]) if symm4 else ''
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
            self.torsion_angles_as_string.append({'atom1': tors.label1,
                                                  'atom2': tors.label2,
                                                  'atom3': tors.label3,
                                                  'atom4': tors.label4,
                                                  'symm1': symmstr1,
                                                  'symm2': symmstr2,
                                                  'symm3': symmstr3,
                                                  'symm4': symmstr4,
                                                  'angle': angle})
        self._symmlist = newsymms
        return torsion_angles


class HydrogenBonds():
    def __init__(self, cif: CifContainer):
        self.cif = cif
        self._symmlist = {}
        self.hydrogen_bonds_as_str: List[Dict[str:str]] = []
        self.hydrogen_bonds = self._get_hydrogen_bonds()
        self.symminfo = get_symminfo(self._symmlist)

    def __len__(self):
        return len(self.hydrogen_bonds)

    @property
    def symmetry_generated_atoms_used(self):
        return len(self._symmlist) > 0

    def _get_hydrogen_bonds(self) -> List[dict]:
        symms = {}
        newsymms = {}
        num = 1
        atoms_list = []
        for h in self.cif.hydrogen_bonds():
            symm = h.symm
            if symm in ('.', '?'):
                symm = None
            num = symmsearch(self.cif, newsymms, num, symm, symms)
            symmval = ('#' + str(symms[symm])) if symm else ''
            a = h.label_d + halbgeviert + h.label_h + ellipsis_mid + h.label_a
            atoms = RichText(a)
            atoms.add(symmval, superscript=True)
            atoms_list.append({'atoms'  : atoms, 'dist_dh': h.dist_dh, 'dist_ha': h.dist_ha,
                               'dist_da': h.dist_da, 'angle_dha': h.angle_dha})
            self.hydrogen_bonds_as_str.append({'atoms'  : a, 'dist_dh': h.dist_dh, 'dist_ha': h.dist_ha,
                                               'dist_da': h.dist_da, 'angle_dha': h.angle_dha, 'symm': symmval})
        self._symmlist = newsymms
        return atoms_list


def get_card(cif: CifContainer, symm: str) -> Union[List[str], None]:
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


def get_symminfo(newsymms: dict) -> str:
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


def symmsearch(cif: CifContainer, newsymms, num, symm, symms_list) -> int:
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


class TemplatedReport():

    def __init__(self):
        self.literature = {'finalcif'   : FinalCifReference(),
                           'ccdc'       : CCDCReference(),
                           'absorption' : '[no reference found]',
                           'solution'   : '[no reference found]',
                           'refinement' : '[no reference found]',
                           'integration': '[no reference found]',
                           }

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

    @staticmethod
    def space_group_subdoc(tpl_doc: DocxTemplate, cif: CifContainer) -> Subdoc:
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

    @staticmethod
    def get_from_to_theta_range(cif: CifContainer) -> str:
        theta_min = cif['_diffrn_reflns_theta_min']
        theta_max = cif['_diffrn_reflns_theta_max']
        radiation_wavelength = cif['_diffrn_radiation_wavelength']
        try:
            d_max = f' ({float(radiation_wavelength) / (2 * sin(radians(float(theta_max)))):.2f}' \
                    f'{protected_space}{angstrom})'
            # 2theta range:
            return f"{2 * float(theta_min):.2f} to {2 * float(theta_max):.2f}{d_max}"
        except ValueError:
            return '? to ?'

    @staticmethod
    def hkl_index_limits(cif: CifContainer) -> str:
        limit_h_min = cif['_diffrn_reflns_limit_h_min']
        limit_h_max = cif['_diffrn_reflns_limit_h_max']
        limit_k_min = cif['_diffrn_reflns_limit_k_min']
        limit_k_max = cif['_diffrn_reflns_limit_k_max']
        limit_l_min = cif['_diffrn_reflns_limit_l_min']
        limit_l_max = cif['_diffrn_reflns_limit_l_max']
        return f'{minus_sign if limit_h_min != "0" else ""}{limit_h_min.replace("-", "")} ' \
               f'{less_or_equal} h {less_or_equal} {limit_h_max}\n' \
            + f'{minus_sign if limit_k_min != "0" else ""}{limit_k_min.replace("-", "")} ' \
              f'{less_or_equal} k {less_or_equal} {limit_k_max}\n' \
            + f'{minus_sign if limit_l_min != "0" else ""}{limit_l_min.replace("-", "")} ' \
              f'{less_or_equal} l {less_or_equal} {limit_l_max}'

    @staticmethod
    def get_radiation(cif: CifContainer) -> RichText:
        rad_element, radtype, radline = format_radiation(cif['_diffrn_radiation_type'])
        radiation = RichText(rad_element)
        radiation.add(radtype, italic=True)
        radiation.add(radline, italic=True, subscript=True)
        return radiation

    @staticmethod
    def get_completeness(cif: CifContainer) -> str:
        try:
            completeness = f"{float(cif['_diffrn_measured_fraction_theta_full']) * 100:.1f}{protected_space}%"
        except ValueError:
            completeness = '?'
        return completeness

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
        integration = gstr(cif['_computing_data_reduction']) or '??'
        integration_prog = '[unknown integration program]'
        if 'SAINT' in integration:
            saintversion = ''
            integration_prog = 'SAINT'
            if len(integration.split()) > 1:
                saintversion = integration.split()[1]
                integration_prog += " " + saintversion
            self.literature['integration'] = SAINTReference('SAINT', saintversion)
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
            self.literature['integration'] = CrysalisProReference(version=version, year=year)
            self.literature['absorption'] = CrysalisProReference(version=version, year=year)
        return integration_prog

    def get_absortion_correction_program(self, cif: CifContainer) -> str:
        absdetails = cif['_exptl_absorpt_process_details'].replace('-', ' ').replace(':', '')
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
            self.literature['absorption'] = SadabsTwinabsReference()
        if 'SORTAV' in absdetails.upper():
            scale_prog = 'SORTAV'
            self.literature['absorption'] = SORTAVReference()
        if 'crysalis' in absdetails.lower():
            scale_prog = 'SCALE3 ABSPACK'
            # see above also
        scale_prog += " " + version

        return scale_prog

    def solution_method(self, cif: CifContainer) -> str:
        solution_method = gstr(cif['_atom_sites_solution_primary']) or '??'
        return solution_method.strip('\n\r')

    def solution_program(self, cif: CifContainer) -> str:
        solution_prog = gstr(cif['_computing_structure_solution']) or '??'
        if solution_prog.upper().startswith(('SHELXT', 'XT')):
            self.literature['solution'] = SHELXTReference()
        if 'SHELXS' in solution_prog.upper():
            self.literature['solution'] = SHELXSReference()
        if 'SHELXD' in solution_prog.upper():
            self.literature['solution'] = SHELXDReference()
        return solution_prog.split()[0]

    def refinement_prog(self, cif: CifContainer) -> str:
        refined = gstr(cif['_computing_structure_refinement']) or '??'
        if 'SHELXL' in refined.upper() or 'XL' in refined.upper():
            self.literature['refinement'] = SHELXLReference()
        if 'OLEX' in refined.upper():
            self.literature['refinement'] = Olex2Reference()
        if ('NOSPHERA2' in refined.upper() or 'NOSPHERA2' in cif['_refine_special_details'].upper() or
            'NOSPHERAT2' in cif['_olex2_refine_details'].upper()):
            self.literature['refinement'] = Nosphera2Reference()
        return refined.split()[0]

    def get_atomic_coordinates(self, cif: CifContainer):
        for at in cif.atoms(without_h=False):
            yield {'label': at.label,
                   'type' : at.type,
                   'x'    : at.x.replace('-', minus_sign),
                   'y'    : at.y.replace('-', minus_sign),
                   'z'    : at.z.replace('-', minus_sign),
                   'part' : at.part.replace('-', minus_sign),
                   'occ'  : at.occ.replace('-', minus_sign),
                   'u_eq' : at.u_eq.replace('-', minus_sign)}

    def get_displacement_parameters(self, cif: CifContainer):
        """
        Yields the anisotropic displacement parameters. With hypehens replaced to minus signs.
        """
        adp = namedtuple('adp', ('label', 'U11', 'U22', 'U33', 'U23', 'U13', 'U12'))
        for label, u11, u22, u33, u23, u13, u12 in cif.displacement_parameters():
            yield adp(label=label,
                      U11=u11.replace('-', minus_sign),
                      U22=u22.replace('-', minus_sign),
                      U33=u33.replace('-', minus_sign),
                      U12=u12.replace('-', minus_sign),
                      U13=u13.replace('-', minus_sign),
                      U23=u23.replace('-', minus_sign))

    def get_crystallization_method(self, cif):
        return gstr(cif['_exptl_crystal_recrystallization_method']) or '[No crystallization method given!]'

    def make_picture(self, options: Options, picfile: Path, tpl_doc: DocxTemplate):
        if options.report_text and picfile and picfile.exists():
            return InlineImage(tpl_doc, str(picfile.resolve()), width=Cm(options.picture_width))
        return None

    def make_templated_report(self, options: Options, cif: CifContainer, output_filename: str, picfile: Path,
                              template_path: Path):
        context, tpl_doc = self.prepare_report_data(cif, options, picfile, template_path)
        # Filter definition for {{foobar|filter}} things:
        jinja_env = jinja2.Environment()
        jinja_env.filters['inv_article'] = get_inf_article
        tpl_doc.render(context, jinja_env=jinja_env, autoescape=True)
        tpl_doc.save(output_filename)

    def prepare_report_data(self, cif: CifContainer, options: Options, picfile: Path, template_path: Path):
        tpl_doc = DocxTemplate(template_path)
        ba = BondsAndAngles(cif, without_h=options.without_h)
        t = TorsionAngles(cif, without_h=options.without_h)
        h = HydrogenBonds(cif)
        context = {'options'                : options,
                   # {'without_h': True, 'atoms_table': True, 'text': True, 'bonds_table': True},
                   'cif'                    : cif,
                   'space_group'            : self.space_group_subdoc(tpl_doc, cif),
                   'structure_figure'       : self.make_picture(options, picfile, tpl_doc),
                   'crystallization_method' : self.get_crystallization_method(cif),
                   'sum_formula'            : self.format_sum_formula(cif['_chemical_formula_sum'].replace(" ", "")),
                   'moiety_formula'         : self.format_sum_formula(cif['_chemical_formula_moiety'].replace(" ", "")),
                   'itnum'                  : cif['_space_group_IT_number'],
                   'crystal_size'           : this_or_quest(cif['_exptl_crystal_size_min']) + timessym +
                                              this_or_quest(cif['_exptl_crystal_size_mid']) + timessym +
                                              this_or_quest(cif['_exptl_crystal_size_max']),
                   'crystal_colour'         : this_or_quest(cif['_exptl_crystal_colour']),
                   'crystal_shape'          : this_or_quest(cif['_exptl_crystal_description']),
                   'radiation'              : self.get_radiation(cif),
                   'wavelength'             : cif['_diffrn_radiation_wavelength'],
                   'theta_range'            : self.get_from_to_theta_range(cif),
                   'diffr_type'             : gstr(cif['_diffrn_measurement_device_type'])
                                              or '[No measurement device type given]',
                   'diffr_device'           : gstr(cif['_diffrn_measurement_device'])
                                              or '[No measurement device given]',
                   'diffr_source'           : gstr(cif['_diffrn_source']).strip('\n\r')
                                              or '[No radiation source given]',
                   'monochromator'          : gstr(cif['_diffrn_radiation_monochromator']) \
                                              or '[No monochromator type given]',
                   'detector'               : gstr(cif['_diffrn_detector_type']) \
                                              or '[No detector type given]',
                   'lowtemp_dev'            : MachineType._get_cooling_device(cif),
                   'index_ranges'           : self.hkl_index_limits(cif),
                   'indepentent_refl'       : this_or_quest(cif['_reflns_number_total']),
                   'r_int'                  : this_or_quest(cif['_diffrn_reflns_av_R_equivalents']),
                   'r_sigma'                : this_or_quest(cif['_diffrn_reflns_av_unetI/netI']),
                   'completeness'           : self.get_completeness(cif),
                   'theta_full'             : cif['_diffrn_reflns_theta_full'],
                   'data'                   : this_or_quest(cif['_refine_ls_number_reflns']),
                   'restraints'             : this_or_quest(cif['_refine_ls_number_restraints']),
                   'parameters'             : this_or_quest(cif['_refine_ls_number_parameters']),
                   'goof'                   : this_or_quest(cif['_refine_ls_goodness_of_fit_ref']),
                   'ls_R_factor_gt'         : this_or_quest(cif['_refine_ls_R_factor_gt']),
                   'ls_wR_factor_gt'        : this_or_quest(cif['_refine_ls_wR_factor_gt']),
                   'ls_R_factor_all'        : this_or_quest(cif['_refine_ls_R_factor_all']),
                   'ls_wR_factor_ref'       : this_or_quest(cif['_refine_ls_wR_factor_ref']),
                   'diff_dens_min'          : self.get_diff_density_min(cif).replace('-', minus_sign),
                   'diff_dens_max'          : self.get_diff_density_max(cif).replace('-', minus_sign),
                   'exti'                   : self.get_exti(cif),
                   'flack_x'                : self.get_flackx(cif),
                   'integration_progr'      : self.get_integration_program(cif),
                   'abstype'                : gstr(cif['_exptl_absorpt_correction_type']) or '??',
                   'abs_details'            : self.get_absortion_correction_program(cif),
                   'solution_method'        : self.solution_method(cif),
                   'solution_program'       : self.solution_program(cif),
                   'refinement_details'     : ' '.join(
                       cif['_refine_special_details'].splitlines(keepends=False)).strip(),
                   'refinement_prog'        : self.refinement_prog(cif),
                   'atomic_coordinates'     : self.get_atomic_coordinates(cif),
                   'displacement_parameters': self.get_displacement_parameters(cif),
                   'bonds'                  : ba.bonds,
                   'angles'                 : ba.angles,
                   'ba_symminfo'            : ba.symminfo,
                   'torsions'               : t.torsion_angles,
                   'torsion_symminfo'       : t.symminfo,
                   'hydrogen_bonds'         : h.hydrogen_bonds,
                   'hydrogen_symminfo'      : h.symminfo,
                   'literature'             : self.literature
                   }
        return context, tpl_doc


if __name__ == '__main__':
    pass
