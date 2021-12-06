"""
This file combines all major CIF dictionarys in order to check for the validity of CIF keys
and to display help texts.
"""

from cif.core_dict import cif_core
from cif.modulation_dict import modulation_dict
from cif.powder_dict import powder_dict
from cif.restraints_dict import restraints_dict
from cif.twin_dict import twinning_dict

additional_keywords = {
    '_olex2_diffrn_ambient_temperature_device'           : 'Not an official cif keyword.\nDevice to cool the crystal during measurement',
    '_diffrn_measurement_ambient_temperature_device_make': 'Will become an official cif keyword.\nDevice to cool the crystal during measurement',
}

cif_all_dict = {}

cif_all_dict.update(cif_core)
cif_all_dict.update(twinning_dict)
cif_all_dict.update(modulation_dict)
cif_all_dict.update(powder_dict)
cif_all_dict.update(restraints_dict)
cif_all_dict.update(additional_keywords)
