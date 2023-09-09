from pathlib import Path
from typing import Union

import gemmi.cif
from gemmi import cif

from finalcif.gui.dialogs import show_general_warning


def read_document_from_cif_file(filename: str) -> Union[gemmi.cif.Document, None]:
    doc: Union[gemmi.cif.Document, None] = None
    try:
        doc = cif.read_file(filename)
    except (RuntimeError, ValueError) as e:
        warning = "{}\n{}".format('This CIF is invalid:', str(e))
        if 'data_' in str(e):
            warning =  f"{warning}\n\nA CIF needs to start with 'data_[some_name]'."
        show_general_warning(warning)
    except IOError as e:
        show_general_warning(f'Unable to open file {filename}:\n{str(e)}')
    return doc