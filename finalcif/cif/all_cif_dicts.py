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
    '_olex2_diffrn_ambient_temperature_device'           : '<pre>Device to cool the '
                                                           'crystal during measurement</pre>',
    '_diffrn_measurement_ambient_temperature_device_make': '<pre>Not an official CIF keyword, but eventually will '
                                                           'become one.\nDevice to '
                                                           'cool the crystal during measurement</pre>',
}

cif_all_dict = {}

cif_all_dict.update(cif_core)
cif_all_dict.update(twinning_dict)
cif_all_dict.update(modulation_dict)
cif_all_dict.update(powder_dict)
cif_all_dict.update(restraints_dict)
cif_all_dict.update(additional_keywords)
