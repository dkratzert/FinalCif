#!python
from __future__ import annotations

import dataclasses
#  Copyright (c)  2019 by Daniel Kratzert
import re
from pathlib import Path

from finalcif.datafiles.utils import get_file_to_parse
from finalcif.tools.misc import to_float, to_int


#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#

# Domain selections of a TWINABS output file:
DOMAIN_ALL = 'all'
DOMAIN_SINGLE = 'single'
DOMAIN_UP_TO = 'up_to'

# Reflection populations of the 'PART 2' statistics of a TWINABS output file:
STATS_SINGLES = 'singles'
STATS_COMPOSITES = 'composites'
STATS_ALL = 'all'


@dataclasses.dataclass
class ScanStatistics:
    """
    A 'PART 2 - Reject outliers and establish error model' statistics block of a TWINABS file:

     Statistics for singles of twin component  1
     -------------------------------------------

     Scan 2-theta  R(int)  Incid. factors  Diffr. factors    K     Total I>2sig(I)
        1  -30.0  0.0332   0.734 - 0.918   0.974 - 1.025   0.612    2283    1808
        ...
       All scans  0.0340   0.655 - 1.056   0.959 - 1.030   0.615   37875   30125

    Unlike the R(int) of the 'PART 3' extraction table, these values are the agreement of
    equivalent measured intensities and not a residual of the twin fraction refinement.
    """
    kind: str = STATS_ALL
    component: int | None = None
    rint: float | None = None
    total: int | None = None
    i_gt_2sigma: int | None = None

    def __repr__(self):
        name = f'{self.kind}({self.component})' if self.component else self.kind
        return f'{name}: R(int)={self.rint}, total={self.total}, I>2sigma={self.i_gt_2sigma}'


@dataclasses.dataclass
class Transmission:
    tmin: float | None = None
    tmax: float | None = None

    def __repr__(self):
        return f'min: {self.tmin}, max: {self.tmax}'


@dataclasses.dataclass
class ExtractionTable:
    """
    The reflection table of a TWINABS 'Unique HKLF 4 data extracted ...' section:

     Cycle   N(1) Rint(1)  N(all) Rint(all) Twin fractions
        1   20257  0.0742   32215  0.0699   0.7080  0.2920
    """
    domain_label: int | None = None
    n_domain: int | None = None
    rint_domain: float | None = None
    n_all: int | None = None
    rint_all: float | None = None
    # Domain selection of the extraction this table belongs to:
    mode: str = 'all'

    def __repr__(self):
        return (f'N({self.domain_label})={self.n_domain}, Rint({self.domain_label})={self.rint_domain}, '
                f'N(all)={self.n_all}, Rint(all)={self.rint_all}')


