import math
import sys
from collections import namedtuple
from math import sqrt
from typing import List, Union, Generator, Any, Tuple

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPalette

from finalcif.cif.atoms import get_radius_from_element, element2color
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.misc import distance

"""
A 2D molecule drawing widget. The idea was taken from this molecule viewer for ascii drawing of molecules:
https://github.com/des4maisons/molecule-viewer
Additionally the rotation method from https://github.com/TheAlgorithms/Python was added.
"""
atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))


class MoleculeWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.atoms_size = 10
        self.bond_width = 3
        self.labels = False
        #
        self.lastPos = None
        self.painter = None
        self.x_rot = 0
        self.y_rot = 0
        #
        pal = QPalette()
        pal.setColor(QPalette.Window, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.atoms: List[Atom] = []
        self.connections = ()

    def open_molecule(self, atoms: Generator[Any, Any, atom], labels=False):
        self.labels = labels
        self.atoms.clear()
        for at in atoms:
            self.atoms.append(Atom(at.x, at.y, at.z, at.label, at.type, at.part))
        self.connections = self.get_conntable_from_atoms()
        self.update()

    def paintEvent(self, event):
        if self.atoms:
            self.painter = QPainter(self)
            self.draw()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        dx = (event.x() - self.lastPos.x()) / 50
        dy = (event.y() - self.lastPos.y()) / 50
        if (event.buttons() == Qt.LeftButton):
            for num, at in enumerate(self.atoms):
                x, y, z = self.rotate(at.coordinate.x, at.coordinate.y, at.coordinate.z, 'y', -dx)
                x, y, z = self.rotate(x, y, z, 'x', dy)
                self.atoms[num] = Atom(x, y, z, at.name, at.type_, at.part)
            self.update()
        self.lastPos = event.pos()

    def draw(self):
        self.painter.setPen(QPen(Qt.gray, self.bond_width, Qt.SolidLine))
        plane = [Coordinate(1, 0, 0), Coordinate(0, 1, 0)]
        max_extreme, min_extreme = self.molecule_dimensions(plane)
        span = max_extreme - min_extreme
        # make everything fit in our dimensions while maintaining proportions
        scale_factor = min((self.width() - 30) / span.x, (self.height() - 30) / span.y)
        # Makes sure the atom size dooes not vary too much:
        self.atoms_size = int(12 * (scale_factor / 25))
        extra_space = Coordinate2D(self.width() - 1, self.height() - 1) - span * scale_factor
        offset = extra_space / 2
        for atom in self.atoms:
            # shift to be in the 1st quadrant (positive coordinates) close to (0,0)
            screen_index = (atom.flatten(plane) - min_extreme) * scale_factor
            screen_index = screen_index + offset
            atom.screenx = int(screen_index.x)
            atom.screeny = int(screen_index.y)
        self.draw_bonds()
        self.draw_atoms()
        self.painter.end()

    def draw_bonds(self):
        offset = int(self.atoms_size / 2)
        for n1, n2 in self.connections:
            at1 = self.atoms[n1]
            at2 = self.atoms[n2]
            self.painter.drawLine(at1.screenx + offset, at1.screeny + offset,
                                  at2.screenx + offset, at2.screeny + offset)

    def draw_atoms(self):
        for atom in self.atoms:
            if self.labels and atom.type_ not in ('H', 'D'):
                self.painter.setPen(QPen(QColor(150, 50, 5), 2, Qt.SolidLine))
                self.painter.drawText(atom.screenx + 9, atom.screeny - 1, atom.name)
            self.painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            color = element2color.get(atom.type_)
            self.painter.setBrush(QBrush(QColor(color), Qt.SolidPattern))
            self.painter.drawEllipse(int(atom.screenx), int(atom.screeny), int(self.atoms_size), int(self.atoms_size))

    def molecule_dimensions(self, plane):
        flattened = [a.flatten(plane) for a in self.atoms]
        max_extreme = Coordinate2D(max([coor.x for coor in flattened]),
                                   max([coor.y for coor in flattened]))
        min_extreme = Coordinate2D(min([coor.x for coor in flattened]),
                                   min([coor.y for coor in flattened]))
        return max_extreme, min_extreme

    def get_conntable_from_atoms(self, extra_param: float = 0.48) -> tuple:
        """
        Returns a connectivity table from the atomic coordinates and the covalence
        radii of the atoms.
        a bond is defined with less than the sum of the covalence radii plus the extra_param:
        """
        connections = []
        h = ('H', 'D')
        for num1, at1 in enumerate(self.atoms, 0):
            rad1 = get_radius_from_element(at1.type_)
            for num2, at2 in enumerate(self.atoms, 0):
                if at1.part * at2.part != 0 and at1.part != at2.part:
                    continue
                if at1.name == at2.name:  # name1 = name2
                    continue
                d = distance(at1.coordinate.x, at1.coordinate.y, at1.coordinate.z,
                             at2.coordinate.x, at2.coordinate.y, at2.coordinate.z)
                if d > 4.0:  # makes bonding faster (longer bonds do not exist)
                    continue
                rad2 = get_radius_from_element(at2.type_)
                if (rad1 + rad2) + extra_param > d:
                    if at1.type_ in h and at2.type_ in h:
                        continue
                    # The extra time for this is not too much:
                    if (num2, num1) in connections:
                        continue
                    connections.append([num1, num2])
        return tuple(connections)

    def rotate(self, x: float, y: float, z: float, axis: str, angle: float) -> Tuple[float, float, float]:
        """
        rotate a point around a certain axis with a certain angle
        angle can be any integer between 1, 360 and axis can be any one of
        'x', 'y', 'z'

        Method taken from https://github.com/TheAlgorithms/Python
        __version__ = "2020.9.26"
        __author__ = "xcodz-dot, cclaus, dhruvmanila"
        # License: MIT
        """
        if not isinstance(axis, str):
            raise TypeError("Axis must be a str")
        # angle = (angle % 360) / 450 * 180 / math.pi
        if axis == "z":
            new_x = x * math.cos(angle) - y * math.sin(angle)
            new_y = y * math.cos(angle) + x * math.sin(angle)
            new_z = z
        elif axis == "x":
            new_y = y * math.cos(angle) - z * math.sin(angle)
            new_z = z * math.cos(angle) + y * math.sin(angle)
            new_x = x
        elif axis == "y":
            new_x = x * math.cos(angle) - z * math.sin(angle)
            new_z = z * math.cos(angle) + x * math.sin(angle)
            new_y = y
        else:
            raise ValueError("not a valid axis, choose one of 'x', 'y', 'z'")
        return new_x, new_y, new_z


class Coordinate2D(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __mul__(self, const: Union[int, float]):
        return Coordinate2D(self.x * const, self.y * const)

    def __add__(self, coor: 'Coordinate2D'):
        return Coordinate2D(self.x + coor.x, self.y + coor.y)

    def __sub__(self, coor: 'Coordinate2D'):
        return self + coor * (-1)

    def __truediv__(self, const: Union[int, float]):
        return self * (1 / const)

    def __repr__(self):
        return "(%.02f, %.02f)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()


class Atom(object):
    def __init__(self, x: float, y: float, z: float, name: str, type_: str, part: int):
        self.coordinate = Coordinate(x, y, z)
        self.name = name
        self.part = part
        self.type_ = type_
        self.screenx = None
        self.screeny = None
        # TODO: atom type to color conversion

    def __repr__(self) -> str:
        return str((self.name, self.type_, self.coordinate))

    def __str__(self) -> str:
        return self.__repr__()

    def flatten(self, plane: List['Coordinate'] = None) -> Coordinate2D:
        return self.coordinate.flatten(plane)


class Coordinate(object):
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = [x, y, z]

    def __repr__(self) -> str:
        return "({:.02f}, {:.02f}, {:.02f})".format(self.x, self.y, self.z)

    def __str__(self) -> str:
        return self.__repr__()

    def __truediv__(self, const: Union[int, float]) -> 'Coordinate':
        return self * (1 / const)

    def __mul__(self, const: Union[int, float]) -> 'Coordinate':
        return Coordinate(self.x * const, self.y * const, self.z * const)

    def __add__(self, coor: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + coor.x, self.y + coor.y, self.z + coor.z)

    # regular dot product
    def dot(self, vector) -> float:
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def length(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    # project self onto 'onto'
    def project(self, onto: 'Coordinate') -> 'Coordinate':
        length = onto.length()
        scale_factor = self.dot(onto) / (length ** 2)
        return onto * scale_factor

    # cross product
    def cross(self, vector: 'Coordinate') -> 'Coordinate':
        a1, a2, a3 = [self.x, self.y, self.z]
        b1, b2, b3 = [vector.x, vector.y, vector.z]
        return Coordinate(a2 * b3 - a3 * b2,
                          a3 * b1 - a1 * b3,
                          a1 * b2 - a2 * b1)

    def flatten(self, plane: List['Coordinate'] = None) -> Coordinate2D:
        """
        flatten takes a 2-element list of coordinates. When interpreted as vectors,
        these define a plane in 3-dim'l space
        """
        if plane is None:  # defaults to x-y plane
            plane = [Coordinate(1, 0, 0), Coordinate(0, 1, 0)]
        # copy the list
        plane = list(plane)
        # get 2 perpendicular vectors that define the same plane
        perp = plane[0].cross(plane[1])
        plane[0] = perp.cross(plane[1])
        # make them unit vectors
        plane[0] = plane[0] / (plane[0].length())
        plane[1] = plane[1] / (plane[1].length())
        proj0 = self.project(plane[0])
        proj1 = self.project(plane[1])
        ratio0 = None
        ratio1 = None
        # the (signed) number of times the unit vector fits into the projection
        # is the 2 dimensional coordinate we want
        # so (2,0) == 2 * (1,0), 2 is what we want. don't divide by zero.
        for component in ["x", "y", "z"]:
            val = getattr(plane[0], component)
            if val != 0:
                ratio0 = getattr(proj0, component) / val
            val = getattr(plane[1], component)
            if val != 0:
                ratio1 = getattr(proj1, component) / val
        if ratio0 is None or ratio1 is None:  # if either are 0
            raise ValueError("plane defined with zero vector")
        return Coordinate2D(ratio0, ratio1)


if __name__ == "__main__":
    # Molecule(atoms).draw()
    app = QtWidgets.QApplication(sys.argv)
    # create our new Qt MainWindow
    window = QtWidgets.QMainWindow()
    # create our new custom VTK Qt widget
    # shx = Shelxfile()
    # shx.read_file('tests/examples/1979688-finalcif.res')
    # atoms = [x.cart_coords for x in shx.atoms]
    # cif = CifContainer('test-data/p21c.cif')
    cif = CifContainer('tests/examples/1979688.cif')
    # cif = CifContainer('/Users/daniel/Documents/GitHub/StructureFinder/test-data/668839.cif')
    render_widget = MoleculeWidget(None)
    render_widget.open_molecule(cif.atoms_orth, labels=True)
    # add and show
    window.setCentralWidget(render_widget)
    window.setMinimumSize(500, 500)
    window.show()
    # start the event loop
    sys.exit(app.exec_())
