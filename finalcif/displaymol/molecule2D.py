from __future__ import annotations

import enum
import sys
from collections import namedtuple
from dataclasses import dataclass
from math import sqrt, cos, sin, dist, radians, atan2, degrees
from pathlib import Path
from typing import NoReturn

import numpy as np
from PySide6.QtGui import QLinearGradient
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPalette, QImage, QResizeEvent, QWheelEvent, \
    QRadialGradient

from finalcif.cif.atoms import get_radius_from_element, element2color
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.dsrmath import vol_unitcell
from finalcif.tools.misc import to_float

"""
A 2D molecule drawing widget. Feed it with a list (or generator) of atoms of this type:
label:   Name of the atom like 'C3'
type:    Atom type as string like 'C'
x, y, z: Atom position in cartesian coordinates
part:    Disorder part in SHELX notation like 1, 2, -1
"""
Atomtuple = namedtuple('Atomtuple', ('label', 'type', 'x', 'y', 'z', 'part', 'symm_matrix'), defaults=(None,))


@dataclass(slots=True)
class RenderItem:
    is_bond: bool
    atom1: Atom
    atom2: Atom | None = None


class MoleculeWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self._astar = None
        self._bstar = None
        self._cstar = None
        self._amatrix = None
        self._adp_map = None
        self._cell = None
        self._factor = 1.0
        self.atoms_size = 12
        self.fontsize = 13
        self.bond_width = 1
        self.labels = False
        self.show_adps = True
        self.bond_drawer = self.draw_bond

        # scaling factor for ADP ellipsoids in screen coordinates
        # 1.5382 is the standard ORTEP scaling factor for 50% probability:
        self.adp_scale = 1.5382
        self.molecule_center = np.array([0, 0, 0])
        self.molecule_radius = 10
        self._lastPos = self.pos()
        self._painter: None | QPainter = None
        self.x_angle = 0
        self.y_angle = 0

        # Color caches
        self.bond_color = QColor('#555555')
        self.fallback_pen_color = QColor(QtCore.Qt.GlobalColor.black)
        self.adp_pen_color = QColor(0, 0, 0, 255)

        # 3D Cylinder gradient colors for bonds
        self.bond_grad_dark = QColor(60, 60, 60)
        self.bond_grad_light = QColor(140, 140, 140)
        self.bond_grad_shadow = QColor(10, 10, 10)

        pal = QPalette()
        pal.setColor(QtGui.QPalette.ColorRole.Window, QtCore.Qt.GlobalColor.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.atoms: list[Atom] = []
        self.connections = ()
        self.objects: list[RenderItem] = []

        self.screen_center = [self.width() / 2, self.height() / 2]
        self.zoom = 1.1

        # Numpy arrays for fast vectorized rotation
        self._coords_array = np.empty((0, 3))
        self._ucart_array = np.empty((0, 3, 3))
        self._has_adp = np.empty(0, dtype=bool)

    def setLabelFont(self, font_size: int):
        if font_size < 0:
            font_size = 1
        self.fontsize = font_size
        self.update()

    def clear(self) -> None:
        self.open_molecule(atoms=[])

    def show_labels(self, value: bool):
        self.labels = value
        self.update()

    def show_adp(self, value: bool):
        self.show_adps = value
        self.update()

    def show_round_bonds(self, bond_type: bool = False):
        if not bond_type:
            self.bond_drawer = self.draw_bond
        else:
            self.bond_drawer = self.draw_bond_rounded
        self.update()

    def open_molecule(self, atoms: list[Atomtuple], cell: list[float] | None = None,
                      adps: list[float] | None = None) -> None:
        if cell is not None and self.show_adps:
            self._cell = cell
            self.calc_amatrix()
            self._adp_map = {}
            try:
                for adp in adps:
                    self._adp_map[adp.label] = (adp.U11, adp.U22, adp.U33, adp.U23, adp.U13, adp.U12)
            except Exception:
                pass  # will show up as circle
        else:
            self._cell = None
            self._adp_map = None

        self.atoms.clear()
        self.make_adps(atoms)
        self.connections = self.get_conntable_from_atoms()
        self.get_center_and_radius()

        # Cache objects array once to save allocation time during rotation
        self.objects.clear()
        for n1, n2 in self.connections:
            at1 = self.atoms[n1]
            at2 = self.atoms[n2]
            if at1.type_ in ('H', 'D') and at2.u_iso is not None:
                if at1.u_iso is None:
                    at1.u_iso = at2.u_iso * 0.8
            elif at2.type_ in ('H', 'D') and at1.u_iso is not None:
                if at2.u_iso is None:
                    at2.u_iso = at1.u_iso * 0.8
            self.objects.append(RenderItem(is_bond=True, atom1=at1, atom2=at2))

        for atom in self.atoms:
            self.objects.append(RenderItem(is_bond=False, atom1=atom))

        # Build numpy arrays for fully vectorized rotation
        self._coords_array = np.array([at.coordinate for at in self.atoms])
        self._ucart_array = np.zeros((len(self.atoms), 3, 3))
        self._has_adp = np.zeros(len(self.atoms), dtype=bool)
        for i, at in enumerate(self.atoms):
            at.z = at.coordinate[2]
            if at.u_cart is not None:
                self._ucart_array[i] = at.u_cart
                self._has_adp[i] = True

        self._factor = min(self.width(), self.height()) / 2 / self.molecule_radius * self.zoom / 100
        self.atoms_size = self._factor * 70
        self.update()

    def calc_amatrix(self):
        a, b, c, alpha, beta, gamma = self._cell
        V = vol_unitcell(a, b, c, alpha, beta, gamma)
        # reciprocal lattice vectors
        self._astar = (b * c * sin(radians(alpha))) / V
        self._bstar = (c * a * sin(radians(beta))) / V
        self._cstar = (a * b * sin(radians(gamma))) / V
        # orthogonalization matrix (fractional -> cartesian)
        self._amatrix = np.array([
            [a, b * cos(radians(gamma)), c * cos(radians(beta))],
            [0, b * sin(radians(gamma)),
             c * (cos(radians(alpha)) - cos(radians(beta)) * cos(radians(gamma))) / sin(radians(gamma))],
            [0, 0, V / (a * b * sin(radians(gamma)))]
        ], dtype=float)

    def make_adps(self, atoms: list[Atomtuple]) -> None:
        self.atoms.clear()
        for at in atoms:
            a = Atom(at.x, at.y, at.z, at.label, at.type, at.part)
            if self._adp_map and self._cell and at.label in self._adp_map:
                try:
                    uvals = tuple(to_float(x) for x in self._adp_map[at.label])
                    symm_matrix = getattr(at, 'symm_matrix', None)
                    if symm_matrix is not None:
                        symm_matrix = np.array(symm_matrix, dtype=float)
                    a.u_cart = self._uij_to_cart(uvals, symm_matrix)
                    a.u_iso = np.trace(a.u_cart) / 3.0
                except Exception:
                    a.u_cart = None
                    a.u_iso = None
            self.atoms.append(a)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event):
        if self.atoms:
            self._painter = QPainter(self)
            self._painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            font = self._painter.font()
            font.setPixelSize(self.fontsize)
            self._painter.setFont(font)
            try:
                self.draw()
            except (ValueError, IndexError) as e:
                print(f'Draw structure crashed: {e}')
                self._painter.end()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._lastPos = event.position()

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.setLabelFont(self.fontsize + 2)
        elif event.angleDelta().y() < 0:
            self.setLabelFont(self.fontsize - 2)

    def save_image(self, filename: Path, image_scale=1.5):
        image = QImage(self.size() * image_scale, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        painter.scale(image_scale, image_scale)
        self.render(painter, QtCore.QPoint(0, 0))
        painter.end()
        image.save(str(filename.resolve()))

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

    def _uij_to_cart(self, uvals: tuple[float, float, float, float, float, float],
                     symm_matrix: np.ndarray | None = None) -> np.ndarray:
        """Convert fractional Uij displacement parameters to Cartesian coordinates."""
        U11, U22, U33, U23, U13, U12 = uvals
        Uij = np.array([[U11, U12, U13],
                        [U12, U22, U23],
                        [U13, U23, U33]], dtype=float)

        # Apply the fractional rotation part of the symmetry operation.
        # The symmetry matrices from sdm.py use row-vector convention (x' = x * m),
        # so the contravariant tensor U transforms as U' = m.T @ U @ m
        if symm_matrix is not None:
            Uij = symm_matrix.T @ Uij @ symm_matrix

        N = np.diag([self._astar, self._bstar, self._cstar])
        Ucart = self._amatrix.dot(N).dot(Uij).dot(N.T).dot(self._amatrix.T)
        return Ucart

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.rotate_molecule(event)
        elif event.buttons() == QtCore.Qt.MouseButton.RightButton:
            self.zoom_molecule(event)
        elif event.buttons() == QtCore.Qt.MouseButton.MiddleButton:
            self.pan_molecule(event)
        self._lastPos = event.position()

    def pan_molecule(self, event):
        self.molecule_center[0] += (self._lastPos.x() - event.position().x()) / 50
        self.molecule_center[1] += (self._lastPos.y() - event.position().y()) / 50
        self.update()

    def zoom_molecule(self, event: QMouseEvent):
        self._factor += (self._lastPos.y() - event.position().y()) / 350
        self._factor = max(0.005, self._factor)
        self.zoom -= (self._lastPos.y() - event.position().y()) / 350
        self.atoms_size = abs(self._factor * 70)
        self.update()

    def rotate_molecule(self, event: QMouseEvent):
        self.y_angle = -(event.position().x() - self._lastPos.x()) / 80
        self.x_angle = (event.position().y() - self._lastPos.y()) / 80
        R_y = self.rotate_y()
        R_x = self.rotate_x()
        R = np.dot(R_x, R_y)

        # Single bulk vector rotation instead of individual loops
        if self.atoms:
            # 1) Rotate all atom coordinates
            self._coords_array = np.dot(self._coords_array - self.molecule_center, R.T) + self.molecule_center

            # 2) Rotate all matrices in one go via broadcasting
            if np.any(self._has_adp):
                self._ucart_array = np.matmul(R, np.matmul(self._ucart_array, R.T))

            # 3) Assign values back to objects
            for i, at in enumerate(self.atoms):
                at.coordinate = self._coords_array[i]
                at.z = at.coordinate[2]  # cache explicit z property for fast sorting
                if self._has_adp[i]:
                    at.u_cart = self._ucart_array[i]

        self.update()

    def draw(self) -> None:
        scale = self._factor * 150
        self.screen_center = [self.width() / 2, self.height() / 2]
        bond_offset = int(self.atoms_size / 2)
        hydrogens = ('H', 'D')

        cx = self.screen_center[0] - self.molecule_center[0] * scale
        cy = self.screen_center[1] - self.molecule_center[1] * scale

        for atom in self.atoms:
            c = atom.coordinate
            atom.screenx = int(c[0] * scale + cx)
            atom.screeny = int(c[1] * scale + cy)

        self.calculate_z_order()
        for item in self.objects:
            if item.is_bond:
                self.bond_drawer(item.atom1, item.atom2, offset=bond_offset)
            else:
                self.draw_atom(item.atom1)
                if self.labels and item.atom1.type_ not in hydrogens:
                    self.draw_label(item.atom1)
        self._painter.end()

    def calculate_z_order(self):
        """
        Orders the cached atoms and bonds by the explicit z coordinates.
        """
        self.objects.sort(reverse=True, key=lambda item: item.atom1.z)

    def distance(self, vector1: np.ndarray, vector2: np.ndarray):
        diff = vector2 - vector1
        return sqrt(np.dot(diff.T, diff))

    def get_center_and_radius(self):
        min_ = [999999, 999999, 999999]
        max_ = [-999999, -999999, -999999]
        for at in self.atoms:
            for j in reversed(range(3)):
                v = at.coordinate[j]
                min_[j] = min(min_[j], v)
                max_[j] = max(max_[j], v)
        c = np.array([0, 0, 0], dtype=np.float32)
        for j in reversed(range(3)):
            c[j] = (max_[j] + min_[j]) / 2
        r = 0
        for atom in self.atoms:
            d = dist(atom.coordinate, c) + 1.5
            r = max(r, d)
        self.molecule_center = np.array(c, dtype=np.float32)
        self.molecule_radius = r or 10

    def draw_bond_rounded(self, at1: Atom, at2: Atom, offset: int):
        # Scale bond width with zoom factor, clamped between max and min
        dynamic_width = max(self.bond_width, min(15, int(self.bond_width * self._factor * 11)))

        x1 = at1.screenx + offset
        y1 = at1.screeny + offset
        x2 = at2.screenx + offset
        y2 = at2.screeny + offset

        # Vector of the bond
        dx = x2 - x1
        dy = y2 - y1
        length = sqrt(dx * dx + dy * dy)
        if length < 0.0001:
            return

        # Normal vector perpendicular to the bond
        nx = -dy / length
        ny = dx / length

        w_half = dynamic_width / 2.0

        # Set up linear gradient perpendicular to the bond to mimic 3D lighting
        grad = QLinearGradient(x1 - nx * w_half, y1 - ny * w_half,
                               x1 + nx * w_half, y1 + ny * w_half)
        grad.setColorAt(0.0, self.bond_grad_dark)
        grad.setColorAt(0.4, self.bond_grad_light)  # Highlight slightly off-center
        grad.setColorAt(1.0, self.bond_grad_shadow)

        pen = QPen(QBrush(grad), dynamic_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_bond(self, at1: Atom, at2: Atom, offset: int):
        dynamic_width = max(self.bond_width, min(15, int(self.bond_width * self._factor * 11)))
        pen = QPen(self.bond_color, dynamic_width, Qt.PenStyle.SolidLine)
        self._painter.setPen(pen)
        self._painter.drawLine(int(at1.screenx + offset), int(at1.screeny + offset),
                               int(at2.screenx + offset), int(at2.screeny + offset))

    def draw_atom(self, atom: Atom):
        # Draw anisotropic displacement parameters (ellipsoids) if requested
        if self.show_adps and atom.u_cart is not None:
            # Analytical 2x2 eigen decomposition of the 2D projected covariance matrix
            # Bypasses expensive np.linalg.eigh overhead
            a = atom.u_cart[0, 0]
            b = atom.u_cart[0, 1]
            c = atom.u_cart[1, 1]

            T = a + c
            D = a * c - b * b
            diff = T * T * 0.25 - D

            if diff >= 0:
                sq = sqrt(diff)
                eig1 = T * 0.5 - sq
                eig2 = T * 0.5 + sq

                if eig1 > 0 and eig2 > 0:
                    scale = self._factor * 150 * self.adp_scale
                    r1 = sqrt(eig1) * scale
                    r2 = sqrt(eig2) * scale

                    if abs(b) > 1e-8:
                        angle = degrees(atan2(eig1 - a, b))
                    else:
                        angle = 0.0 if a < c else 90.0

                    cx = atom.screenx + self.atoms_size / 2
                    cy = atom.screeny + self.atoms_size / 2
                    self._painter.save()
                    self._painter.translate(cx, cy)
                    self._painter.rotate(angle)
                    gradient = self.make_gradient(angle, atom, r1, r2)
                    brush = QBrush(gradient)
                    pen = QPen(self.adp_pen_color, 1, Qt.PenStyle.SolidLine)
                    self._painter.setBrush(brush)
                    self._painter.setPen(pen)
                    self._painter.drawEllipse(int(-r1), int(-r2), int(2 * r1), int(2 * r2))

                    # Draw an ORTEP-like center cross (slightly transparent to blend with 3D)
                    cross_pen = QPen(QColor(0, 0, 0, 120), 1, Qt.PenStyle.SolidLine)
                    self._painter.setPen(cross_pen)
                    self._painter.drawLine(int(-r1), 0, int(r1), 0)
                    self._painter.drawLine(0, int(-r2), 0, int(r2))

                    self._painter.restore()
                    # Return early to prevent drawing the standard circular atom
                    return

        # Standard circle fallback if ADPs are absent or calculation failed
        circle_size = self.atoms_size
        if self.show_adps and atom.u_iso is not None:
            # Scale the radius exactly like the ellipsoids using U_iso
            r = sqrt(atom.u_iso) * self._factor * 150 * self.adp_scale
            circle_size = r * 2

        cx = atom.screenx + self.atoms_size / 2
        cy = atom.screeny + self.atoms_size / 2
        radius = circle_size / 2

        # 3D Gradient for the standard circle
        gradient = QRadialGradient(cx - radius * 0.3, cy - radius * 0.3, circle_size)
        gradient.setColorAt(0.0, atom.color_light)
        gradient.setColorAt(0.4, atom.color)
        gradient.setColorAt(1.0, atom.color_dark)

        self._painter.setPen(QPen(self.fallback_pen_color, 1, Qt.PenStyle.SolidLine))
        self._painter.setBrush(QBrush(gradient))
        # Draw the circle centered perfectly with the bonds
        self._painter.drawEllipse(int(cx - radius), int(cy - radius),
                                  int(circle_size), int(circle_size))

    def make_gradient(self, angle: float, atom: Atom, r1: float, r2: float) -> QRadialGradient:
        # 3D Gradient for the ellipsoid with a fixed global light source
        max_r = max(r1, r2)
        # Desired screen-space offset (top-left)
        sx, sy = -max_r * 0.3, -max_r * 0.3
        # Un-rotate the gradient focal point against the painter's rotation
        rad = radians(angle)
        fx = sx * cos(rad) + sy * sin(rad)
        fy = -sx * sin(rad) + sy * cos(rad)

        gradient = QRadialGradient(fx, fy, max_r * 1.5)
        gradient.setColorAt(0.0, atom.color_light)
        gradient.setColorAt(0.4, atom.color)
        gradient.setColorAt(1.0, atom.color_dark)
        return gradient

    def draw_label(self, atom: Atom):
        self._painter.setPen(QPen(QColor(100, 50, 5), 2, Qt.PenStyle.SolidLine))
        self._painter.drawText(atom.screenx + 18, atom.screeny - 4, atom.name)

    def get_conntable_from_atoms(self, extra_param: float = 1.2) -> tuple:
        """
        Returns a connectivity table from the atomic coordinates and the covalence
        radii of the atoms.
        a bond is defined with less than the sum of the covalence radii plus the extra_param:
        """
        connections = []
        h = ('H', 'D')
        for num1, at1 in enumerate(self.atoms, 0):
            for num2, at2 in enumerate(self.atoms, 0):
                if (at1.part != 0 and at2.part != 0) and at1.part != at2.part:
                    continue
                # at2 can be generated by symmetry from at1, so this is not good:
                # if at1.name == at2.name:  # name1 = name2
                #    continue
                d = dist(at1.coordinate, at2.coordinate)
                if d > 4.0:  # makes bonding faster (longer bonds do not exist)
                    continue
                if (at1.radius + at2.radius) * extra_param > d:
                    if at1.type_ in h and at2.type_ in h:
                        continue
                    # The extra time for this is not too much:
                    if (num2, num1) in connections:
                        continue
                    connections.append((num1, num2))
        return tuple(connections)


class Atom:
    __slots__ = ['coordinate', 'name', 'part', 'radius', 'screenx', 'screeny', 'type_', 'u_cart', 'color',
                 'color_light',
                 'color_dark', 'u_iso', 'z']

    def __init__(self, x: float, y: float, z: float, name: str, type_: str, part: int):
        self.coordinate = np.array([x, y, z], dtype=np.float32)
        self.z = z
        self.name = name
        self.part = part
        self.type_ = type_
        self.screenx = 0
        self.screeny = 0
        self.radius = get_radius_from_element(type_)
        self.u_cart = None
        self.color = QColor(element2color.get(self.type_, '#000000'))  # Default to black if unknown
        self.color_light = self.color.lighter(160)
        self.color_dark = self.color.darker(160)
        self.u_iso = None

    def __repr__(self) -> str:
        return str((self.name, self.type_, self.coordinate))


def display(atoms: list[Atomtuple], cell: list[float] | None = None, adps: list[float] | None = None,
            cif: CifContainer | None = None) -> NoReturn:
    """
    This function is for testing purposes.
    """
    import time
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    render_widget = MoleculeWidget(None)
    t1 = time.perf_counter()

    adp_checkbox = QtWidgets.QCheckBox("Show ADP")
    grow_checkbox = QtWidgets.QCheckBox("Grow")
    label_checkbox = QtWidgets.QCheckBox("Show Labels")
    bond_type_checkbox = QtWidgets.QCheckBox("Round Bonds")

    adp_checkbox.setChecked(True)

    adp_checkbox.toggled.connect(lambda x: render_widget.show_adp(x))
    label_checkbox.toggled.connect(lambda x: render_widget.show_labels(x))
    bond_type_checkbox.toggled.connect(lambda x: render_widget.show_round_bonds(x))

    def toggle_grow(checked: bool) -> None:
        if checked:
            from sdm import SDM
            t1 = time.perf_counter()
            sdm = SDM(tuple(cif.atoms_fract), cif.symmops, cif.cell[:6], centric=cif.is_centrosymm)
            needsymm = sdm.calc_sdm()
            grown_atoms = sdm.packer(sdm, needsymm)
            render_widget.open_molecule(atoms=grown_atoms, cell=cif.cell[:6], adps=cif.displacement_parameters())
            print(f'Time to display grown molecule: {time.perf_counter() - t1:5.4} s')
        else:
            t1 = time.perf_counter()
            render_widget.open_molecule(atoms=cif.atoms_orth, cell=cif.cell[:6], adps=cif.displacement_parameters())
            print(f'Time to display molecule: {time.perf_counter() - t1:5.4} s')

    grow_checkbox.toggled.connect(toggle_grow)

    render_widget.open_molecule(atoms=atoms, cell=cell, adps=adps)
    render_widget.labels = False
    print(f'Time to display molecule: {time.perf_counter() - t1:5.4} s')

    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)
    vl = QtWidgets.QVBoxLayout(central_widget)
    window.setMinimumSize(800, 600)
    vl.addWidget(render_widget)

    hl = QtWidgets.QHBoxLayout()
    hl.addWidget(adp_checkbox)
    hl.addWidget(label_checkbox)
    hl.addWidget(grow_checkbox)
    hl.addWidget(bond_type_checkbox)
    hl.addStretch()

    vl.addLayout(hl)
    window.show()
    # start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    # shx = Shelxfile()
    # shx.read_file('tests/examples/1979688-finalcif.res')
    # atoms = [x.cart_coords for x in shx.atoms]
    # cif = CifContainer('test-data/p21c.cif')
    # cif = CifContainer(r'../41467_2015.cif')
    # cif = CifContainer(r"D:\frames\Workordner\huge_structure\p-1-finalcif.cif")
    # cif = CifContainer('tests/examples/1979688.cif')
    # cif = CifContainer('/Users/daniel/Documents/GitHub/StructureFinder/test-data/668839.cif')
    cif = CifContainer(Path('test-data/4060314.cif'))
    cif.load_this_block(len(cif.doc) - 1)

    display(atoms=cif.atoms_orth, cell=cif.cell[:6], adps=cif.displacement_parameters(), cif=cif)
