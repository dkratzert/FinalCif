def unify_line_endings(text: str):
    return '\n'.join(text.splitlines())


export_templ_data = ['data_D8__VENTURE',
                     "_diffrn_radiation_monochromator   'mirror optics'",
                     "_diffrn_measurement_device        'three-circle diffractometer'",
                     "_diffrn_measurement_device_type   'Bruker D8 VENTURE dual wavelength Mo/Cu'",
                     "_diffrn_measurement_method        '\\w and \\f scans'",
                     "_diffrn_source                    'microfocus sealed X-ray tube'",
                     '_diffrn_detector_area_resol_mean  7.41',
                     '_diffrn_detector                  CPAD',
                     "_diffrn_detector_type             'Bruker PHOTON III'",
                     "_diffrn_source_type               'Incoatec I\\ms'",
                     '_diffrn_radiation_probe           x-ray',
                     "_diffrn_measurement_specimen_support 'MiTeGen micromount'",
                     "_olex2_diffrn_ambient_temperature_device 'Oxford Cryostream 800'",
                     '_diffrn_ambient_environment       N~2~']
addr = """Albert-Ludwigs-Universität Freiburg
Institut für Anorganische und Analytische Chemie
Albertstraße 21
Freiburg i. Br.
79104
Germany"""
export_prop_data = r"""data_Molecular__Graphics
loop_
_computing_molecular_graphics
'Olex2 (Dolomanov et al., 2009)'
'ShelXle (Hu\"bschle 2011)'
'ORTEP Farrujia 2012'
'Bruker SHELXTL, XP (G. Sheldrick)'
'Mercury CSD, C. F. Macrae et al. 2008'
'PLATON (A.L.Spek, 2019)'
"""