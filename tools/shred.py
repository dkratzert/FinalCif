from pathlib import Path
from typing import Union

from cif.cif_file_io import CifContainer
from gui.dialogs import show_general_warning
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.misc import strip_finalcif_of_name
from tools.statusbar import StatusBar


class ShredCIF():
    """
    This class extracts the .res and .hkl file content from a cif file.
    """

    def __init__(self, cif: CifContainer, ui: Union[Ui_FinalCifWindow, None]):
        self._cif = cif
        self._statusbar = StatusBar(ui)
        self._final_cif_file_name = Path(strip_finalcif_of_name(str(self._cif.fileobj.stem)) + '-finalcif.cif')

    def shred_cif(self) -> None:
        """
        Saves res and hkl file from the cif.
        """
        self._statusbar.show_message('')
        resfile_path = Path(self._final_cif_file_name.stem + '.res')
        hklfile_path = Path(self._final_cif_file_name.stem + '.hkl')
        res_data = None
        hkl_data = None
        if not self._cif:
            return
        if not any([self._cif.res_file_data, self._cif.hkl_file]):
            self._statusbar.show_message('No .res and .hkl file data found!')
            return
        if self._cif.res_file_data:
            res_data = self._cif.res_file_data.splitlines(keepends=True)
        if self._cif.hkl_file:
            hkl_data = self._cif.hkl_file.splitlines(keepends=True)
        if not self._data_is_valid(res_data):
            self._statusbar.show_message('No .res file data found!')
        else:
            res_data = res_data[1:-1]  # first and last char is a semicolon
            if not self._write_res_file(resfile_path, res_data):
                return None
        if not self._data_is_valid(hkl_data):
            self._statusbar.show_message('No .hkl file data found!')
        else:
            hkl_data = self.format_hkl_data(hkl_data)
            if not self._write_hkl_file(hklfile_path, hkl_data):
                return None
        self._show_info(resfile_path, hklfile_path, res_data, hkl_data)

    @staticmethod
    def format_hkl_data(hkl_data: list) -> list:
        for num, line in enumerate(hkl_data):
            if line[:1] == ')':
                hkl_data[num] = ';' + line[1:]
        return hkl_data

    def _show_info(self, resname: Path, hklname: Path, resdata: list, hkldata: list) -> None:
        if resdata and not hkldata:
            self._statusbar.show_message(
                self._statusbar.current_message + '\nFinished writing data to {}.'.format(resname))
        if hkldata and not resdata:
            self._statusbar.show_message(
                self._statusbar.current_message + '\nFinished writing data to {}.'.format(hklname))
        if hkldata and resdata:
            self._statusbar.show_message(
                self._statusbar.current_message + '\nFinished writing data to {} \nand {}.'.format(resname, hklname))

    @staticmethod
    def _data_is_valid(data: list) -> bool:
        if not data or len(data) < 3:
            return False
        else:
            return True

    @staticmethod
    def _write_hkl_file(hklfile: Path, hkl: list) -> bool:
        try:
            with open(hklfile, mode='w', newline='\n') as f:
                for line in hkl:
                    f.write(line)
        except Exception as e:
            print(e)
            show_general_warning('Unable to write files: ' + str(e))
            return False
        return True

    def cif_has_hkl_or_res_file(self) -> bool:
        """
        Check whether hkl and/or res file content is included in the cif file.
        """
        if not self._cif.res_file_data:
            self._statusbar.show_message('No .res file data found!')
        if not self._cif.hkl_file:
            self._statusbar.show_message(self._statusbar.current_message + '\nNo .hkl file data found!')
        if not any([self._cif.res_file_data, self._cif.hkl_file]):
            self._statusbar.show_message('No .res and .hkl file data found!')
            return False
        else:
            return True

    @staticmethod
    def _write_res_file(resfile: Path, reslines: list) -> bool:
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
