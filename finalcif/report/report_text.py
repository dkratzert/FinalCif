import os
from builtins import str
from typing import Union, List, Tuple

import gemmi
from docx import Document
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from lxml import etree
from shelxfile.atoms.atoms import Atom as SHXAtom

from finalcif.app_path import application_path
from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.text import retranslate_delimiter, string_to_utf8
from finalcif.report.references import DummyReference, SAINTReference, SORTAVReference, ReferenceList, CCDCReference, \
    SHELXLReference, SHELXTReference, SHELXSReference, FinalCifReference, ShelXleReference, Olex2Reference, \
    SHELXDReference, SadabsTwinabsReference, CrysalisProReference, Nosphera2Reference, XDSReference, DSRReference2015, \
    DSRReference2018, XRedReference
from finalcif.tools.misc import protected_space, angstrom, zero_width_space, remove_line_endings, flatten


def math_to_word(eq: str) -> str:
    """Transform a sympy equation to be printed in word document."""
    tree = etree.fromstring(eq)
    xslt = etree.parse(os.path.join(application_path, 'template/mathml2omml.xsl'))
    transform = etree.XSLT(xslt)
    new_dom = transform(tree)
    return new_dom.getroot()


def clean_string(string: str) -> str:
    """
    Removes control characters from a string.
    >>> clean_string('This is a sentence\\nwith newline.')
    'This is a sentence with newline'
    >>> clean_string('')
    ''
    >>> clean_string('  This is  a sentence\\nwith. newline.  ')
    'This is  a sentence with. newline'
    """
    repl = string.replace('\t', ' ') \
        .replace('\f', ' ') \
        .replace('\0', ' ') \
        .strip(' ') \
        .strip('.')
    return remove_line_endings(repl)


def gstr(string: str) -> str:
    """
    Turn a string into a gemmi string and remove control characters.
    """
    return clean_string(gemmi.cif.as_string(string))


class FormatMixin():

    def bold(self, run: Run):
        r = run.bold = True
        return r


