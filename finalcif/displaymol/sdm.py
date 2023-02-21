# -*- encoding: utf-8 -*-
# möp
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <dkratzert@gmx.de> wrote this file. As long as you retain
# this notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy me a beer in return.
# Daniel Kratzert
# ----------------------------------------------------------------------------
#


import time
from collections import namedtuple
from math import sqrt, cos, radians, sin
from typing import List, Tuple

from finalcif.cif.atoms import get_radius_from_element
from finalcif.tools.dsrmath import Array, SymmetryElement, Matrix, frac_to_cart

DEBUG = False
Atomtuple = namedtuple('Atomtuple', 'label, type, x, y, z, part')


class SymmCards():
    """
    Contains the list of SYMM cards
    """

    def __init__(self):
        self._symmcards = [SymmetryElement(['X', 'Y', 'Z'])]

    def _as_str(self) -> str:
        return "\n".join([str(x) for x in self._symmcards])

    def __repr__(self) -> str:
        return self._as_str()

    def __str__(self) -> str:
        return self._as_str()

    def __getitem__(self, item):
        return self._symmcards[item]

    def __iter__(self):
        for x in self._symmcards:
            yield x

    def __len__(self):
        return len(self._symmcards)

    def append(self, symmData: list) -> None:
        """
        Add the content of a Shelxl SYMM command to generate the appropriate SymmetryElement instance.
        :param symmData: list of strings. eg.['1/2+X', '1/2+Y', '1/2+Z']
        :return: None
        """
        newSymm = SymmetryElement(symmData)
        if not newSymm in self._symmcards:
            self._symmcards.append(newSymm)


class SDMItem(object):
    __slots__ = ['dist', 'atom1', 'atom2', 'a1', 'a2', 'symmetry_number', 'covalent', 'dddd']

    def __init__(self):
        self.dist = 0.0
        self.atom1 = None
        self.a1 = 0
        self.atom2 = None
        self.a2 = 0
        self.symmetry_number = 0
        self.covalent = True
        self.dddd = 0

    def __lt__(self, a2) -> bool:
        return True if self.dist < a2.dist else False

    def __eq__(self, other: 'SDMItem') -> bool:
        if other.a1 == self.a2 and other.a2 == self.a1:
            return True
        return False

    def __repr__(self):
        return '{} {} {} {} dist: {} coval: {} sn: {} {}'.format(self.atom1.name, self.atom2.name, self.a1, self.a2,
                                                                 self.dist, self.covalent,
                                                                 self.symmetry_number, self.dddd)


