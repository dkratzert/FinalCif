import gemmi.cif
from gemmi import cif

from finalcif.gui.dialogs import show_general_warning


def read_document_from_cif_file(filename: str) -> gemmi.cif.Document | None:
    doc: gemmi.cif.Document | None = None
    try:
        doc = cif.read_file(filename)
    except (RuntimeError, ValueError) as e:
        warning = "{}\n{}".format('This CIF is invalid:', str(e))
        if 'data_' in str(e):
            warning = f"{warning}\n\nA CIF needs to start with 'data_[some_name]'."
        show_general_warning(parent=None, warn_text=warning)
    except OSError as e:
        show_general_warning(parent=None, warn_text=f'Unable to open file {filename}:\n{e!s}')
    return doc
