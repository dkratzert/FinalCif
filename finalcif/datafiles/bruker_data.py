#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from __future__ import annotations

import re
from contextlib import suppress
from pathlib import Path

from gemmi import cif as gcif

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.hkl import calculate_rint, reference_domain
from finalcif.datafiles.bruker_frame import BrukerFrameHeader
from finalcif.datafiles.data import WorkDataMixin
from finalcif.datafiles.p4p_reader import P4PFile
from finalcif.datafiles.sadabs import Dataset, Sadabs
from finalcif.datafiles.saint import SaintListFile
from finalcif.datafiles.shelx_lst import SolutionProgram
from finalcif.gui.dialogs import show_general_warning


def source_path(file: Path | str | None) -> str:
    """
    Returns the absolute path of a data source file or an empty string if it does not exist.
    """
    if not file:
        return ''
    path = Path(file)
    with suppress(OSError):
        path = path.resolve()
        if path.is_file():
            return str(path)
    return ''


class MissingCifData:
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value


class BrukerData(WorkDataMixin):

    def __init__(self, app, cif: CifContainer):
        super().__init__()
        self.cif = cif
        self.app = app
        self.saint_data = SaintListFile(name_patt='*_0*m._ls', directory=self.cif.fileobj.parent.resolve())
        # Using the saint list files name as base reference for all other data containing files:
        basename = self.saint_data.filename.stem.split('_0m')[0]
        self.basename = re.sub(r'^(cu|mo|ag)_', '', basename)
        # This is only in this list file, not in the global:
        saint_first_ls = SaintListFile(name_patt='*_01._ls', directory=self.cif.fileobj.parent.resolve())
        sol = SolutionProgram(cif)
        solution_program = None
        if 'shelx' in self.cif.block.find_value('_audit_creation_method').lower():
            shelx = 'Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n'
        else:
            shelx = ''
        if cif.res_file_data and cif.dsr_used:
            dsr = 'The program DSR was used for model building:\n' \
                  'D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508'
            shelx += dsr
        abstype = '?'
        t_min = '?'
        t_max = '?'
        sadabs = self.sadabs
        # Going back from last dataset:
        for n in range(1, len(sadabs.datasets) + 1):
            try:
                abstype = 'numerical' if sadabs.dataset(-n).numerical else 'multi-scan'
                t_min = sadabs.dataset(-n).transmission.tmin
                t_max = sadabs.dataset(-n).transmission.tmax
                if all([abstype, t_min, t_max]):
                    break
            except (KeyError, AttributeError, TypeError):
                pass
                # print('No .abs file found.')
                # no abs file found
        # the lower temp is more likely:
        try:
            temp1 = self.frame_header.temperature
        except (AttributeError, KeyError, FileNotFoundError):
            temp1 = None
        try:
            kilovolt = self.frame_header.kilovolts
        except (AttributeError, KeyError, FileNotFoundError):
            kilovolt = ''
        try:
            milliamps = self.frame_header.milliamps
        except (AttributeError, KeyError, FileNotFoundError):
            milliamps = ''
        try:
            frame_name = source_path(self.frame_header.filename)
        except FileNotFoundError:
            frame_name = ''
        if not self.cif['_computing_structure_solution'] and self.cif.solution_program_details:
            solution_program = (self.cif.solution_program_details, source_path(self.cif.fileobj))
        if self.cif['_computing_structure_solution']:
            solution_program = (gcif.as_string(self.cif['_computing_structure_solution']),
                                source_path(self.cif.fileobj))
        if not solution_program:
            solution_program = (sol.program.version, source_path(sol.program.filename))
        if self.cif.absorpt_process_details:
            absdetails = (self.cif.absorpt_process_details, source_path(self.cif.fileobj))
        else:
            absdetails = (sadabs.version, source_path(sadabs.filename))
        if self.cif.absorpt_correction_type:
            abscorrtype = (self.cif.absorpt_correction_type, source_path(self.cif.fileobj))
        else:
            abscorrtype = (abstype, source_path(sadabs.filename))
        if self.cif.absorpt_correction_t_max:
            abs_tmax = (self.cif.absorpt_correction_t_max, source_path(self.cif.fileobj))
        else:
            abs_tmax = (str(t_max), source_path(sadabs.filename))
        if self.cif.absorpt_correction_t_min:
            abs_tmin = (self.cif.absorpt_correction_t_min, source_path(self.cif.fileobj))
        else:
            abs_tmin = (str(t_min), source_path(sadabs.filename))

        self._add_reflection_data(sadabs)
        temp2 = self.p4p.temperature
        if temp1 is not None and temp2 is not None:
            temperature = round(min([temp1, temp2]), 1)
        elif temp1:
            temperature = temp1
        else:
            temperature = temp2
        if temperature is None:
            temperature = '?'
        if (self.cif['_diffrn_ambient_temperature'].split('(')[0] or
            self.cif['_cell_measurement_temperature']).split('(')[0] == '0':
            show_general_warning(self.app, '<b>Warning of impossible temperature specification</b>:<br>'
                                           'You probably entered &minus;273.15 °C instead '
                                           'of &minus;173.15 °C into the SHELX instruction file.<br>'
                                           'A temperature of 0 K is likely to be wrong.')
        try:
            temperature_diff = abs(int(self.cif['_diffrn_ambient_temperature'].split('(')[0]) - int(temperature)) >= 2
        except ValueError:
            temperature_diff = False
        if (temperature_diff and not self.app.temperature_warning_displayed):
            self.app.temperature_warning_displayed = True
            show_general_warning(self.app,
                                 f'<b>Warning</b>: The temperature from the measurement and from SHELX '
                                 f'differ. Please double-check for correctness.'
                                 f'<br><br>SHELX says: {self.cif["_diffrn_ambient_temperature"].split("(")[0]} K'
                                 f'<br>The P4P file says: {temp2} {"K" if temp2 else ""}<br>Frame header says: '
                                 f'{temp1} {"K" if temp2 else ""}<br><br>You may add a '
                                 f'<a href="http://shelx.uni-goettingen.de/shelxl_html.php#TEMP">TEMP</a> '
                                 f'instruction to your SHELX file (in °C).')
        if not self.cif['_space_group_name_H-M_alt']:
            try:
                self.sources['_space_group_name_H-M_alt'] = (
                    self.cif.space_group, 'Calculated by gemmi: https://gemmi.readthedocs.io')
            except AttributeError:
                pass
        if not self.cif['_space_group_name_Hall']:
            with suppress(AttributeError):
                self.sources['_space_group_name_Hall'] = (
                    self.cif.hall_symbol, 'Calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif['_space_group_IT_number']:
            with suppress(AttributeError):
                self.sources['_space_group_IT_number'] = (
                    self.cif.spgr_number_from_symmops, 'Calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif['_space_group_crystal_system']:
            with suppress(AttributeError):
                csystem = self.cif.crystal_system
                self.sources['_space_group_crystal_system'] = (
                    csystem, 'calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif.symmops and self.cif.symmops_from_spgr:
            loop = self.cif.block.init_loop('_space_group_symop_operation_', ['xyz'])
            for symmop in reversed(self.cif.symmops_from_spgr):
                loop.add_row([gcif.quote(symmop)])
        # All sources that are not filled with data will be yellow in the main table
        #                          data                         tooltip
        self.sources['_cell_measurement_reflns_used'] = (
            self.saint_data.cell_reflections, source_path(self.saint_data.filename))
        self.sources['_cell_measurement_theta_min'] = (
            self.saint_data.cell_res_min_theta or '', source_path(self.saint_data.filename))
        self.sources['_cell_measurement_theta_max'] = (
            self.saint_data.cell_res_max_theta or '', source_path(self.saint_data.filename))
        self.sources['_computing_data_collection'] = (saint_first_ls.aquire_software,
                                                      source_path(saint_first_ls.filename))
        self.sources['_computing_cell_refinement'] = (self.saint_data.version, source_path(self.saint_data.filename))
        self.sources['_computing_data_reduction'] = (self.saint_data.version, source_path(self.saint_data.filename))
        self.sources['_exptl_absorpt_correction_type'] = abscorrtype
        self.sources['_exptl_absorpt_correction_T_min'] = abs_tmin
        self.sources['_exptl_absorpt_correction_T_max'] = abs_tmax
        self.sources['_exptl_absorpt_process_details'] = absdetails
        self.sources['_cell_measurement_temperature'] = (temperature, source_path(self.p4p.filename))
        self.sources['_diffrn_ambient_temperature'] = (temperature, source_path(self.p4p.filename))
        self.sources['_exptl_crystal_colour'] = (self.p4p.crystal_color, source_path(self.p4p.filename))
        self.sources['_exptl_crystal_description'] = (self.p4p.morphology, source_path(self.p4p.filename))
        self.sources['_exptl_crystal_size_min'] = (self.p4p.crystal_size[0] or '', source_path(self.p4p.filename))
        self.sources['_exptl_crystal_size_mid'] = (self.p4p.crystal_size[1] or '', source_path(self.p4p.filename))
        self.sources['_exptl_crystal_size_max'] = (self.p4p.crystal_size[2] or '', source_path(self.p4p.filename))
        self.sources['_computing_structure_solution'] = solution_program
        self.sources['_atom_sites_solution_primary'] = (sol.method, 'Inherited from solution program.')
        self.sources['_diffrn_source_voltage'] = (kilovolt or '', frame_name)
        self.sources['_diffrn_source_current'] = (milliamps or '', frame_name)
        self.sources['_chemical_formula_moiety'] = ('', '')
        self.sources['_publ_section_references'] = (shelx, '')
        self.sources['_refine_special_details'] = ('', '')
        self.sources['_exptl_crystal_recrystallization_method'] = ('', '')
        if not self.cif.is_centrosymm:
            self.sources['_chemical_absolute_configuration'] = ('', '')
        if self.saint_data.is_twin and self.saint_data.components_firstsample == 2:
            with suppress(Exception):
                law = self.saint_data.twinlaw[next(iter(self.saint_data.twinlaw.keys()))]
                saint_file = source_path(self.saint_data.filename)
                self.sources['_twin_individual_twin_matrix_11'] = (str(law[0][1]), saint_file)
                self.sources['_twin_individual_twin_matrix_12'] = (str(law[0][2]), saint_file)
                self.sources['_twin_individual_twin_matrix_13'] = (str(law[0][0]), saint_file)
                self.sources['_twin_individual_twin_matrix_21'] = (str(law[1][1]), saint_file)
                self.sources['_twin_individual_twin_matrix_22'] = (str(law[1][2]), saint_file)
                self.sources['_twin_individual_twin_matrix_23'] = (str(law[1][0]), saint_file)
                self.sources['_twin_individual_twin_matrix_31'] = (str(law[2][1]), saint_file)
                self.sources['_twin_individual_twin_matrix_32'] = (str(law[2][2]), saint_file)
                self.sources['_twin_individual_twin_matrix_33'] = (str(law[2][0]), saint_file)
                self.sources['_twin_individual_id'] = (
                    str(self.saint_data.components_firstsample), saint_file)
                self.sources['_twin_special_details'] = (
                    'The data was integrated as a 2-component twin.', saint_file)

    def _add_reflection_data(self, sadabs: Sadabs) -> None:
        """
        Adds the number of measured reflections and R(int) of the data set that belongs to the
        hkl file of this refinement. SHELXL can not determine these values from an HKLF 5 file,
        thus the number of reflections of a TWINABS file and a calculated R(int) take precedence
        over the values in the CIF.
        """
        dataset = sadabs.select_dataset(hkl_basename=self._hkl_basename,
                                        reflections=self._reflections_in_hkl_file(),
                                        hklf=self.cif.hklf_number)
        self._add_rint(dataset, sadabs)
        if dataset and dataset.reflections_number:
            self.sources['_diffrn_reflns_number'] = (dataset.reflections_number, source_path(sadabs.filename))
            if sadabs.is_twinabs and dataset.filetype == 5:
                self.overrides.add('_diffrn_reflns_number')

    def _add_rint(self, dataset: Dataset | None, sadabs: Sadabs) -> None:
        """
        The R(int) of an HKLF 5 refinement is calculated from the reflection data, because the
        R(int) of a TWINABS listing file is a residual of the TWINABS twin fraction refinement
        and not the agreement of symmetry equivalent reflections.
        """
        calculated = self._rint_from_hkl_data()
        listed = dataset.rint if dataset else None
        twinned = self._is_twinned(dataset, sadabs)
        if twinned:
            rint, source = calculated, self._calculated_rint_source(twinned)
            if not rint:
                rint, source = listed, self._listed_rint_source(dataset, sadabs)
        else:
            rint, source = listed, source_path(sadabs.filename)
            if not rint:
                rint, source = calculated, self._calculated_rint_source(twinned)
        if not rint:
            return
        self.sources['_diffrn_reflns_av_R_equivalents'] = (rint, source)
        if twinned:
            self.overrides.add('_diffrn_reflns_av_R_equivalents')

    def _is_twinned(self, dataset: Dataset | None, sadabs: Sadabs) -> bool:
        """
        SHELXL can not determine R(int) of HKLF 5 data, thus FinalCif has to do it.
        """
        return self.cif.hklf_number >= 5 or bool(
            sadabs.is_twinabs and dataset and dataset.filetype == 5)

    def _calculated_rint_source(self, twinned: bool) -> str:
        if twinned:
            return (f'calculated from {source_path(self.cif.fileobj)} '
                    f'(singles of twin component {self._reference_domain()}, '
                    f'merged in {self.cif.space_group})')
        return f'calculated from {source_path(self.cif.fileobj)}'

    def _reference_domain(self) -> int | None:
        return self._twst() or reference_domain(self.cif.hkl_file)

    def _listed_rint_source(self, dataset: Dataset | None, sadabs: Sadabs) -> str:
        """
        The R(int) of the TWINABS statistics is only valid for the point group the equivalent
        reflections were defined with.
        """
        source = source_path(sadabs.filename)
        statistics = dataset.singles_statistics if dataset else None
        if statistics and dataset.equivalents_point_group:
            return (f'{source} (singles of twin component {statistics.component}, '
                    f'point group {dataset.equivalents_point_group})')
        return source

    def _rint_from_hkl_data(self) -> float | None:
        """
        R(int) calculated from the reflection data of the CIF.

        SADABS writes no overall R(int) into its listing file and SHELXL can not determine it
        from an HKLF 5 file, therefore it is calculated here. For HKLF 4 data this only happens
        if the CIF has no R(int) yet, while for HKLF 5 data the calculated value is always
        preferred over the R(int) of a TWINABS listing file, which is a model residual of the
        TWINABS twin fraction refinement instead of a merging R(int).
        """
        if self.cif.hklf_number == 4 and gcif.as_string(
                self.cif['_diffrn_reflns_av_R_equivalents']).strip(' ?'):
            return None
        return calculate_rint(self.cif.hkl_file, self.cif.space_group,
                              cell=self.cif.cell, resolution=self._resolution_limits(),
                              hklf=self.cif.hklf_number, twst=self._twst())

    def _twst(self) -> int | None:
        """The reference domain of a SHELX TWST instruction."""
        match = re.search(r'^TWST\s+(-?\d+)', self.cif.res_file_data or '', re.MULTILINE)
        return int(match.group(1)) if match else None

    def _resolution_limits(self) -> tuple[float, float] | None:
        """The resolution limits of a SHELX SHEL instruction, if there is one."""
        shel = getattr(self.cif.shx, 'shel', None)
        if not shel:
            return None
        with suppress(AttributeError, TypeError):
            return float(shel.lowres), float(shel.highres)
        return None

    @property
    def _hkl_basename(self) -> str:
        return self.cif.fileobj.stem.replace('-finalcif', '')

    def _reflections_in_hkl_file(self) -> int | None:
        """
        The number of reflections in the hkl file of this refinement, without the terminating
        0 0 0 reflection and the SADABS/TWINABS footer.
        """
        hkl = self.cif.hkl_file_without_foot
        if not hkl:
            return None
        lines = [x for x in hkl.splitlines(keepends=False) if x.strip()]
        return len(lines) - 1 if lines else None

    @property
    def sadabs(self):
        sad = Sadabs(basename='*.abs', searchpath=self.cif.fileobj.parent)
        return sad

    @property
    def frame_header(self):
        return BrukerFrameHeader(self.basename, self.cif.fileobj.parent)

    @property
    def p4p(self):
        return P4PFile(self.basename, self.cif.fileobj.parent)