class SDM():
    sdm_list: List[SDMItem]

    def __init__(self, atoms: Tuple[List], symmlist: list, cell: Tuple[float, float, float, float, float, float],
                 centric=False):
        """
        Calculates the shortest distance matrix
                        0      1      2  3  4   5     6          7
        :param atoms: [Name, Element, X, Y, Z, Part, ocuupancy, molindex -> (later)]
        :param symmlist:
        :param cell:
        """
        self.atoms = atoms
        self.symmcards = SymmCards()
        if centric:
            self.symmcards.append(['-X', '-Y', '-Z'])
            self.symmcards[-1].centric = True
        for s in symmlist:
            self.symmcards.append(s.split(','))
        self.cell = cell
        self.cosal = cos(radians(cell[3]))
        self.cosbe = cos(radians(cell[4]))
        self.cosga = cos(radians(cell[5]))
        self.aga = self.cell[0] * self.cell[1] * self.cosga
        self.bbe = self.cell[0] * self.cell[2] * self.cosbe
        self.cal = self.cell[1] * self.cell[2] * self.cosal
        self.asq = self.cell[0] ** 2
        self.bsq = self.cell[1] ** 2
        self.csq = self.cell[2] ** 2
        self.sdm_list = []  # list of sdmitems
        self.maxmol = 1
        self.sdmtime = 0

    def orthogonal_matrix(self):
        """
        Converts von fractional to cartesian by .
        Invert the matrix to do the opposite.
        """
        return Matrix([[self.cell[0], self.cell[1] * cos(self.cell[5]), self.cell[2] * cos(self.cell[4])],
                       [0, self.cell[1] * sin(self.cell[5]),
                        (self.cell[2] * (cos(self.cell[3]) - cos(self.cell[4]) * cos(self.cell[5])) / sin(
                            self.cell[5]))],
                       [0, 0, self.cell[6] / (self.cell[0] * self.cell[1] * sin(self.cell[5]))]])

    def calc_sdm(self) -> list:
        t1 = time.perf_counter()
        h = {'H', 'D'}
        nlen = len(self.symmcards)
        at2_plushalf = [Array([j + 0.5 for j in x[2:5]]) for x in self.atoms]
        for i, at1 in enumerate(self.atoms):
            prime_array = [Array(at1[2:5]) * symop.matrix + symop.trans for symop in self.symmcards]
            for j, at2 in enumerate(self.atoms):
                mind = 1000000
                hma = False
                atp = at2_plushalf[j]
                sdm_item = SDMItem()
                for n in range(nlen):
                    D = prime_array[n] - atp
                    dp = [v - 0.5 for v in D - D.floor]
                    dk = self.vector_length(*dp)
                    if n:
                        dk += 0.0001
                    if dk > 4.0:
                        continue
                    if (dk > 0.01) and (mind >= dk):
                        mind = min(dk, mind)
                        sdm_item.dist = mind
                        sdm_item.atom1 = at1
                        sdm_item.atom2 = at2
                        sdm_item.a1 = i
                        sdm_item.a2 = j
                        sdm_item.symmetry_number = n
                        hma = True
                if not sdm_item.atom1:
                    # Do not grow grown atoms:
                    continue
                if (sdm_item.atom1[1] not in h and sdm_item.atom2[1] not in h) and \
                    sdm_item.atom1[5] * sdm_item.atom2[5] == 0 or sdm_item.atom1[5] == sdm_item.atom2[5]:
                    dddd = (get_radius_from_element(at1[1]) + get_radius_from_element(at2[1])) * 1.2
                    sdm_item.dddd = dddd
                else:
                    dddd = 0.0
                if sdm_item.dist < dddd:
                    if hma:
                        sdm_item.covalent = True
                else:
                    sdm_item.covalent = False
                if hma:
                    self.sdm_list.append(sdm_item)
        t2 = time.perf_counter()
        self.sdmtime = t2 - t1
        print('Time for sdm:', round(self.sdmtime, 3), 's')
        self.sdm_list.sort()
        self.calc_molindex(self.atoms)
        need_symm = self.collect_needed_symmetry()
        if DEBUG:
            print("The asymmetric unit contains {} fragments.".format(self.maxmol))
        return need_symm

    def collect_needed_symmetry(self) -> list:
        need_symm = []
        h = ('H', 'D')
        # Collect needsymm list:
        for sdm_item in self.sdm_list:
            if sdm_item.covalent:
                if sdm_item.atom1[-1] < 1 or sdm_item.atom1[-1] > 6:
                    continue
                for n, symop in enumerate(self.symmcards):
                    if sdm_item.atom1[5] * sdm_item.atom2[5] != 0 and \
                        sdm_item.atom1[5] != sdm_item.atom2[5]:
                        continue
                    # Both the same atomic number and number 0 (hydrogen)
                    if sdm_item.atom1[1] == sdm_item.atom2[1] and sdm_item.atom1[1] in h:
                        continue
                    prime = Array(sdm_item.atom1[2:5]) * symop.matrix + symop.trans
                    D = prime - Array(sdm_item.atom2[2:5]) + Array([0.5, 0.5, 0.5])
                    floorD = D.floor
                    dp = D - floorD - Array([0.5, 0.5, 0.5])
                    if n == 0 and Array([0, 0, 0]) == floorD:
                        continue
                    dk = self.vector_length(*dp)
                    dddd = sdm_item.dist + 0.2
                    if sdm_item.atom1[1] in h and sdm_item.atom2[1] in h:
                        dddd = 1.8
                    if (dk > 0.001) and (dddd >= dk):
                        bs = [n + 1, (5 - floorD[0]), (5 - floorD[1]), (5 - floorD[2]), sdm_item.atom1[-1]]
                        if bs not in need_symm:
                            need_symm.append(bs)
        return need_symm

    def calc_molindex(self, all_atoms):
        # Start for George's "bring atoms together algorithm":
        someleft = 1
        nextmol = 1
        for at in all_atoms:
            at.append(-1)
        all_atoms[0][-1] = 1
        while nextmol:
            someleft = 1
            nextmol = 0
            while someleft:
                someleft = 0
                for sdm_item in self.sdm_list:
                    if sdm_item.covalent and sdm_item.atom1[-1] * sdm_item.atom2[-1] < 0:
                        sdm_item.atom1[-1] = self.maxmol  # last item is the molindex
                        sdm_item.atom2[-1] = self.maxmol
                        someleft += 1
            for ni, at in enumerate(all_atoms):
                if at[-1] < 0:
                    nextmol = ni
                    break
            if nextmol:
                self.maxmol += 1
                all_atoms[nextmol][-1] = self.maxmol

    def vector_length(self, x: float, y: float, z: float) -> float:
        """
        Calculates the vector length given in fractional coordinates.
        """
        A = 2.0 * (x * y * self.aga + x * z * self.bbe + y * z * self.cal)
        return sqrt(x ** 2 * self.asq + y ** 2 * self.bsq + z ** 2 * self.csq + A)

    def packer(self, sdm: 'SDM', need_symm: list, with_qpeaks=False) -> List[Atomtuple]:
        """
        Packs atoms of the asymmetric unit to real molecules.
        """
        showatoms = list(self.atoms)
        new_atoms = []
        for symm in need_symm:
            s, h, k, l, symmgroup = symm
            h -= 5
            k -= 5
            l -= 5
            s -= 1
            for atom in self.atoms:
                if atom[-1] == symmgroup:
                    coords = Array(atom[2:5]) * self.symmcards[s].matrix \
                             + Array(self.symmcards[s].trans) + Array([h, k, l])
                    # The new atom:
                    new = [atom[0], atom[1]] + list(coords) + [atom[5], atom[6], atom[7], 'symmgen']
                    new_atoms.append(new)
                    isthere = False
                    # Only add atom if its occupancy (new[5]) is greater zero:
                    if new[5] >= 0:
                        for atom in showatoms:
                            if atom[5] != new[5]:
                                continue
                            length = sdm.vector_length(new[2] - atom[2],
                                                       new[3] - atom[3],
                                                       new[4] - atom[4])
                            if length < 0.2:
                                isthere = True
                    if not isthere:
                        showatoms.append(new)
        cart_atoms = []
        cell = self.cell[:6]
        for at in showatoms:
            x, y, z = frac_to_cart([at[2], at[3], at[4]], cell)
            cart_atoms.append(Atomtuple(label=at[0], type=at[1], x=x, y=y, z=z, part=at[5]))
        return cart_atoms


def make_molecule(cif: 'CifContainer') -> List[Atomtuple]:
    atoms = tuple(cif.atoms_fract)
    sdm = SDM(atoms, cif.symmops, cif.cell[:6], centric=cif.is_centrosymm)
    needsymm = sdm.calc_sdm()
    atoms = sdm.packer(sdm, needsymm)
    return atoms


if __name__ == "__main__":
    from pathlib import Path
    from molecule2D import display
    from pathlib import Path
    from finalcif.cif.cif_file_io import CifContainer

    cif = CifContainer(Path('test-data/4060314.cif'))
    atoms = make_molecule(cif)
    display(atoms)
