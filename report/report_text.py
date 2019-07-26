from builtins import str

from docx.document import Document
from docx.text import run
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from cif.file_reader import CifContainer


class FormatMixin():

    def bold(self, run: Run):
        return run.font.bold = True


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
    def __init__(self, cif: CifContainer, paragraph = Paragraph):
        self.cif = cif
        sentence = "The data were collected on a Bruker APEXII QUAZAR with an Incoatec microfocus source with mirror " \
                   "optics as monochromator. The diffrac¬tometer were equipped with an Oxford Cryosystems 800 low " \
                   "temperature device1 and used MoK radiation, λ = 0.71073 Å."
        self.txt = sentence.format()

