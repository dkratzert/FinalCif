from math import inf


class BaseLimits:
    upper: int | float | str
    lower: int | float | str
    valid: callable
    value_type: type[int | float | str]
    help_text: str

    def __init__(self, lower, upper, help_text: str = ''):
        self.lower = lower
        self.upper = upper
        self.help_text = help_text
        self.valid = self.validate_cif_key

    def __repr__(self):
        return (f"<{self.__class__.__name__}(lower bound: {self.lower}, upper bound: {self.upper}, "
                f"type: {self.value_type})> )>")

    def validate_cif_key(self, value: str):
        if '(' in value and ')' in value:
            value, esd = value.split('(')
            value = value.strip()
            after_esd = esd.split(')')[1]
            if after_esd:
                return False
        valid = False
        value = value.split('(')[0].strip()
        if value in ('', '?', '.'):
            return True
        try:
            value = self.value_type(value)
        except Exception:
            return False
        if self.lower <= value <= self.upper:
            valid = True
        return valid


class Integerlimits(BaseLimits):
    value_type = int

    def __init__(self, lower: int, upper: int, help_text: str | None = None):
        if not help_text:
            help_text = (f'Must be a {"negative" if lower < 0 else "positive"} '
                         f'integer number between {lower} and {upper}.')
        super().__init__(lower, upper, help_text)

    def validate_cif_key(self, value: str):
        valid = super().validate_cif_key(value)
        value = value.split('(')[0].strip()
        if not value.replace('-', '').isdigit() and value not in ('', '?', '.'):
            valid = False
        return valid


class Floatlimits(BaseLimits):
    value_type = float

    def __init__(self, lower: float = -inf, upper: float = inf, help_text: str | None = None):
        if not help_text:
            if lower < 0 and upper <= 0:
                limit = 'negative '
            elif lower < 0 < upper:
                limit = ''
            else:
                limit = 'positive '
            help_text = (f'Must be a {limit}'
                         f'decimal number between {lower} and {upper}.')
        super().__init__(lower, upper, help_text)


class Stringlimits:
    def __init__(self, help_text: str | None = None):
        self.valid = self.validate_cif_key
        self.help_text = 'Must be letters'
        if help_text:
            self.help_text = help_text

    def validate_cif_key(self, value: str):
        if value.isalpha():
            return True
        return False


class Textlimits:
    def __init__(self, options: list[str], help_text: str | None= None):
        self.valid = self.validate_cif_key
        self.options = options
        self.help_text = f'Must be one of: {", ".join(options)}.'
        if help_text:
            self.help_text = help_text

    def validate_cif_key(self, value: str):
        if value in ('', '?', '.') or value.lower() in (x.lower() for x in self.options if x is not None):
            return True
        return False


