from pathlib import Path

from cif import file_parser


class CifContainer():
    """
    This class holds the content of a cif file, independent of the file parser used.
    """

    def __init__(self):
        self.cif_dict = None

    def open_cif_with_gemmi(self, filename: Path):
        """
        Reads a CIF file into gemmi and returns a sole block.
        """
        import gemmi as gemmi
        doc = gemmi.cif.read_file(filename.absolute())
        return doc

    def open_cif_with_fileparser(self, filename: Path):
        """
        """
        c = file_parser.Cif()

    def __getitem__(self, item):
        return self.cif[item] if self.cif[item] else ''
