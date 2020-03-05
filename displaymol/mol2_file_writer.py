"""

8 @<TRIPOS>MOLECULE
9 benzene
10 12 12 1 0 0
11 SMALL
12 NO_CHARGES
13
14
15 @<TRIPOS>ATOM
16 1 C1 1.207 2.091 0.000 C.ar 1 BENZENE0.000
17 2 C2 2.414 1.394 0.000 C.ar 1 BENZENE0.000
18 3 C3 2.414 0.000 0.000 C.ar 1 BENZENE0.000
19 4 C4 1.207 -0.697 0.000 C.ar 1 BENZENE0.000
20 5 C5 0.000 0.000 0.000 C.ar 1 BENZENE0.000
21 6 C6 0.000 1.394 0.000 C.ar 1 BENZENE0.000
22 7 H1 1.207 3.175 0.000 H 1 BENZENE0.000
23 8 H2 3.353 1.936 0.000 H 1 BENZENE0.000
24 9 H3 3.353 -0.542 0.000 H 1 BENZENE0.000
25 10 H4 1.207 -1.781 0.000 H 1 BENZENE0.000
26 11 H5 -0.939 -0.542 0.000 H 1 BENZENE0.000
27 12 H6 -0.939 1.936 0.000 H 1 BENZENE0.000
28 @<TRIPOS>BOND
29 1 1 2 ar
30 2 1 6 ar
31 3 2 3 ar
32 4 3 4 ar
33 5 4 5 ar
34 6 5 6 ar
35 7 1 7 1
36 8 2 8 1
37 9 3 9 1
38 10 4 10 1
39 11 5 11 1
40 12 6 12 1
41 @<TRIPOS>SUBSTRUCTURE
42 1 BENZENE1 PERM 0 **** **** 0 ROOT
"""
import os

from searcher import misc
from searcher.atoms import get_radius_from_element
from searcher.database_handler import StructureTable


class MolFile():
    """
    This mol2 file writer is only to use the file with JSmol, not to implement the standard completely!
    """
    def __init__(self, id: str, db: StructureTable):
        self.db = db
        self.atoms = self.db.get_atoms_table(id, cartesian=True)
        self.bonds = self.get_conntable_from_atoms()
        self.bondscount = len(self.bonds)
        self.atomscount = len(self.atoms)

    def header(self) -> str:
        """
        For JSmol, I don't need a facy header.
        """
        return "{}{}{}".format(os.linesep, os.linesep, os.linesep)

    def connection_table(self) -> str:
        """
        num_atoms [num_bonds [num_subst [num_feat [num_sets]]]]
        """
        tab = " {0}  {1}  1  0  0\nSMALL\nNO_CHARGES\n\n".format(self.atomscount, self.bondscount)
        return tab

    def get_atoms_string(self) -> str:
        """
        Returns a string with an atom in each line.
        atom_id atom_name x y z atom_type [subst_id [subst_name [charge [status_bit]]]]
             1 Ga1      6.3692  11.7421   4.8631   Ga        1 RES1   0.0000
        """
        atoms = []
        for num, at in enumerate(self.atoms, 1):
            x = at[2]
            y = at[3]
            z = at[4]
            element = at[1]
            name = at[0]
            atoms.append(" {} {} {:>9.5f} {:>9.5f} {:>9.5f} {:<2s}  1".format(num, name, x, y, z, element))
        return '\n'.join(atoms)

    def get_bonds_string(self) -> str:
        """
        bond_id  origin_atom_id  target_atom_id  bond_type [status_bits]
        """
        blist = []
        for num, bo in enumerate(self.bonds, 1):
            blist.append("{} {:>6d} {:>6d}  1  ".format(num, bo[0], bo[1]))
        return '\n'.join(blist)

    def get_conntable_from_atoms(self, extra_param = 0.16):
        """
        returns a connectivity table from the atomic coordinates and the covalence
        radii of the atoms.
        TODO:
        - read FREE command from db to contro binding here.
        :param cart_coords: cartesian coordinates of the atoms
        :type cart_coords: list
        :param atom_types: Atomic elements
        :type atom_types: list of strings
        :param atom_names: atom name in the file like C1
        :type atom_names: list of strings
        """
        conlist = []
        for num1, at1 in enumerate(self.atoms, 1):
            name1 = at1[0]
            radius1 = get_radius_from_element(at1[1])
            x1 = at1[2]
            y1 = at1[3]
            z1 = at1[4]
            for num2, at2 in enumerate(self.atoms, 1):
                name2 = at2[0]
                radius2 = get_radius_from_element(at2[1])
                x2 = at2[2]
                y2 = at2[3]
                z2 = at2[4]
                if name1 == name2:
                    continue
                d = misc.distance(x1, y1, z1, x2, y2, z2)
                # a bond is defined with less than the sum of the covalence
                # radii plus the extra_param:
                if d <= (radius1 + radius2) + extra_param and d > (radius1 or radius2):
                    conlist.append([num1, num2])
                    #print(num1, num2, d)
                    if len(conlist) == 99:
                        return conlist
                    if [num2, num1] or [num1, num2] in conlist:
                        continue
        return conlist

    def footer(self) -> str:
        """
        """
        return "\n"

    def make_mol(self):
        """
        """
        header = '@<TRIPOS>MOLECULE\nfoobar'
        connection_table = self.connection_table()
        atoms = self.get_atoms_string()
        bonds = self.get_bonds_string()
        footer = self.footer()
        mol = "{0}{5}{1}@<TRIPOS>ATOM{5}{2}{5}@<TRIPOS>BOND{3}{5}{4}".format(header,            # 0
                                                                          connection_table,  # 1
                                                                          atoms,             # 2
                                                                          bonds,             # 3
                                                                          footer,            # 4
                                                                          '\n')              # 5
        return mol