validators: dict[str, BaseLimits] = {
    '_database_code_depnum_ccdc_archive'   : Integerlimits(lower=0, upper=inf),
    '_cell_measurement_reflns_used'        : Integerlimits(lower=0, upper=inf),
    '_cell_measurement_theta_min'          : Floatlimits(lower=0.0, upper=90.0),
    '_cell_measurement_theta_max'          : Floatlimits(lower=0.0, upper=90.0),
    '_chemical_melting_point'              : Floatlimits(lower=0.0, upper=5000.0),
    '_diffrn_reflns_number'                : Integerlimits(lower=0, upper=inf),
    '_exptl_crystal_density_meas'          : Floatlimits(lower=0, upper=25.0),
    '_exptl_crystal_density_diffrn'        : Floatlimits(lower=0, upper=25.0),
    '_diffrn_ambient_temperature'          : Floatlimits(lower=0, upper=inf),
    '_diffrn_source_current'               : Floatlimits(lower=0.0, upper=inf),
    '_diffrn_source_voltage'               : Floatlimits(lower=0.0, upper=inf),
    '_exptl_absorpt_correction_T_max'      : Floatlimits(lower=0.0, upper=1.0),
    '_exptl_absorpt_correction_T_min'      : Floatlimits(lower=0.0, upper=1.0),
    '_exptl_transmission_factor_max'       : Floatlimits(lower=0.0, upper=1.0),
    '_exptl_transmission_factor_min'       : Floatlimits(lower=0.0, upper=1.0),
    '_cell_angle_alpha'                    : Floatlimits(lower=0.0, upper=180.0),
    '_cell_angle_beta'                     : Floatlimits(lower=0.0, upper=180.0),
    '_cell_angle_gamma'                    : Floatlimits(lower=0.0, upper=180.0),
    '_cell_formula_units_Z'                : Integerlimits(lower=1, upper=inf),
    '_cell_length_a'                       : Floatlimits(lower=0.0, upper=inf),
    '_cell_length_b'                       : Floatlimits(lower=0.0, upper=inf),
    '_cell_length_c'                       : Floatlimits(lower=0.0, upper=inf),
    '_cell_measurement_temperature'        : Floatlimits(lower=0.0, upper=inf),
    '_cell_volume'                         : Floatlimits(lower=0.0, upper=inf),
    '_chemical_formula_weight'             : Floatlimits(lower=1.0, upper=inf),
    '_diffrn_measured_fraction_theta_full' : Floatlimits(lower=0.0, upper=1.0),
    '_diffrn_measured_fraction_theta_max'  : Floatlimits(lower=0.0, upper=1.0),
    '_diffrn_radiation_wavelength'         : Floatlimits(lower=0.0, upper=1.0 * inf),
    '_diffrn_reflns_Laue_'
    'measured_fraction_full'               : Floatlimits(lower=0.95,
                                                         upper=1.0,
                                                         help_text="This number should not be between zero and 0.95,\n"
                                                                   "since it represents the fraction of reflections\n"
                                                                   "measured in the part of the diffraction pattern\n"
                                                                   "that is essentially complete."),
    '_diffrn_reflns_point_group_'
    'measured_fraction_full'               : Floatlimits(lower=0.95,
                                                         upper=1.0,
                                                         help_text="This number should not be between zero and 0.95,\n"
                                                                   "since it represents the fraction of reflections\n"
                                                                   "measured in the part of the diffraction pattern\n"
                                                                   "that is essentially complete."),
    '_diffrn_reflns_Laue_'
    'measured_fraction_max'                : Floatlimits(lower=0.0, upper=1.0),
    '_diffrn_reflns_point_'
    'group_measured_fraction_max'          : Floatlimits(lower=0.0, upper=1.0),
    '_diffrn_reflns_theta_full'            : Floatlimits(lower=0.0, upper=90.0),
    '_diffrn_reflns_theta_max'             : Floatlimits(lower=0.0, upper=90.0),
    '_diffrn_reflns_theta_min'             : Floatlimits(lower=0.0, upper=90.0),
    '_diffrn_reflns_av_R_equivalents'      : Floatlimits(lower=0.0, upper=inf),
    '_diffrn_reflns_av_unetI/netI'         : Floatlimits(lower=0.0, upper=inf),
    '_diffrn_reflns_limit_h_max'           : Integerlimits(lower=0, upper=inf),
    '_diffrn_reflns_limit_k_max'           : Integerlimits(lower=0, upper=inf),
    '_diffrn_reflns_limit_l_max'           : Integerlimits(lower=0, upper=inf),
    '_diffrn_reflns_limit_h_min'           : Integerlimits(lower=-inf, upper=0),
    '_diffrn_reflns_limit_k_min'           : Integerlimits(lower=-inf, upper=0),
    '_diffrn_reflns_limit_l_min'           : Integerlimits(lower=-inf, upper=0),
    '_exptl_absorpt_coefficient_mu'        : Floatlimits(lower=0.0, upper=inf),
    '_exptl_crystal_size_max'              : Floatlimits(lower=0.0, upper=inf),
    '_exptl_crystal_size_min'              : Floatlimits(lower=0.0, upper=inf),
    '_exptl_crystal_size_mid'              : Floatlimits(lower=0.0, upper=inf),
    '_refine_diff_density_max'             : Floatlimits(lower=0.0, upper=inf),
    '_refine_diff_density_min'             : Floatlimits(lower=-inf, upper=0.0),
    '_refine_diff_density_rms'             : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_R_factor_all'              : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_R_factor_gt'               : Floatlimits(lower=0.0, upper=inf),
    # In fact from 0.0-1.0, but some software does other:
    '_refine_ls_abs_structure_Flack'       : Floatlimits(lower=-inf, upper=inf),
    '_refine_ls_goodness_of_fit_ref'       : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_number_parameters'         : Integerlimits(lower=0, upper=inf),
    '_refine_ls_number_reflns'             : Integerlimits(lower=0, upper=inf),
    '_refine_ls_number_restraints'         : Integerlimits(lower=0, upper=inf),
    '_refine_ls_restrained_S_all'          : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_shift/su_max'              : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_shift/su_mean'             : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_wR_factor_gt'              : Floatlimits(lower=0.0, upper=inf),
    '_refine_ls_wR_factor_ref'             : Floatlimits(lower=0.0, upper=inf),
    '_reflns_Friedel_coverage'             : Floatlimits(lower=0.0, upper=1.0),
    '_reflns_Friedel_fraction_full'        : Floatlimits(lower=0.0, upper=1.0),
    '_reflns_Friedel_fraction_max'         : Floatlimits(lower=0.0, upper=1.0),
    '_reflns_number_gt'                    : Integerlimits(lower=0.0, upper=inf),
    '_reflns_number_total'                 : Integerlimits(lower=0.0, upper=inf),
    '_shelx_estimated_absorpt_T_max'       : Floatlimits(lower=0.0, upper=1.0),
    '_shelx_estimated_absorpt_T_min'       : Floatlimits(lower=0.0, upper=1.0),
    '_shelx_hkl_checksum'                  : Integerlimits(lower=0, upper=inf),
    '_shelx_res_checksum'                  : Integerlimits(lower=0, upper=inf),
    '_shelx_fcf_checksum'                  : Integerlimits(lower=0, upper=inf),
    '_space_group_IT_number'               : Integerlimits(lower=1, upper=230),
    '_space_group_crystal_system'          : Textlimits(options=['triclinic',
                                                                 'monoclinic',
                                                                 'orthorhombic',
                                                                 'tetragonal',
                                                                 'trigonal',
                                                                 'hexagonal',
                                                                 'cubic', ]),
    # '_atom_type_description'              : Stringlimits(help_text='Must be an atom type'),
    '_atom_type_scat_dispersion_real'      : Floatlimits(lower=-inf, upper=inf),
    '_atom_type_scat_dispersion_imag'      : Floatlimits(lower=-inf, upper=inf),
    '_atom_site_fract_x'                   : Floatlimits(lower=-inf, upper=inf),
    '_atom_site_fract_y'                   : Floatlimits(lower=-inf, upper=inf),
    '_atom_site_fract_z'                   : Floatlimits(lower=-inf, upper=inf),
    '_atom_site_U_iso_or_equiv'            : Floatlimits(lower=0, upper=inf),
    '_atom_site_adp_type'                  : Textlimits(options=['Uani',
                                                                 'Uiso',
                                                                 'Uovl',
                                                                 'Umpe',
                                                                 'Bani',
                                                                 'Biso',
                                                                 'Bovl'
                                                                 ]),
    '_atom_site_occupancy'                 : Floatlimits(lower=0.0, upper=1.0),
    '_atom_site_site_symmetry_order'       : Floatlimits(lower=-inf, upper=inf),
    '_atom_site_calc_flag'                 : Textlimits(options=['d', 'calc', 'c', 'dum']),
    '_atom_site_refinement_flags_posn'     : Textlimits(options=['None',
                                                                 'D',
                                                                 'G',
                                                                 'R',
                                                                 'S',
                                                                 'DG',
                                                                 'DR',
                                                                 'DS',
                                                                 'GR',
                                                                 'GS',
                                                                 'RS',
                                                                 'DGR',
                                                                 'DGS',
                                                                 'DRS',
                                                                 'GRS',
                                                                 'DGRS']),
    '_atom_site_refinement_flags_adp'      : Textlimits(options=['None', 'T', 'U', 'TU']),
    '_atom_site_refinement_flags_occupancy': Textlimits(options=['None', 'P']),
    '_atom_site_disorder_assembly'         : Textlimits(options=['A', 'B', 'S']),
    '_atom_site_aniso_U_11'                : Floatlimits(),
    '_atom_site_aniso_U_22'                : Floatlimits(),
    '_atom_site_aniso_U_33'                : Floatlimits(),
    '_atom_site_aniso_U_23'                : Floatlimits(),
    '_atom_site_aniso_U_13'                : Floatlimits(),
    '_atom_site_aniso_U_12'                : Floatlimits(),
    '_geom_bond_distance'                  : Floatlimits(lower=0.0, upper=inf),
    '_geom_bond_publ_flag'                 : Textlimits(options=['No', 'n', 'Yes', 'y']),
    '_geom_angle'                          : Floatlimits(),
    '_geom_torsion'                        : Floatlimits(),
    '_geom_angle_publ_flag'                : Textlimits(options=['No', 'n', 'Yes', 'y']),
    '_geom_torsion_publ_flag'              : Textlimits(options=['No', 'n', 'Yes', 'y']),

}

if __name__ == '__main__':
    limits = validators['_chemical_melting_point']
    print(limits.valid('5'))
    print(limits.valid('-5'))

    min_ = validators['_diffrn_reflns_limit_h_min']
    print(min_.valid('-5'))
    print(min_.help_text)

    min_ = validators['_diffrn_reflns_Laue_measured_fraction_max']
    print(min_.valid('-5'))
    print(min_.help_text)

    min_ = validators['_refine_ls_number_restraints']
    print(min_.valid('-5'))
    print(min_.help_text)

    min_ = validators['_space_group_crystal_system']
    print(min_.valid('Triclinic'))
    print(min_.help_text)
