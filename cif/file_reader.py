from pathlib import Path

from cif import file_parser


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self, filename: Path):
        self.cif_data = None
        self.filename = filename

    def open_cif_with_gemmi(self):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        import gemmi as gemmi
        doc = gemmi.cif.read_file(self.filename.absolute())
        return doc

    def open_cif_with_fileparser(self):
        """
        """
        self.cif_data = file_parser.Cif(self.filename.absolute())

    def __getitem__(self, item):
        return self.cif_data[item] if self.cif_data[item] else ''

    def atoms(self):
        return self.cif_data.atoms

    def cell(self):
        return self.cif_data.cell