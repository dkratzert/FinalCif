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
"""

import sys
from dataclasses import dataclass
from math import sqrt, cos, sin, dist, radians, atan2, degrees
from pathlib import Path
from typing import NoReturn, Callable

import numpy as np
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QPalette, QImage, QResizeEvent, QWheelEvent, \
    QRadialGradient, QLinearGradient

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

    def __init__(self, parent=None):
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
        self.bond_drawer = self._draw_bond

        # scaling factor for ADP ellipsoids in screen coordinates
        # 1.5382 is the standard ORTEP scaling factor for 50% probability:
        self.adp_scale = 1.5382
        self.molecule_center = np.array([0, 0, 0])
        self.molecule_radius = 10
        self._lastPos = self.pos()
        self._painter: None | QPainter = None
        self.x_angle = 0
        self.y_angle = 0

        self.scale = 150.0
        self.cx_global = 0.0
        self.cy_global = 0.0

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
        """Set the pixel size used for atom labels and schedule a repaint.

        :param font_size: Desired font size in pixels (clamped to a minimum of 1).
        """
        if font_size < 0:
            font_size = 1
        self.fontsize = font_size
        self.update()

    def clear(self) -> None:
        """Remove all atoms and bonds from the widget."""
        self.open_molecule(atoms=[])

    def show_labels(self, value: bool):
        """Toggle the display of non-hydrogen atom labels.

        :param value: ``True`` to show labels, ``False`` to hide them.
        """
        self.labels = value
        self.update()

    def show_adp(self, value: bool):
        """Toggle the display of ADP ellipsoids / isotropic spheres.

        When disabled, all atoms are drawn as fixed-size circles.

        :param value: ``True`` to show displacement parameters, ``False`` to hide them.
        """
        self.show_adps = value
        self.update()

    def show_round_bonds(self, bond_type: bool = True):
        """Switch between flat and 3D-shaded (rounded) bond rendering.

        :param bond_type: ``True`` for rounded/cylinder-shaded bonds,
                          ``False`` for flat single-colour bonds.
        """
        if not bond_type:
            self.bond_drawer = self._draw_bond
        else:
            self.bond_drawer = self._draw_bond_rounded
        self.update()

    def open_molecule(self, atoms: list[Atomtuple],
                      cell: tuple[float, float, float, float, float, float] | None = None,
                      adps: dict[str, tuple[float, float, float, float, float, float]] | None = None) -> None:
        """Populate the widget with molecule data and trigger a repaint.

        Builds the internal atom list, connectivity table, and render objects.
        When *cell* and *adps* are both provided, anisotropic displacement
        parameter ellipsoids are computed; otherwise atoms fall back to
        isotropic spheres or fixed-size circles.

        Hydrogen atoms that lack a ``u_iso`` value automatically inherit
        80 % of the ``u_iso`` of their bonded non-hydrogen neighbor.

        :param atoms: Atom positions as a list of
            :class:`~finalcif.displaymol.sdm.Atomtuple` instances.
        :param cell: Optional unit-cell parameters
            ``(a, b, c, alpha, beta, gamma)`` in Ångströms / degrees.
        :param adps: Optional mapping of atom label to anisotropic
            displacement parameters ``(U11, U22, U33, U23, U13, U12)``.
        """
        self._cell = cell
        self._adp_map = adps if adps is not None else {}

        if self._cell is not None and self.show_adps:
            self.calc_amatrix()

        self.atoms.clear()
        self.make_adps(atoms)
        self.connections = self.get_conntable_from_atoms()
        self.get_center_and_radius()

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
        """Compute the orthogonalisation matrix and reciprocal-lattice lengths.

        Derives ``_amatrix`` (fractional → Cartesian transformation) and the
        reciprocal-axis lengths ``_astar``, ``_bstar``, ``_cstar`` from the
        current unit-cell parameters stored in ``_cell``.  These quantities
        are required by :meth:`_uij_to_cart`.
        """
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
        """Convert Atomtuples to internal :class:`Atom` objects with Cartesian ADPs.

        Replaces the contents of :attr:`atoms`.  For each atom whose label
        appears in :attr:`_adp_map`, the fractional *Uij* values are
        transformed to a Cartesian tensor via :meth:`_uij_to_cart`, and the
        equivalent isotropic displacement ``u_iso`` is set to the trace / 3.

        :param atoms: Source atoms to convert.
        """
        self.atoms.clear()
        for at in atoms:
            a = Atom(at.x, at.y, at.z, at.label, at.type, at.part)
            if self._adp_map and self._cell and at.label in self._adp_map:
                try:
                    uvals = self._adp_map[at.label]
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
        """Repaint the widget by re-rendering the molecule scene.
        """
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

    def wheelEvent(self, event: QWheelEvent):
        """Increase or decrease the label font size on scroll."""
        if event.angleDelta().y() > 0:
            self.setLabelFont(self.fontsize + 2)
        elif event.angleDelta().y() < 0:
            self.setLabelFont(self.fontsize - 2)

    def save_image(self, filename: Path, image_scale: float = 1.5) -> None:
        """Render the current molecule view to an image file.

        :param filename: Destination path (format inferred from suffix).
        :param image_scale: Multiplicative resolution scale factor.
        """
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
        """Convert fractional *Uij* displacement parameters to a Cartesian tensor.

        Applies an optional fractional symmetry-rotation matrix before
        transforming the 3×3 *Uij* tensor through the orthogonalisation
        matrix and reciprocal-lattice scaling.

        :param uvals: Anisotropic displacement parameters
            ``(U11, U22, U33, U23, U13, U12)`` in fractional coordinates.
        :param symm_matrix: Optional 3×3 fractional rotation matrix of the
            symmetry operation that generated this atom.
        :return: 3×3 numpy array of the Cartesian displacement tensor.
        """
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
        """Translate the molecule center based on the middle-button drag delta.

        :param event: The current mouse-move event.
        """
        self.molecule_center[0] += (self._lastPos.x() - event.position().x()) / 50
        self.molecule_center[1] += (self._lastPos.y() - event.position().y()) / 50
        self.update()

    def zoom_molecule(self, event: QMouseEvent):
        """Adjust the zoom / scale factor based on the right-button drag delta.

        :param event: The current mouse-move event.
        """
        self._factor += (self._lastPos.y() - event.position().y()) / 350
        self._factor = max(0.005, self._factor)
        self.zoom -= (self._lastPos.y() - event.position().y()) / 350
        self.atoms_size = abs(self._factor * 70)
        self.update()

    def rotate_molecule(self, event: QMouseEvent):
        """Rotate the molecule around X and Y axes using the left-button drag delta.

        Applies a combined rotation matrix to all atom coordinates and ADP
        tensors using vectorised numpy operations.

        :param event: The current mouse-move event.
        """
        self.y_angle = -(event.position().x() - self._lastPos.x()) / 80
        self.x_angle = (event.position().y() - self._lastPos.y()) / 80
        R_y = self.rotate_y()
        R_x = self.rotate_x()
        R = np.dot(R_x, R_y)

        # Single bulk vector rotation instead of individual loops
        if self.atoms:
            self._coords_array = np.dot(self._coords_array - self.molecule_center, R.T) + self.molecule_center

            if np.any(self._has_adp):
                self._ucart_array = np.matmul(R, np.matmul(self._ucart_array, R.T))

            for i, at in enumerate(self.atoms):
                at.coordinate = self._coords_array[i]
                at.z = at.coordinate[2]  # cache explicit z property for fast sorting
                if self._has_adp[i]:
                    at.u_cart = self._ucart_array[i]

        self.update()

    def get_spherical_radius(self, atom: Atom) -> float:
        """Return an approximate isotropic radius for UI purposes (e.g. label offset).

        When ADP display is active and ``u_iso`` is available, the radius is
        ``sqrt(u_iso)``; otherwise a fixed default is returned.

        :param atom: The atom to query.
        :return: Radius in model-space units.
        """
        if self.show_adps and atom.u_iso is not None:
            return sqrt(atom.u_iso)  # * self.adp_scale
        return 35.0 / 150.0

    def get_directional_radius(self, atom: Atom, v: np.ndarray) -> float:
        """Return the distance from the atom centre to its ellipsoid surface along *v*.

        When the atom has an anisotropic displacement tensor, the ray–ellipsoid
        intersection is computed exactly using the inverse of *U_cart*.
        Falls back to an isotropic sphere (``sqrt(u_iso) * adp_scale``) or
        a fixed default radius when no ADP data is available.

        :param atom: The atom whose radius is queried.
        :param v: Direction vector (need not be normalised) in Cartesian space.
        :return: Radius along *v* in model-space units, or ``0.0`` if *v* is
            near-zero.
        """
        d = np.linalg.norm(v)
        if d < 1e-8:
            return 0.0

        if self.show_adps and atom.u_cart is not None:
            u = v / d
            try:
                # Intersect ray with 3D Covariance Ellipsoid
                # R = C / sqrt( u^T * U^-1 * u )
                U_inv = np.linalg.inv(atom.u_cart)
                val = np.dot(u, np.dot(U_inv, u))
                if val > 0:
                    return self.adp_scale / sqrt(val)
            except np.linalg.LinAlgError:
                pass

        # Fallback to sphere
        if self.show_adps and atom.u_iso is not None:
            return sqrt(atom.u_iso) * self.adp_scale

        return 35.0 / 150.0

    def draw(self) -> None:
        """Execute the main rendering pass.

        Projects every atom to screen coordinates, sorts render objects
        back-to-front by depth, then paints bonds and atoms (with optional
        labels) using the active :attr:`_painter`.
        """
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
            if item.is_bond:
                self.bond_drawer(item.atom1, item.atom2)
            else:
                self.draw_atom(item.atom1)
                if self.labels and item.atom1.type_ not in hydrogens:
                    self.draw_label(item.atom1)
        self._painter.end()

    def calculate_z_order(self):
        """Sort :attr:`objects` back-to-front by depth for the painter's algorithm.

        Bonds use the average depth of their two atoms; atom items use the
        atom's own depth.
        """
        for item in self.objects:
            if item.is_bond:
                item.z_order = (item.atom1.z + item.atom2.z) / 2.0
            else:
                item.z_order = item.atom1.z

        self.objects.sort(reverse=True, key=lambda item: item.z_order)

    def get_center_and_radius(self):
        """Compute the bounding sphere of the current atom set.

        Sets :attr:`molecule_center` to the midpoint of the axis-aligned
        bounding box and :attr:`molecule_radius` to the maximum distance
        from that centre to any atom (plus a small padding).
        """
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

    def _draw_bond_rounded(self, at1: Atom, at2: Atom):
        """Draw a 3D-shaded (cylinder-like) bond between two atoms.

        Uses a :class:`QLinearGradient` perpendicular to the bond axis to
        simulate specular highlighting and shadow on a cylindrical surface.
        The bond is clipped at the directional ADP radii of each atom so
        that it does not overlap the ellipsoids.

        :param at1: First atom of the bond.
        :param at2: Second atom of the bond.
        """
        c1 = at1.coordinate
        c2 = at2.coordinate
        v = c2 - c1
        d = np.linalg.norm(v)

        # Calculate precise bounding limits along the directional vector
        r1 = self.get_directional_radius(at1, v)
        r2 = self.get_directional_radius(at2, -v)

        if d <= r1 + r2:
            return

        v_norm = v / d
        p1 = c1 + v_norm * r1
        p2 = c2 - v_norm * r2

        x1 = p1[0] * self.scale + self.cx_global
        y1 = p1[1] * self.scale + self.cy_global
        x2 = p2[0] * self.scale + self.cx_global
        y2 = p2[1] * self.scale + self.cy_global

        dx = x2 - x1
        dy = y2 - y1
        length = sqrt(dx * dx + dy * dy)
        if length < 0.0001:
            return

        # 2D Normal vector
        nx = -dy / length
        ny = dx / length

        # Align normal to point towards the global light source (Top-Left is approx -1, -1)
        Lx, Ly = -1.0, -1.0
        if (nx * Lx + ny * Ly) < 0:
            nx = -nx
            ny = -ny

        dynamic_width = max(self.bond_width, min(15, int(self.bond_width * self._factor * 11)))
        w_half = dynamic_width / 2.0

        # Gradient from lit side (+n) to shadow side (-n)
        grad = QLinearGradient(x1 + nx * w_half, y1 + ny * w_half,
                               x1 - nx * w_half, y1 - ny * w_half)
        grad.setColorAt(0.0, self.bond_grad_dark)  # Slight rim light/ambient
        grad.setColorAt(0.2, self.bond_grad_light)  # Main specular highlight
        grad.setColorAt(1.0, self.bond_grad_shadow)  # Core shadow

        pen = QPen(QBrush(grad), dynamic_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)  # Creates perfect elliptical intersection blend
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def _draw_bond(self, at1: Atom, at2: Atom) -> None:
        """Draw a flat single-colour bond between two atoms.

        The bond is clipped at the directional ADP radii of each atom so
        that it does not overlap the ellipsoids.

        :param at1: First atom of the bond.
        :param at2: Second atom of the bond.
        """
        c1 = at1.coordinate
        c2 = at2.coordinate
        v = c2 - c1
        d = np.linalg.norm(v)

        r1 = self.get_directional_radius(at1, v)
        r2 = self.get_directional_radius(at2, -v)

        if d <= r1 + r2:
            return

        v_norm = v / d
        p1 = c1 + v_norm * r1
        p2 = c2 - v_norm * r2

        x1 = p1[0] * self.scale + self.cx_global
        y1 = p1[1] * self.scale + self.cy_global
        x2 = p2[0] * self.scale + self.cx_global
        y2 = p2[1] * self.scale + self.cy_global

        dynamic_width = max(self.bond_width, min(15, int(self.bond_width * self._factor * 11)))
        pen = QPen(self.bond_color, dynamic_width, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self._painter.setPen(pen)
        self._painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_atom(self, atom: Atom) -> None:
        """Draw a single atom as an ADP ellipsoid, isotropic sphere, or fixed-size circle.

        When an anisotropic displacement tensor is available, the 2D projected
        ellipse is computed from the xy-block of *u_cart*.  Otherwise the atom
        is rendered as a radial-gradient circle whose size depends on *u_iso*
        (if present) or a fixed fallback radius.

        :param atom: The atom to render.
        """
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
                    gradient = self.make_gradient(angle, atom, r1, r2)
                    brush = QBrush(gradient)
                    pen = QPen(self.adp_pen_color, 1, Qt.PenStyle.SolidLine)
                    self._painter.setBrush(brush)
                    self._painter.setPen(pen)
                    self._painter.drawEllipse(int(-r1), int(-r2), int(2 * r1), int(2 * r2))

                    cross_pen = QPen(QColor(0, 0, 0, 120), 1, Qt.PenStyle.SolidLine)
                    self._painter.setPen(cross_pen)
                    self._painter.drawLine(int(-r1), 0, int(r1), 0)
                    self._painter.drawLine(0, int(-r2), 0, int(r2))

                    self._painter.restore()
                    return

        circle_size = self.atoms_size
        if self.show_adps and atom.u_iso is not None:
            r = sqrt(atom.u_iso) * self.scale * self.adp_scale
            circle_size = r * 2

        radius = circle_size / 2

        gradient = QRadialGradient(cx - radius * 0.3, cy - radius * 0.3, circle_size)
        gradient.setColorAt(0.0, atom.color_light)
        gradient.setColorAt(0.4, atom.color)
        gradient.setColorAt(1.0, atom.color_dark)

        self._painter.setPen(QPen(self.fallback_pen_color, 1, Qt.PenStyle.SolidLine))
        self._painter.setBrush(QBrush(gradient))
        self._painter.drawEllipse(int(cx - radius), int(cy - radius),
                                  int(circle_size), int(circle_size))

    def make_gradient(self, angle: float, atom: Atom, r1: float, r2: float) -> QRadialGradient:
        """Create a radial gradient for an ADP ellipsoid with a simulated light source.

        The gradient focal point is offset to produce a 3D shading effect,
        and the colours are derived from the atom's element colour.

        :param angle: Rotation angle of the ellipse in degrees.
        :param atom: The atom whose colour is used.
        :param r1: Semi-axis along the first eigenvector (screen pixels).
        :param r2: Semi-axis along the second eigenvector (screen pixels).
        :return: Configured :class:`QRadialGradient`.
        """
        max_r = max(r1, r2)
        sx, sy = -max_r * 0.3, -max_r * 0.3
        rad = radians(angle)
        fx = sx * cos(rad) + sy * sin(rad)
        fy = -sx * sin(rad) + sy * cos(rad)

        gradient = QRadialGradient(fx, fy, max_r * 1.5)
        gradient.setColorAt(0.0, atom.color_light)
        gradient.setColorAt(0.4, atom.color)
        gradient.setColorAt(1.0, atom.color_dark)
        return gradient

    def draw_label(self, atom: Atom):
        """Draw the atom's name next to its ellipsoid/sphere.

        The label is offset from the atom centre by its spherical radius so
        that it does not overlap the drawn shape.

        :param atom: The atom whose label is drawn.
        """
        self._painter.setPen(QPen(QColor(100, 50, 5), 2, Qt.PenStyle.SolidLine))
        r_pix = self.get_spherical_radius(atom) * self.scale
        self._painter.drawText(int(atom.screenx + r_pix + 2), int(atom.screeny - r_pix - 2), atom.name)

    def get_conntable_from_atoms(self, extra_param: float = 1.2) -> tuple:
        """Build a connectivity table from atomic coordinates and covalent radii.

        Two atoms are considered bonded when their distance is less than
        ``(r1 + r2) * extra_param``.  Hydrogen–hydrogen bonds are excluded,
        and atoms belonging to different non-zero disorder parts are skipped.

        :param extra_param: Tolerance factor applied to the sum of covalent
            radii (default 1.2).
        :return: Tuple of ``(index1, index2)`` pairs referencing :attr:`atoms`.
        """
        connections = []
        h = ('H', 'D')
        for num1, at1 in enumerate(self.atoms, 0):
            for num2, at2 in enumerate(self.atoms, 0):
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
    """Internal representation of a single atom for rendering.

    Stores Cartesian coordinates, element-derived color and radius, screen
    projection coordinates, and optional displacement parameters (anisotropic
    tensor ``u_cart`` and isotropic equivalent ``u_iso``).

    :param x: Cartesian X coordinate (Å).
    :param y: Cartesian Y coordinate (Å).
    :param z: Cartesian Z coordinate (Å).
    :param name: Atom label, e.g. ``'C3'``.
    :param type_: Element symbol, e.g. ``'C'``.
    :param part: SHELX disorder part number (0 = all parts).
    """

    __slots__ = ['coordinate', 'name', 'part', 'radius', 'screenx', 'screeny', 'type_', 'u_cart', 'color',
                 'color_light', 'color_dark', 'u_iso', 'z']

    def __init__(self, x: float, y: float, z: float, name: str, type_: str, part: int) -> None:
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


def display(atoms: list[Atomtuple],
            cell: tuple[float, float, float, float, float, float] | None = None,
            adps: dict[str, tuple[float, float, float, float, float, float]] | None = None,
            grow_callback: Callable | None = None) -> NoReturn:
    """Launch a standalone :class:`MoleculeWidget` viewer window for testing.

    Opens a :class:`QMainWindow` containing the molecule widget together with
    checkboxes to toggle ADP display, labels, rounded bonds, and an optional
    symmetry-grow control.

    :param atoms: Atom positions as a list of
        :class:`~finalcif.displaymol.sdm.Atomtuple` instances.
    :param cell: Optional unit-cell parameters
        ``(a, b, c, alpha, beta, gamma)`` in Ångströms / degrees.
    :param adps: Optional mapping of atom label to anisotropic displacement
        parameters ``(U11, U22, U33, U23, U13, U12)``.
    :param grow_callback: Optional callable that returns a grown atom list
        when the *Grow* checkbox is toggled on.
    """
    import time
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    render_widget = MoleculeWidget(None)

    t1 = time.perf_counter()

    adp_checkbox = QtWidgets.QCheckBox("Show ADP")
    label_checkbox = QtWidgets.QCheckBox("Show Labels")
    bond_type_checkbox = QtWidgets.QCheckBox("Round Bonds")

    adp_checkbox.setChecked(True)

    adp_checkbox.toggled.connect(lambda x: render_widget.show_adp(x))
    label_checkbox.toggled.connect(lambda x: render_widget.show_labels(x))
    bond_type_checkbox.toggled.connect(lambda x: render_widget.show_round_bonds(x))

    render_widget.open_molecule(atoms=atoms, cell=cell, adps=adps)
    render_widget.labels = False
    render_widget.show_round_bonds(True)
    print(f'Time to display molecule: {time.perf_counter() - t1:5.4} s')

    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)
    vl = QtWidgets.QVBoxLayout(central_widget)
    window.setMinimumSize(800, 600)
    vl.addWidget(render_widget)

    hl = QtWidgets.QHBoxLayout()
    hl.addWidget(adp_checkbox)
    hl.addWidget(label_checkbox)
    hl.addWidget(bond_type_checkbox)

    if grow_callback is not None:
        grow_checkbox = QtWidgets.QCheckBox("Grow")

        def handle_grow(checked: bool):
            if checked:
                grown_atoms = grow_callback()
                render_widget.open_molecule(atoms=grown_atoms, cell=cell, adps=adps)
            else:
                render_widget.open_molecule(atoms=atoms, cell=cell, adps=adps)

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
        cif = CifContainer('test-data/p21c.cif')
        # cif = CifContainer(r'../41467_2015.cif') # huge
        # cif = CifContainer(r"D:\frames\Workordner\huge_structure\p-1-finalcif.cif")
        # cif = CifContainer('tests/examples/1979688.cif')
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
