from builtins import str

from cif.file_reader import CifContainer


class ReportText():
    def __init__(self):
        pass


class CrstalSelection():
    def __init__(self, cif: CifContainer):
        self.temp = temp
        self._names = names
        self.txt = "The data for {} were collected from shock-cooled crystals at {} K".format(self.names, temp)

    @property
    def names(self) -> str:
        return ', '.join(self._names)
