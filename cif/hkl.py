import re
from pathlib import Path

import gemmi
from gemmi.cif import Loop, Document, Style


class HKL():
    """
    loop_
      _refln_index_h
      _refln_index_k
      _refln_index_l
      _refln_F_squared_meas
      _refln_F_squared_sigma
      _refln_scale_group_code
    """

    def __init__(self, hkl_file: str, block_name: str, hklf_type: int = 4):
        self._hkl_file = hkl_file
        self.hklf_type = hklf_type
        self._doc: Document = gemmi.cif.Document()
        self._doc.add_new_block(block_name)
        self.block = self._doc.sole_block()

    @property
    def hkl_as_cif(self) -> str:
        loop_header = ['index_h',
                       'index_k',
                       'index_l',
                       'F_squared_meas' if self.hklf_type != 3 else 'F_meas',
                       'F_squared_sigma' if self.hklf_type != 3 else 'F_sigma',
                       'scale_group_code']
        loop: Loop = self.block.init_loop('_refln_', self._trim_header_to_hkl_width(loop_header))
        zero_reflection_pattern = re.compile(r'^\s+0\s+0\s+0\s+0.*')
        for line in self._hkl_file.splitlines(keepends=False):
            splitline = line.split()
            if not splitline:
                continue
            # Do not use data after the 0 0 0 reflection
            if zero_reflection_pattern.match(line):
                loop.add_row(splitline)
                break
            try:
                loop.add_row(splitline[:len(loop_header)])
            # RuntimeError ist from gemmi.cif.add_row:
            except (IndexError, RuntimeError):
                continue
        return self._doc.as_string(style=Style.Simple)

    def __repr__(self) -> str:
        return self.hkl_as_cif[:250]

    def _trim_header_to_hkl_width(self, loop_header):
        hkl_with = self._get_hkl_with()
        trimmed_header = loop_header[:hkl_with]
        return trimmed_header

    def _get_hkl_with(self) -> int:
        first_lines = self._hkl_file[:150].strip().splitlines(keepends=False)
        if len(first_lines) > 1:
            return len(first_lines[1].split())
        return len(first_lines[0].split())


if __name__ == '__main__':
    h = HKL(Path('tests/examples/test.hkl').read_text(), '123234')
    as_cif = h.hkl_as_cif
    print(as_cif[:250])

