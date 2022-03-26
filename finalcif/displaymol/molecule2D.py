import sys
from collections import namedtuple
from math import sqrt
from typing import List, Union, Generator, Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent

from finalcif.cif.atoms import get_radius_from_element, element2color
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.misc import distance


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

    # flatten takes a 2-element list of coordinates. When interpreted as vectors,
    # these define a plane in 3-dim'l space
    def flatten(self, plane: List['Coordinate'] = None) -> Coordinate2D:
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


atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))


class MoleculeWidget(QtWidgets.QWidget):
    def __init__(self, shx_atoms: Generator[Any, Any, atom]):
        super().__init__()
        self.lastPos = None
        self.painter = None
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.atoms: List[Atom] = []
        for at in shx_atoms:
            self.atoms.append(Atom(at.x, at.y, at.z, at.label, at.type, at.part))
        self.connections = self.get_conntable_from_atoms()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.draw()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if (event.buttons() == Qt.LeftButton):
            setXRotation(xRot + 8 * dy)
            setYRotation(yRot + 8 * dx)
        self.lastPos = event.pos()

    # dimensions is 2-tuple of the number of characters on x and y axis
    def draw(self):
        self.painter.setPen(QPen(Qt.darkGray, 2, Qt.SolidLine))
        plane = [Coordinate(1, 0, 0), Coordinate(0, 1, 0)]
        max_extreme, min_extreme = self.molecule_dimensions(plane)
        span = max_extreme - min_extreme
        # make everything fit in our dimensions while maintaining proportions
        scale_factor = min((self.width() - 1) / span.x, (self.height() - 1) / span.y)
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
        for at1, at2 in self.connections:
            self.painter.drawLine(at1.screenx + 4, at1.screeny + 4, at2.screenx + 4, at2.screeny + 4)

    def draw_atoms(self):
        self.painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for atom in self.atoms:
            color = element2color.get(atom.type_)
            self.painter.setBrush(QBrush(QColor(color), Qt.SolidPattern))
            self.painter.drawEllipse(atom.screenx, atom.screeny, 9, 9)

    def molecule_dimensions(self, plane):
        flattened = [a.flatten(plane) for a in self.atoms]
        max_extreme = Coordinate2D(max([coor.x for coor in flattened]),
                                   max([coor.y for coor in flattened]))
        min_extreme = Coordinate2D(min([coor.x for coor in flattened]),
                                   min([coor.y for coor in flattened]))
        return max_extreme, min_extreme

    def get_conntable_from_atoms(self, extra_param: float = 0.48) -> list:
        """
        Returns a connectivity table from the atomic coordinates and the covalence
        radii of the atoms.
        a bond is defined with less than the sum of the covalence radii plus the extra_param:
        """
        connections = []
        # t1 = perf_counter()
        h = ('H', 'D')
        for num1, at1 in enumerate(self.atoms, 1):
            rad1 = get_radius_from_element(at1.type_)
            for num2, at2 in enumerate(self.atoms, 1):
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
                    # print(num1, num2, d)
                    # The extra time for this is not too much:
                    if [num2, num1] in connections:
                        continue
                    connections.append([at1, at2])
        # t2 = perf_counter()
        # print('Bondzeit:', round(t2-t1, 3), 's')
        # print('len:', len(conlist))
        return connections


if __name__ == "__main__":
    # Molecule(atoms).draw()
    app = QtWidgets.QApplication(sys.argv)
    # create our new Qt MainWindow
    window = QtWidgets.QMainWindow()
    # create our new custom VTK Qt widget
    # shx = Shelxfile()
    # shx.read_file('tests/examples/1979688-finalcif.res')
    # atoms = [x.cart_coords for x in shx.atoms]
    cif = CifContainer('tests/examples/1979688.cif')
    render_widget = MoleculeWidget(cif.atoms_orth)
    # add and show
    window.setCentralWidget(render_widget)
    window.setMinimumSize(500, 500)
    window.show()
    # start the event loop
    sys.exit(app.exec_())
