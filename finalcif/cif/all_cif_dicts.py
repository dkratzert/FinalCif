"""
This file combines all major CIF dictionarys in order to check for the validity of CIF keys
and to display help texts.
"""

from finalcif.cif.core_dict import cif_core
from finalcif.cif.modulation_dict import modulation_dict
from finalcif.cif.powder_dict import powder_dict
from finalcif.cif.restraints_dict import restraints_dict
from finalcif.cif.twin_dict import twinning_dict

additional_keywords = {
    '_exptl_absorpt_special_details'          : '<pre><h2>_exptl_absorpt_special_details</h2>'
                                                "Details of the absorption correction process applied to the"
                                                "measured intensities that cannot otherwise be given using"
                                                "other data items from the EXPTL_ABSORBT category."
                                                '</pre>'
                                                '<br><p><h4>Type:</h4> Text</p>\n',
    '_shelx_estimated_absorpt_T_max'          : '<pre><h2>_shelx_estimated_absorpt_T_max</h2>'
                                                'The maximum and minimum transmission factors estimatedby SHELXL.</pre>'
                                                '<br><p><h4>Type:</h4> number (int or float)</p>\n'
                                                '<br><p><h4>Limits:</h4> 0.0:1.0 </p>',
    '_shelx_estimated_absorpt_T_min'          : '<pre><h2>_shelx_estimated_absorpt_T_min</h2>'
                                                'The maximum and minimum transmission factors estimatedby SHELXL.</pre>'
                                                '<br><p><h4>Type:</h4> number (int or float)</p>\n'
                                                '<br><p><h4>Limits:</h4> 0.0:1.0 </p>',
    '_shelx_hkl_file'                         : '<pre><h2>_shelx_hkl_file</h2>'
                                                'HKL file used to refine the model in SHELXL. Do not '
                                                'edit this value!</pre>'
                                                '<br><p><h4>Type:</h4> string</p>\n',
    '_shelx_res_file'                         : '<pre><h2>_shelx_res_file</h2>'
                                                'Results file used to refine the model in SHELXL. Do not '
                                                'edit this value!</pre>'
                                                '<br><p><h4>Type:</h4> string</p>\n',
    '_shelx_hkl_checksum'                     : '<pre><h2>_shelx_hkl_checksum</h2>'
                                                'Checksum used to ensure the consistency of refinement model '
                                                'with the hkl data attached to the CIF.</pre>'
                                                '<br><p><h4>Type:</h4> integer number</p>\n',
    '_shelx_res_checksum'                     : '<pre><h2>_shelx_res_checksum</h2>'
                                                'Checksum used to ensure the consistency of refinement model '
                                                'with the results file attached to the CIF.</pre>'
                                                '<br><p><h4>Type:</h4> integer number</p>\n',
    '_olex2_diffrn_ambient_temperature_device': '<pre>Device to cool the '
                                                'crystal during measurement</pre>'
                                                '<h3>Example:</h3>\n'
                                                'Oxford Cryostream 800'
                                                '<br><p><h4>Type:</h4> string</p>',
    '_diffrn_measurement_ambient_'
    'temperature_device_make'                 : '<pre><h2>_diffrn_measurement_ambient_temperature_device_make</h2>'
                                                'Device model used to cool the crystal during the '
                                                'diffraction experiment,</pre>'
                                                '<h3>Example:</h3>\n'
                                                'Oxford Cryostream 800'
                                                '<br><p><h4>Type:</h4> string</p>',
    '_bruker_diffrn_'
    'measurement_temperature_device'          : '<pre><h2>_bruker_diffrn_measurement_temperature_device</h2>'
                                                'Device model used to cool the crystal during the '
                                                'diffraction experiment.</pre>'
                                                '<h3>Example:</h3>\n'
                                                'Oxford Cryostream 800'
                                                '<br><p><h4>Type:</h4> string</p>',
    '_diffrn_measurement_'
    'bruker_total_exposure_time'              : '<pre><h2>_diffrn_measurement_bruker_total_exposure_time</h2>'
                                                'Total X-ray exposure time of the crystal during data '
                                                'collection (seconds).</pre>'
                                                '<br><p><h4>Type:</h4> number (int or float)</p>',
    '_computing_bruker_data_scaling'          : '<pre><h2>_computing_bruker_data_scaling</h2>'
                                                'Program used to scale and correct the data for absorption.</pre>'
                                                '<br><p><h4>Type:</h4> Text</p>\n',
    '_diffrn_reflns_bruker_av_norm_I'         : '<pre><h2>_diffrn_reflns_bruker_av_norm_I</h2>'
                                                'Average normalized (to 1 min/deg) intensity.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_diffrn_reflns_bruker_twinabs_number'    : '<pre><h2>_diffrn_reflns_bruker_twinabs_number</h2>'
                                                'Total number of measured intensities as counted by TWINABS.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_nr'                 : '<pre><h2>_platon_squeeze_void_nr</h2>'
                                                'Sequential number for the voids where SQUEEZE found electron desnity.</pre>'
                                                '<br><p><h4>Type:</h4> number (int)</p>\n',
    '_platon_squeeze_void_average_x'          : '<pre><h2>_platon_squeeze_void_average_x</h2>'
                                                'x-position of the void.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_average_y'          : '<pre><h2>_platon_squeeze_void_average_y</h2>'
                                                'y-position of the void.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_average_z'          : '<pre><h2>_platon_squeeze_void_average_z</h2>'
                                                'z-position of the void.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_volume'             : '<pre><h2>_platon_squeeze_void_volume</h2>'
                                                'Volume of the respective solvent mask void.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_count_electrons'    : '<pre><h2>_platon_squeeze_void_count_electrons</h2>'
                                                'Number of electrons representing the molecular content of the void.</pre>'
                                                '<br><p><h4>Type:</h4> number (float)</p>\n',
    '_platon_squeeze_void_content'            : '<pre><h2>_platon_squeeze_void_content</h2>'
                                                'Formula that describes the content of the void as close as possible.'
                                                'The _chemical_formula_sum should not contain the SQUEEZEd atoms.</pre>'
                                                '<br><p><h4>Type:</h4> string </p>\n',
    '_platon_squeeze_void_probe_radius'       : '<pre><h2>_platon_squeeze_void_probe_radius</h2>'
                                                'Probe radius used to determine the void volume.</pre>'
                                                '<br><p><h4>Type:</h4> number (float) </p>\n',
    '_platon_squeeze_details'                 : '<pre><h2>_platon_squeeze_details</h2>'
                                                'Detailed description of the SQUEEZE process and the reasons why it '
                                                'was chosen over an atomistic (disorder) model.</pre>'
                                                '<h3>Example:</h3>\n'
                                                'The O(CH2CH3)2 solvent molecule (42 electrons) disordred around '
                                                'an inverstion center was treated by SQUEEZE. '
                                                '<br><p><h4>Type:</h4> string </p>\n',
    '_exptl_bruker_absorpt_correction_T_ratio': '<pre><h2>_exptl_bruker_absorpt_correction_T_ratio</h2>'
                                                'SADABS (and other scaling programs) can only determine the RATIO of '
                                                'absorpt_correction_Tmin/Tmax, so this value determined by SHELXL is used to '
                                                'scale the transmission values from SADABS.</pre>'
                                                '<br><p><h4>Type:</h4> number (float) </p>\n',
}

cif_all_dict = {}

cif_all_dict.update(cif_core)
cif_all_dict.update(twinning_dict)
cif_all_dict.update(modulation_dict)
cif_all_dict.update(powder_dict)
cif_all_dict.update(restraints_dict)
cif_all_dict.update(additional_keywords)
