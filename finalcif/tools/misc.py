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
import re
from datetime import datetime
from math import sqrt
from os import path
from pathlib import Path
from typing import Union, Tuple, List

# protected space character:
protected_space = u'\u00A0'
# Angstrom character:
# angstrom = u'\u212B'    # Unicode angstrom sign (only for compatibility)
angstrom = u'\u00C5'  # Latin capital A with ring above. The Unicode consortium recommends to use the regular letter
# capital theta symbol:
Theta_symbol = u'\u03F4'
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


def get_file_with_new_ending(file: Path, new_ending: str, strip_from_name: str = '') -> Path:
    """
    Retruns a file path with a new ending. If strip_strip_from_name is given, this string is also
    removed from the file name before the suffix.
    """
    basename = file.stem
    if strip_from_name:
        basename = re.sub('{}$'.format(strip_from_name), '', basename)
    return file.parent.joinpath(Path(basename + new_ending))


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


def strip_finalcif_of_name(pth: str) -> str:
    """
    Strips '-finalcif' from the stem path
    """
    return re.sub('-finalcif$', '', pth)


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


# '_space_group_centring_type',  # seems to be used nowere
# '_exptl_absorpt_special_details',   # This is not official?!?
essential_keys = {
    # '_atom_sites_solution_secondary'                   : 'Codes which identify how the remaining non-hydrogen sites were located',
    # '_diffrn_measurement_specimen_adhesive'            : 'Adhesive used to hold the crystal on the _diffrn_measurement_specimen_support during intensity measurement.',
    # '_diffrn_source_power'                             : 'The power in kilowatts at which the radiation source was operated',
    # '_diffrn_source_target'                            : 'The chemical element symbol for the X-ray target (usually the anode) used to generate X-rays.',
    # '_olex2_diffrn_ambient_temperature_device'         : 'Device to cool the crystal during measurement',
    '_diffrn_measurement_ambient_temperature_device_make'         : 'Device to cool the crystal during measurement',
    '_atom_sites_solution_hydrogens': 'Codes which identify the methods used to locate the initial hydrogen atom sites',
    '_atom_sites_solution_primary': 'Codes which identify the methods used to locate the initial atom sites',
    '_audit_contact_author_address': 'The address of the cif author',
    '_audit_contact_author_email': 'The email address of the cif author',
    '_audit_contact_author_name': 'The name of the cif author',
    '_audit_contact_author_phone': 'The phone number of the cif author',
    '_audit_creation_method': 'The program that created this cif file after refinement',
    '_cell_angle_alpha': 'Unit-cell angle in degree',
    '_cell_angle_beta': 'Unit-cell angle in degree',
    '_cell_angle_gamma': 'Unit-cell angle in degree',
    '_cell_formula_units_Z': 'The number of the formula units in the unit cell as specified by _chemical_formula_sum',
    '_cell_length_a': 'Unit-cell length in angstroms',
    '_cell_length_b': 'Unit-cell length in angstroms',
    '_cell_length_c': 'Unit-cell length in angstroms',
    '_cell_measurement_reflns_used': 'The total number of reflections used to determine the unit cell',
    '_cell_measurement_temperature': 'The temperature in kelvins at which the unit-cell parameters were measured',
    '_cell_measurement_theta_max': 'The minimum theta angles of reflections used to measure the unit cell in degrees',
    '_cell_measurement_theta_min': 'The maximum theta angles of reflections used to measure the unit cell in degrees',
    '_cell_volume': 'Unit-cell volume in cubic angstroms',
    '_chemical_absolute_configuration': 'Method how the absolute configuration was established',
    '_chemical_formula_moiety': 'Formula with each discrete bonded residue or ion separated',
    '_chemical_formula_sum': 'The sum formula specifies the composition of the compound',
    '_chemical_formula_weight': 'Formula mass in daltons',
    '_chemical_melting_point': 'The temperature in kelvins at which the crystalline solid changes to a liquid',
    '_chemical_name_common': 'Trivial name by which the compound is commonly known',
    '_chemical_name_systematic': 'IUPAC or Chemical Abstracts full name of the compound',
    '_computing_cell_refinement': 'Computer program used to index and refine the unit cell parameters',
    '_computing_data_collection': 'Computer program used to collect the intensity data',
    '_computing_data_reduction': 'Computer program used to integrate the intensity data',
    '_computing_molecular_graphics': 'Computer program used to make molecular graphics',
    '_computing_publication_material': 'Computer program used to generate publication material',
    '_computing_structure_refinement': 'Computer program used for structure refinement',
    '_computing_structure_solution': 'Computer program used for structure solution',
    '_diffrn_ambient_environment': 'The gas or liquid surrounding the sample, if not air.',
    '_diffrn_ambient_temperature': 'The mean temperature in kelvins at which the intensities were measured',
    '_diffrn_detector': 'The general class of the radiation detector.',
    '_diffrn_detector_area_resol_mean': 'The resolution of an area detector, in pixels/mm.',
    '_diffrn_detector_type': 'The make, model or name of the detector device used.',
    '_diffrn_measured_fraction_theta_full': 'Fraction of unique (symmetry-independent) reflections measured out to _diffrn_reflns_theta_full',
    '_diffrn_measured_fraction_theta_max': 'Fraction of unique (symmetry-independent) reflections measured out to _diffrn_reflns_theta_max',
    '_diffrn_measurement_device': 'The general class of goniometer or device used to support and orient the specimen.',
    '_diffrn_measurement_device_type': 'The make, model or name of the measurement device used.',
    '_diffrn_measurement_method': "Method used to measure the intensities, eg.g 'omega scans'",
    '_diffrn_measurement_specimen_support': 'The physical device used to support the crystal during data collection.',
    '_diffrn_radiation_monochromator': r'The typ monochromator type to get _diffrn_radiation_wavelength',
    '_diffrn_radiation_probe': 'The nature of the radiation used',
    '_diffrn_radiation_type': r'The type of the radiation, e.g. Mo K\a',
    '_diffrn_radiation_wavelength': 'The radiation wavelength in angstroms',
    '_diffrn_reflns_Laue_measured_fraction_full': 'Fraction of Laue unique reflections measured out to the resolution given in _diffrn_reflns_theta_full',
    '_diffrn_reflns_Laue_measured_fraction_max': 'Fraction of Laue unique reflections measured out to the resolution given in _diffrn_reflns_theta_max',
    '_diffrn_reflns_av_R_equivalents': 'The residual for symmetry-equivalent reflections used to calculate the average intensity',
    '_diffrn_reflns_av_unetI/netI': 'Measure [sum |u(net I)|/sum|net I|] for all measured reflections',
    '_diffrn_reflns_number': 'The total number of measured intensities excluding systematic absent',
    '_diffrn_reflns_point_group_measured_fraction_full': 'Fraction of crystal point-group unique reflections measured out to the resolution given in _diffrn_reflns_theta_full',
    '_diffrn_reflns_point_group_measured_fraction_max': 'Fraction of crystal point-group unique reflections measured out to the resolution given in _diffrn_reflns_theta_max',
    '_diffrn_reflns_theta_full': 'The theta angle at which the measured reflection count is close to complete',
    '_diffrn_reflns_theta_max': 'Maximum theta angle in degrees for the measured intensities',
    '_diffrn_reflns_theta_min': 'Minimum theta angle in degrees for the measured intensities',
    '_diffrn_source': "The general class of the source of radiation, e.g.'sealed X-ray tube'",
    '_diffrn_source_current': 'The current in milliamperes at which the radiation source was operated',
    '_diffrn_source_type': 'The make, model or name of the source of radiation.',
    '_diffrn_source_voltage': 'The voltage in kilovolts at which the radiation source was operated',
    '_exptl_absorpt_coefficient_mu': 'The absorption coefficient mu in reciprocal millimetres',
    '_exptl_absorpt_correction_T_max': 'The calculated maximum value of the transmission factor for the specimen',
    '_exptl_absorpt_correction_T_min': 'The calculated minimum value of the transmission factor for the specimen',
    '_exptl_absorpt_correction_type': 'The absorption-correction type and method',
    '_exptl_absorpt_process_details': 'Description of the absorption process applied to the intensities',
    '_exptl_crystal_F_000': 'The effective number of electrons in the crystal unit cell contributing to F(000)',
    '_exptl_crystal_colour': 'The colour of the crystal',
    '_exptl_crystal_density_diffrn': 'Density values calculated from the crystal cell and contents',
    '_exptl_crystal_density_meas': 'Density value measured using standard chemical and physical methods',
    '_exptl_crystal_density_method': 'The method used to measure _exptl_crystal_density_meas',
    '_exptl_crystal_description': 'A description of the quality and habit of the crystal',
    '_exptl_crystal_recrystallization_method': 'Describes the method used to crystallize the sample',
    '_exptl_crystal_size_max': 'Maximum dimension of the crystal in mm',
    '_exptl_crystal_size_mid': 'Medium dimension of the crystal in mm',
    '_exptl_crystal_size_min': 'Minimum dimension of the crystal in mm',
    '_exptl_special_details': 'Any details about the experimental work prior to the measurement',
    '_geom_special_details': 'The description of geometrical extra information such as least-squares planes',
    '_publ_contact_author_id_orcid': 'The ORCID ID of the author submitting the manuscript and data block',
    '_publ_section_references': 'References for programs used to process the data',
    '_refine_ls_R_factor_all': 'Residual factor for all reflections. This is the conventional R factor',
    '_refine_ls_R_factor_gt': 'Residual R1 factor for the reflections satisfying the _reflns_threshold_expression',
    '_refine_ls_abs_structure_Flack': 'The measure of absolute structure as defined by Flack (1983)',
    '_refine_ls_abs_structure_details': 'The nature of the absolute structure and how it was determined',
    '_refine_ls_extinction_coef': 'The extinction coefficient used to calculate the correction factor applied to the structure-factor data',
    '_refine_ls_extinction_method': 'A description of the extinction-correction method applied',
    '_refine_ls_goodness_of_fit_ref': 'The l.s. goodness-of-fit parameter S for all reflections in the refinement',
    '_refine_ls_hydrogen_treatment': 'Treatment of hydrogen atoms in the least-squares refinement',
    '_refine_ls_matrix_type': 'Type of matrix used to accumulate the least-squares derivatives',
    '_refine_ls_number_parameters': 'The number of parameters refined in the least-squares process',
    '_refine_ls_number_reflns': 'The number of unique reflections contributing to the least-squares refinement calculation',
    '_refine_ls_number_restraints': 'The number of restrained parameters',
    '_refine_ls_restrained_S_all': "The l.s. goodness-of-fit parameter S' for all reflections in the refinement and including the restraints applied",
    '_refine_ls_shift/su_max': 'The largest ratio of the final least-squares parameter shift to the final standard uncertainty',
    '_refine_ls_shift/su_mean': 'The average ratio of the final least-squares parameter shift to the final standard uncertainty',
    '_refine_ls_structure_factor_coef': 'Structure-factor coefficient |F|, F^2^ or I used in the least-squares refinement process',
    '_refine_ls_wR_factor_gt': 'Weighted residual factor for reflections satisfying _reflns_threshold_expression',
    '_refine_ls_wR_factor_ref': 'Weighted residual factors wR2 for all reflections included in the refinement.',
    '_refine_ls_weighting_details': 'A description of special aspects of the weighting scheme used in the least-squares refinement',
    '_refine_ls_weighting_scheme': 'The weighting scheme applied in the least-squares process',
    '_refine_special_details': 'Detailed refinement description, e.g. information about a disorder model',
    '_reflns_Friedel_coverage': 'The proportion of Friedel-related reflections present in the number of independent reflections',
    '_reflns_Friedel_fraction_full': 'The number of Friedel pairs measured out to _diffrn_reflns_theta_full',
    '_reflns_Friedel_fraction_max': 'The number of Friedel pairs measured out to _diffrn_reflns_theta_max',
    '_reflns_number_gt': 'The number of reflections in the _refln_ list that are significantly intense',
    '_reflns_number_total': 'The total number of reflections in the _refln_ list (not the _diffrn_refln_ list)',
    '_reflns_special_details': 'Description of the properties of the reported reflection list',
    '_reflns_threshold_expression': 'The threshold that serves to identify significantly intense reflections',
    '_space_group_IT_number': 'The number as assigned in International Tables for Crystallography Vol. A',
    '_space_group_crystal_system': 'The name of the crystal system to which the space group belongs',
    '_space_group_name_H-M_alt': 'Hermann-Mauguin symbol to describe the space group',
    '_space_group_name_Hall': 'Space-group symbol defined by S. R. Hall (1981)',
    # '_space_group_symop_operation_xyz'                 : 'Symmetry operations of the space group',
}

