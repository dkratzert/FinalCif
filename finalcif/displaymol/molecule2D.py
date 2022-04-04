import math
import sys
from collections import namedtuple
from math import cos, sin
from pathlib import Path
from typing import List, Generator, Any, Union

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPalette, QImage, QResizeEvent

from finalcif.cif.atoms import get_radius_from_element, element2color
from finalcif.cif.cif_file_io import CifContainer

# from finalcif.tools.misc import distance

"""
A 2D molecule drawing widget. The idea was taken from this molecule viewer for ascii drawing of molecules:
https://github.com/des4maisons/molecule-viewer
Additionally the rotation method from https://github.com/TheAlgorithms/Python was added.
"""
atom = namedtuple('Atom', ('label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'))


class MoleculeWidget(QtWidgets.QWidget):
    painter: QPainter

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.factor = None
        self.atoms_size = 12
        self.bond_width = 2
        self.labels = False
        self.molecule_center = np.array([0, 0, 0])
        self.molecule_radius = 10
        #
        self.lastPos = self.pos()
        self.painter = Union[None, QPainter]
        self.x_angle = 0
        self.y_angle = 0
        #
        pal = QPalette()
        pal.setColor(QPalette.Window, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.atoms: List['Atom'] = []
        self.connections = ()
        # Takes all atoms and bonds
        self.objects = []
        self.screen_center = [self.width() / 2, self.height() / 2]
        self.projection_matrix = np.matrix([[1, 0, 0],
                                            [0, 1, 0]], dtype=np.float32)
        self.projected_points = []
        self.zoom = 1.0

    def open_molecule(self, atoms: Generator[Any, Any, atom], labels=False):
        self.labels = labels
        self.atoms.clear()
        for at in atoms:
            self.atoms.append(Atom(at.x, at.y, at.z, at.label, at.type, at.part))
        if len(self.atoms) > 200:
            self.bond_width = 1
        self.connections = self.get_conntable_from_atoms()
        self.get_center_and_radius()
        self.factor = min(self.width(), self.height()) / 2 / self.molecule_radius * self.zoom / 100
        self.atoms_size = self.factor * 70
        self.update()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # self.setFixedWidth(int(self.height() * 1.8))
        super().resizeEvent(event)

    def paintEvent(self, event):
        if self.atoms:
            self.painter = QPainter(self)
            self.painter.setRenderHint(QPainter.Antialiasing)
            font = self.painter.font()
            font.setPixelSize(13)
            self.painter.setFont(font)
            self.draw()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.lastPos = event.pos()

    def save_image(self, filename: Path, image_scale=1.5):
        image = QImage(self.size() * image_scale, QImage.Format_RGB32)
        image.fill(Qt.white)
        imgpainter = QPainter(image)
        imgpainter.scale(image_scale, image_scale)
        self.render(imgpainter)
        image.save(str(filename.resolve()))
        imgpainter.end()

    def rotate_x(self):
        return np.array([
            [1, 0, 0],
            [0, cos(self.x_angle), -sin(self.x_angle)],
            [0, sin(self.x_angle), cos(self.x_angle)],
        ], dtype=np.float32)

    def rotate_y(self):
        return np.array([
            [cos(self.y_angle), 0, sin(self.y_angle)],
            [0, 1, 0],
            [-sin(self.y_angle), 0, cos(self.y_angle)],
        ], dtype=np.float32)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.rotate_molecule(event)
        elif event.buttons() == Qt.RightButton:
            self.zoom_molecule(event)
        elif event.buttons() == Qt.MiddleButton:
            self.pan_molecule(event)
        self.lastPos = event.pos()

    def pan_molecule(self, event):
        self.molecule_center[0] += (self.lastPos.x() - event.x()) / 50
        self.molecule_center[1] += (self.lastPos.y() - event.y()) / 50
        self.update()

    def zoom_molecule(self, event: QMouseEvent):
        self.factor += (self.lastPos.y() - event.y()) / 350
        if self.factor <= 0.005:
            # Prevents zooming to infinity where nothing is visible:
            self.factor = 0.005
        self.zoom -= (self.lastPos.y() - event.y()) / 350
        self.atoms_size = abs(self.factor * 70)
        self.update()

    def rotate_molecule(self, event):
        self.y_angle = -(event.x() - self.lastPos.x()) / 80
        self.x_angle = (event.y() - self.lastPos.y()) / 80
        for num, at in enumerate(self.atoms):
            rotated2d = np.dot(self.rotate_y(), at.coordinate - self.molecule_center)
            x, y, z = np.dot(self.rotate_x(), rotated2d) + self.molecule_center
            self.atoms[num] = Atom(x, y, z, at.name, at.type_, at.part)
        self.update()

    def draw(self):
        scale = self.factor * 150
        self.screen_center = [self.width() / 2, self.height() / 2]
        bond_offset = int(self.atoms_size / 2)
        hydrogens = ('H', 'D')
        for atom in self.atoms:
            projected2d = np.dot(self.projection_matrix, atom.coordinate.reshape(3, 1))
            atom.screenx = int(projected2d[0][0] * scale + self.screen_center[0] - self.molecule_center[0] * scale)
            atom.screeny = int(projected2d[1][0] * scale + self.screen_center[1] - self.molecule_center[1] * scale)
        self.calculate_z_order()
        for item in self.objects:
            # atoms
            if item[0] == 0:
                atom = item[1]
                self.draw_atom(atom)
                if self.labels and atom.type_ not in hydrogens:
                    self.draw_label(atom)
            # bonds:
            if item[0] == 1:
                self.draw_bond(item[1], item[2], offset=bond_offset)
        self.painter.end()

    def calculate_z_order(self):
        """
        Orders the atoms and bonds by z coordinates.
        """
        self.objects.clear()
        for n1, n2 in self.connections:
            # 1 means bond:
            at1 = self.atoms[n1]
            at2 = self.atoms[n2]
            self.objects.append((1, at1, at2))
        for atom in self.atoms:
            # 0 means atom
            self.objects.append((0, atom))
        self.objects.sort(reverse=True, key=lambda atom: atom[1].coordinate[2])

    def distance(self, vector1: np.array, vector2: np.array):
        """
        d = 0
        for i in range(3):
            d += (a[i] - b[i]) ** 2
        return math.sqrt(d)
        This is faster:
        """
        diff = vector2 - vector1
        squareDistance = np.dot(diff.T, diff)
        return math.sqrt(squareDistance)

    def get_center_and_radius(self):
        min_ = [999999, 999999, 999999]
        max_ = [-999999, -999999, -999999]
        for at in self.atoms:
            for j in reversed(range(3)):
                v = at.coordinate[j]
                if v < min_[j]:
                    min_[j] = v
                if v > max_[j]:
                    max_[j] = v
        c = np.array([0, 0, 0])
        for j in reversed(range(3)):
            c[j] = (max_[j] + min_[j]) / 2
        r = 0
        for atom in self.atoms:
            d = self.distance(atom.coordinate, c) + 0.5
            if d > r:
                r = d
        self.molecule_center = np.array(c, dtype=np.float32)
        self.molecule_radius = r or 10

    def draw_bond(self, at1: 'Atom', at2: 'Atom', offset: int):
        self.painter.setPen(QPen(Qt.darkGray, self.bond_width, Qt.SolidLine))
        self.painter.drawLine(at1.screenx + offset, at1.screeny + offset,
                              at2.screenx + offset, at2.screeny + offset)

    def draw_atom(self, atom: 'Atom'):
        self.painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        self.painter.setBrush(QBrush(atom.color, Qt.SolidPattern))
        self.painter.drawEllipse(int(atom.screenx), int(atom.screeny), int(self.atoms_size), int(self.atoms_size))

    def draw_label(self, atom: 'Atom'):
        self.painter.setPen(QPen(QColor(100, 50, 5), 2, Qt.SolidLine))
        self.painter.drawText(atom.screenx + 18, atom.screeny - 4, atom.name)

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
                d = self.distance(at1.coordinate, at2.coordinate)
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


class Atom(object):
    def __init__(self, x: float, y: float, z: float, name: str, type_: str, part: int):
        self.coordinate = np.array((x, y, z), dtype=np.float32)
        self.name = name
        self.part = part
        self.type_ = type_
        self.screenx = None
        self.screeny = None

    @property
    def color(self):
        return QColor(element2color.get(self.type_))

    def __repr__(self) -> str:
        return str((self.name, self.type_, self.coordinate))


if __name__ == "__main__":
    # Molecule(atoms).draw()
    app = QtWidgets.QApplication(sys.argv)
    # create our new Qt MainWindow
    window = QtWidgets.QMainWindow()
    # create our new custom VTK Qt widget
    # shx = Shelxfile()
    # shx.read_file('tests/examples/1979688-finalcif.res')
    # atoms = [x.cart_coords for x in shx.atoms]
    cif = CifContainer('test-data/p21c.cif')
    # cif = CifContainer(r'../41467_2015.cif')
    # cif = CifContainer('tests/examples/1979688.cif')
    # cif = CifContainer('/Users/daniel/Documents/GitHub/StructureFinder/test-data/668839.cif')
    cif.load_this_block(len(cif.doc) - 1)
    render_widget = MoleculeWidget(None)
    render_widget.open_molecule(cif.atoms_orth, labels=False)
    # add and show
    window.setCentralWidget(render_widget)
    window.setMinimumSize(800, 600)
    window.show()
    # render_widget.save_image(Path('myimage2.png'))
    # start the event loop
    sys.exit(app.exec_())