class Dataset:
    def __init__(self):
        self.written_reflections: int | None = None
        self.hklfile: str | None = None
        self.transmission = Transmission()
        self.mu_r: str | None = None
        self.point_group_merge: str | None = '1'
        self.filetype: int | None = 4
        self.domain: str = '1'
        self.numerical: bool = False
        self.rint1 = None
        # Which domains went into this output file:
        self.domain_mode: str = DOMAIN_ALL
        self.domain_number: int | None = None
        # The reflection table this data set was extracted from:
        self.table: ExtractionTable | None = None
        # Values of the 'Rint = ... observations' line of this output block:
        self.rint_observations: float | None = None
        self.observations: int | None = None
        self.is_twin: bool = False
        self.fallback_reflections: int | None = None
        self.fallback_rint: float | None = None
        # The 'PART 2' statistics blocks that are valid for this output file:
        self.statistics: list[ScanStatistics] = []
        # Point group the equivalent reflections were defined with:
        self.equivalents_point_group: str | None = None

    @property
    def reflections_number(self) -> int | None:
        """
        The number of measured reflections (_diffrn_reflns_number) of this output file.
        """
        if not self.is_twin:
            return self.written_reflections
        if self.table:
            if self.domain_mode == DOMAIN_SINGLE and self.table.n_domain is not None:
                return self.table.n_domain
            if self.table.n_all is not None:
                return self.table.n_all
        return self.observations or self.fallback_reflections

    @property
    def rint(self) -> float | None:
        """
        R(int) of the reflections in this output file (_diffrn_reflns_av_R_equivalents).

        For HKLF 5 files the statistics of the 'PART 2' section are preferred, because the
        R(int) of the 'PART 3' extraction table is the agreement between observed intensities
        and intensities calculated from the twin fractions refined by TWINABS. Such a file is
        refined with the twin fractions of SHELXL instead.
        """
        if not self.is_twin:
            return self.fallback_rint
        if self.filetype and self.filetype >= 5:
            return self.rint_of_singles or self._rint_of_table() or self._rint_fallback()
        return self._rint_of_table() or self._rint_fallback()

    @property
    def rint_of_singles(self) -> float | None:
        """
        R(int) of the singly indexed reflections of the domain of this output file. This is the
        population Olex2 uses for the R(int) of HKLF 5 data.
        """
        statistics = self.singles_statistics
        return statistics.rint if statistics else None

    @property
    def singles_statistics(self) -> ScanStatistics | None:
        """
        The statistics of the singly indexed reflections of the domain of this output file, or
        of the domain with the most singles if this file is not restricted to one domain.
        """
        singles = [x for x in self.statistics if x.kind == STATS_SINGLES and x.rint]
        if not singles:
            return None
        domain = self.domain_number if self.domain_mode == DOMAIN_SINGLE else None
        domain = domain or self._largest_component(singles)
        for stats in singles:
            if stats.component == domain:
                return stats
        return None

    @property
    def statistics_of_all_reflections(self) -> ScanStatistics | None:
        for stats in self.statistics:
            if stats.kind == STATS_ALL:
                return stats
        return None

    @staticmethod
    def _largest_component(singles: list[ScanStatistics]) -> int | None:
        return max(singles, key=lambda x: x.total or 0).component

    def _rint_of_table(self) -> float | None:
        if not self.table:
            return None
        if self.domain_mode == DOMAIN_SINGLE and self.table.rint_domain is not None:
            return self.table.rint_domain
        return self.table.rint_all

    def _rint_fallback(self) -> float | None:
        all_reflections = self.statistics_of_all_reflections
        if all_reflections and all_reflections.rint:
            return all_reflections.rint
        return self.rint_observations or self.fallback_rint

    def __repr__(self):
        out = ''
        out += f'written refl.:\t{self.written_reflections}\n'
        out += f'transmission:\t{self.transmission}\n'
        out += f'Mu*r:\t\t\t{self.mu_r}\n'
        out += f'Merging:\t\t{self.point_group_merge}\n'
        out += f'hklfile:\t\t{self.hklfile}\n'
        out += f'HKL file type:\t{self.filetype}\n'
        out += f'Domain in hkl:\t{self.domain}\n'
        out += f'Abs. type:\t\t{"multi-scan" if not self.numerical else "numerical"}'
        out += '\n'
        return out