twin_keys = {
    '_twin_individual_id': 'The unique identifier for this twin individual',
    '_twin_individual_twin_lattice_type': 'Identification of the symmetry relationships between the twin lattices',
    '_twin_special_details': 'Information about twinning in the sample not described elsewhere',
    '_twin_individual_mass_fraction_refined': 'The refined mass fraction of this twin individual',
    '_twin_individual_twin_matrix_11': 'Elements of the matrix',
    '_twin_individual_twin_matrix_12': 'Elements of the matrix',
    '_twin_individual_twin_matrix_13': 'Elements of the matrix',
    '_twin_individual_twin_matrix_21': 'Elements of the matrix',
    '_twin_individual_twin_matrix_22': 'Elements of the matrix',
    '_twin_individual_twin_matrix_23': 'Elements of the matrix',
    '_twin_individual_twin_matrix_31': 'Elements of the matrix',
    '_twin_individual_twin_matrix_32': 'Elements of the matrix',
    '_twin_individual_twin_matrix_33': 'Elements of the matrix',
}

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

ABSORPTION_CORRECTION_TYPES = (
    (0, ''),  # , ''),
    (1, 'multi-scan'),  # , 'symmetry-related measurements'),
    (2, 'numerical'),  # , 'numerical from crystal shape'),
    (3, 'empirical'),  # , 'empirical from intensities'),
    (4, 'gaussian'),  # , 'Gaussian from crystal shape'),
    (5, 'integration'),  # , 'integration from crystal shape'),
    (6, 'analytical'),  # , 'analytical from crystal shape'),
    (7, 'none'),  # , 'no absorption correction applied'),
    (8, 'cylinder'),  # , 'cylindrical'),
    (9, 'psi-scan'),  # , 'psi-scan corrections'),
    (10, 'refdelf'),  # , 'refined from delta-F'),
    (11, 'sphere'),  # , 'spherical'),
)

