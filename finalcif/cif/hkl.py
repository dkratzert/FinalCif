from __future__ import annotations

import re
from collections import namedtuple
from collections.abc import Sequence
from pathlib import Path

import gemmi
import numpy as np
from gemmi.cif import Loop, Document, Style
from packaging import version

Limit = namedtuple('Limit', 'h_max, h_min, k_max, k_min, l_max, l_min')


class HKL:
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
        self._add_hkl_as_loop()

    @property
    def hkl_as_cif(self) -> str:
        if version.parse(gemmi.__version__) < version.parse('0.5.1'):
            return self._doc.as_string(style=Style.Simple)
        else:
            return self._doc.as_string(options=gemmi.cif.WriteOptions(Style.Simple))

    def _add_hkl_as_loop(self) -> None:
        """
        Adds the hkl data from a SHELX hkl file as local loop.
        """
        hkl_width = self._get_hkl_width()
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
                # Need to truncate, because some programs add the scale group even if
                # there is no scale group in other reflections
                loop.add_row(splitline[:hkl_width])
                break
            try:
                loop.add_row(splitline[:len(loop_header)])
            # RuntimeError ist from gemmi.cif.add_row:
            except (IndexError, RuntimeError):
                continue

    def __repr__(self) -> str:
        return self.hkl_as_cif[:250]

    def _trim_header_to_hkl_width(self, loop_header: list[str]) -> list[str]:
        hkl_with = self._get_hkl_width()
        trimmed_header = loop_header[:hkl_with]
        return trimmed_header

    def _get_hkl_width(self) -> int:
        first_lines = self._hkl_file[:150].strip().splitlines(keepends=False)
        if len(first_lines) > 1:
            return len(first_lines[1].split())
        return len(first_lines[0].split())

    def get_hkl_min_max(self) -> Limit:
        hkl: gemmi.ReflnBlock = gemmi.hkl_cif_as_refln_block(self.block)
        miller = hkl.make_miller_array()
        h_max, k_max, l_max = np.max(miller, axis=0)
        h_min, k_min, l_min = np.min(miller, axis=0)
        return Limit(h_max=h_max, h_min=h_min, k_max=k_max, k_min=k_min, l_max=l_max, l_min=l_min)


def calculate_rint(hkl_file: str, space_group: str, cell: Sequence[float] | None = None,
                   resolution: tuple[float, float] | None = None) -> float | None:
    """
    R(int) of an unmerged SHELX HKLF 4 file, calculated the way SHELXL does it:

        R(int) = sum|Fo^2 - Fo^2(mean)| / sum[Fo^2]

    Systematically absent reflections are rejected and Friedel opposites are only merged in
    centrosymmetric space groups. Fo^2(mean) is the mean weighted with 1/sigma^2.

    SADABS writes no overall R(int) into its listing file, only the wR2(int) of the parameter
    refinement and the R(int) values of the individual runs.

    Args:
        hkl_file: Content of a SHELX HKLF 4 file.
        space_group: Space group name, e.g. 'P n a 21'.
        cell: Unit cell parameters, needed to apply a resolution limit.
        resolution: Lowest and highest resolution in Angstrom (a SHELX SHEL instruction).
    """
    miller, intensities, sigmas = _reflections_from_shelx_hkl(hkl_file)
    if not len(miller) or not space_group:
        return None
    try:
        operations = gemmi.SpaceGroup(space_group).operations()
    except (RuntimeError, ValueError):
        return None
    used = ~_systematically_absent(miller, operations)
    used &= _within_resolution(miller, cell, resolution)
    miller, intensities, sigmas = miller[used], intensities[used], sigmas[used]
    if not len(miller):
        return None
    groups, counts = _group_equivalents(miller, operations)
    if len(counts) >= len(miller):
        # Merged data have no equivalent reflections to compare:
        return None
    return _rint_of_groups(groups, counts, intensities, sigmas)


