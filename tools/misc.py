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


"""
_chemical_name_systematic         ?
_chemical_name_common             ?
_chemical_melting_point           ?
_chemical_formula_moiety          ?
_cell_measurement_reflns_used     ?
_cell_measurement_theta_min       ?
_cell_measurement_theta_max       ?
_cell_measurement_temperature     100(2)
_cell_formula_units_Z             2
_exptl_crystal_description        ?
_exptl_crystal_colour             ?
_exptl_crystal_density_meas       ?
_exptl_crystal_density_method     ?
_exptl_transmission_factor_min    ?
_exptl_transmission_factor_max    ?
_exptl_absorpt_correction_type    ?
_exptl_absorpt_correction_T_min   ?
_exptl_absorpt_correction_T_max   ?
_exptl_absorpt_process_details    ?
_exptl_absorpt_special_details    ?
_exptl_crystal_size_max           0.180
_exptl_crystal_size_mid           0.150
_exptl_crystal_size_min           0.060
_exptl_absorpt_coefficient_mu     0.077
_diffrn_ambient_temperature       100(2)
_diffrn_source                    ?
_diffrn_measurement_device_type   ?
_diffrn_measurement_method        ?
_diffrn_radiation_type            MoK\a
_diffrn_reflns_av_R_equivalents   ?
_computing_data_collection        ?
_computing_cell_refinement        ?
_computing_data_reduction         ?
_computing_structure_solution     ?
_computing_molecular_graphics     ?
_computing_publication_material   ?
_refine_special_details           ?
_atom_sites_solution_primary      ?
_atom_sites_solution_secondary    ?
_refine_ls_hydrogen_treatment     constr

_atom_sites_solution_primary      direct 
_atom_sites_solution_secondary    difmap 
"""

high_prio_keys = ['_chemical_formula_moiety',
                  '_space_group_name_H-M_alt',
                  '_space_group_centring_type',
                  '_space_group_IT_number',
                  '_space_group_crystal_system',
                  '_cell_formula_units_Z',
                  '_audit_creation_method',
                  '_chemical_formula_sum',
                  '_chemical_formula_weight',
                  '_exptl_crystal_description',
                  '_exptl_crystal_colour',
                  '_chemical_absolute_configuration',
                  '_exptl_crystal_size_max',
                  '_exptl_crystal_size_mid',
                  '_exptl_crystal_size_min',
                  '_exptl_absorpt_coefficient_mu',
                  '_exptl_absorpt_correction_type',
                  '_exptl_absorpt_process_details',
                  '_exptl_absorpt_special_details',
                  '_diffrn_ambient_temperature',
                  '_exptl_absorpt_correction_T_min',
                  '_exptl_absorpt_correction_T_max',
                  '_cell_measurement_reflns_used',
                  '_cell_measurement_temperature',
                  '_cell_measurement_theta_min',
                  '_cell_measurement_theta_max',
                  '_diffrn_source',
                  '_diffrn_measurement_device_type',
                  '_diffrn_measurement_method',
                  '_diffrn_radiation_type',
                  '_diffrn_reflns_av_R_equivalents',
                  '_computing_data_collection',  # from frame header: 'PROGRAM': 'BIS V6.2.10/2018-10-02',
                  '_computing_cell_refinement',
                  '_computing_data_reduction',
                  '_computing_structure_solution',
                  '_computing_molecular_graphics',
                  '_computing_publication_material',
                  '_refine_special_details',
                  '_atom_sites_solution_primary',
                  # '_atom_sites_solution_secondary',
                  '_refine_ls_hydrogen_treatment',  # use a combo-box or dropdown
                  '',
                  '',
                  ]
medium_prio_keys = ['_chemical_name_systematic',
                    '_chemical_name_common',
                    ]
low_prio_keys = ['']

absorption_correction_types = {
    'analytical' : 'analytical from crystal shape',
    'cylinder'   : 'cylindrical',
    'empirical'  : 'empirical from intensities',
    'gaussian'   : 'Gaussian from crystal shape',
    'integration': 'integration from crystal shape',
    'multi-scan' : 'symmetry-related measurements',
    'none'       : 'no absorption correction applied',
    'numerical'  : 'numerical from crystal shape',
    'psi-scan'   : 'psi-scan corrections',
    'refdelf'    : 'refined from delta-F',
    'sphere'     : 'spherical',
}

COLOUR_CHOICES = (
    (0, 'not applicable'),
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
    ('ad', 'Anomalous dispersion'),
    ('rm', 'Reference Molecule'),
    ('rmad', 'Reference Molecule and anomalous dispersion'),
    ('syn', 'Synthesis'),
    ('unk', 'Unknown'),
    ('.', 'Inapplicable'),
)

special_fields = {'_exptl_crystal_colour'           : COLOUR_CHOICES,
                  '_chemical_absolute_configuration': ABSOLUTE_CONFIGURATION_CHOICES,

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