COLOUR_CHOICES = (
    (0, ''),
    (1, 'colourless'),
    (2, 'white'),
    (3, 'black'),
    (4, 'gray'),
    (5, 'brown'),
    (6, 'red'),
    (7, 'pink'),
    (8, 'orange'),
    (9, 'yellow'),
    (10, 'green'),
    (11, 'blue'),
    (12, 'violet')
)

SPECIMEN_SUPPORT = (
    (0, ''),
    (1, 'MiTeGen micromount'),
    (2, 'glass capillary'),
    (3, 'quartz capillary'),
    (4, 'glass fiber'),
    (5, 'metal loop'),
    (6, 'nylon loop'),
    (7, 'cactus needle'),
    (8, 'cat whisker'),
    (9, 'carbon fiber'),
    (10, 'beryllium pin'),
)

ADHESIVE = (
    (0, ''),
    (1, 'perfluorether oil'),
    (2, 'epoxy glue'),
    (3, 'motor oil'),
    (4, 'grease'),
    (5, 'honey'),
)

ABSOLUTE_CONFIGURATION_CHOICES = (
    (0, ''),  #
    (1, 'ad'),  # , 'Anomalous dispersion'),
    (2, 'rm'),  # , 'Reference Molecule'),
    (3, 'rmad'),  # , 'Reference Molecule and ad'),
    (4, 'syn'),  # , 'Synthesis'),
    (5, 'unk'),  # , 'Unknown'),
    (6, '.'),  # , 'Inapplicable'),
)

