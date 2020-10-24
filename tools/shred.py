from pathlib import Path

from cif.cif_file_io import CifContainer
from gui.dialogs import show_general_warning
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.misc import strip_finalcif_of_name


class ShredCIF():
    """
    This class extracts the .res and .hkl file content from a cif file.
    """

    def __init__(self, cif: CifContainer, ui: Ui_FinalCifWindow):
        self.cif = cif
        self.ui = ui
        self.final_cif_file_name = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.cif')

    def shred_cif(self) -> None:
        """
        Saves res and hkl file from the cif.
        """
        self.ui.statusBar.showMessage('')
        resfile_path = Path(self.final_cif_file_name.stem + '.res')
        hklfile_path = Path(self.final_cif_file_name.stem + '.hkl')
        res_data = None
        hkl_data = None
        if not self.cif:
            return
        if not any([self.cif.res_file_data, self.cif.hkl_file]):
            self.ui.statusBar.showMessage('No .res and .hkl file data found!')
            return
        if self.cif.res_file_data:
            res_data = self.cif.res_file_data.splitlines(keepends=True)
        if self.cif.hkl_file:
            hkl_data = self.cif.hkl_file.splitlines(keepends=True)
        if not self.data_is_valid(res_data):
            self.ui.statusBar.showMessage('No .res file data found!')
        else:
            res_data = res_data[1:-1]  # first and last char is a semicolon
            if not self.write_res_file(resfile_path, res_data):
                return None
        if not self.data_is_valid(hkl_data):
            self.ui.statusBar.showMessage('No .hkl file data found!')
        else:
            hkl_data = self.format_hkl_data(hkl_data)
            if not self.write_hkl_file(hklfile_path, hkl_data):
                return None
        self.show_info(resfile_path, hklfile_path, res_data, hkl_data)

    @staticmethod
    def format_hkl_data(hkl_data: list) -> list:
        hkl_data = hkl_data[1:-1]
        for num, line in enumerate(hkl_data):
            if line[:1] == ')':
                hkl_data[num] = ';' + line[1:]
        return hkl_data

    def show_info(self, resname: Path, hklname: Path, resdata: list, hkldata: list) -> None:
        if resdata and not hkldata:
            self.ui.statusBar.showMessage(
                self.ui.statusBar.currentMessage() + '\nFinished writing data to {}.'.format(resname))
        if hkldata and not resdata:
            self.ui.statusBar.showMessage(
                self.ui.statusBar.currentMessage() + '\nFinished writing data to {}.'.format(hklname))
        if hkldata and resdata:
            self.ui.statusBar.showMessage(
                self.ui.statusBar.currentMessage() + '\nFinished writing data to {} \nand {}.'.format(resname, hklname))

    @staticmethod
    def data_is_valid(data: list) -> bool:
        if not data or len(data) < 3:
            return False
        else:
            return True

    @staticmethod
    def write_hkl_file(hklfile: Path, hkl: list) -> bool:
        try:
            with open(hklfile, mode='w', newline='\n') as f:
                for line in hkl:
                    f.write(line)
        except Exception as e:
            print(e)
            show_general_warning('Unable to write files: ' + str(e))
            return False
        return True

    def check_hkl_res_files(self):
        """
        Check whether hkl and/or res file content is included in the cif file.
        """
        if not self.cif.res_file_data:
            self.ui.statusBar.showMessage('No .res file data found!')
        if not self.cif.hkl_file:
            self.ui.statusBar.showMessage(self.ui.statusBar.currentMessage() + '\nNo .hkl file data found!')
        if not any([self.cif.res_file_data, self.cif.hkl_file]):
            self.ui.statusBar.showMessage('No .res and .hkl file data found!')
            self.ui.ShredCifButton.setDisabled(True)
        else:
            self.ui.ShredCifButton.setEnabled(True)

    @staticmethod
    def write_res_file(resfile: Path, reslines: list) -> bool:
        """
        Writes a res file from the cif content.
        """
        try:
            with open(resfile, mode='w', newline='\n') as f:
                for line in reslines:
                    f.write(line)
            return True
        except Exception as e:
            print(e)
            show_general_warning('Unable to write files: ' + str(e))
            return False