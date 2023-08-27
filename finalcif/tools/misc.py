#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#
import hashlib
import itertools as it
import os
import re
import subprocess
import sys
from datetime import datetime
from math import sqrt
from os import path
from pathlib import Path
from typing import Union, Tuple, List

# protected space character:
protected_space = u'\u00A0'
medium_math_space = u'\u205F'
# Angstrom character:
# angstrom = u'\u212B'  # Unicode angstrom sign (only for compatibility)
# angstrom = 'Å'      # MSWord seems unable to render the regular letter correctly. It looks like a different font?
angstrom = u'\u00C5'  # Latin capital A with ring above. The Unicode consortium recommends to use the regular letter
# Greek Small Letter Theta θ:
theta_symbol = u'\u03B8'
# Greek Small Letter Pi
pi_symbol = u'\u03C0'
# bigger or equal:
bequal = u'\u2265'
# small_sigma:
sigma_sm = u'\u03C3'
# en dash:
halbgeviert = u'\u2013'
# minus sign:
minus_sign = u'\u2212'
# degree sign:
degree_sign = u'\u00B0'
# middle ellipsis
ellipsis_mid = u'\u22EF'
# ellipsis
ellipsis_char = u'\u2026'
# middle dot
middle_dot = u'\u00B7'
# less or equal sign
less_or_equal = u'\u2264'
# times (cross) symbol
timessym = u'\u00d7'
# lambda
lambdasym = u'\u03bb'
# one bar
one_bar = u'\u0031\u0305'
# Zero-with space ZWSP
zero_width_space = u'\u200B'


def isnumeric(value: str) -> bool:
    """
    Determines if a string can be converted to a number.
    """
    value = value.split('(')[0]
    try:
        float(value)
    except ValueError:
        return False
    return True


def sha512_checksum_of_file(filename: str, block_size=65536):
    """
    Calculates a SHA512 checksum from a file.
    """
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha512.update(block)
    return sha512.hexdigest()