class Crystallization(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        crystalization_method = gstr(cif['_exptl_crystal_recrystallization_method'])
        if not crystalization_method:
            crystalization_method = "[No _exptl_crystal_recrystallization_method like 'The compound was " \
                                    "crystallized from methanol by evaporation at 25 °C.' was given]"
        delimiter = retranslate_delimiter(f"{crystalization_method}. ")
        paragraph.add_run(delimiter)


class CrystalSelection(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        shape = gstr(cif['_exptl_crystal_description'])
        crystal_mount = gstr(cif['_diffrn_measurement_specimen_support'])
        colour = gstr(cif['_exptl_crystal_colour']).strip()
        if colour:
            colour = f" {colour}{',' if shape else ''}"
        # adhesive = gstr(cif['_diffrn_measurement_specimen_adhesive'])
        # if not adhesive:
        #    adhesive = '[No _diffrn_measurement_specimen_adhesive given]'
        shaped = f" {shape}-shaped " if shape else ' '
        if crystal_mount:
            txt_crystal = (f"A{colour}{shaped}crystal of {cif.block.name} was mounted on a "
                           f"{crystal_mount} with perfluoroether oil. ")
            paragraph.add_run(retranslate_delimiter(txt_crystal))
        else:
            txt_crystal = (f"A{colour}{shaped}crystal of {cif.block.name} "
                           f"was mounted on the goniometer. ")
            paragraph.add_run(retranslate_delimiter(txt_crystal))


class DataCollection(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        temperature = gstr(cif['_diffrn_ambient_temperature'])
        if not temperature:
            temperature = '[No _diffrn_ambient_temperature given]'
        method = 'shock-cooled '
        try:
            if float(temperature.split('(')[0]) > 200:
                method = ''
        except ValueError:
            method = ''
        txt_data = (f"Data were collected from a {method}single crystal at "
                    f"{temperature}{protected_space}K")
        paragraph.add_run(retranslate_delimiter(txt_data))


class MachineType():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.difftype = gstr(cif['_diffrn_measurement_device_type']) \
                        or '[No _diffrn_measurement_device_type given]'
        self.device = gstr(cif['_diffrn_measurement_device']) \
                      or '[No _diffrn_measurement_device given]'
        self.source = gstr(cif['_diffrn_source']).strip('\n\r') \
                      or '[No _diffrn_source given]'
        self.monochrom = gstr(cif['_diffrn_radiation_monochromator']) \
                         or '[No _diffrn_radiation_monochromator given]'
        if not self.monochrom:
            self.monochrom = '?'
        self.cooling = self._get_cooling_device(cif)
        self.rad_type = gstr(cif['_diffrn_radiation_type']) \
                        or '[No _diffrn_radiation_type given]'
        radtype = format_radiation(self.rad_type)
        self.wavelen = gstr(cif['_diffrn_radiation_wavelength']) \
                       or '[No _diffrn_radiation_wavelength given]'
        self.detector_type = ''
        detector_type = gstr(cif['_diffrn_detector_type']) \
                        or '[No _diffrn_detector_type given]'
        if detector_type:
            self.detector_type = " and a {} detector".format(detector_type)
        sentence1 = "on {0} {1} {2} with {3} {4} using a {5} as monochromator{6}. " \
                    "The diffractometer was equipped with {7} {8}low temperature device and used "
        sentence2 = " radiation (λ = {}" + protected_space + "{}). ".format(angstrom)
        txt = sentence1.format(get_inf_article(self.difftype), self.difftype, self.device,
                               get_inf_article(self.source), self.source, self.monochrom,
                               self.detector_type, get_inf_article(self.cooling), self.cooling)
        paragraph.add_run(retranslate_delimiter(txt))
        # radiation type e.g. Mo:
        paragraph.add_run(retranslate_delimiter(radtype[0]))
        # K line:
        radrunita = paragraph.add_run(radtype[1])
        radrunita.font.italic = True
        alpha = paragraph.add_run(retranslate_delimiter(radtype[2]))
        alpha.font.italic = True
        alpha.font.subscript = True
        txt2 = sentence2.format(self.wavelen)
        paragraph.add_run(txt2)

    @staticmethod
    def _get_cooling_device(cif):
        olx = gstr(cif['_olex2_diffrn_ambient_temperature_device'])
        iucr = gstr(cif['_diffrn_measurement_ambient_temperature_device_make'])
        if olx and iucr:
            return iucr + ' '
        if olx:
            return olx + ' '
        elif iucr:
            return iucr + ' '
        else:
            return ''


class DataReduction():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        integration = gstr(cif['_computing_data_reduction']) or '??'
        abstype = gstr(cif['_exptl_absorpt_correction_type']) or '??'
        abs_details = gstr(cif['_exptl_absorpt_process_details']) or '??'
        data_reduct_ref = DummyReference()
        absorpt_ref = DummyReference()
        integration_prog = '[unknown integration program]'
        scale_prog = '[unknown program]'
        if 'SAINT' in integration:
            data_reduct_ref, integration_prog = self.add_saint_reference(integration)
        if 'XDS' in integration:
            data_reduct_ref = XDSReference()
            integration_prog = 'XDS'
        if 'CrysAlisPro'.lower() in integration.lower():
            data_reduct_ref, absorpt_ref, integration_prog = self.add_crysalispro_reference(integration)
        if 'STOE X-RED'.lower() in integration.lower():
            data_reduct_ref, integration_prog = self.add_x_red_reference(integration)
        absdetails = cif['_exptl_absorpt_process_details'].replace('-', ' ')
        if 'SADABS' in absdetails.upper() or 'TWINABS' in absdetails.upper():
            # if len(absdetails.split()) > 1:
            #    version = absdetails.split()[1]
            # else:
            #    version = 'unknown version'
            if 'SADABS' in absdetails:
                scale_prog = 'SADABS'
            else:
                scale_prog = 'TWINABS'
            # absorpt_ref = SAINTReference(scale_prog, version)
            absorpt_ref = SadabsTwinabsReference()
        if 'SORTAV' in absdetails.upper():
            scale_prog = 'SORTAV'
            absorpt_ref = SORTAVReference()
        if 'crysalis' in abs_details.lower():
            scale_prog = 'SCALE3 ABSPACK'
        txt = (f'All data were integrated with {integration_prog} and {get_inf_article(abstype)} '
               f'{abstype} absorption correction using {scale_prog} was applied.')
        paragraph.add_run(retranslate_delimiter(txt))
        ref.append([data_reduct_ref, absorpt_ref])

    def add_saint_reference(self, integration):
        saintversion = 'unknown version'
        if len(integration.split()) > 1:
            saintversion = integration.split()[1]
        integration_prog = 'SAINT'
        data_reduct_ref = SAINTReference('SAINT', saintversion)
        return data_reduct_ref, integration_prog

    def add_x_red_reference(self, integration):
        xredversion = 'unknown version'
        # if len(integration.split()) > 1:
        #    xredversion = integration.split()[1]
        integration_prog = 'STOE X-RED'
        data_reduct_ref = XRedReference('X-RED', xredversion)
        return data_reduct_ref, integration_prog

    def add_crysalispro_reference(self, integration: str) -> Tuple[CrysalisProReference, CrysalisProReference, str]:
        """
        CrysAlisPro, Agilent Technologies,Version 1.171.37.31h (release 21-03-2014 CrysAlis171 .NET)
            (compiled Mar 21 2014,18:13:45)
        CrysAlisPro 1.171.42.58a (Rigaku OD, 2022)
        """
        year = 'unknown version'
        version = 'unknown year'
        pages = 'Rigaku OD'
        length = len(integration.split())
        if 3 < length <= 5:
            year = integration.split()[4][:-1]
            version = integration.split()[1][:-1]
        elif length > 8 and 'agilent' in integration.lower():
            pages = 'Agilent Technologies'
            year = integration.split()[5]
            if '-' in year:
                year = year.split('-')[-1]
            version = integration.split()[3]
        integration_prog = 'Crysalispro'
        data_reduct_ref = CrysalisProReference(version=version, year=year, pages=pages)
        absorpt_ref = CrysalisProReference(version=version, year=year, pages=pages)
        return data_reduct_ref, absorpt_ref, integration_prog


class SolveRefine():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        manual_method = False
        refineref = DummyReference()
        solveref = DummyReference()
        solution_prog = gstr(cif['_computing_structure_solution']) or '[No _computing_structure_solution given]'
        solution_method = gstr(cif['_atom_sites_solution_primary']).strip(
            '\n\r') or '[No _atom_sites_solution_primary given]'
        if 'isomor' in solution_method:
            manual_method = True
        if solution_prog.upper().startswith(('SHELXT', 'XT')):
            solveref = SHELXTReference()
        if 'SHELXS' in solution_prog.upper():
            solveref = SHELXSReference()
        if 'SHELXD' in solution_prog.upper():
            solveref = SHELXDReference()
        refined = gstr(cif['_computing_structure_refinement']).split(' ')[
                      0] or '[No _computing_structure_refinement given]'
        if refined.upper().startswith(('SHELXL', 'XL')):
            refineref = SHELXLReference()
        if 'OLEX' in refined.upper():
            refineref = Olex2Reference()
        if 'NOSPHERA2' in solution_prog.upper() or 'NOSPHERA2' in cif['_refine_special_details'].upper() \
            or 'NOSPHERA2' in cif['_olex2_refine_details'].upper():
            refineref = [Olex2Reference(), Nosphera2Reference()]
        refine_coef = gstr(cif['_refine_ls_structure_factor_coef'])
        if manual_method:
            methods = f"{solution_prog} "
        else:
            methods = f"{solution_method} methods using {solution_prog.split(' ')[0]} "
        txt = (f"The structure was solved by {methods}and refined by full-matrix least-squares methods against ")
        paragraph.add_run(retranslate_delimiter(txt))
        paragraph.add_run('F').font.italic = True
        if refine_coef.lower() == 'fsqd':
            paragraph.add_run('2').font.superscript = True
        paragraph.add_run(f' by {refined}')
        gui_reference = None
        if 'shelxle' in refined.lower() or 'shelxle' in cif['_computing_molecular_graphics'].lower():
            paragraph.add_run(' using ShelXle')
            gui_reference = ShelXleReference()
        if 'olex' in refined.lower() or 'olex' in cif['_computing_molecular_graphics'].lower():
            paragraph.add_run(' using Olex2')
            gui_reference = Olex2Reference()
        paragraph.add_run('.')
        ref.append(flatten([solveref, refineref, gui_reference]))


class Atoms():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        """
        Text for non-hydrogen atoms.
        """
        self.cif = cif
        self.n_isotropic = self.number_of_isotropic_atoms(without_h=True)
        self.n_isotropic_with_h = self.number_of_isotropic_atoms(without_h=False)
        number = 'All'
        parameter_type = 'anisotropic'
        if 0 < self.n_isotropic < self.cif.natoms(without_h=True):
            number = (f'Some atoms ({self.n_isotropic}) were refined using isotropic displacement parameters. '
                      f'All other')
        if self.n_isotropic > 0 and self.n_isotropic > self.cif.natoms(without_h=True):
            number = (f'Most atoms ({self.n_isotropic}) were refined using isotropic displacement parameters. '
                      f'All other')
        if self.n_isotropic == self.cif.natoms(without_h=True):
            number = 'All'
            parameter_type = 'isotropic'
        non_h = 'non-hydrogen '
        sentence1 = (f"{number} {non_h if self.n_isotropic_with_h > 0 else ''}atoms were refined with {parameter_type} "
                     f"displacement parameters. ")
        paragraph.add_run(sentence1)

    def number_of_isotropic_atoms(self, without_h: bool = True) -> Union[float, int]:
        isotropic_count = 0
        for site in self.cif.atomic_struct.sites:
            if self.atom_is_isotropic(site, without_h):
                isotropic_count += 1
        return isotropic_count

    @staticmethod
    def atom_is_isotropic(site, without_h: bool):
        if without_h:
            return not site.aniso.nonzero() and not site.element.is_hydrogen
        else:
            return not site.aniso.nonzero()


class Hydrogens():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        """
        The hydrogen atoms were refined isotropically on calculated positions using
        a riding model with their Uiso values constrained to 1.5 times the Ueq of
        their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other
        carbon atoms.
        """
        hatoms: List[SHXAtom] = [x for x in cif.shx.atoms.all_atoms if x.is_hydrogen]
        n_hatoms = len(hatoms)
        n_anisotropic_h = len([x for x in hatoms if sum([abs(y) for y in x.uvals[1:]]) > 0.0001])
        n_constr_h = len([x for x in hatoms if x.uvals[0] < -1.0])
        riding_atoms = [x for x in hatoms if x.afix]
        pivot_atoms = self.get_hydrogen_pivot_atoms(riding_atoms)
        n_riding = len(riding_atoms)
        n_non_riding = len(hatoms) - n_riding

        atom_type = "carbon"
        number = "The"
        sentence_isotropic = "isotropic"
        sentence_anisotropic = "anisotropic"

        if n_anisotropic_h == n_hatoms:
            # number = "All"
            utype = sentence_anisotropic
        elif n_anisotropic_h > 0 and n_anisotropic_h < n_hatoms:
            number = "Some"
            utype = sentence_isotropic + " and some with anisotropic "
        else:
            if all(self.pivot_atom_types(pivot_atoms)):
                number = "All"
            elif any(self.pivot_atom_types(pivot_atoms)):
                number = "All C-bound"
            else:
                number = "The heteroatom-bound"
            utype = sentence_isotropic
        sentence_riding = "on calculated positions using a riding model with their "
        sentence_free_pos = "freely"
        sentence_15 = " values constrained to 1.5 times the "  # Ueq
        sentence_pivot = " of their pivot atoms for terminal sp"  # 3
        sentence_12 = f" {atom_type} atoms and 1.2 times for all other {atom_type} atoms."

        if n_riding == n_hatoms:
            paragraph.add_run(f"{number} hydrogen atoms were refined {utype} ")
            riding = sentence_riding
            paragraph.add_run(riding)
            self.u_iso(paragraph)
            paragraph.add_run(sentence_15)
            self.u_eq(paragraph)
            paragraph.add_run(sentence_pivot)
            paragraph.add_run('3').font.superscript = True
            paragraph.add_run(sentence_12)
        elif n_non_riding == n_hatoms:
            if n_constr_h == n_hatoms:
                paragraph.add_run(f"{number} hydrogen atoms were refined {sentence_free_pos}"
                                  f" with their ")
            else:
                paragraph.add_run(f"{number} hydrogen atoms were refined {sentence_free_pos}"
                                  f" with {utype} displacement parameters.")
            if n_constr_h == n_hatoms:
                self.u_iso(paragraph)
                paragraph.add_run(sentence_15)
                self.u_eq(paragraph)
                paragraph.add_run(sentence_pivot)
                paragraph.add_run('3').font.superscript = True
                paragraph.add_run(sentence_12)
        else:
            paragraph.add_run(f"{number} hydrogen atoms were refined with {utype} displacement parameters. ")
            riding = f"Some were refined {sentence_free_pos} and some {sentence_riding}"
            paragraph.add_run(riding)
            self.u_iso(paragraph)
            paragraph.add_run(sentence_15)
            self.u_eq(paragraph)
            paragraph.add_run(sentence_pivot)
            paragraph.add_run('3').font.superscript = True
            paragraph.add_run(sentence_12)

    def pivot_atom_types(self, pivot_atoms):
        return [x.element == 'C' for x in pivot_atoms]

    def get_hydrogen_pivot_atoms(self, riding_atoms):
        pivot_atoms = []
        for at in riding_atoms:
            pivot_atoms.extend(at.find_atoms_around(dist=1.2))
        return pivot_atoms

    def u_eq(self, paragraph):
        paragraph.add_run('U').font.italic = True
        paragraph.add_run('eq').font.subscript = True

    def u_iso(self, paragraph):
        paragraph.add_run('U').font.italic = True
        paragraph.add_run('iso').font.subscript = True


class Disorder():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, reflist: ReferenceList):
        """
        TODO: Search for SIMU, DELU, SADI, DFIX, etc in cif.shx.restraints in order to
              make the sentence1 more specific.
        """

        self.dsr_sentence = ''
        sentence1 = "Disordered moieties were refined using bond lengths " \
                    "restraints and displacement parameter restraints. "
        paragraph.add_run(sentence1)
        if cif.dsr_used:
            dsr_sentence = "Some parts of the disorder model were introduced by the " \
                           "program DSR."
            paragraph.add_run(dsr_sentence)
            reflist.append([DSRReference2015(), DSRReference2018()])
            SpaceChar(paragraph).regular()


class Twinning():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, reflist: ReferenceList):
        """ _twin_formation_mechanism         gt
            _twin_dimensionality              triperiodic
            _twin_morphology                  polysynthetic
            _twin_special_details             'The data was integrated as a 2-component twin.'
            _twin_individual_id               2
            _twin_individual_twin_matrix_11   -0.00018
            _twin_individual_twin_matrix_12   -0.00091
            _twin_individual_twin_matrix_13   -0.9998
            _twin_individual_twin_matrix_21   0.99999
            _twin_individual_twin_matrix_22   -0.26475
            _twin_individual_twin_matrix_23   -0.36925
            _twin_individual_twin_matrix_31   0.00018
            _twin_individual_twin_matrix_32   -1.00019
            _twin_individual_twin_matrix_33   0.00187
        """
        twining = cif['_twin_individual_id']
        if twining:
            sentence = f''


class SpaceChar():
    def __init__(self, paragraph: Paragraph):
        self.p = paragraph

    def regular(self) -> None:
        self.p.add_run(' ')

    def protected(self):
        self.p.add_run(protected_space)


class CCDC():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        ccdc_num = gstr(cif['_database_code_depnum_ccdc_archive']) or '??????'
        splitted_number = ccdc_num.split(' ')
        if len(splitted_number) > 1 and splitted_number[1].isdigit():
            ccdc_num = splitted_number[1]
        sentence1 = "Crystallographic data for the structures reported here " \
                    "have been deposited with the Cambridge Crystallographic Data Centre."
        sentence2 = f"CCDC {ccdc_num} contain the supplementary crystallographic data for this paper. " \
                    "These data can be obtained free of charge from The Cambridge Crystallographic Data Centre " \
                    f"via www.ccdc.cam.ac.uk/{zero_width_space}structures."
        paragraph.add_run(sentence1)
        ref.append(CCDCReference())
        SpaceChar(paragraph).regular()
        paragraph.add_run(sentence2)


class FinalCifreport():
    def __init__(self, paragraph: Paragraph, reflist: ReferenceList):
        sentence = "This report and the CIF file were generated using FinalCif."
        paragraph.add_run(sentence)
        reflist.append(FinalCifReference())


class RefinementDetails():
    def __init__(self, cif: CifContainer, document: Document):
        ph = document.add_paragraph(style='Heading 2')
        ph.add_run(text=fr"Refinement details for {cif.block.name}")
        p = document.add_paragraph()
        p.style = document.styles['fliesstext']
        text = ' '.join(cif['_refine_special_details'].splitlines(keepends=False))
        if cif['_olex2_refine_details']:
            text += ' '.join(cif['_olex2_refine_details'].splitlines(keepends=False))
        # Replacing semicolon, because it can damage the CIF:
        text = text.replace(';', '.')
        p.add_run(string_to_utf8(text).strip())


def get_inf_article(next_word: str) -> str:
    if not next_word:
        return 'a'
    voc = 'aeiou'
    return 'an' if next_word[0].lower() in voc else 'a'


def format_radiation(radiation_type: str) -> list:
    radtype = list(radiation_type.partition("K"))
    if len(radtype) > 2:
        radtype[2] = retranslate_delimiter(radtype[2])
        return radtype
    else:
        return radtype


def make_report_text(cif, document: Document) -> ReferenceList:
    paragr = document.add_paragraph()
    paragr.style = document.styles['fliesstext']
    ref = ReferenceList(paragr)
    # -- The main text:
    paragr.add_run('The following text is only a suggestion: ').font.bold = True
    Crystallization(cif, paragr)
    CrystalSelection(cif, paragr)
    DataCollection(cif, paragr)
    SpaceChar(paragr).regular()
    MachineType(cif, paragr)
    DataReduction(cif, paragr, ref)
    SpaceChar(paragr).regular()
    SolveRefine(cif, paragr, ref)
    SpaceChar(paragr).regular()
    if cif.hydrogen_atoms_present:
        a = Atoms(cif, paragr)
        if a.n_isotropic_with_h != 0 and (a.n_isotropic_with_h > a.n_isotropic):
            Hydrogens(cif, paragr)
            SpaceChar(paragr).regular()
    if cif.disorder_present:
        Disorder(cif, paragr, ref)
    CCDC(cif, paragr, ref)
    SpaceChar(paragr).regular()
    FinalCifreport(paragr, ref)
    return ref