REFINE_LS_HYDROGEN_TREATMENT = (
    (0, ''),
    (1, 'undef'),
    (2, 'mixed'),
    (3, 'constr'),
    (4, 'noref'),
    (5, 'refall'),
    (6, 'refxyz'),
    (7, 'refU'),
    (8, 'hetero'),
    (9, 'heteroxyz'),
    (10, 'heteroU'),
    (11, 'heteronoref'),
    (12, 'hetero-mixed'),
    (13, 'heteroxyz-mixed'),
    (14, 'heteroU-mixed'),
    (15, 'heteronoref-mixed'),
)

RADIATION_TYPE = (
    (0, r''),
    (1, r'Mo K\a'),
    (2, r'Cu K\a'),
    (3, r'Ag K\a')
)

SOLUTION_PRIMARY = (
    (0, ''),
    (1, 'direct'),
    (2, 'vecmap'),
    (3, 'heavy'),
    (4, 'difmap'),
    (5, 'geom'),
    (6, 'disper'),
    (7, 'isomor'),
    (8, 'notdet'),
    (9, 'dual'),
    (10, 'iterative'),
    (11, 'other'),
)

SOLUTION_SECONDARY = (
    (0, ''),
    (1, 'direct'),
    (2, 'vecmap'),
    (3, 'heavy'),
    (4, 'difmap'),
    (5, 'geom'),
    (6, 'disper'),
    (7, 'isomor'),
    (8, 'notdet'),
    (9, 'dual'),
    (10, 'iterative'),
    (11, 'other'),
)

