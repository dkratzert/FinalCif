from builtins import str

import gemmi
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from cif.file_reader import CifContainer


class FormatMixin():

    def bold(self, run: Run):
        r = run.bold = True
        return r


class ReportText():
    def __init__(self):
        pass


class CrstalSelection(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        self.temp = self.cif['_diffrn_ambient_temperature']
        self._name = cif.fileobj.name
        method = 'shock-cooled '
        sentence = "The data for {} were collected from a {}single crystal at {}\u00A0K."
        if float(self.temp.split('(')[0]) > 200:
            method = ''
        self.txt = sentence.format(self.name, method, self.temp)
        paragraph.add_run(self.txt)

    @property
    def name(self) -> str:
        if self._name:
            return self._name
        else:
            return '?'


class MachineType():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        gstr = gemmi.cif.as_string
        self.difftype = gstr(self.cif.block.find_value('_diffrn_measurement_device_type'))
        self.device = gstr(self.cif['_diffrn_measurement_device'])
        self.source = gstr(self.cif['_diffrn_source'])
        self.monochrom = gstr(self.cif['_diffrn_radiation_monochromator'])
        if not self.monochrom:
            self.monochrom = '?'
        self.cooling = gstr(self.cif['_olex2_diffrn_ambient_temperature_device'])
        if not self.cooling:
            self.cooling = '?'
        self.rad_type = gstr(self.cif['_diffrn_radiation_type'])
        self.wavelen = gstr(self.cif['_diffrn_radiation_wavelength'])
        sentence = "The data were collected on a {} {} with an {} using {} as monochromator. " \
                   "The diffractometer were equipped with an {} low " \
                   "temperature device and used {} radiation, λ = {}\u00A0Å."
        self.txt = sentence.format(self.difftype, self.device, self.source, self.monochrom, self.cooling,
                                   self.rad_type, self.wavelen)
        paragraph.add_run(self.txt)