def _within_resolution(miller: np.ndarray, cell: Sequence[float] | None,
                       resolution: tuple[float, float] | None) -> np.ndarray:
    """
    Applies the resolution limits of a SHELX SHEL instruction.
    """
    if not resolution or not cell:
        return np.ones(len(miller), dtype=bool)
    lowest, highest = max(resolution), min(resolution)
    try:
        spacing = gemmi.UnitCell(*cell[:6]).calculate_d_array(miller)
    except (RuntimeError, TypeError, ValueError):
        return np.ones(len(miller), dtype=bool)
    return (spacing <= lowest) & (spacing >= highest)


def _rint_of_groups(groups: np.ndarray, counts: np.ndarray, intensities: np.ndarray,
                    sigmas: np.ndarray) -> float | None:
    weights = np.where(sigmas > 0.0, 1.0 / np.square(np.where(sigmas > 0.0, sigmas, 1.0)), 1.0)
    weight_sum = np.bincount(groups, weights=weights, minlength=len(counts))
    mean = np.bincount(groups, weights=weights * intensities, minlength=len(counts)) / weight_sum
    with_equivalents = counts[groups] > 1
    numerator = np.abs(intensities - mean[groups])[with_equivalents].sum()
    denominator = intensities[with_equivalents].sum()
    if not denominator:
        return None
    return round(float(numerator / denominator), 4)


def _group_equivalents(miller: np.ndarray, operations: gemmi.GroupOps) -> tuple[np.ndarray, np.ndarray]:
    """
    Assigns a group number to every reflection that is symmetry equivalent to another one.
    """
    equivalents = [_encode(miller @ _rotation(op)) for op in operations.sym_ops]
    if operations.is_centrosymmetric():
        equivalents += [_encode(-(miller @ _rotation(op))) for op in operations.sym_ops]
    representative = np.max(np.stack(equivalents), axis=0)
    _, groups, counts = np.unique(representative, return_inverse=True, return_counts=True)
    return groups, counts


def _systematically_absent(miller: np.ndarray, operations: gemmi.GroupOps) -> np.ndarray:
    absent = np.zeros(len(miller), dtype=bool)
    for op in operations.sym_ops:
        translation = np.array(op.tran, dtype=np.float64) / op.DEN
        if not translation.any():
            continue
        unchanged = (miller @ _rotation(op) == miller).all(axis=1)
        phase = miller @ translation
        absent |= unchanged & (np.abs(phase - np.round(phase)) > 1e-6)
    for centering in operations.cen_ops:
        translation = np.array(centering, dtype=np.float64) / gemmi.Op.DEN
        if not translation.any():
            continue
        phase = miller @ translation
        absent |= np.abs(phase - np.round(phase)) > 1e-6
    return absent


def _rotation(op: gemmi.Op) -> np.ndarray:
    """The rotation part of a symmetry operation, applicable as ``miller @ rotation``."""
    return np.array(op.rot, dtype=np.int64) // op.DEN


def _encode(miller: np.ndarray) -> np.ndarray:
    """Packs Miller indices into single numbers that keep their lexicographic order."""
    shifted = miller.astype(np.int64) + 2 ** 20
    return (shifted[:, 0] << 42) | (shifted[:, 1] << 21) | shifted[:, 2]


def _reflections_from_shelx_hkl(hkl_file: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    miller, intensities, sigmas = [], [], []
    for line in hkl_file.splitlines(keepends=False):
        if len(line) < 28:
            continue
        try:
            index = (int(line[0:4]), int(line[4:8]), int(line[8:12]))
            if not any(index):
                break
            intensity, sigma = float(line[12:20]), float(line[20:28])
        except ValueError:
            continue
        miller.append(index)
        intensities.append(intensity)
        sigmas.append(sigma)
    return (np.array(miller, dtype=np.int32).reshape(-1, 3),
            np.array(intensities, dtype=np.float64),
            np.array(sigmas, dtype=np.float64))


if __name__ == '__main__':
    h = HKL(Path('tests/examples/work/test_hkl_file.txt').read_text(), '123234')
    # print(h.hkl_as_cif[:250])
    m = h.get_hkl_min_max()
    print(m)