combobox_fields = {'_exptl_crystal_colour': COLOUR_CHOICES,
                   '_chemical_absolute_configuration': ABSOLUTE_CONFIGURATION_CHOICES,
                   '_exptl_absorpt_correction_type': ABSORPTION_CORRECTION_TYPES,
                   '_refine_ls_hydrogen_treatment': REFINE_LS_HYDROGEN_TREATMENT,
                   '_diffrn_radiation_type': RADIATION_TYPE,
                   '_atom_sites_solution_primary': SOLUTION_PRIMARY,
                   '_atom_sites_solution_secondary': SOLUTION_PRIMARY,
                   '_diffrn_measurement_specimen_support': SPECIMEN_SUPPORT,
                   '_atom_sites_solution_hydrogens': SOLUTION_PRIMARY,
                   '_diffrn_measurement_specimen_adhesive': ADHESIVE,
                   }

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
    '_atom_site_aniso_label': 'Displacement Parameters',
    '_atom_site_label': 'Atomic Coordinates',
    '_atom_type_symbol': 'Scattering Factors',
    '_audit_author_name': 'CIF Author',
    '_citation_doi': 'Citations',
    '_citation_id': 'Citations',
    '_citation_year': 'Citations',
    '_geom_angle_atom_site_label_1': 'Angles',
    '_geom_bond_atom_site_label_1': 'Bonds',
    '_geom_torsion_atom_site_label_1': 'Torsion Angles',
    '_shelx_res_file': 'SHELX res File',
    '_space_group_symop_id': 'Symmetry',
    '_space_group_symop_operation_xyz': 'Symmetry',
    '_symmetry_equiv_pos_site_id': 'Symmetry',
    '_symmetry_equiv_pos_as_xyz': 'Symmetry',
    '_publ_contact_author_name': 'Publication Contact Author',
    '_publ_author_name': 'Publication Authors',
    '_geom_hbond_atom_site_label_D': 'Hydrogen Bonds',
    '_geom_hbond_atom_site_label_H': 'Hydrogen Bonds',
    '_geom_hbond_atom_site_label_A': 'Hydrogen Bonds',
    '_exptl_crystal_face_index_h': 'Crystal Faces',
    '_exptl_oxdiff_crystal_face_indexfrac_h': 'Crystal Faces Fractional',
    '_platon_squeeze_void_nr': 'Platon SQUEEZE Voids',
    '_smtbx_masks_void_nr': 'smtbx Solvent Mask',
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

