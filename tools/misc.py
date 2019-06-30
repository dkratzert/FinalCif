import itertools as it
import operator
import os


def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return it.zip_longest(*iters, fillvalue=fillvalue)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_files_from_current_dir():
    files = []
    for f in os.listdir('./'):
        if f.endswith('.cif'):
            files.append(f)
    return files


def this_or_quest(value):
    """
    Returns the value or a question mark if the value is None.
    """
    return value if value else '?'


class Manufacturer():
    """
    A class to count evidences for the manufacturer of a dataset.

    >>> from tools.misc import Manufacturer
    >>> m = Manufacturer()
    >>> m.points['bruker'] += 1
    >>> m.points['bruker'] += 1
    >>> m
    bruker
    >>> m.points['stoe'] += 1
    >>> m.points['stoe'] += 10
    >>> m
    stoe
    >>> m2 = Manufacturer()
    >>> m2
    """

    def __init__(self):
        self.points = {'bruker': 0,
                       'stoe'  : 0,
                       'rigaku': 0,
                       'other' : 0
                       }

    def get_manufacturer(self):
        """
        Returns the manufacturer with the most points.
        """
        if not any(self.points.values()):
            # all with 0 points
            return 'other'
        return max(self.points.items(), key=operator.itemgetter(1))[0]

    def __repr__(self):
        return self.get_manufacturer()


# '_space_group_centring_type',  # seems to be used nowere
# '_exptl_absorpt_special_details',   # This is not official?!?
high_prio_keys = [
    '_audit_creation_method',
    '_chemical_formula_moiety',
    '_chemical_formula_sum',
    '_chemical_formula_weight',
    '_space_group_crystal_system',  # formerly known as _symmetry_cell_setting
    '_space_group_IT_number',
    '_space_group_name_H-M_alt',
    '_exptl_crystal_description',
    '_exptl_crystal_colour',
    '_exptl_crystal_density_diffrn',
    '_exptl_crystal_F_000',
    '_exptl_crystal_size_max',
    '_exptl_crystal_size_mid',
    '_exptl_crystal_size_min',
    '_exptl_absorpt_coefficient_mu',
    '_exptl_absorpt_correction_type',
    '_exptl_absorpt_correction_T_min',
    '_exptl_absorpt_correction_T_max',
    '_exptl_absorpt_process_details',  # Program and reference e.g. 'MolEN (Fair, 1990)'
    '_cell_formula_units_Z',
    '_cell_measurement_temperature',
    '_cell_measurement_reflns_used',
    '_cell_measurement_theta_min',
    '_cell_measurement_theta_max',
    '_diffrn_ambient_temperature',
    '_diffrn_radiation_wavelength',
    '_diffrn_radiation_type',
    '_diffrn_source',
    '_diffrn_measurement_device_type',
    '_diffrn_measurement_method',
    '_diffrn_reflns_number',
    '_diffrn_reflns_av_unetI/netI',
    '_diffrn_reflns_av_R_equivalents',
    '_diffrn_reflns_theta_min',
    '_diffrn_reflns_theta_max',
    '_diffrn_reflns_theta_full',
    '_diffrn_measured_fraction_theta_max',
    '_diffrn_measured_fraction_theta_full',
    '_diffrn_reflns_Laue_measured_fraction_max',
    '_diffrn_reflns_Laue_measured_fraction_full',
    '_diffrn_reflns_point_group_measured_fraction_max',
    '_diffrn_reflns_point_group_measured_fraction_full',
    '_reflns_number_total',
    '_reflns_number_gt',
    '_reflns_threshold_expression',
    '_reflns_Friedel_coverage',
    '_reflns_Friedel_fraction_max',
    '_reflns_Friedel_fraction_full',
    '_reflns_special_details',
    '_chemical_absolute_configuration',  # TODO: only in non-centro cases
    '_computing_data_collection',  # from frame header: 'PROGRAM': 'BIS V6.2.10/2018-10-02',
    '_computing_cell_refinement',
    '_computing_data_reduction',
    '_computing_structure_solution',
    '_computing_structure_refinement',  # 'SHELXL-2016/6 (Sheldrick, 2016)'
    '_refine_ls_hydrogen_treatment',
    '_refine_special_details',
    '_refine_ls_structure_factor_coef',
    '_refine_ls_matrix_type',
    '_refine_ls_weighting_scheme',
    '_atom_sites_solution_primary',
    '_refine_ls_weighting_details',
    '_atom_sites_solution_hydrogens',
    '_refine_ls_hydrogen_treatment',
    '_refine_ls_extinction_method',
    '_refine_ls_extinction_coef',
    '_refine_ls_number_reflns',
    '_refine_ls_number_parameters',
    '_refine_ls_number_restraints',
    '_refine_ls_R_factor_all',
    '_refine_ls_R_factor_gt',
    '_refine_ls_wR_factor_ref',
    '_refine_ls_wR_factor_gt',
    '_refine_ls_goodness_of_fit_ref',
    '_refine_ls_restrained_S_all',
    '_refine_ls_shift/su_max',
    '_refine_ls_shift/su_mean',
    '',
]

