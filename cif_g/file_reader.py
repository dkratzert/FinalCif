from pathlib import Path


def open_cif_file(filename: Path):
    """
    Raads a CIF file into gemmi and returns a sole block.
    """
    doc = gemmi.cif.read_file(filename.absolute())
    return doc


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, cif):
        self.cif = None

    def _get_cif_data_from_gemmi(self):
        pass

    def _get_cif_data_from_cifdk(self):
        pass

    def __getitem__(self, item):
        return self.cif[item] if self.cif[item] else ''
