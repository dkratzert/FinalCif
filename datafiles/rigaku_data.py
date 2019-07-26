from pathlib import Path

import gemmi


class RigakuData():

    def __init__(self, cifod: Path):
        self.fileobj = cifod
        self.filename = cifod.name
        self.open_cif()
        self.sources = {}
        self.get_sources()
        # Open with own parser to get the keys for gemmi?
        # add the cif_od data only if there is no value in the main cif?
        # compare unit cell. it should be the same

    def open_cif(self):
        try:
            self.doc = gemmi.cif.read_file(str(self.fileobj.absolute()))
            self.block = self.doc.sole_block()
        except Exception as e:
            print('Unable to read file:', e)
            raise

    def __getitem__(self, item):
        result = self.block.find_value(item)
        return result if result else ''

    def get_sources(self):

        keys = ['_audit_creation_method',
                '_computing_data_collection',
                '_computing_cell_refinement',
                '_computing_data_reduction',
                '_cell_length_a',
                '_cell_length_b',
                '_cell_length_c',
                '_cell_angle_alpha',
                '_cell_angle_beta',
                '_cell_angle_gamma',
                '_cell_measurement_temperature',
                '_cell_measurement_reflns_used',
                '_cell_measurement_theta_min',
                '_cell_measurement_theta_max',
                '_exptl_crystal_size_max',
                '_exptl_crystal_size_mid',
                '_exptl_crystal_size_min',
                '_exptl_absorpt_coefficient_mu',
                '_exptl_absorpt_correction_T_min',
                '_exptl_absorpt_correction_T_max',
                '_exptl_absorpt_correction_type',
                '_exptl_absorpt_process_details',
                '_diffrn_ambient_temperature',
                '_diffrn_ambient_environment',
                '_diffrn_source',
                '_diffrn_source_type',
                '_diffrn_radiation_probe',
                '_diffrn_radiation_type',
                '_diffrn_radiation_wavelength',
                '_diffrn_radiation_monochromator',
                '_diffrn_measurement_device',
                '_diffrn_measurement_device_type',
                '_diffrn_detector',
                '_diffrn_detector_type',
                '_diffrn_detector_area_resol_mean',
                '_diffrn_reflns_number',
                '_diffrn_reflns_av_R_equivalents',
                '_diffrn_reflns_av_sigmaI/netI',
                '_diffrn_reflns_theta_min',
                '_diffrn_reflns_theta_max',
                '_diffrn_measured_fraction_theta_max',
                '_diffrn_reflns_theta_full',
                '_diffrn_measured_fraction_theta_full',
                '_diffrn_orient_matrix_type',
                '_diffrn_orient_matrix_UB_11',
                '_diffrn_orient_matrix_UB_12',
                '_diffrn_orient_matrix_UB_13',
                '_diffrn_orient_matrix_UB_21',
                '_diffrn_orient_matrix_UB_22',
                '_diffrn_orient_matrix_UB_23',
                '_diffrn_orient_matrix_UB_31',
                '_diffrn_orient_matrix_UB_32',
                '_diffrn_orient_matrix_UB_33',
                '_diffrn_measurement_details',
                '_diffrn_measurement_method',
                '_diffrn_oxdiff_ac3_digest_frames',
                '_diffrn_oxdiff_ac3_digest_hkl',
                '_space_group_IT_number',
                '_space_group_crystal_system',
                '_space_group_name_H-M_alt',
                '',
                '',
                '',
                ]
        for k in keys:
            self.sources[k] = (self[k], self.fileobj.name)
