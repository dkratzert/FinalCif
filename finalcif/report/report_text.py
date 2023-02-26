import os
from builtins import str
from typing import Union, List

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
    SHELXDReference, SadabsTwinabsReference, CrysalisProReference, Nosphera2Reference, XDSReference
from finalcif.tools.misc import protected_space, angstrom, zero_width_space, remove_line_endings


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
    >>> clean_string('This is a sentence\\r with newline.')
    'This is a sentence with newline'
    >>> clean_string('')
    ''
    >>> clean_string('  This is  a sentence\\r with. newline.  ')
    'This is  a sentence with. newline'
    """
    return string \
        .replace('\n', '') \
        .replace('\r', '') \
        .replace('\t', '') \
        .replace('\f', '') \
        .replace('\0', '') \
        .strip(' ') \
        .strip('.')


def gstr(string: str) -> str:
    """
    Turn a string into a gemmi string and remove control characters.
    """
    return clean_string(gemmi.cif.as_string(string).strip("'"))


class FormatMixin():

    def bold(self, run: Run):
        r = run.bold = True
        return r


class ReportText():
    def __init__(self):
        pass


class Crystallization(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        self.crytsalization_method = gstr(self.cif['_exptl_crystal_recrystallization_method'])
        if not self.crytsalization_method:
            self.crytsalization_method = '[No crystallization method was given]'
        sentence = "The sample was crystallized {}. "
        self.text = sentence.format(remove_line_endings(retranslate_delimiter(self.crytsalization_method)))
        paragraph.add_run(retranslate_delimiter(self.text))


class CrstalSelection(FormatMixin):
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        temperature = gstr(self.cif['_diffrn_ambient_temperature'])
        if not temperature:
            temperature = '[No _diffrn_ambient_temperature given]'
        shape = gstr(self.cif['_exptl_crystal_description'])
        if not shape:
            shape = '[No _exptl_crystal_description given]'
        colour = gstr(self.cif['_exptl_crystal_colour'])
        crystal_mount = gstr(self.cif['_diffrn_measurement_specimen_support'])
        #adhesive = gstr(self.cif['_diffrn_measurement_specimen_adhesive'])
        #if not adhesive:
        #    adhesive = '[No _diffrn_measurement_specimen_adhesive given]'
        if not crystal_mount:
            crystal_mount = '[No _diffrn_measurement_specimen_support given]'
        method = 'shock-cooled '
        try:
            if float(temperature.split('(')[0]) > 200:
                method = ''
        except ValueError:
            method = ''
        txt_crystal = (f"A {colour}{', ' if colour else ''}{shape} shaped crystal of {self.cif.block.name} was mounted on a "
                       f"{crystal_mount} with perfluoroether oil. ")
        txt_data = (f"Data were collected from a {method}single crystal at {temperature}{protected_space}K ")
        paragraph.add_run(retranslate_delimiter(txt_crystal))
        Crystallization(cif, paragraph)
        paragraph.add_run(retranslate_delimiter(txt_data))


class MachineType():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        self.difftype = gstr(self.cif['_diffrn_measurement_device_type']) \
                        or '[No _diffrn_measurement_device_type given]'
        self.device = gstr(self.cif['_diffrn_measurement_device']) \
                      or '[No _diffrn_measurement_device given]'
        self.source = gstr(self.cif['_diffrn_source']).strip('\n\r') \
                      or '[No _diffrn_source given]'
        self.monochrom = gstr(self.cif['_diffrn_radiation_monochromator']) \
                         or '[No _diffrn_radiation_monochromator given]'
        if not self.monochrom:
            self.monochrom = '?'
        self.cooling = self._get_cooling_device(self.cif)
        self.rad_type = gstr(self.cif['_diffrn_radiation_type']) \
                        or '[No _diffrn_radiation_type given]'
        radtype = format_radiation(self.rad_type)
        self.wavelen = gstr(self.cif['_diffrn_radiation_wavelength']) \
                       or '[No _diffrn_radiation_wavelength given]'
        self.detector_type = ''
        detector_type = gstr(self.cif['_diffrn_detector_type']) \
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


class DataReduct():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        self.cif = cif
        integration = gstr(self.cif['_computing_data_reduction']) or '??'
        abstype = gstr(self.cif['_exptl_absorpt_correction_type']) or '??'
        abs_details = gstr(self.cif['_exptl_absorpt_process_details']) or '??'
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
        absdetails = cif['_exptl_absorpt_process_details'].replace('-', ' ')
        if 'SADABS' in absdetails.upper() or 'TWINABS' in absdetails.upper():
            #if len(absdetails.split()) > 1:
            #    version = absdetails.split()[1]
            #else:
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
        sentence = 'All data were integrated with {} and {} {} absorption correction using {} was applied.'
        txt = sentence.format(integration_prog,
                              get_inf_article(abstype),
                              abstype,
                              scale_prog)
        paragraph.add_run(retranslate_delimiter(txt))
        ref.append([data_reduct_ref, absorpt_ref])

    def add_saint_reference(self, integration):
        saintversion = 'unknown version'
        if len(integration.split()) > 1:
            saintversion = integration.split()[1]
        integration_prog = 'SAINT'
        data_reduct_ref = SAINTReference('SAINT', saintversion)
        return data_reduct_ref, integration_prog

    def add_crysalispro_reference(self, integration):
        year = 'unknown version'
        if len(integration.split()) > 3:
            year = integration.split()[4][:-1]
        version = 'unknown year'
        if len(integration.split()) >= 1:
            version = integration.split()[1][:-1]
        integration_prog = 'Crysalispro'
        data_reduct_ref = CrysalisProReference(version=version, year=year)
        absorpt_ref = CrysalisProReference(version=version, year=year)
        return data_reduct_ref, absorpt_ref, integration_prog


class SolveRefine():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        self.cif = cif
        refineref = DummyReference()
        solveref = DummyReference()
        solution_prog = gstr(self.cif['_computing_structure_solution']) or '??'
        solution_method = gstr(self.cif['_atom_sites_solution_primary']) or '??'
        if solution_prog.upper().startswith(('SHELXT', 'XT')):
            solveref = SHELXTReference()
        if 'SHELXS' in solution_prog.upper():
            solveref = SHELXSReference()
        if 'SHELXD' in solution_prog.upper():
            solveref = SHELXDReference()
        refined = gstr(self.cif['_computing_structure_refinement']) or '??'
        if refined.upper().startswith(('SHELXL', 'XL')):
            refineref = SHELXLReference()
        if 'OLEX' in refined.upper():
            refineref = Olex2Reference()
        if 'NOSPHERA2' in solution_prog.upper() or 'NOSPHERA2' in self.cif['_refine_special_details'].upper():
            refineref = Nosphera2Reference()
        refine_coef = gstr(self.cif['_refine_ls_structure_factor_coef'])
        sentence = r"The structure was solved by {} methods using {} and refined by full-matrix " \
                   "least-squares methods against "
        txt = sentence.format(solution_method.strip('\n\r'), solution_prog.split()[0])
        paragraph.add_run(retranslate_delimiter(txt))
        paragraph.add_run('F').font.italic = True
        if refine_coef.lower() == 'fsqd':
            paragraph.add_run('2').font.superscript = True
        paragraph.add_run(' by {}'.format(refined.split()[0]))
        shelxle = None
        if 'shelxle' in refined.lower() or 'shelxle' in self.cif['_computing_molecular_graphics'].lower():
            paragraph.add_run(' using ShelXle')
            shelxle = ShelXleReference()
        paragraph.add_run('.')
        ref.append([solveref, refineref, shelxle])


class Atoms():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        """
        Text for non-hydrogen atoms.
        """
        self.cif = cif
        n_isotropic = self.number_of_isotropic_atoms()
        number = 'All'
        parameter_type = 'anisotropic'
        if 0 < n_isotropic < self.cif.natoms(without_h=True):
            number = f'Some atoms ({n_isotropic}) were refined using isotropic displacement parameters.' \
                     ' All other'
        if n_isotropic > 0 and n_isotropic > self.cif.natoms(without_h=True):
            number = f'Most atoms ({n_isotropic}) were refined using isotropic displacement parameters.' \
                     ' All other'
        if n_isotropic == self.cif.natoms(without_h=True):
            number = 'All'
            parameter_type = 'isotropic'
        # TODO: test how many hydrogen atoms have ueq < -1.0 -> constrained or free refinement
        #                                                       of hydrogen displacement params
        # TODO: detect riding model of hydrogen atoms -> res file?
        sentence1 = f"{number} non-hydrogen atoms were refined with {parameter_type} displacement parameters. "
        paragraph.add_run(sentence1)

    def number_of_isotropic_atoms(self) -> Union[float, int]:
        isotropic_count = 0
        for site in self.cif.atomic_struct.sites:
            if self.atom_is_isotropic_and_not_hydrogen(site):
                isotropic_count += 1
        return isotropic_count

    @staticmethod
    def atom_is_isotropic_and_not_hydrogen(site):
        return not site.aniso.nonzero() and not site.element.is_hydrogen


class Hydrogens():
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        """
        The hydrogen atoms were refined isotropically on calculated positions using
        a riding model with their Uiso values constrained to 1.5 times the Ueq of
        their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other
        carbon atoms.
        """
        self.cif = cif
        hatoms: List[SHXAtom] = [x for x in self.cif.shx.atoms.all_atoms if x.is_hydrogen]
        n_hatoms = len(hatoms)
        n_anisotropic_h = len([x for x in hatoms if sum(x.uvals[1:]) > 0.0001])
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
    def __init__(self, cif: CifContainer, paragraph: Paragraph):
        self.cif = cif
        self.dsr_sentence = ''
        sentence1 = "Disordered moieties were refined using bond lengths " \
                    "restraints and displacement parameter restraints. "
        if self.cif.dsr_used:
            self.dsr_sentence = "Some parts of the disorder model were introduced by the " \
                                "program DSR."
        paragraph.add_run(sentence1)
        if self.dsr_sentence:
            paragraph.add_run(self.dsr_sentence)


class SpaceChar(object):
    def __init__(self, paragraph: Paragraph):
        self.p = paragraph

    def regular(self):
        self.p.add_run(' ')

    def porotected(self):
        self.p.add_run(protected_space)


class CCDC():
    def __init__(self, cif: CifContainer, paragraph: Paragraph, ref: ReferenceList):
        self.cif = cif
        ccdc_num = gstr(self.cif['_database_code_depnum_ccdc_archive']) or '??????'
        sentence1 = "Crystallographic data for the structures reported in this " \
                    "paper have been deposited with the Cambridge Crystallographic Data Centre."
        sentence2 = "CCDC {} contain the supplementary crystallographic data for this paper. " \
                    "These data can be obtained free of charge from The Cambridge Crystallographic Data Centre " \
                    "via www.ccdc.cam.ac.uk/{}structures.".format(ccdc_num, zero_width_space)
        paragraph.add_run(sentence1)
        ref.append(CCDCReference())
        SpaceChar(paragraph).regular()
        paragraph.add_run(sentence2)


class FinalCifreport():
    def __init__(self, paragraph: Paragraph, ref: ReferenceList):
        sentence = "This report and the CIF file were generated using FinalCif."
        paragraph.add_run(sentence)
        ref.append(FinalCifReference())


class RefinementDetails():
    def __init__(self, cif: CifContainer, document: Document):
        ph = document.add_paragraph(style='Heading 2')
        ph.add_run(text=fr"Refinement details for {cif.block.name}")
        p = document.add_paragraph()
        p.style = document.styles['fliesstext']
        text = ' '.join(cif['_refine_special_details'].splitlines(keepends=False))
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
