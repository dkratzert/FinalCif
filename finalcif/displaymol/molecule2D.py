from __future__ import annotations

"""
A versatile 2D/3D molecule drawing widget for PyQt/PySide.
Renders molecules as ORTEP-style thermal ellipsoid plots (when anisotropic
displacement parameters are provided) or as simple ball-and-stick diagrams.
The widget supports interactive mouse rotation, zooming, and panning.

Feed it with a list of :class:`~finalcif.displaymol.sdm.Atomtuple` objects
whose fields are:

- **label**:       Atom name, e.g. ``'C3'``.
- **type**:        Element symbol as string, e.g. ``'C'``.
- **x, y, z**:    Atom position in Cartesian coordinates (Ångströms).
- **part**:        Disorder part in SHELX notation (0 = all parts, ..., -1, -2, 1, 2, ...).
- **symm_matrix**: Optional 3×3 fractional rotation matrix used to rotate
  the ADP tensor for symmetry-generated atoms.

Mouse controls (inside :class:`MoleculeWidget`):

- **Left drag**:   Rotate the molecule.
- **Right drag**:  Zoom in / out.
- **Middle drag**: Pan the view.
- **Scroll wheel**: Increase / decrease label font size.
- **Left click**:  Select a single atom or bond (clears previous selection).
- **Ctrl + Left click**: Toggle selection of multiple atoms and bonds.
"""

import sys
from dataclasses import dataclass
from math import sqrt, cos, sin, dist, radians, atan2, degrees, pi
from pathlib import Path
from typing import NoReturn, Callable

import numpy as np
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtCore import Qt, QRectF
from qtpy.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPalette, QImage, QResizeEvent, QWheelEvent, \
    QRadialGradient, QLinearGradient, QTransform

from finalcif.cif.atoms import get_radius_from_element, element2color
from finalcif.displaymol.sdm import Atomtuple
from finalcif.tools.misc import to_float


