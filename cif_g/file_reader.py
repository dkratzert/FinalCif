from pathlib import Path

from gemmi import cif

def open_cif_file(filename: Path):
    """
    Raads a CIF file into gemmi and returns a sole block.
    """
    doc = cif.read_file(filename.absolute())
    return doc