def distance(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    """
    distance between two points in space for orthogonal axes.
    """
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return it.zip_longest(*iters, fillvalue=fillvalue)


def get_error_from_value(value: str) -> Tuple[float, float]:
    """
    Returns the error value from a number string.
    """
    try:
        value = value.replace(" ", "")
    except AttributeError:
        return float(value), 0.0
    if "(" in value:
        vval, err = value.split("(")
        val = vval.split('.')
        err = err.split(")")[0]
        if not err:
            return float(vval), 0.0
        if len(val) > 1:
            return float(vval), int(err) * (10 ** (-1 * len(val[1])))
        else:
            return float(vval), float(err)
    else:
        try:
            return float(value), 0.0
        except ValueError:
            return 0.0, 0.0


def next_path(path_pattern: str) -> str:
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    https://stackoverflow.com/questions/17984809/how-do-i-create-a-incrementing-filename-in-python/47087513
    """
    i = 1
    # First do an exponential search
    while path.exists(path_pattern % i):
        i = i * 2
    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2  # interval midpoint
        a, b = (c, b) if path.exists(path_pattern % c) else (a, c)
    return path_pattern % b


def file_modification_time(file_path: Path) -> float:
    """
    """
    from os import path
    return path.getmtime(file_path.resolve())


def file_age_in_days(file_path: Path) -> int:
    today = datetime.today()
    try:
        file_mod_time = datetime.fromtimestamp(file_modification_time(file_path))
    except Exception:
        # In case 'file_path' was not found:
        file_mod_time = datetime(2001, 1, 1)
    diff = (today.replace(second=2) - file_mod_time.replace(second=0)).days
    return diff


class Multilog(object):
    """
    This class copies all output from stdout and stderr to a file
    It acts like tee with following usage:
    sys.stdout = multifile([sys.stdout, lstfileobj])
    """

    def __init__(self, files):
        self._files = files

    def __getattr__(self, attr, *args):
        return self._wrap(attr, *args)

    def _wrap(self, attr, *args):
        def g(*a, **kw):
            res = ''
            for f in self._files:
                res = getattr(f, attr, *args)(*a, **kw)
            return res

        return g


def strip_finalcif_of_name(pth: Union[str, Path], till_name_ends=False) -> str:
    """
    Strips '-finalcif' from the stem path
    """
    pth = str(pth)
    return re.sub(f'-finalcif{".*" if till_name_ends else ""}$', '', pth)


def flatten(lis: list) -> list:
    """
    Given a list, possibly nested to any level, return it flattened.
    From: http://code.activestate.com/recipes/578948-flattening-an-arbitrarily-nested-list-in-python/
    """
    new_lis = []
    for item in lis:
        if isinstance(item, list):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis


def find_line(inputlist: list, regex: str) -> int:
    for num, string in enumerate(inputlist):
        if re.match(regex, string, re.IGNORECASE):
            return num  # returns the index number if regex found
    return 0


def this_or_quest(value: Union[str, int, float, None]) -> Union[str, int, float]:
    """
    Returns the value or a question mark if the value is None.
    """
    if value == '' or value is None:
        return '?'
    else:
        return value


def to_float(st) -> Union[float, List[float], None]:
    if isinstance(st, list):
        try:
            return [float(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return float(st.split('(')[0])
        except ValueError:
            return None


def to_int(st: Union[str, List[Union[str, int]]]) -> Union[int, List[int], None]:
    if isinstance(st, list):
        try:
            return [int(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return int(float(st.split('(')[0]))
        except ValueError:
            return None


def make_numbered(items):
    items.insert(0, '')
    return [(x, y) for x, y in enumerate(items)]


# '_space_group_centring_type',  # seems to be used nowere
# '_exptl_absorpt_special_details',   # This is not official?!?
essential_keys = (
    # '_atom_sites_solution_secondary'
    # '_diffrn_measurement_specimen_adhesive'
    # '_diffrn_source_power'
    # '_diffrn_source_target'
    # '_olex2_diffrn_ambient_temperature_device'
    '_diffrn_measurement_ambient_temperature_device_make',
    '_atom_sites_solution_hydrogens',
    '_atom_sites_solution_primary',
    # '_audit_contact_author_name',
    # '_audit_contact_author_address',
    # '_audit_contact_author_email',
    # '_audit_contact_author_phone',
    '_audit_creation_method',
    '_publ_section_references',
    '_cell_angle_alpha',
    '_cell_angle_beta',
    '_cell_angle_gamma',
    '_cell_formula_units_Z',
    '_cell_length_a',
    '_cell_length_b',
    '_cell_length_c',
    '_cell_measurement_reflns_used',
    '_cell_measurement_temperature',
    '_cell_measurement_theta_max',
    '_cell_measurement_theta_min',
    '_cell_volume',
    '_chemical_absolute_configuration',
    '_chemical_formula_moiety',
    '_chemical_formula_sum',
    '_chemical_formula_weight',
    '_chemical_melting_point',
    '_chemical_name_common',
    '_chemical_name_systematic',
    '_computing_cell_refinement',
    '_computing_data_collection',
    '_computing_data_reduction',
    '_computing_molecular_graphics',
    '_computing_publication_material',
    '_computing_structure_refinement',
    '_computing_structure_solution',
    '_diffrn_ambient_environment',
    '_diffrn_ambient_temperature',
    '_diffrn_detector',
    '_diffrn_detector_area_resol_mean',
    '_diffrn_detector_type',
    '_diffrn_measured_fraction_theta_full',
    '_diffrn_measured_fraction_theta_max',
    '_diffrn_measurement_device',
    '_diffrn_measurement_device_type',
    '_diffrn_measurement_method',
    '_diffrn_measurement_specimen_support',
    '_diffrn_radiation_monochromator',
    '_diffrn_radiation_probe',
    '_diffrn_radiation_type',
    '_diffrn_radiation_wavelength',
    '_diffrn_reflns_Laue_measured_fraction_full',
    '_diffrn_reflns_Laue_measured_fraction_max',
    '_diffrn_reflns_av_R_equivalents',
    '_diffrn_reflns_av_unetI/netI',
    '_diffrn_reflns_number',
    '_diffrn_reflns_point_group_measured_fraction_full',
    '_diffrn_reflns_point_group_measured_fraction_max',
    '_diffrn_reflns_theta_full',
    '_diffrn_reflns_theta_max',
    '_diffrn_reflns_theta_min',
    '_diffrn_source',
    '_diffrn_source_current',
    '_diffrn_source_type',
    '_diffrn_source_voltage',
    '_exptl_absorpt_coefficient_mu',
    '_exptl_absorpt_correction_T_max',
    '_exptl_absorpt_correction_T_min',
    '_exptl_absorpt_correction_type',
    '_exptl_absorpt_process_details',
    '_exptl_crystal_F_000',
    '_exptl_crystal_colour',
    '_exptl_crystal_density_diffrn',
    '_exptl_crystal_density_meas',
    '_exptl_crystal_density_method',
    '_exptl_crystal_description',
    '_exptl_crystal_recrystallization_method',
    '_exptl_crystal_size_max',
    '_exptl_crystal_size_mid',
    '_exptl_crystal_size_min',
    '_exptl_special_details',
    '_geom_special_details',
    '_refine_ls_R_factor_all',
    '_refine_ls_R_factor_gt',
    '_refine_ls_abs_structure_Flack',
    '_refine_ls_abs_structure_details',
    '_refine_ls_extinction_coef',
    '_refine_ls_extinction_method',
    '_refine_ls_goodness_of_fit_ref',
    '_refine_ls_hydrogen_treatment',
    '_refine_ls_matrix_type',
    '_refine_ls_number_parameters',
    '_refine_ls_number_reflns',
    '_refine_ls_number_restraints',
    '_refine_ls_restrained_S_all',
    '_refine_ls_shift/su_max',
    '_refine_ls_shift/su_mean',
    '_refine_ls_structure_factor_coef',
    '_refine_ls_wR_factor_gt',
    '_refine_ls_wR_factor_ref',
    '_refine_ls_weighting_details',
    '_refine_ls_weighting_scheme',
    '_refine_special_details',
    '_reflns_Friedel_coverage',
    '_reflns_Friedel_fraction_full',
    '_reflns_Friedel_fraction_max',
    '_reflns_number_gt',
    '_reflns_number_total',
    '_reflns_special_details',
    '_reflns_threshold_expression',
    '_space_group_IT_number',
    '_space_group_crystal_system',
    '_space_group_name_H-M_alt',
    '_space_group_name_Hall',
    # '_space_group_symop_operation_xyz'     
)

non_centrosymm_keys = ('_chemical_absolute_configuration', '_refine_ls_abs_structure_Flack',
                       '_refine_ls_abs_structure_details')

# Keys that get a text field in the main list. These fields have more hight.
text_field_keys = ('_refine_special_details',
                   '_refine_ls_weighting_details',
                   '_reflns_special_details',
                   '_exptl_absorpt_process_details',
                   '_publ_section_references',
                   '_audit_contact_author_address',
                   '_exptl_crystal_recrystallization_method',
                   '_exptl_special_details',
                   '_geom_special_details',
                   '_diffrn_measurement_details',
                   '_diffrn_oxdiff_ac3_digest_frames',
                   '_diffrn_oxdiff_ac3_digest_hkl',
                   '_oxdiff_exptl_absorpt_empirical_details',
                   )

do_not_import_keys = (
    '_cell_length_a',
    '_cell_length_b',
    '_cell_length_c',
    '_cell_angle_alpha',
    '_cell_angle_beta',
    '_cell_angle_gamma',
    '_space_group_IT_number',
    '_space_group_crystal_system',
    '_space_group_name_H-M_alt',
    '_shelx_res_file',
    '_shelx_hkl_file',
    '_shelx_res_checksum',
    '_shelx_hkl_checksum',
    '_shelx_fab_file',
    '_shelx_fab_checksum',
    '_shelx_fcf_file',
    '_shelx_fcf_checksum',
    '_exptl_absorpt_coefficient_mu',
    '_exptl_crystal_F_000',
    '_exptl_crystal_density_diffrn',
    '_reflns_number_total',
    '_reflns_number_gt',
)

do_not_import_from_stoe_cfx = (
    '_diffrn_measured_fraction_theta_max',
    '_diffrn_measured_fraction_theta_full',
    '_diffrn_reflns_av_R_equivalents',
    '_diffrn_reflns_av_unetI/netI',
    '_diffrn_reflns_limit_h_min',
    '_diffrn_reflns_limit_h_max',
    '_diffrn_reflns_limit_k_min',
    '_diffrn_reflns_limit_k_max',
    '_diffrn_reflns_limit_l_min',
    '_diffrn_reflns_limit_l_max',
    '_diffrn_reflns_number',
    '_diffrn_reflns_theta_min',
    '_diffrn_reflns_theta_max',
    '_diffrn_reflns_theta_full',
    '_reflns_special_details',
    '_audit_author_name',
    '_audit_contact_author',
    '_audit_contact_author_address',
    '_audit_contact_author_email',
    '_audit_contact_author_fax',
    '_audit_contact_author_phone',
    '_audit_creation_method',
    '',
    '',
    '',
)

include_equipment_imports = (
    '_diffrn_detector',
    '_diffrn_detector_area_resol_mean',
    '_diffrn_detector_type',
    '_diffrn_measurement_device',
    '_diffrn_radiation_monochromator',
    '_diffrn_radiation_probe',
    '_diffrn_radiation_type',
    '_diffrn_source',
    '_diffrn_source_type',
    '_exptl_absorpt_process_details',
    '_exptl_absorpt_process_details',
)

cif_to_header_label = {
    # translates CIF keys into regular headers for loops
    '_atom_site_aniso_label'                : 'Displacement Parameters',
    '_atom_site_label'                      : 'Atomic Coordinates',
    '_atom_type_symbol'                     : 'Scattering Factors',
    '_citation_doi'                         : 'Citations',
    '_citation_id'                          : 'Citations',
    '_citation_year'                        : 'Citations',
    '_geom_angle_atom_site_label_1'         : 'Angles',
    '_geom_bond_atom_site_label_1'          : 'Bonds',
    '_geom_torsion_atom_site_label_1'       : 'Torsion Angles',
    '_shelx_res_file'                       : 'SHELX res File',
    '_space_group_symop_id'                 : 'Symmetry',
    '_space_group_symop_operation_xyz'      : 'Symmetry',
    '_symmetry_equiv_pos_site_id'           : 'Symmetry',
    '_symmetry_equiv_pos_as_xyz'            : 'Symmetry',
    '_audit_author_name'                    : 'CIF Author',
    '_audit_contact_author_name'            : 'CIF Contact Authors',
    '_publ_author_name'                     : 'Publication Authors',
    '_publ_contact_author_name'             : 'Publication Contact Authors',
    '_geom_hbond_atom_site_label_D'         : 'Hydrogen Bonds',
    '_geom_hbond_atom_site_label_H'         : 'Hydrogen Bonds',
    '_geom_hbond_atom_site_label_A'         : 'Hydrogen Bonds',
    '_exptl_crystal_face_index_h'           : 'Crystal Faces',
    '_exptl_oxdiff_crystal_face_indexfrac_h': 'Crystal Faces Fractional',
    '_platon_squeeze_void_nr'               : 'Platon SQUEEZE Voids',
    '_smtbx_masks_void_nr'                  : 'smtbx Solvent Mask',
}

"""
_publ_section_references
;
D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51.

Dolomanov, O.V., Bourhis, L.J., Gildea, R.J, Howard, J.A.K. & Puschmann, H.
 (2009), J. Appl. Cryst. 42, 339-341.

Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.

Sheldrick, G.M. (2015). Acta Cryst. C71, 3-8.
;
"""
# Equipment templates

predefined_equipment_templates = [
    {'name' : 'D8 VENTURE',
     'items': [
         ['_diffrn_radiation_monochromator', 'mirror optics'],
         ['_diffrn_measurement_device', 'three-circle diffractometer'],
         ['_diffrn_measurement_device_type', 'Bruker D8 VENTURE dual wavelength Mo/Cu'],
         ['_diffrn_measurement_method', r'\w and \f scans'],
         ['_diffrn_source', 'microfocus sealed X-ray tube'],
         # ['_diffrn_source_current', '50'],
         # ['_diffrn_source_voltage', '1.1'],
         ['_diffrn_detector_area_resol_mean', '7.41'],
         ['_diffrn_detector', 'CPAD'],
         ['_diffrn_detector_type', 'Bruker PHOTON III'],
         ['_diffrn_source_type', r'Incoatec I\ms'],
         ['_diffrn_radiation_probe', 'x-ray'],
         ['_diffrn_measurement_specimen_support', 'MiTeGen micromount'],
         ['_diffrn_measurement_ambient_temperature_device_make', 'Oxford Cryostream 800'],
         ['_diffrn_ambient_environment', 'N~2~'],
     ]
     },
    {'name' : 'APEX2 QUAZAR',
     'items': [
         ['_diffrn_radiation_monochromator', 'mirror optics'],
         ['_diffrn_measurement_device', 'three-circle diffractometer'],
         ['_diffrn_measurement_device_type', 'Bruker APEX2 QUAZAR'],
         ['_diffrn_measurement_method', r'\w and \f scans'],
         ['_diffrn_source', 'microfocus sealed X-ray tube'],
         ['_diffrn_source_type', r'Incoatec I\ms'],
         ['_diffrn_detector', 'CCD'],
         ['_diffrn_detector_type', 'Bruker APEXII'],
         ['_diffrn_detector_area_resol_mean', '8.3'],
         ['_diffrn_radiation_probe', 'x-ray'],
         ['_diffrn_measurement_specimen_support', 'MiTeGen micromount'],
         ['_diffrn_measurement_ambient_temperature_device_make', 'Oxford Cryostream 800'],
         ['_diffrn_ambient_environment', 'N~2~'],
     ]
     },
    {'name' : 'Rigaku Spider',
     'items': [
         ['_diffrn_radiation_monochromator', 'graphite'],
         ['_diffrn_measurement_device', 'four-circle diffractometer'],
         ['_diffrn_measurement_device_type', 'Rigaku R-AXIS SPIDER'],
         ['_diffrn_measurement_method', r'\w scans'],
         ['_diffrn_source', 'sealed X-ray tube'],  # obsolete: _diffrn_radiation_source
         ['_diffrn_detector', 'Image Plate'],
         ['_diffrn_detector_type', 'Rigaku Image Plate'],
         ['_diffrn_detector_area_resol_mean', '?'],
         ['_diffrn_radiation_probe', 'x-ray'],
         ['_diffrn_measurement_specimen_support', 'MiTeGen micromount'],
         ['_diffrn_measurement_ambient_temperature_device_make', 'Bruker Kryoflex II'],
     ]
     },
    {'name' : 'Crystallographer Details',
     'items': [
         ['_audit_contact_author_name', '?'],
         ['_audit_contact_author_address', "?"],
         ['_audit_contact_author_email', '?'],
         ['_audit_contact_author_phone', '?'],
     ]
     },
]

### Property contents:

predefined_property_templates = [
    {'name'  : 'Absolute Configuration',
     'values': ['_chemical_absolute_configuration',
                ['', 'ad', 'rm', 'rmad', 'syn', 'unk', '.']]
     },
    {'name'  : 'Crystal Color',
     'values': ['_exptl_crystal_colour',
                ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue',
                 'green', 'gray', 'pink', 'orange', 'violet', 'brown']]
     },
    {'name'  : 'Crystal Color Primary',
     'values': ['_exptl_crystal_colour_primary',
                ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue',
                 'green', 'gray', 'pink', 'orange', 'violet', 'brown']]
     },
    {'name'  : 'Crystal Habit Description',
     'values': ['_exptl_crystal_description',
                ['', 'block', 'needle', 'plate', 'prism', 'sphere']]
     },
    {'name'  : 'Cell Measurement Temperature',
     'values': ['_cell_measurement_temperature',
                ['', '15', '80(2)', '100(2)', '110(2)',
                 '120(2)', '130(2)', '150(2)', '200(2)', '298(2)']]
     },
    {'name'  : 'Measurement Temperature',
     'values': ['_diffrn_ambient_temperature',
                ['', '15(1)', '80(2)', '100(2)', '110(2)',
                 '120(2)', '130(2)', '150(2)', '200(2)', '293.15(2)', '298(2)']]
     },
    {'name'  : 'Molecular Graphics',
     'values': ['_computing_molecular_graphics',
                ['', 'Olex2 (Dolomanov et al., 2009)',
                 'ShelXle (Hübschle 2011)',
                 'ORTEP Farrujia 2012',
                 'Bruker SHELXTL, XP (G. Sheldrick)',
                 'Mercury CSD, C. F. Macrae et al. 2008',
                 'PLATON (A.L.Spek, 2019)'
                 ]]
     },
    {'name'  : 'Crystal Cooling Device',
     'values': ['_diffrn_measurement_ambient_temperature_device_make',
                ['',
                 'Oxford Cryostream',
                 'Oxford Cryostream 800',
                 'Oxford Cryostream 700',
                 'Oxford Cryostream 600',
                 'Oxford N-Helix',
                 'Oxford Smartstream',
                 'Oxford Cobra',
                 'Bruker Kryofelx II',
                 'Bruker Kryofelx I',
                 ]
                ]

     },
    {'name'  : 'Radiation Type',
     'values': ['_diffrn_radiation_probe',
                ['',
                 'x-ray',
                 'neutron',
                 'electron',
                 'gamma',
                 ]
                ]

     },
    {'name'  : 'Sample environment',
     'values': ['_diffrn_ambient_environment',
                ['',
                 'N~2~',
                 'He',
                 'vacuum',
                 'mother liquor',
                 'Ar',
                 'H~2~'
                 ]
                ]

     },
    {'name'  : 'Twin relationship',
     'values': ['_twin_individual_twin_lattice_type',
                ['',
                 'ref',  # reference twin
                 'mt_I',  # merohedral class I (simple inversion)
                 'mt_II',  # merohedral class II (mirror or twofold)
                 'mt_I+II',  # class I and II simultaneously present
                 'rmt',  # reticular merohedral
                 'pmt',  # pseudo-merohedral
                 'rpmt',  # reticular pseudo-merohedral
                 'nmt',  # non-merohedral
                 ]
                ]
     },
    {'name'  : 'Absorption correction type',
     'values': ['_exptl_absorpt_correction_type',
                ['', 'multi-scan', 'numerical', 'empirical', 'gaussian', 'integration', 'analytical', 'none',
                 'cylinder', 'psi-scan', 'refdelf', 'sphere']]
     },
    {'name'  : 'Hydrogen refinement treatment',
     'values': ['_refine_ls_hydrogen_treatment',
                ['', 'undef', 'mixed', 'constr', 'noref', 'refall', 'refxyz', 'refU', 'hetero', 'heteroxyz', 'heteroU',
                 'heteronoref', 'hetero-mixed', 'heteroxyz-mixed', 'heteroU-mixed', 'heteronoref-mixed']]
     },
    {'name'  : 'Radiation type',
     'values': ['_diffrn_radiation_type',
                ['', 'Mo K\\a', 'Cu K\\a', 'Ag K\\a', 'In K\\a', 'Ga K\\a', 'Fe K\\a', 'W K\\a']]
     },
    {'name'  : 'Solution type',
     'values': ['_atom_sites_solution_primary',
                ['', 'direct', 'vecmap', 'heavy', 'difmap', 'geom', 'disper', 'isomor', 'notdet', 'dual', 'iterative',
                 'other']]
     },
    {'name'  : 'Solution type secondary',
     'values': ['_atom_sites_solution_secondary',
                ['', 'direct', 'vecmap', 'heavy', 'difmap', 'geom', 'disper', 'isomor', 'notdet', 'dual', 'iterative',
                 'other']]
     },
    {'name'  : 'Specimen support',
     'values': ['_diffrn_measurement_specimen_support',
                ['', 'MiTeGen micromount', 'glass capillary', 'quartz capillary', 'glass fiber', 'metal loop',
                 'nylon loop', 'cactus needle', 'cat whisker', 'carbon fiber', 'beryllium pin']]
     },
    {'name'  : 'Hydrogen solution type',
     'values': ['_atom_sites_solution_hydrogens',
                ['', 'direct', 'vecmap', 'heavy', 'difmap', 'geom', 'disper', 'isomor', 'notdet', 'dual', 'iterative',
                 'other']]
     },
    {'name'  : 'Specimen adhesive',
     'values': ['_diffrn_measurement_specimen_adhesive',
                ['', 'perfluorether oil', 'epoxy glue', 'motor oil', 'grease', 'honey']]
     },
    {'name'  : 'Type of structure',
     'values': ['_exptl_crystal_type_of_structure',
                ['cryst', 'mod', 'comp']]
     },
    {'name'  : 'Twin overlap',
     'values': ['_twin_dimensionality',
                ['', 'triperiodic', 'diperiodic', 'monoperiodic']]
     },
    {'name'  : 'Crystal system',
     'values': ['_space_group_crystal_system',
                ['', 'triclinic', 'monoclinic', 'orthorhombic', 'tetragonal', 'trigonal', 'hexagonal', 'cubic']]
     },
    # Obsolete by _space_group_crystal_system
    {'name'  : 'Crystal system (obsolete)',
     'values': ['_symmetry_cell_setting',
                ['', 'triclinic', 'monoclinic', 'orthorhombic', 'tetragonal', 'rhombohedral', 'trigonal', 'hexagonal',
                 'cubic']]
     },
    {'name'  : 'Paper submission category',
     'values': ['_publ_requested_category',
                ['', 'AD', 'CI', 'CM', 'CO', 'EI', 'EM', 'EO', 'FA', 'FI', 'FM', 'FO', 'GI', 'GM', 'GO', 'HI', 'HM',
                 'HO', 'QI', 'QM', 'QO', 'SC']]
     },
    {'name'  : 'Text section role',
     'values': ['_publ_body_element',
                ['', 'section', 'subsection', 'subsubsection', 'appendix', 'footnote']]
     },
    {'name'  : 'Text body format',
     'values': ['_publ_body_format',
                ['', 'ascii', 'cif', 'latex', 'rtf', 'sgml', 'tex', 'troff']]
     },
    {'name'  : 'Crystal color lustre',
     'values': ['_exptl_crystal_colour_lustre',
                ['', 'metallic', 'dull', 'clear']]
     },
    {'name'  : 'Crystal color modifier',
     'values': ['_exptl_crystal_colour_modifier',
                ['', 'light', 'dark', 'whitish', 'blackish', 'grayish', 'brownish', 'reddish', 'pinkish', 'orangish',
                 'yellowish', 'greenish', 'bluish']]
     },
    {'name'  : 'Structure-factor coefficient for refinement',
     'values': ['_refine_ls_structure_factor_coef',
                ['', 'F', 'Fsqd', 'Inet']]
     },
    {'name'  : 'Refinement matrix type',
     'values': ['_refine_ls_matrix_type',
                ['', 'full', 'fullcycle', 'atomblock', 'userblock', 'diagonal', 'sparse']]
     },
    {'name'  : 'Refinement software',
     'values': ['_computing_structure_refinement',
                ['', 'SHELXL-2019/2', 'SHELXL-2018/3', 'SHELXL-2018/1', 'SHELXL-97', 'olex2.refine', 'NoSpherA2',
                 'Jana2006', 'Jana2020', 'MoPro', 'BayMEM']]
     },
    {'name'  : 'Data reduction software',
     'values': ['_computing_data_reduction',
                ['', 'SAINT', 'CrysalisPro', 'XDS', 'OpenHKL', 'HKL-2000', 'HKL-3000']]
     },
]

celltxt = """
    <html>
    <body>
    <div align="right">
        <table border="0" cellspacing="1" cellpadding="1" style='font-size: 12px'>
            <tr>
                <td align='right'><i>a</i> = </td>
                <td align='right'>{0:>7.3f} Å,</td>
                <td align='right'><i>&alpha;</i> = </td> 
                <td align='right'>{3:>7.3f}°</td>
            </tr>
            <tr>
                <td align='right'><i>b</i> = </td>
                <td align='right'>{1:>7.3f} Å,</td>
                <td align='right'><i>&beta;</i> = </td> 
                <td align='right'>{4:>7.3f}°</td>
            </tr>
            <tr>
                <td align='right'><i>c</i> = </td>
                <td align='right'>{2:>7.3f} Å,</td>
                <td align='right'><i>&gamma;</i> = </td> 
                <td align='right'>{5:>7.3f}°</td>
            </tr>
       </table>
   </div>
   <div align='right' style="margin-left:0">
    Volume = {6:8.2f} Å<sup>3</sup>, <b>{7}</b>
   </div>
   </body>
   </html>
    """


def is_database_number(input_num: Union[str, int]) -> bool:
    if isinstance(input_num, int):
        input_num = str(input_num)
    state: bool = False
    if len(input_num) == 7 and isnumeric(input_num):
        state = True
    return state


def unify_line_endings(text: str):
    return '\n'.join(text.splitlines())


def remove_line_endings(text: str):
    return ''.join(text.splitlines())


def open_file(report_filename: Path):
    if report_filename.exists():
        if os.name == 'nt':
            os.startfile(report_filename)
        if sys.platform == 'darwin':
            subprocess.call(['open', report_filename])


if __name__ == '__main__':
    pass