class Sadabs:
    """
    This is a SADABS/TWINABS file parsing object.

    A TWINABS listing file may contain an arbitrary number of output data sets, because the
    user can write several HKLF 4 and HKLF 5 files in a row during one program run. Every
    output block ends with the 'Additional spherical absorption correction' line.
    """
    _refl_written_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')
    _rint3sig_regex = re.compile(r'^.*Rint\s=.*observations with')
    _extraction_regex = re.compile(r'^\s*Unique HKLF\s+(\d+)\s+data extracted', re.IGNORECASE)
    _hklf5_regex = re.compile(r'^\s*HKLF\s+(\d+)\s+dataset constructed', re.IGNORECASE)
    _table_header_regex = re.compile(r'^\s*Cycle\s+N\((\d+)\)\s+Rint\(\d+\)\s+N\(all\)\s+Rint\(all\)')
    _table_row_regex = re.compile(r'^\s*\d+\s+\d+\s+\d+\.\d+\s+\d+\s+\d+\.\d+')
    _statistics_regex = re.compile(r'^\s*Statistics for (singles of twin component\s+(\d+)|'
                                   r'all composite reflections|all single and composite reflections)',
                                   re.IGNORECASE)
    _all_scans_regex = re.compile(r'^\s*All scans\s+(\d+\.\d+)')
    _point_group_regex = re.compile(r'^\s*Equivalent reflections defined (?:according to|by) '
                                    r'point group\s+(\S+)', re.IGNORECASE)
    _domain_single_regex = re.compile(r'involving domain\s+(\d+)', re.IGNORECASE)
    _domain_up_to_regex = re.compile(r'involving domains\s+1\.\.(\d+)', re.IGNORECASE)
    _rejections_regex = re.compile(r'^\s*(\d+)\s+total and\s+\d+\s+unique reflections left after')

    def __init__(self, basename: str = '', searchpath: Path = Path(__file__).parent.parent,
                 fileobj: Path | None = None):
        """
        """
        self.faces = False
        self.version = ''
        self.twin_components = 1
        self.Rint = None
        self.wR2int = None
        self.observations = None
        self.Rint_3sig = None
        self.observations_3sig = None
        self.input_files = []
        self.datasets: list[Dataset] = []
        self.batch_input = None
        self.filename = Path('')
        self.tables: list[ExtractionTable] = []
        self.statistics: list[ScanStatistics] = []
        self.equivalents_point_group: str | None = None
        self._current_dataset: Dataset | None = None
        self._current_table: ExtractionTable | None = None
        self._current_statistics: ScanStatistics | None = None
        self._reflections_after_rejection: int | None = None
        if fileobj:
            self._fileobj = fileobj
        elif basename:
            self._fileobj = get_file_to_parse(name_pattern=basename, base_directory=searchpath)
        else:
            self._fileobj = get_file_to_parse(fileobj=fileobj)
        if self._fileobj:
            self.filename = self._fileobj.resolve()
            self.parse_file()

    def parse_file(self) -> None:
        filetxt = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
        for line in filetxt:
            self._parse_line(line)
        # A file may end without the closing mu*r line:
        self._finish_dataset()
        self._apply_global_values()

    def _parse_line(self, line: str) -> None:
        spline = line.split()
        if self._rint_regex.match(line):
            #  Rint = 0.0873  for all   11683  observations and
            self.Rint = to_float(spline[2])
            self.observations = to_int(spline[5])
            self._dataset().rint_observations = to_float(spline[2])
            self._dataset().observations = to_int(spline[5])
        if self._rint3sig_regex.match(line):
            #  Rint = 0.0376  for all   44606  observations with I > 3sigma(I)
            self.Rint_3sig = to_float(spline[2])
            self.observations_3sig = to_float(spline[5])
        if line.startswith(" Reading file"):
            self.input_files.append(spline[2])
        if line.startswith(" Reading batch"):
            self.input_files.append(spline[-1])
            self.batch_input = spline[2]
        if line.startswith(' wR2(int)'):
            # wR2(int) is not R(int)! SADABS writes no overall R(int) at all.
            self.wR2int = to_float(spline[2])
        if line.startswith(' Crystal faces:'):
            self.faces = True
        if 'SADABS' in line or 'TWINABS' in line:
            self.version = line.lstrip().strip() + ": Krause, L., Herbst-Irmer, R., Sheldrick G.M. & Stalke D., " \
                                                   "J. Appl. Cryst. 48 (2015) 3-10"
        if 'twin components' in line:
            self.twin_components = to_int(spline[0])
        if self._rejections_regex.match(line):
            #    32949 total and  11913 unique reflections left after |I-<I>|/su test
            self._reflections_after_rejection = to_int(spline[0])
        if line.startswith(' Reflections merged according'):
            self._dataset().point_group_merge = spline[-1]
        if self._point_group_regex.match(line):
            #   Equivalent reflections defined according to point group -1
            self.equivalents_point_group = self._point_group_regex.match(line).group(1)
        if 'PART 2 - Reject outliers' in line:
            # A listing file may contain more than one program run:
            self.statistics = []
        if self._statistics_regex.match(line):
            #  Statistics for singles of twin component  1
            self._start_statistics(line)
        elif self._current_statistics and self._all_scans_regex.match(line):
            #    All scans  0.0340   0.655 - 1.056   0.959 - 1.030   0.615   37875   30125
            self._all_scans_row(spline)
        if self._extraction_regex.match(line):
            #  Unique HKLF 4 data extracted from all observations involving domain 1
            self._start_extraction(line)
        if self._table_header_regex.match(line):
            #  Cycle   N(1) Rint(1)  N(all) Rint(all) Twin fractions
            self._start_table(line)
        elif self._current_table and self._table_row_regex.match(line):
            #     1   20257  0.0742   32215  0.0699   0.7080  0.2920
            self._table_row(spline)
        if self._hklf5_regex.match(line):
            #  HKLF 5 dataset constructed from all observations involving domain 1
            self._start_hklf5(line, spline)
        if self._refl_written_regex.match(line):
            #     2330 Corrected reflections written to file IK_KG_CF_3_0m_5.hkl
            self._dataset().written_reflections = to_int(spline[0])
            self._dataset().hklfile = spline[-1]
        if "Estimated minimum and maximum transmission" in line \
                or 'Minimum and maximum apparent transmission' in line:
            try:
                transmissions = [float(x) for x in spline[-2:]]
                self._dataset().transmission.tmin = min(transmissions)
                self._dataset().transmission.tmax = max(transmissions)
            except ValueError:
                pass
        # This is always the last line of an output data set:
        if line.startswith(" Additional spherical absorption correction"):
            self._dataset().mu_r = spline[-1]
            self._dataset().numerical = self.faces
            self._finish_dataset()

    def _dataset(self) -> Dataset:
        """
        The data set that is currently being filled with values.
        """
        if self._current_dataset is None:
            self._current_dataset = Dataset()
            self._current_dataset.table = self._current_table or self._first_table()
        return self._current_dataset

    def _finish_dataset(self) -> None:
        if self._current_dataset is None:
            return
        self.datasets.append(self._current_dataset)
        self._current_dataset = None

    def _first_table(self) -> ExtractionTable | None:
        return self.tables[0] if self.tables else None

    def _start_extraction(self, line: str) -> None:
        """
        Starts a new HKLF 4 output block and remembers which domains were used for it.
        """
        self._finish_dataset()
        dataset = self._dataset()
        dataset.filetype = to_int(self._extraction_regex.match(line).group(1))
        self._set_domain(dataset, line)

    def _start_hklf5(self, line: str, spline: list[str]) -> None:
        """
        Starts a new HKLF 5 output block. Such a block has no own reflection table, it refers
        to a table written earlier in the file.
        """
        self._finish_dataset()
        dataset = self._dataset()
        dataset.filetype = to_int(spline[1])
        self._set_domain(dataset, line)

    def _set_domain(self, dataset: Dataset, line: str) -> None:
        up_to = self._domain_up_to_regex.search(line)
        single = self._domain_single_regex.search(line)
        if up_to:
            dataset.domain_mode = DOMAIN_UP_TO
            dataset.domain_number = to_int(up_to.group(1))
        elif single:
            dataset.domain_mode = DOMAIN_SINGLE
            dataset.domain_number = to_int(single.group(1))
        else:
            dataset.domain_mode = DOMAIN_ALL
            dataset.domain_number = None
        dataset.domain = str(dataset.domain_number) if dataset.domain_number else 'all'
        dataset.table = self._table_for(dataset)

    def _table_for(self, dataset: Dataset) -> ExtractionTable | None:
        """
        The reflection table that fits to the domain selection of this data set. HKLF 5 blocks
        may refer to a table that was written for a different domain selection, therefore the
        most recent table with a matching column label is preferred. Tables of a 'domains 1..N'
        extraction are skipped, because their N(N) column holds all domains, not domain N.
        """
        if dataset.domain_mode == DOMAIN_SINGLE:
            for table in reversed(self.tables):
                if table.domain_label == dataset.domain_number and table.mode != DOMAIN_UP_TO:
                    return table
        return self._current_table or self._first_table()

    def _start_table(self, line: str) -> None:
        table = ExtractionTable(domain_label=to_int(self._table_header_regex.match(line).group(1)))
        if self._current_dataset is not None:
            table.mode = self._current_dataset.domain_mode
        self.tables.append(table)
        self._current_table = table
        if self._current_dataset is not None:
            self._current_dataset.table = self._table_for(self._current_dataset)

    def _table_row(self, spline: list[str]) -> None:
        """
        Only the values of the last cycle are of interest.
        """
        self._current_table.n_domain = to_int(spline[1])
        self._current_table.rint_domain = to_float(spline[2])
        self._current_table.n_all = to_int(spline[3])
        self._current_table.rint_all = to_float(spline[4])

    def _start_statistics(self, line: str) -> None:
        """
        Starts a 'Statistics for ...' block of the PART 2 section.
        """
        component = to_int(self._statistics_regex.match(line).group(2) or '0')
        if component:
            kind = STATS_SINGLES
        elif 'single and composite' in line.lower():
            kind = STATS_ALL
        else:
            kind = STATS_COMPOSITES
        self._current_statistics = ScanStatistics(kind=kind, component=component or None)
        self.statistics.append(self._current_statistics)

    def _all_scans_row(self, spline: list[str]) -> None:
        """
        The 'All scans' summary row closes a statistics block.
        """
        self._current_statistics.rint = to_float(spline[2])
        self._current_statistics.total = to_int(spline[-2])
        self._current_statistics.i_gt_2sigma = to_int(spline[-1])
        self._current_statistics = None

    def _apply_global_values(self) -> None:
        for dataset in self.datasets:
            dataset.is_twin = self.is_twinabs
            dataset.fallback_reflections = self._reflections_after_rejection
            dataset.fallback_rint = self.Rint
            dataset.statistics = self.statistics
            dataset.equivalents_point_group = self.equivalents_point_group
            if dataset.table is None:
                # An HKLF 5 file may be written before any table was printed:
                dataset.table = self._table_written_later(dataset)

    def _table_written_later(self, dataset: Dataset) -> ExtractionTable | None:
        if dataset.domain_mode == DOMAIN_SINGLE:
            for table in self.tables:
                if table.domain_label == dataset.domain_number and table.mode != DOMAIN_UP_TO:
                    return table
            return None
        return self._first_table()

    def select_dataset(self, hkl_basename: str = '', reflections: int | None = None,
                       hklf: int | None = None) -> Dataset | None:
        """
        Returns the output data set that belongs to the refinement in question.

        The same file name may be written more than once during a TWINABS run, thus the last
        matching data set wins, because it overwrote the previous file on disk.
        """
        if not self.datasets:
            return None
        for candidate in (self._by_name(hkl_basename), self._by_reflections(reflections), self._by_hklf(hklf)):
            if candidate:
                return candidate
        return self.datasets[-1]

    def _by_name(self, hkl_basename: str) -> Dataset | None:
        if not hkl_basename:
            return None
        name = Path(hkl_basename).stem.lower()
        matching = [x for x in self.datasets if x.hklfile and Path(x.hklfile).stem.lower() == name]
        return matching[-1] if matching else None

    def _by_reflections(self, reflections: int | None) -> Dataset | None:
        if not reflections:
            return None
        matching = [x for x in self.datasets if x.written_reflections == reflections]
        return matching[-1] if matching else None

    def _by_hklf(self, hklf: int | None) -> Dataset | None:
        if not hklf:
            return None
        matching = [x for x in self.datasets if x.filetype == hklf]
        return matching[-1] if matching else None

    @property
    def is_twinabs(self) -> bool:
        return self.version.startswith('TWINABS')

    def __iter__(self):
        return iter(x for x in self.datasets)

    @property
    def program(self) -> str:
        return self.version.split()[0].split('-')[0]

    def dataset(self, n: int) -> Dataset:
        try:
            return self.datasets[n]
        except IndexError:
            return Dataset()

    def __repr__(self):
        out = f'Program:\t\t{self.program}\n'
        out += f'version:\t\t{self.version}\n'
        out += f'Abs File:\t\t{self.filename.name}\n'
        out += f'raw input File:\t{" ".join(self.input_files)}\n'
        out += f'Input Batch:\t{self.batch_input}\n'
        out += f'Rint:\t\t\t{self.Rint}\n'
        out += f'wR2int:\t\t\t{self.wR2int}\n'
        out += f'Rint-3sig:\t\t{self.Rint_3sig}\n'
        out += f'components:\t\t{self.twin_components}\n'
        out += '\n'
        return out


if __name__ == '__main__':
    print('###############\n\n')
    s = Sadabs(fileobj=Path(r'test-data/twinabs_multi_options.abs'))
    print(s)
    for dat in s:
        print(dat)
