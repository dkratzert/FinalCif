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
        A description of the quality and habit of the crystal.
   The crystal dimensions should not normally be reported here;
   use instead _exptl_crystal_size_ for the gross dimensions of
   the crystal and _exptl_crystal_face_ to describe the
   relationship between individual faces.
_exptl_crystal_colour             ?
_exptl_crystal_density_meas       ?
_exptl_crystal_density_method     ?
_exptl_transmission_factor_min    ?
_exptl_transmission_factor_max    ?
_exptl_absorpt_correction_type    ?
_exptl_absorpt_correction_T_min   ?
_exptl_absorpt_correction_T_max   ?
_exptl_absorpt_process_details    ? 
      Description of the absorption process applied to the
   intensities. A literature reference should be supplied
   for psi-scan techniques.
        'MolEN (Fair, 1990)'	
        '(North, Phillips & Mathews, 1968)'
_exptl_absorpt_special_details    ?
       Das ist kein Offizieller Key?
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
                  '_refine_ls_hydrogen_treatment',
                  '_atom_sites_solution_primary',
                  # '_atom_sites_solution_secondary',
                  ]
medium_prio_keys = ['_chemical_name_systematic',
                    '_chemical_name_common',
                    '',
                    '',
                    ]
low_prio_keys = ['']

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

special_fields = {'_exptl_crystal_colour'           : COLOUR_CHOICES,
                  '_chemical_absolute_configuration': ABSOLUTE_CONFIGURATION_CHOICES,
                  '_exptl_absorpt_correction_type'  : ABSORPTION_CORRECTION_TYPES,
                  '_refine_ls_hydrogen_treatment'   : REFINE_LS_HYDROGEN_TREATMENT,

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
                                  'green', 'gray', 'pink', 'orange', 'violet', 'brown']]},
                     {'name'  : 'Crystal Habit',
                      'values': ['_exptl_crystal_description', ['', 'block', 'needle', 'plate', 'prism', 'sphere']]
                      },
                     {'name'  : 'Cell Measurement Temperature',
                      'values': ['_cell_measurement_temperature', ['', '0', '15', '80(2)', '100(2)', '110(2)',
                                                                   '120(2)', '130(2)', '150(2)', '200(2)', '298(2)']]
                      },
                     {'name'  : 'Measurement Temperature',
                      'values': ['_diffrn_ambient_temperature', ['', '0', '15', '80(2)', '100(2)', '110(2)',
                                                                 '120(2)', '130(2)', '150(2)', '200(2)', '298(2)']]}
                     ],