medium_prio_keys = [
    '_computing_molecular_graphics',
    '_computing_publication_material',
    '_chemical_name_systematic',
    '_chemical_name_common',
    '_chemical_melting_point',
    '_space_group_name_Hall',
    '_exptl_crystal_density_meas',
    '_exptl_crystal_density_method',
    '_diffrn_source_current',
    '_diffrn_source_voltage',
    '',
]
low_prio_keys = ['']

# Keys that get a text field in the main list.
text_field_keys = ('_refine_special_details',
                   '_refine_ls_weighting_details',
                   '_reflns_special_details',
                   '_exptl_absorpt_process_details'
                   '_refine_special_details',
                   )

ABSORPTION_CORRECTION_TYPES = (
    (0, ''),  # , ''),
    (1, 'analytical'),  # , 'analytical from crystal shape'),
    (2, 'cylinder'),  # , 'cylindrical'),
    (3, 'empirical'),  # , 'empirical from intensities'),
    (4, 'gaussian'),  # , 'Gaussian from crystal shape'),
    (5, 'integration'),  # , 'integration from crystal shape'),
    (6, 'multi-scan'),  # , 'symmetry-related measurements'),
    (7, 'none'),  # , 'no absorption correction applied'),
    (8, 'numerical'),  # , 'numerical from crystal shape'),
    (9, 'psi-scan'),  # , 'psi-scan corrections'),
    (10, 'refdelf'),  # , 'refined from delta-F'),
    (11, 'sphere'),  # , 'spherical'),
)

COLOUR_CHOICES = (
    (0, '?'),
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

ABSOLUTE_CONFIGURATION_CHOICES = (
    (0, ''),  # , '?'),
    (1, 'ad'),  # , 'Anomalous dispersion'),
    (2, 'rm'),  # , 'Reference Molecule'),
    (3, 'rmad'),  # , 'Reference Molecule and ad'),
    (4, 'syn'),  # , 'Synthesis'),
    (5, 'unk'),  # , 'Unknown'),
    (6, '.'),  # , 'Inapplicable'),
)

REFINE_LS_HYDROGEN_TREATMENT = (
    (0, '?'),
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
    (0, r'Mo K\a'),
    (1, r'Cu K\a'),
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
    (0, 'difmap'),
    (1, 'vecmap'),
    (2, 'heavy'),
    (3, 'direct'),
    (4, 'geom'),
    (5, 'disper'),
    (6, 'isomor'),
    (7, 'notdet'),
    (8, 'dual'),
    (9, 'iterative'),
    (10, 'other'),
)

special_fields = {'_exptl_crystal_colour'           : COLOUR_CHOICES,
                  '_chemical_absolute_configuration': ABSOLUTE_CONFIGURATION_CHOICES,
                  '_exptl_absorpt_correction_type'  : ABSORPTION_CORRECTION_TYPES,
                  '_refine_ls_hydrogen_treatment'   : REFINE_LS_HYDROGEN_TREATMENT,
                  '_diffrn_radiation_type'          : RADIATION_TYPE,
                  '_atom_sites_solution_primary'    : SOLUTION_PRIMARY,
                  '_atom_sites_solution_secondary'  : SOLUTION_PRIMARY,
                  }


def to_float(st):
    if isinstance(st, list):
        try:
            return [float(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return float(st)
        except ValueError:
            return None


def to_int(st):
    if isinstance(st, list):
        try:
            return [int(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return int(st)
        except ValueError:
            return None


### Property contents:

predef_prop_templ = [{'name'  : 'Crystal Color',
                      'values': ['_exptl_crystal_colour',
                                 ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue',
                                  'green', 'gray', 'pink', 'orange', 'violet', 'brown']]
                      },
                     {'name'  : 'Crystal Habit',
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
                      }
                     ]

predef_equipment_templ = [{'name' : 'D8 VENTURE',
                           'items': [
                               ['_diffrn_radiation_monochromator', 'mirror optics'],
                               ['_diffrn_measurement_device', 'three-circle diffractometer'],
                               ['_diffrn_measurement_device_type', 'Bruker D8 VENTURE dual wavelength Mo/Cu'],
                               ['_diffrn_measurement_method', '\w and \f scans'],
                               ['_diffrn_source', 'microfocus sealed X-ray tube'],
                               ['_diffrn_source_current', '50'],
                               ['_diffrn_source_voltage', '1.1'],
                               ['_diffrn_source_type', 'Incoatec I\ms'],
                           ]
                           },
                          {'name' : 'Rigaku Spider',
                           'items': [
                               ['_diffrn_radiation_source', ''],
                               ['_diffrn_radiation_monochromator', 'graphite'],
                               ['_diffrn_measurement_device', 'three-circle diffractometer'],
                               ['_diffrn_measurement_device_type', ''],
                               ['_diffrn_measurement_method', ''],
                               ['_diffrn_source', ''],
                           ]
                           },
                          ]