predef_equipment_templ = [{'name': 'D8 VENTURE',
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
                          {'name': 'APEX2 QUAZAR',
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
                          {'name': 'Rigaku Spider',
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
                          {'name': 'Crystallographer Details',
                           'items': [
                               ['_audit_contact_author_name', '?'],
                               ['_audit_contact_author_address', "?"],
                               ['_audit_contact_author_email', '?'],
                               ['_audit_contact_author_phone', '?'],
                               ['_publ_contact_author_id_orcid', '?'],
                           ]
                           },
                          ]

"""
{'name' : 'Contact author name and address',
'items': [
   ['_audit_contact_author_name', 'Dr. Daniel Kratzert'],
   ['_audit_contact_author_address',
    "Albert-Ludwigs-Universität Freiburg\n"
    "Institut für Anorganische und Analytische Chemie\n"
    "Albertstraße 21\n"
    "Freiburg i. Br.\n"
    "79104\n"
    "Germany"],
   ['_audit_contact_author_email', 'dkratzert@gmx.de'],
   ['_audit_contact_author_phone', '+497612036156'],
   ['_publ_contact_author_id_orcid', 'https://orcid.org/0000-0003-0970-9780'],
]
},"""

### Property contents:

predef_prop_templ = [{'name': 'Crystal Color',
                      'values': ['_exptl_crystal_colour',
                                 ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue',
                                  'green', 'gray', 'pink', 'orange', 'violet', 'brown']]
                      },
                     {'name': 'Crystal Habit Description',
                      'values': ['_exptl_crystal_description',
                                 ['', 'block', 'needle', 'plate', 'prism', 'sphere']]
                      },
                     {'name': 'Cell Measurement Temperature',
                      'values': ['_cell_measurement_temperature',
                                 ['', '15', '80(2)', '100(2)', '110(2)',
                                  '120(2)', '130(2)', '150(2)', '200(2)', '298(2)']]
                      },
                     {'name': 'Measurement Temperature',
                      'values': ['_diffrn_ambient_temperature',
                                 ['', '15(1)', '80(2)', '100(2)', '110(2)',
                                  '120(2)', '130(2)', '150(2)', '200(2)', '293.15(2)', '298(2)']]
                      },
                     {'name': 'Molecular Graphics',
                      'values': ['_computing_molecular_graphics',
                                 ['', 'Olex2 (Dolomanov et al., 2009)',
                                  'ShelXle (Hübschle 2011)',
                                  'ORTEP Farrujia 2012',
                                  'Bruker SHELXTL, XP (G. Sheldrick)',
                                  'Mercury CSD, C. F. Macrae et al. 2008',
                                  'PLATON (A.L.Spek, 2019)'
                                  ]]
                      },
                     {'name': 'Crystal Cooling Device',
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
                     {'name': 'Radiation Type',
                      'values': ['_diffrn_radiation_probe',
                                 ['',
                                  'x-ray',
                                  'neutron',
                                  'electron',
                                  'gamma',
                                  ]
                                 ]

                      },
                     {'name': 'Sample environment',
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
                     {'name': 'Twin relationship',
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
                      }

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
