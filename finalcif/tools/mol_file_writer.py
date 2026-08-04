from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from fastmolwidget.atoms import get_radius_from_element
from fastmolwidget.sdm import SDM

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from finalcif.cif.cif_file_io import CifContainer

HYDROGEN = frozenset({'H', 'D'})
MAX_BOND_LENGTH = 4.0


class CartesianAtom(Protocol):
    """An atom with orthogonal (Cartesian) coordinates in Angstrom."""
    label: str
    type: str
    x: float
    y: float
    z: float
    part: int


class MolFile:
    """
    This mol file writer is only to use the file with Miew or JSmol, not to implement the standard exactly!
    """

    def __init__(self, quoted: bool = False):
        self.quoted = quoted
        self.bondscount = 0
        self.atomscount = 0
        self.atoms_string = ''
        self.bonds_string = ''

    def load_from_atoms(self, atoms: Iterable[CartesianAtom]) -> str:
        atom_list = list(atoms)
        bonds = self._connection_table(atom_list)
        self.atomscount = len(atom_list)
        self.bondscount = len(bonds)
        self.atoms_string = self._get_atoms_string(atom_list)
        self.bonds_string = self._get_bonds_string(bonds)
        return self.make_mol()

    def atomscount_bondscount(self) -> str:
        return f"{self.atomscount:>5d}{self.bondscount:>5d} 0 0 0"

    def _get_atoms_string(self, atoms: Sequence[CartesianAtom]) -> str:
        """
        Returns a string with an atom in each line.
        1 C          -0.7600    1.1691   -0.0005 C.ar    1  BENZENE       0.000
        """
        return '\n'.join(
            f"{num:>6d} {at.label:<4s} {at.x:>10.4f}{at.y:>10.4f}{at.z:>10.4f} {at.type:<6s} 1  NONAME  0.000"
            for num, at in enumerate(atoms, 1)
        )

    def _get_bonds_string(self, bonds: Sequence[tuple[int, int]]) -> str:
        """
        This is not accordingly to the file standard!
        The standard wants to have fixed format 3 digits for the bonds.
        """
        return '\n'.join(f"{num:>4d} {bo[0]:>4d} {bo[1]:>4d}  1" for num, bo in enumerate(bonds, 1))

    def _connection_table(self, atoms: Sequence[CartesianAtom],
                          extra_param: float = 0.48) -> list[tuple[int, int]]:
        """
        Returns a connectivity table from the atomic coordinates and the covalence radii of the atoms.
        A bond is defined with less than the sum of the covalence radii plus the extra_param.

        :param extra_param: additional distance to the sum of the covalence radii
        """
        radii = [get_radius_from_element(at.type) for at in atoms]
        parts = [_as_int(at.part) for at in atoms]
        is_hydrogen = [at.type in HYDROGEN for at in atoms]
        max_dist_squared = MAX_BOND_LENGTH ** 2
        bonds = []
        for num1, at1 in enumerate(atoms):
            for num2 in range(num1 + 1, len(atoms)):
                at2 = atoms[num2]
                if is_hydrogen[num1] and is_hydrogen[num2]:
                    continue
                if parts[num1] * parts[num2] != 0 and parts[num1] != parts[num2]:
                    continue
                dist_squared = (at1.x - at2.x) ** 2 + (at1.y - at2.y) ** 2 + (at1.z - at2.z) ** 2
                # makes bonding faster (longer bonds do not exist):
                if dist_squared > max_dist_squared:
                    continue
                if (radii[num1] + radii[num2] + extra_param) ** 2 > dist_squared:
                    bonds.append((num1 + 1, num2 + 1))
        return bonds

    def footer(self) -> str:
        return ""

    def make_mol(self) -> str:
        """
        Combines all above to a mol file.
        """
        header = ('# Bruker molecule file\n'
                  '@<TRIPOS>MOLECULE\n'
                  'noname')
        # Quote for javascript:
        quote = '`' if self.quoted else ''
        return (f"{quote}\n"
                f"{header}\n"
                f"{self.atomscount_bondscount()}\n"
                f"SMALL\n"
                f"NO_CHARGES\n"
                f"****\n\n"
                f"@<TRIPOS>ATOM\n"
                f"{self.atoms_string}\n"
                f"@<TRIPOS>BOND\n"
                f"{self.bonds_string}\n"
                f"{self.footer()}"
                f"{quote}\n")


def _as_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _make_sdm(cif: CifContainer) -> SDM | None:
    atoms_fract = tuple(cif.atoms_fract)
    if not atoms_fract or not cif.cell.a:
        return None
    return SDM(atoms_fract, cif.symmops, cif.cell[:6], centric=cif.is_centrosymm)


def grown_atoms(cif: CifContainer) -> list[CartesianAtom]:
    """Atoms of the asymmetric unit expanded by symmetry to complete molecules."""
    sdm = _make_sdm(cif)
    if sdm is None:
        return []
    return sdm.packer(sdm, sdm.calc_sdm())


def packed_cell_atoms(cif: CifContainer) -> list[CartesianAtom]:
    """All symmetry equivalent atoms packed into one unit cell."""
    sdm = _make_sdm(cif)
    if sdm is None:
        return []
    return sdm.pack_unit_cell()


def mol_from_asymmetric_unit(cif: CifContainer, quoted: bool = False) -> str:
    """A mol file of the atoms as they are in the CIF file."""
    return MolFile(quoted=quoted).load_from_atoms(cif.atoms_orth)


def mol_from_grown_atoms(cif: CifContainer, quoted: bool = False) -> str:
    """A mol file of the symmetry completed molecules."""
    return MolFile(quoted=quoted).load_from_atoms(grown_atoms(cif))


def mol_from_packed_cell(cif: CifContainer, quoted: bool = False) -> str:
    """A mol file of the packed unit cell."""
    return MolFile(quoted=quoted).load_from_atoms(packed_cell_atoms(cif))
