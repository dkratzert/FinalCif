from pathlib import Path
from typing import Union
from unittest.mock import Mock

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.dialogs import show_general_warning
from finalcif.tools.statusbar import StatusBar


class ShredCIF:
    """
    This class extracts the .res and .hkl file content from a cif file.
    """

    def __init__(self, cif: CifContainer, statusbar: StatusBar | None):
        self._cif = cif
        self._statusbar = statusbar or Mock()

    def shred_cif(self) -> None:
        """
        Saves res and hkl file from the cif.
        """
        self._statusbar.show_message('')
        if self._cif.is_multi_cif:
            resfile_path = self._cif.finalcif_file_prefixed(prefix='',
                                                            suffix='_' + self._cif.block.name + '-finalcif.res')
            hklfile_path = self._cif.finalcif_file_prefixed(prefix='',
                                                            suffix='_' + self._cif.block.name + '-finalcif.hkl')
            fabfile_path = self._cif.finalcif_file_prefixed(prefix='',
                                                            suffix='_' + self._cif.block.name + '-finalcif.fab')
        else:
            resfile_path = self._cif.finalcif_file.with_suffix('.res')
            hklfile_path = self._cif.finalcif_file.with_suffix('.hkl')
            fabfile_path = self._cif.finalcif_file.with_suffix('.fab')
        res_data = None
        hkl_data = None
        if not self._cif:
            return
        if not any([self._cif.res_file_data, self._cif.hkl_file]):
            self._statusbar.show_message('No .res and .hkl file data found!')
            return
        if self._cif.res_file_data:
            res_data = self._cif.res_file_data
        if self._cif.hkl_file:
            hkl_data = self._cif.hkl_file
        if not self._data_is_valid(res_data):
            self._statusbar.show_message('No .res file data found!')
        elif not self._write_res_file(resfile_path, res_data):
            return None
        if not self._data_is_valid(hkl_data):
            self._statusbar.show_message('No .hkl file data found!')
        else:
            hkl_data = self.format_hkl_data(hkl_data)
            if not self._write_hkl_file(hklfile_path, hkl_data):
                return None
        if fab_data := self._cif.fab_file:
            self._write_hkl_file(fabfile_path, fab_data)
        self._show_info(resfile_path, hklfile_path, res_data, hkl_data)

    @staticmethod
    def format_hkl_data(hkl_data: str) -> str:
        """
        Replaces ')' characters at the start of lines in the hkl file (after the 0 0 0 reflection)
        with ';' characters. The round brackets are placed there by SADABS, because a semicolon
        would interfere with the CIF syntax.
        """
        lines = []
        for line in hkl_data.splitlines(keepends=False):
            if line.startswith(')'):
                line = ';' + line[1:]
            lines.append(line)
        return '\n'.join(lines).lstrip('\n')

    def _show_info(self, resname: Path, hklname: Path, resdata: str | None, hkldata: str | None) -> None:
        if resdata and not hkldata:
            self._statusbar.show_message(f'{self._statusbar.current_message}\nFinished writing data to {resname.name}.')
        if hkldata and not resdata:
            self._statusbar.show_message(f'{self._statusbar.current_message}\nFinished writing data to {hklname.name}.')
        if hkldata and resdata:
            self._statusbar.show_message(
                f'{self._statusbar.current_message}\nFinished writing data to {resname.name} and {hklname.name}.')

    @staticmethod
    def _data_is_valid(data: str | None) -> bool:
        if not data or len(data.splitlines(keepends=False)) < 3:
            return False
        else:
            return True

    @staticmethod
    def _write_hkl_file(hklfile: Path, hkl: str | None) -> bool:
        try:
            hklfile.write_text(hkl, encoding='latin1', errors='ignore')
        except Exception as e:
            print(e)
            show_general_warning(parent=None, warn_text='Unable to write files: ' + str(e))
            return False
        return True

    def cif_has_hkl_or_res_file(self) -> bool:
        """
        Check whether hkl and/or res file content is included in the cif file.
        """
        if not self._cif.res_file_data:
            self._statusbar.show_message('No .res file data found!')
        if not self._cif.hkl_file and isinstance(self._statusbar.current_message, str):
            self._statusbar.show_message(self._statusbar.current_message + '\nNo .hkl file data found!')
        if not any([self._cif.res_file_data, self._cif.hkl_file]):
            self._statusbar.show_message('No .res and .hkl file data found!')
            return False
        else:
            return True

    @staticmethod
    def _write_res_file(resfile: Path, reslines: str | None) -> bool:
        """
        Writes a res file from the cif content.
        """
        try:
            resfile.write_text(reslines, encoding='latin1', errors='ignore', newline='\n')
        except Exception as e:
            print(e)
            show_general_warning(parent=None, warn_text='Unable to write files: ' + str(e))
            return False
        return True
