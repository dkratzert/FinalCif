import unittest

from finalcif.cif.cif_file_io import CifContainer


class TestNosphera2(unittest.TestCase):
    """
    CIF files from Nosphera2 have no _atom_site_disorder_group. This test checks if the CIF is
    nevertheless readable.
    """

    def setUp(self) -> None:
        self.cif = CifContainer('test-data/nospera2.cif')

    def test_atoms(self):
        self.assertEqual("Atom(label='O1', type='O', x='0.282284(16)', y='0.56940(2)', "
                         "z='0.869432(5)', part='0', occ='1.000000', u_eq='0.02037(4)')",
                         str(list(self.cif.atoms())[0]))

    def test_natoms(self):
        self.assertEqual(9, self.cif.natoms())

    def test_natoms3(self):
        self.assertEqual("['O1', 'O', 0.282284, 0.5694, 0.869432, 0, 1.0, 0.02037]",
                         str(list(self.cif.atoms_fract)[0]))

    def test_atomic_struct_site(self):
        atom = self.cif.atomic_struct.sites
        self.assertEqual('<gemmi.SmallStructure.Site O1>', str(atom[0]))

    def test_atomic_struct_site_occ(self):
        atom = self.cif.atomic_struct.sites[0]
        self.assertEqual(1.0, atom.occ)

    def test_atomic_struct_site_disorder_group(self):
        atom = self.cif.atomic_struct.sites[0]
        self.assertEqual(0, atom.disorder_group)

    def test_atomic_struct_site_uiso(self):
        atom = self.cif.atomic_struct.sites[0]
        self.assertEqual(0.02037, atom.u_iso)

    def test_shelx_file(self):
        # Even though, this gives an empty string: -->
        self.assertEqual('', self.cif['_shelx_res_file'])
        self.assertEqual('TITL mo_1558 in P2(1)/n',
                         self.cif['_iucr_refine_instructions_details'].lstrip('\r\n')[:24].strip('\r\n'))

    def test_iucr_refine_instructions(self):
        # <-- We have res file data, because there is iucr_refine_instructions:
        self.assertEqual(''';
TITL mo_1558 in P2(1)/n
CELL 0.71073 10.3975 7.4''', self.cif.res_file_data.lstrip()[:50].strip('\r\n'))