def calc_volume(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> float:
    ca, cb, cg = cos(radians(alpha)), cos(radians(beta)), cos(radians(gamma))
    return a * b * c * sqrt(1 + 2 * ca * cb * cg - ca ** 2 - cb ** 2 - cg ** 2)


@dataclass(slots=True)
class RenderItem:
    """A single renderable element (atom or bond) in the z-ordered draw list.

    :param is_bond: ``True`` for a bond, ``False`` for an atom.
    :param z_order: Depth value used to sort back-to-front for the painter's algorithm.
    :param atom1: The first (or only) atom involved.
    :param atom2: The second atom of a bond, or ``None`` for an atom item.
    """

    is_bond: bool
    z_order: float = 0.0
    atom1: Atom = None
    atom2: Atom | None = None


class MoleculeWidget(QtWidgets.QWidget):
    """Interactive Qt widget that renders a molecule as a 2D projection.

    Supports ORTEP-style anisotropic displacement parameter (ADP) ellipsoids
    at 50 % probability level, isotropic spheres, and simple ball-and-stick
    representations.  The molecule can be rotated (left-drag), zoomed
    (right-drag), and panned (middle-drag) with the mouse.

    Typical usage::

        widget = MoleculeWidget(parent)
        widget.open_molecule(atoms=atom_list, cell=cell_params, adps=adp_dict)

    :param parent: Optional parent widget.
    """

    atomClicked = QtCore.Signal(str)
    bondClicked = QtCore.Signal(str, str)

    def __init__(self, parent: QtGui.QWidget = None):
        super().__init__(parent)
        self._astar = None
        self._bstar = None
        self._cstar = None
        self._amatrix = None
        self._adp_map = None
        self._cell = None
        self._factor = 1.0
        self.atoms_size = 12
        self.fontsize = 13
        self.bond_width = 3
        self.labels = True
        self.show_adps = True
        self.bond_drawer = self._draw_bond_rounded

        self.show_hydrogens_flag = True

        # Track selected atoms and bonds as sets for multi-selection
        self.selected_atoms: set[str] = set()
        self.selected_bonds: set[tuple[str, str]] = set()

        # scaling factor for ADP ellipsoids in screen coordinates
        # 1.5382 is the standard ORTEP scaling factor for 50% probability:
        self.adp_scale = 1.5382
        self.molecule_center = np.array([0, 0, 0])
        self.molecule_radius = 10
        self._lastPos = self.pos()
        self._pressPos = self.pos()
        self._painter: None | QPainter = None
        self.x_angle = 0
        self.y_angle = 0

        self.scale = 150.0
        self.cx_global = 0.0
        self.cy_global = 0.0

        # Cumulative rotation matrix to preserve orientation during grow
        self.cumulative_R = np.eye(3, dtype=np.float32)

        # Color caches
        self.bond_color = QColor('#555555')
        self.fallback_pen_color = QColor(QtCore.Qt.GlobalColor.black)
        self.adp_pen_color = QColor(0, 0, 0, 255)

        # 3D Cylinder gradient colors for bonds
        self.bond_grad_dark = QColor(60, 60, 60)
        self.bond_grad_light = QColor(140, 140, 140)
        self.bond_grad_shadow = QColor(10, 10, 10)

        bg = QLinearGradient(0, 1, 0, -1)
        bg.setColorAt(0.0, self.bond_grad_dark)
        bg.setColorAt(0.2, self.bond_grad_light)
        bg.setColorAt(1.0, self.bond_grad_shadow)
        self.bond_brush = QBrush(bg)

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
        self._eigenvalues_array = np.empty((0, 3))
        self._eigenvectors_array = np.empty((0, 3, 3))
        self._u_inv_array = np.empty((0, 3, 3))

        self.mouse_pressed = False
        self.labels = True
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.atomClicked.connect(lambda x: print(f"Atom Selected: {x}"))
        self.bondClicked.connect(lambda x, y: print(f"Bond Selected: {x}-{y}"))

    def set_background_color(self, color: QColor):
        """Set the background color of the widget."""
        self.bg_color = color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

    def set_bond_width(self, width: int):
        """Set the width of the bonds."""
        self.bond_width = width
        self.update()

    def set_labels_visible(self, visible: bool):
        """Toggle visibility of atom labels."""
        self.labels = visible
        self.update()

    def show_hydrogens(self, value: bool):
        """Toggle display of hydrogen atoms and their bonds."""
        self.show_hydrogens_flag = value
        self.update()

    def reset_view(self):
        """Reset zoom and rotation to defaults."""
        self.zoom = 1.0
        self.x_angle = 180.0
        self.y_angle = 180.0
        self.z_angle = 0.0
        self.x_shift_screen = 0
        self.y_shift_screen = 0
        self.cumulative_R = np.eye(3, dtype=np.float32)
        self.update()

    def setLabelFont(self, font_size: int):
        """Set the pixel size used for atom labels and schedule a repaint."""
        if font_size < 0:
            font_size = 1
        self.fontsize = font_size
        self.update()

    def clear(self) -> None:
        """Remove all atoms and bonds from the widget."""
        self.open_molecule(atoms=[])

    def show_labels(self, value: bool):
        """Toggle the display of non-hydrogen atom labels."""
        self.labels = value
        self.update()

    def show_adp(self, value: bool):
        """Toggle the display of ADP ellipsoids / isotropic spheres."""
        self.show_adps = value
        self.update()

    def show_round_bonds(self, bond_type: bool = True):
        """Switch between flat and 3D-shaded (rounded) bond rendering."""
        if not bond_type:
            self.bond_drawer = self._draw_bond
        else:
            self.bond_drawer = self._draw_bond_rounded
        self.update()

    def open_molecule(self, atoms: list[Atomtuple],
                      cell: tuple[float, float, float, float, float, float] | None = None,
                      adps: dict[str, tuple[float, float, float, float, float, float]] | None = None,
                      keep_view: bool = False) -> None:
        """
        Loads a new molecule and completely resets the view (zoom, pan, rotation).
        """
        self._load_molecule(atoms, cell, adps, keep_view=keep_view)

    def grow_molecule(self, atoms: list[Atomtuple],
                      cell: tuple[float, float, float, float, float, float] | None = None,
                      adps: dict[str, tuple[float, float, float, float, float, float]] | None = None) -> None:
        """Updates the molecule while preserving the current view (zoom, pan, rotation)."""
        self._load_molecule(atoms, cell, adps, keep_view=True)

    def _load_molecule(self, atoms: list[Atomtuple],
                       cell: tuple[float, float, float, float, float, float] | None = None,
                       adps: dict[str, tuple[float, float, float, float, float, float]] | None = None,
                       keep_view: bool = False) -> None:

        self._cell = cell
        self._adp_map = adps if adps is not None else {}

        if self._cell is not None and self.show_adps:
            self.calc_amatrix()

        self.atoms.clear()
        self.make_adps(atoms)
        self.connections = self.get_conntable_from_atoms()

        if not keep_view:
            self.get_center_and_radius()
            self.cumulative_R = np.eye(3, dtype=np.float32)
            self.selected_atoms.clear()
            self.selected_bonds.clear()

        self.objects.clear()
        for n1, n2 in self.connections:
            at1 = self.atoms[n1]
            at2 = self.atoms[n2]

            self.objects.append(RenderItem(is_bond=True, atom1=at1, atom2=at2))

        for atom in self.atoms:
            if atom.type_ in ('H', 'D'):
                atom.u_iso = 0.01
            self.objects.append(RenderItem(is_bond=False, atom1=atom))

        # Build numpy arrays for fully vectorized rotation
        self._coords_array = np.array([at.coordinate for at in self.atoms])
        self._ucart_array = np.zeros((len(self.atoms), 3, 3))
        self._has_adp = np.zeros(len(self.atoms), dtype=bool)
        self._eigenvalues_array = np.zeros((len(self.atoms), 3))
        self._eigenvectors_array = np.zeros((len(self.atoms), 3, 3))
        self._u_inv_array = np.zeros((len(self.atoms), 3, 3))

        # Apply accumulated rotation to the new coordinates
        if keep_view and not np.allclose(self.cumulative_R, np.eye(3)):
            self._coords_array = np.dot(self._coords_array - self.molecule_center,
                                        self.cumulative_R.T) + self.molecule_center

        for i, at in enumerate(self.atoms):
            if keep_view and not np.allclose(self.cumulative_R, np.eye(3)):
                at.coordinate = self._coords_array[i]

            at.z = at.coordinate[2]
            if at.u_cart is not None:
                if keep_view and not np.allclose(self.cumulative_R, np.eye(3)):
                    # Rotate the ADP tensor before computing eigenvectors/values
                    at.u_cart = np.matmul(self.cumulative_R, np.matmul(at.u_cart, self.cumulative_R.T))

                try:
                    evals, evecs = np.linalg.eigh(at.u_cart)
                    if np.any(evals <= 0):
                        at.adp_valid = False
                    else:
                        at.adp_valid = True
                    u_invers = np.linalg.inv(at.u_cart)

                    self._ucart_array[i] = at.u_cart
                    self._eigenvalues_array[i] = evals
                    self._eigenvectors_array[i] = evecs
                    self._u_inv_array[i] = u_invers
                    self._has_adp[i] = True

                    at.u_eigvals = evals
                    at.u_eigvecs = evecs
                    at.u_inv = u_invers
                except np.linalg.LinAlgError:
                    at.adp_valid = False
                    at.u_cart = None
                    at.u_iso = None

        if not keep_view:
            self._factor = min(self.width(), self.height()) / 2 / self.molecule_radius * self.zoom / 100
            self.atoms_size = self._factor * 70

        self.update()

    def calc_amatrix(self):
        """Compute the orthogonalisation matrix and reciprocal-lattice lengths."""
        a, b, c, alpha, beta, gamma = self._cell
        V = calc_volume(a, b, c, alpha, beta, gamma)
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
        """Convert Atomtuples to internal :class:`Atom` objects with Cartesian ADPs."""
        self.atoms.clear()
        name_counts = {}

        for at in atoms:
            base_name = at.label
            count = name_counts.get(base_name, 0)

            if count == 0:
                internal_name = base_name
            else:
                internal_name = f"{base_name}>>{count}"

            name_counts[base_name] = count + 1

            a = Atom(at.x, at.y, at.z, internal_name, at.type, at.part)
            if self._adp_map and self._cell and base_name in self._adp_map:
                try:
                    uvals = self._adp_map[base_name]
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

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Repaint the widget by re-rendering the molecule scene."""
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
        """Record the initial cursor position for subsequent drag operations."""
        self._lastPos = event.position()
        self._pressPos = event.position()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Detect clicks on atoms or bonds and emit corresponding signals."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            dx = event.position().x() - self._pressPos.x()
            dy = event.position().y() - self._pressPos.y()
            if abs(dx) < 5 and abs(dy) < 5:
                x = event.position().x()
                y = event.position().y()

                clicked_atom = None
                clicked_bond = None
                front_z = float('inf')

                # Check all objects to find the single one that is most in front
                for item in self.objects:
                    # Skip hidden hydrogens
                    if not self.show_hydrogens_flag:
                        if item.atom1.type_ in ('H', 'D') or (item.is_bond and item.atom2.type_ in ('H', 'D')):
                            continue

                    if item.is_bond:
                        if self.is_point_near_bond(item.atom1, item.atom2, x, y):
                            if item.z_order < front_z:
                                front_z = item.z_order
                                clicked_bond = tuple(sorted((item.atom1.name, item.atom2.name)))
                                clicked_atom = None
                    else:
                        if self.is_point_inside_atom(item.atom1, x, y):
                            if item.z_order < front_z:
                                front_z = item.z_order
                                clicked_atom = item.atom1
                                clicked_bond = None

                # Update selection state
                modifiers = event.modifiers()
                ctrl_pressed = bool(modifiers & Qt.KeyboardModifier.ControlModifier)
                selection_changed = False

                if clicked_atom:
                    if ctrl_pressed:
                        if clicked_atom.name in self.selected_atoms:
                            self.selected_atoms.remove(clicked_atom.name)
                        else:
                            self.selected_atoms.add(clicked_atom.name)
                    else:
                        self.selected_atoms = {clicked_atom.name}
                        self.selected_bonds.clear()

                    selection_changed = True
                    self.atomClicked.emit(clicked_atom.name)

                elif clicked_bond:
                    if ctrl_pressed:
                        if clicked_bond in self.selected_bonds:
                            self.selected_bonds.remove(clicked_bond)
                        else:
                            self.selected_bonds.add(clicked_bond)
                    else:
                        self.selected_bonds = {clicked_bond}
                        self.selected_atoms.clear()

                    selection_changed = True
                    self.bondClicked.emit(clicked_bond[0], clicked_bond[1])

                else:
                    if not ctrl_pressed and (self.selected_atoms or self.selected_bonds):
                        self.selected_atoms.clear()
                        self.selected_bonds.clear()
                        selection_changed = True

                if selection_changed:
                    self.update()

        super().mouseReleaseEvent(event)

    def is_point_inside_atom(self, atom: Atom, px: float, py: float) -> bool:
        """Check if a screen coordinate is inside the atom's drawn 2D projection."""
        cx = atom.screenx
        cy = atom.screeny
        dx = px - cx
        dy = py - cy

        if self.show_adps and atom.u_cart is not None:
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
                    r1 = sqrt(eig1) * self.scale * self.adp_scale
                    r2 = sqrt(eig2) * self.scale * self.adp_scale

                    if abs(b) > 1e-8:
                        angle = degrees(atan2(eig1 - a, b))
                    else:
                        angle = 0.0 if a < c else 90.0

                    rad = radians(angle)
                    cos_a = cos(rad)
                    sin_a = sin(rad)

                    # Transform to ellipse local coordinates
                    local_x = dx * cos_a + dy * sin_a
                    local_y = -dx * sin_a + dy * cos_a

                    if (local_x ** 2 / r1 ** 2) + (local_y ** 2 / r2 ** 2) <= 1.0:
                        return True
                    return False

        # Fallback for isotropic spheres or fixed-size circles
        circle_size = self.atoms_size
        if self.show_adps and atom.u_iso is not None:
            r = sqrt(atom.u_iso) * self.scale * self.adp_scale
            circle_size = r * 2

        radius = circle_size / 2
        return dx ** 2 + dy ** 2 <= radius ** 2

    def is_point_near_bond(self, at1: Atom, at2: Atom, px: float, py: float) -> bool:
        """Check if a screen coordinate is sufficiently close to a drawn bond segment."""
        line_data = self._get_bond_line(at1, at2)
        if not line_data:
            return False

        x1, y1, x2, y2, dynamic_width = line_data

        line_vec = np.array([x2 - x1, y2 - y1])
        p_vec = np.array([px - x1, py - y1])
        line_len_sq = np.dot(line_vec, line_vec)

        if line_len_sq == 0.0:
            return False

        t = max(0, min(1, np.dot(p_vec, line_vec) / line_len_sq))
        proj = np.array([x1, y1]) + t * line_vec
        dist_sq = (px - proj[0]) ** 2 + (py - proj[1]) ** 2

        # Add 4 extra pixels of hit area tolerance around the bond
        tolerance = max(5.0, dynamic_width / 2.0 + 4.0)
        return dist_sq <= tolerance ** 2

    def wheelEvent(self, event: QWheelEvent):
        """Increase or decrease the label font size on scroll."""
        if event.angleDelta().y() > 0:
            self.setLabelFont(self.fontsize + 2)
        elif event.angleDelta().y() < 0:
            self.setLabelFont(self.fontsize - 2)

    def save_image(self, filename: Path, image_scale: float = 1.5) -> None:
        """Render the current molecule view to an image file."""
        image = QImage(self.size() * image_scale, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        painter.scale(image_scale, image_scale)
        self.render(painter, QtCore.QPoint(0, 0))
        painter.end()
        image.save(str(filename.resolve()))

    def rotate_x(self) -> np.typing.NDArray[np.float32]:
        """Return a 3×3 rotation matrix around the X axis by :attr:`x_angle` radians."""
        return np.array([
            [1, 0, 0],
            [0, cos(self.x_angle), -sin(self.x_angle)],
            [0, sin(self.x_angle), cos(self.x_angle)],
        ], dtype=np.float32)

    def rotate_y(self) -> np.typing.NDArray[np.float32]:
        """Return a 3×3 rotation matrix around the Y axis by :attr:`y_angle` radians."""
        return np.array([
            [cos(self.y_angle), 0, sin(self.y_angle)],
            [0, 1, 0],
            [-sin(self.y_angle), 0, cos(self.y_angle)],
        ], dtype=np.float32)

    def _uij_to_cart(self, uvals: tuple[float, float, float, float, float, float],
                     symm_matrix: np.ndarray | None = None) -> np.ndarray:
        """Convert fractional *Uij* displacement parameters to a Cartesian tensor."""
        U11, U22, U33, U23, U13, U12 = uvals
        Uij = np.array([[U11, U12, U13],
                        [U12, U22, U23],
                        [U13, U23, U33]], dtype=float)

        # Apply the fractional rotation part of the symmetry operation.
        if symm_matrix is not None:
            Uij = symm_matrix.T @ Uij @ symm_matrix

        N = np.diag([self._astar, self._bstar, self._cstar])
        Ucart = self._amatrix.dot(N).dot(Uij).dot(N.T).dot(self._amatrix.T)
        return Ucart

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Dispatch drag events to rotate, zoom, or pan depending on the mouse button."""
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.rotate_molecule(event)
        elif event.buttons() == QtCore.Qt.MouseButton.RightButton:
            self.zoom_molecule(event)
        elif event.buttons() == QtCore.Qt.MouseButton.MiddleButton:
            self.pan_molecule(event)
        self._lastPos = event.position()

    def pan_molecule(self, event):
        """Translate the molecule center based on the middle-button drag delta."""
        self.molecule_center[0] += (self._lastPos.x() - event.position().x()) / 50
        self.molecule_center[1] += (self._lastPos.y() - event.position().y()) / 50
        self.update()

    def zoom_molecule(self, event: QMouseEvent):
        """Adjust the zoom / scale factor based on the right-button drag delta."""
        self._factor += (self._lastPos.y() - event.position().y()) / 350
        self._factor = max(0.005, self._factor)
        self.zoom -= (self._lastPos.y() - event.position().y()) / 350
        self.atoms_size = abs(self._factor * 70)
        self.update()

    def rotate_molecule(self, event: QMouseEvent):
        """Rotate the molecule around X and Y axes using the left-button drag delta."""
        self.y_angle = -(event.position().x() - self._lastPos.x()) / 80
        self.x_angle = (event.position().y() - self._lastPos.y()) / 80
        R_y = self.rotate_y()
        R_x = self.rotate_x()
        R = np.dot(R_x, R_y)

        # Track the cumulative rotation matrix
        self.cumulative_R = np.dot(R, self.cumulative_R)

        # Single bulk vector rotation instead of individual loops
        if self.atoms:
            self._coords_array = np.dot(self._coords_array - self.molecule_center, R.T) + self.molecule_center

            if np.any(self._has_adp):
                self._ucart_array = np.matmul(R, np.matmul(self._ucart_array, R.T))
                self._eigenvectors_array = np.matmul(R, self._eigenvectors_array)
                self._u_inv_array = np.matmul(R, np.matmul(self._u_inv_array, R.T))

            for i, at in enumerate(self.atoms):
                at.coordinate = self._coords_array[i]
                at.z = at.coordinate[2]  # cache explicit z property for fast sorting
                if self._has_adp[i]:
                    at.u_cart = self._ucart_array[i]
                    at.u_eigvecs = self._eigenvectors_array[i]
                    at.u_inv = self._u_inv_array[i]

        self.update()

    def get_spherical_radius(self, atom: Atom) -> float:
        """Return an approximate isotropic radius for UI purposes (e.g. label offset)."""
        if self.show_adps and atom.u_iso is not None:
            return sqrt(atom.u_iso)  # * self.adp_scale
        return 0.23

    def get_directional_radius(self, atom: Atom, v: np.ndarray) -> float:
        """Return the distance from the atom centre to its ellipsoid surface along *v*."""
        d = np.linalg.norm(v)
        if d < 1e-8:
            return 0.23

        if not atom.adp_valid:
            return 0.23

        if self.show_adps and atom.u_inv is not None:
            u = v / d
            val = np.dot(u, np.dot(atom.u_inv, u))
            if val > 0:
                return self.adp_scale / sqrt(val)

        # Fallback to sphere
        if self.show_adps and atom.u_iso is not None:
            return sqrt(atom.u_iso) * self.adp_scale

        return 0.23

    def draw(self) -> None:
        """Execute the main rendering pass."""
        self.scale = self._factor * 150
        self.screen_center = [self.width() / 2, self.height() / 2]
        self.cx_global = self.screen_center[0] - self.molecule_center[0] * self.scale
        self.cy_global = self.screen_center[1] - self.molecule_center[1] * self.scale

        hydrogens = ('H', 'D')

        # Precise 2D centers
        for atom in self.atoms:
            c = atom.coordinate
            atom.screenx = c[0] * self.scale + self.cx_global
            atom.screeny = c[1] * self.scale + self.cy_global

        self.calculate_z_order()

        for item in self.objects:
            if not self.show_hydrogens_flag:
                if item.atom1.type_ in hydrogens or (item.is_bond and item.atom2.type_ in hydrogens):
                    continue
            if item.is_bond:
                self.bond_drawer(item.atom1, item.atom2)
            else:
                self.draw_atom(item.atom1)
                if self.labels and item.atom1.type_ not in hydrogens:
                    self.draw_label(item.atom1)
        self._painter.end()

    def calculate_z_order(self):
        """Sort :attr:`objects` back-to-front by depth for the painter's algorithm."""
        for item in self.objects:
            if item.is_bond:
                item.z_order = (item.atom1.z + item.atom2.z) / 2.0
            else:
                item.z_order = item.atom1.z

        self.objects.sort(reverse=True, key=lambda item: item.z_order)

    def get_center_and_radius(self):
        """Compute the bounding sphere of the current atom set."""
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

    def _get_bond_line(self, at1: Atom, at2: Atom) -> tuple[float, float, float, float, int] | None:
        """Calculate the 2D projected line segment and width for a bond."""
        c1 = at1.coordinate
        c2 = at2.coordinate
        v = c2 - c1
        d = np.linalg.norm(v)

        r1 = self.get_directional_radius(at1, v)
        r2 = self.get_directional_radius(at2, -v)

        if d <= r1 + r2:
            return None

        v_norm = v / d
        p1 = c1 + v_norm * r1
        p2 = c2 - v_norm * r2

        x1 = p1[0] * self.scale + self.cx_global
        y1 = p1[1] * self.scale + self.cy_global
        x2 = p2[0] * self.scale + self.cx_global
        y2 = p2[1] * self.scale + self.cy_global

        dynamic_width = max(1, int(self.bond_width * self._factor * 5))
        return x1, y1, x2, y2, dynamic_width

    def _draw_bond_selection(self, x1: float, y1: float, x2: float, y2: float, dynamic_width: int):
        """Draws a crisp cyan outline behind a selected bond."""
        sel_width = dynamic_width + max(4, int(12 * self._factor))
        pen = QPen(QColor(0, 190, 255), sel_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def _draw_bond_rounded(self, at1: Atom, at2: Atom):
        """Draw a 3D-shaded (cylinder-like) bond between two atoms."""
        line_data = self._get_bond_line(at1, at2)
        if not line_data:
            return

        x1, y1, x2, y2, dynamic_width = line_data

        dx = x2 - x1
        dy = y2 - y1
        length = sqrt(dx * dx + dy * dy)
        if length < 0.0001:
            return

        # Check Selection
        bond_key = tuple(sorted((at1.name, at2.name)))
        if bond_key in self.selected_bonds:
            self._draw_bond_selection(x1, y1, x2, y2, dynamic_width)

        # 2D Normal vector
        nx = -dy / length
        ny = dx / length

        # Align normal to point towards the global light source (Top-Left is approx -1, -1)
        Lx, Ly = -1.0, -1.0
        if (nx * Lx + ny * Ly) < 0:
            nx = -nx
            ny = -ny

        t = QTransform(ny * dynamic_width / 2.0, -nx * dynamic_width / 2.0, nx * dynamic_width / 2.0,
                       ny * dynamic_width / 2.0,
                       x1, y1)
        self.bond_brush.setTransform(t)

        pen = QPen(self.bond_brush, dynamic_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)  # Creates perfect elliptical intersection blend
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def _draw_bond(self, at1: Atom, at2: Atom) -> None:
        """Draw a flat single-colour bond between two atoms."""
        line_data = self._get_bond_line(at1, at2)
        if not line_data:
            return

        x1, y1, x2, y2, dynamic_width = line_data

        # Check Selection
        bond_key = tuple(sorted((at1.name, at2.name)))
        if bond_key in self.selected_bonds:
            self._draw_bond_selection(x1, y1, x2, y2, dynamic_width)

        pen = QPen(self.bond_color, dynamic_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    # Bounding rect for a unit circle, used by _draw_principal_arcs with QTransform
    _UNIT_RECT = QRectF(-1.0, -1.0, 2.0, 2.0)

    def _draw_principal_arcs(self, atom: Atom, r1: float, r2: float, angle: float) -> None:
        """Draw ORTEP-style curved arcs for the three principal planes of the ADP ellipsoid."""
        if getattr(atom, 'u_eigvals', None) is None or np.any(atom.u_eigvals <= 0):
            self._painter.drawLine(int(-r1), 0, int(r1), 0)
            self._painter.drawLine(0, int(-r2), 0, int(r2))
            return

        eigenvalues = atom.u_eigvals
        eigenvectors = atom.u_eigvecs

        angle_rad = radians(angle)
        cos_a = cos(angle_rad)
        sin_a = sin(angle_rad)
        c = self.adp_scale
        s = self.scale

        # Use cosmetic pen so line width is independent of the QTransform scale
        pen = self._painter.pen()
        pen.setCosmetic(True)
        self._painter.setPen(pen)
        self._painter.setBrush(Qt.BrushStyle.NoBrush)

        base_transform = self._painter.transform()

        # Each principal plane is normal to one eigenvector and spanned by the other two
        plane_pairs = ((1, 2), (0, 2), (0, 1))

        for i_ax, j_ax in plane_pairs:
            li = eigenvalues[i_ax]
            lj = eigenvalues[j_ax]
            if li <= 0 or lj <= 0:
                continue

            ri_3d = c * sqrt(li)
            rj_3d = c * sqrt(lj)

            vi = eigenvectors[:, i_ax]
            vj = eigenvectors[:, j_ax]

            Ax = s * ri_3d * (vi[0] * cos_a + vi[1] * sin_a)
            Bx = s * rj_3d * (vj[0] * cos_a + vj[1] * sin_a)
            Ay = s * ri_3d * (-vi[0] * sin_a + vi[1] * cos_a)
            By = s * rj_3d * (-vj[0] * sin_a + vj[1] * cos_a)

            arc_xform = QTransform(Ax, Ay, Bx, By, 0.0, 0.0)
            self._painter.setTransform(arc_xform * base_transform)

            Az = ri_3d * vi[2]
            Bz = rj_3d * vj[2]
            z_amp = sqrt(Az * Az + Bz * Bz)

            if z_amp < 1e-8:
                self._painter.drawArc(self._UNIT_RECT, 0, 5760)
            else:
                phi_z = atan2(Bz, Az)
                start_deg = degrees(-(phi_z + 1.5 * pi))
                self._painter.drawArc(self._UNIT_RECT, int(start_deg * 16), 2880)

        # Restore the original painter transform
        self._painter.setTransform(base_transform)

    def _draw_selection(self, r1: float, r2: float):
        """Draws a crisp, thick cyan outline to indicate selection."""
        padding = 4.0  # pixels
        pen = QPen(QColor(0, 190, 255), max(3, 12 * self._factor), Qt.PenStyle.SolidLine)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self._painter.setPen(pen)
        self._painter.setBrush(Qt.BrushStyle.NoBrush)

        self._painter.drawEllipse(QRectF(-r1 - padding, -r2 - padding, (r1 + padding) * 2, (r2 + padding) * 2))

    def draw_atom(self, atom: Atom) -> None:
        """Draw a single atom as an ADP ellipsoid, isotropic sphere, or fixed-size circle."""
        if self.show_adps and atom.u_cart is not None:
            if not atom.adp_valid:
                self._draw_invalid_adp(atom)
                return
        cx = atom.screenx
        cy = atom.screeny

        if self.show_adps and atom.u_cart is not None:
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
                    r1 = sqrt(eig1) * self.scale * self.adp_scale
                    r2 = sqrt(eig2) * self.scale * self.adp_scale

                    if abs(b) > 1e-8:
                        angle = degrees(atan2(eig1 - a, b))
                    else:
                        angle = 0.0 if a < c else 90.0

                    self._painter.save()
                    self._painter.translate(cx, cy)
                    self._painter.rotate(angle)

                    # Draw selection outline matching the ellipsoid shape
                    if atom.name in self.selected_atoms:
                        self._draw_selection(r1, r2)

                    max_r = max(r1, r2)
                    sx, sy = -max_r * 0.3, -max_r * 0.3
                    rad = radians(angle)
                    fx = sx * cos(rad) + sy * sin(rad)
                    fy = -sx * sin(rad) + sy * cos(rad)

                    t = QTransform()
                    t.translate(fx, fy)
                    t.scale(max_r * 1.5, max_r * 1.5)
                    atom.adp_brush.setTransform(t)

                    pen = QPen(self.adp_pen_color, 1, Qt.PenStyle.SolidLine)
                    self._painter.setBrush(atom.adp_brush)
                    self._painter.setPen(pen)
                    self._painter.drawEllipse(QRectF(-r1, -r2, 2 * r1, 2 * r2))

                    cross_pen = QPen(QColor(0, 0, 0, 120), 1, Qt.PenStyle.SolidLine)
                    self._painter.setPen(cross_pen)
                    self._draw_principal_arcs(atom, r1, r2, angle)

                    self._painter.restore()
                    return

        circle_size = self.atoms_size
        if self.show_adps and atom.u_iso is not None:
            r = sqrt(atom.u_iso) * self.scale * self.adp_scale
            circle_size = r * 2

        radius = circle_size / 2

        self._painter.save()
        self._painter.translate(cx, cy)

        # Draw selection outline for spheres
        if atom.name in self.selected_atoms:
            self._draw_selection(radius, radius)

        self._painter.setPen(QPen(self.fallback_pen_color, 1, Qt.PenStyle.SolidLine))
        self._painter.setBrush(atom.sphere_brush)
        self._painter.drawEllipse(QRectF(-radius, -radius, circle_size, circle_size))

        self._painter.restore()

    def _draw_invalid_adp(self, atom: Atom) -> None:
        cx = atom.screenx
        cy = atom.screeny

        size = self.atoms_size

        self._painter.save()
        self._painter.translate(cx, cy)

        # Selection highlight
        if atom.name in self.selected_atoms:
            self._draw_selection(size / 2, size / 2)

        # Cube points (isometric projection)
        s = size * 0.4
        dx = size * 0.3
        dy = -size * 0.3

        # Front face
        fl = QtCore.QPointF(-s - dx / 2, s - dy / 2)
        fr = QtCore.QPointF(s - dx / 2, s - dy / 2)
        tl = QtCore.QPointF(-s - dx / 2, -s - dy / 2)
        tr = QtCore.QPointF(s - dx / 2, -s - dy / 2)

        # Back face visible corners
        btl = QtCore.QPointF(-s + dx / 2, -s + dy / 2)
        btr = QtCore.QPointF(s + dx / 2, -s + dy / 2)
        bbr = QtCore.QPointF(s + dx / 2, s + dy / 2)

        # Faces
        front_face = [tl, tr, fr, fl]
        top_face = [tl, btl, btr, tr]
        right_face = [tr, btr, bbr, fr]

        # Colors for shading (light source top-left)
        color_base = atom.color
        color_light = atom.color_light
        color_dark = atom.color_dark

        pen = QPen(self.fallback_pen_color, 1)
        self._painter.setPen(pen)

        # Draw faces with simple shading
        self._painter.setBrush(QBrush(color_light))
        self._painter.drawPolygon(QtGui.QPolygonF(top_face))
        self._painter.setBrush(QBrush(color_base))
        self._painter.drawPolygon(QtGui.QPolygonF(front_face))
        self._painter.setBrush(QBrush(color_dark))
        self._painter.drawPolygon(QtGui.QPolygonF(right_face))
        # self.draw_npd_text(dx, dy, s)
        self._painter.restore()

    def draw_npd_text(self, dx: float, dy: float, s: float):
        self._painter.setPen(QPen(Qt.GlobalColor.white))
        font = self._painter.font()
        old_size = font.pixelSize()
        font.setPixelSize(max(int(self.atoms_size * 0.3), 1))
        self._painter.setFont(font)
        front_rect = QRectF(-s - dx / 2, -s - dy / 2, 2 * s, 2 * s)
        self._painter.drawText(front_rect, Qt.AlignmentFlag.AlignCenter, "NPD")
        font.setPixelSize(old_size)
        self._painter.setFont(font)

    def draw_label(self, atom: Atom):
        """Draw the atom's name next to its ellipsoid/sphere."""
        self._painter.setPen(QPen(QColor(100, 50, 5), 2, Qt.PenStyle.SolidLine))
        r_pix = self.get_spherical_radius(atom) * self.scale
        self._painter.drawText(int(atom.screenx + r_pix + 2), int(atom.screeny - r_pix - 2), atom.name)

    def get_conntable_from_atoms(self, extra_param: float = 1.2) -> tuple:
        """Build a connectivity table from atomic coordinates and covalent radii."""
        connections = []
        h = ('H', 'D')
        for num1, at1 in enumerate(self.atoms, 0):
            for num2, at2 in enumerate(self.atoms, 0):
                if num1 == num2:
                    continue
                if (at1.part != 0 and at2.part != 0) and at1.part != at2.part:
                    continue
                d = dist(at1.coordinate, at2.coordinate)
                if d > 4.0:
                    continue
                if (at1.radius + at2.radius) * extra_param > d:
                    if at1.type_ in h and at2.type_ in h:
                        continue
                    if (num2, num1) in connections:
                        continue
                    connections.append((num1, num2))
        return tuple(connections)


class Atom:
    """Internal representation of a single atom for rendering."""

    __slots__ = ['coordinate', 'name', 'part', 'radius', 'screenx', 'screeny', 'type_', 'u_cart', 'color',
                 'color_light', 'color_dark', 'u_iso', 'z', 'u_eigvals', 'u_eigvecs', 'u_inv',
                 'sphere_brush', 'adp_brush', 'adp_valid']

    def __init__(self, x: float, y: float, z: float, name: str, type_: str, part: int) -> None:
        self.coordinate = np.array([x, y, z], dtype=np.float32)
        self.adp_valid = True
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
        self.color_dark = self.color.darker(180)
        self.u_iso = None
        self.u_eigvals = None
        self.u_eigvecs = None
        self.u_inv = None

        self.sphere_brush = QBrush()
        sg = QRadialGradient(0.35, 0.35, 1.0)
        sg.setCoordinateMode(QRadialGradient.CoordinateMode.ObjectBoundingMode)
        sg.setColorAt(0.0, self.color_light)
        sg.setColorAt(0.4, self.color)
        sg.setColorAt(1.0, self.color_dark)
        self.sphere_brush = QBrush(sg)

        ag = QRadialGradient(0.0, 0.0, 1.0)
        ag.setColorAt(0.0, self.color_light)
        ag.setColorAt(0.4, self.color)
        ag.setColorAt(1.0, self.color_dark)
        self.adp_brush = QBrush(ag)

    def __repr__(self) -> str:
        return str((self.name, self.type_, self.coordinate))


def display(atoms: list[Atomtuple],
            cell: tuple[float, float, float, float, float, float] | None = None,
            adps: dict[str, tuple[float, float, float, float, float, float]] | None = None,
            grow_callback: Callable | None = None) -> NoReturn:
    """Launch a standalone :class:`MoleculeWidget` viewer window for testing."""
    import time
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    render_widget = MoleculeWidget(None)

    t1 = time.perf_counter()

    adp_checkbox = QtWidgets.QCheckBox("Show ADP")
    label_checkbox = QtWidgets.QCheckBox("Show Labels")
    bond_type_checkbox = QtWidgets.QCheckBox("Round Bonds")
    hydrogens_checkbox = QtWidgets.QCheckBox("Show Hydrogens")

    bw_label = QtWidgets.QLabel("Bond Width:")
    bond_width_spinbox = QtWidgets.QSpinBox()
    bond_width_spinbox.setRange(1, 15)
    bond_width_spinbox.setValue(3)

    adp_checkbox.setChecked(True)
    bond_type_checkbox.setChecked(True)
    hydrogens_checkbox.setChecked(True)

    adp_checkbox.toggled.connect(lambda x: render_widget.show_adp(x))
    label_checkbox.toggled.connect(lambda x: render_widget.show_labels(x))
    bond_type_checkbox.toggled.connect(lambda x: render_widget.show_round_bonds(x))
    hydrogens_checkbox.toggled.connect(lambda x: render_widget.show_hydrogens(x))
    bond_width_spinbox.valueChanged.connect(lambda x: render_widget.set_bond_width(x))

    render_widget.set_bond_width(3)
    render_widget.open_molecule(atoms=atoms, cell=cell, adps=adps)
    render_widget.labels = False
    render_widget.show_round_bonds(True)
    print(f'Time to display molecule: {time.perf_counter() - t1:5.4} s')

    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)
    vl = QtWidgets.QVBoxLayout(central_widget)
    window.setMinimumSize(1400, 900)
    vl.addWidget(render_widget)

    hl = QtWidgets.QHBoxLayout()
    hl.addWidget(adp_checkbox)
    hl.addWidget(label_checkbox)
    hl.addWidget(bond_type_checkbox)
    hl.addWidget(hydrogens_checkbox)
    hl.addWidget(bw_label)
    hl.addWidget(bond_width_spinbox)

    if grow_callback is not None:
        grow_checkbox = QtWidgets.QCheckBox("Grow")

        def handle_grow(checked: bool):
            if checked:
                grown_atoms = grow_callback()
                render_widget.grow_molecule(atoms=grown_atoms, cell=cell, adps=adps)
            else:
                render_widget.grow_molecule(atoms=atoms, cell=cell, adps=adps)

        grow_checkbox.toggled.connect(handle_grow)
        hl.addWidget(grow_checkbox)

    hl.addStretch()
    vl.addLayout(hl)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":

    try:
        from finalcif.cif.cif_file_io import CifContainer
        from sdm import SDM

        # Load sample data
        # cif = CifContainer('test-data/p21c.cif')
        # cif = CifContainer(r'../41467_2015.cif')  # huge
        # cif = CifContainer(r"D:\frames\Workordner\huge_structure\p-1-finalcif.cif")
        # cif = CifContainer('tests/examples/1979688.cif')
        cif = CifContainer('test-data/p31c.cif')
        # cif = CifContainer('/Users/daniel/Documents/GitHub/StructureFinder/test-data/668839.cif')
        # cif = CifContainer(Path('test-data/4060314.cif'))
        cif.load_this_block(len(cif.doc) - 1)

        # Build generic ADP dictionary
        adp_dict = {}
        for dp in cif.displacement_parameters():
            adp_dict[dp.label] = (to_float(dp.U11), to_float(dp.U22), to_float(dp.U33),
                                  to_float(dp.U23), to_float(dp.U13), to_float(dp.U12))


        def build_grown_structure() -> list[Atomtuple]:
            # optional callback for symmetry expansion
            atoms_fract = tuple(cif.atoms_fract)
            sdm = SDM(atoms_fract, cif.symmops, cif.cell[:6], centric=cif.is_centrosymm)
            needsymm = sdm.calc_sdm()
            return sdm.packer(sdm, needsymm)


        display(atoms=list(cif.atoms_orth),
                cell=cif.cell[:6],
                adps=adp_dict,
                grow_callback=build_grown_structure)

    except ImportError:
        print("FinalCif not found. Provide your own Atomtuples to run.")
