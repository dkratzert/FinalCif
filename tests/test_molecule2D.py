import pytest
from pathlib import Path
from fastmolwidget.sdm import Atomtuple
from finalcif.cif.cif_file_io import CifContainer
from fastmolwidget.molecule2D import calc_volume, MoleculeWidget, RenderItem
from qtpy import QtWidgets

app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])


def test_calc_volume():
    # Test with orthogonal cell (e.g., cubic 10, 10, 10, 90, 90, 90)
    vol = calc_volume(10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
    assert vol == pytest.approx(1000.0, rel=1e-5)

    # Test with monoclinic cell
    vol = calc_volume(10.0, 10.0, 10.0, 90.0, 120.0, 90.0)
    assert vol == pytest.approx(866.0254, rel=1e-5)


def test_render_item():
    item = RenderItem(is_bond=True, z_order=1.5)
    assert item.is_bond is True
    assert item.z_order == 1.5
    assert item.atom1 is None


def test_molecule_widget_creation():
    widget = MoleculeWidget()
    assert widget.atoms_size == 12
    assert widget.fontsize == 13
    assert widget.bond_width == 3
    assert widget.labels is True
    assert widget._show_adps is True
    assert widget.bond_drawer == widget._draw_bond_rounded


def test_molecule_widget_with_cif():
    cif = CifContainer(Path('tests/examples/1979688_small.cif'))
    adp_dict = {dp.label: (dp.U11, dp.U22, dp.U33, dp.U23, dp.U13, dp.U12) for dp in cif.displacement_parameters()}

    widget = MoleculeWidget()
    widget.resize(800, 600)
    widget.open_molecule(list(cif.atoms_orth), cif.cell[:6], adp_dict)
    widget.show()

    assert len(widget.atoms) == 94

    clicked_atom = widget.atoms[7]
    clicked_atom.screenx = 80
    clicked_atom.screeny = 222
    assert widget.is_point_inside_atom(clicked_atom, 80.0, 222) == True

    # Ensure grabbing the widget content as pixmap (invoking paintEvent) does not crash
    pixmap = widget.grab()
    assert not pixmap.isNull()

    # Test setting parameters and re-drawing
    widget.labels = False
    widget._show_adps = False
    widget.atoms_size = 15
    widget.bond_width = 4
    widget.repaint()

    # Test grabbing again to ensure settings do not crash rendering
    pixmap_updated = widget.grab()
    assert not pixmap_updated.isNull()

    # Test interaction (zooming, reset)
    widget.reset_view()
    widget.zoom = 1.2

    pixmap_transformed = widget.grab()
    assert not pixmap_transformed.isNull()


def test_molecule_widget_toggles():
    widget = MoleculeWidget()

    # Test setting label visibility
    widget.set_labels_visible(False)
    assert widget.labels is False
    widget.show_labels(True)
    assert widget.labels is True

    # Test hydrogen visibility
    widget.show_hydrogens(False)
    assert widget.show_hydrogens_flag is False

    # Test ADP visibility
    widget.show_adps(False)
    assert widget._show_adps is False

    # Test label font setting
    widget.setLabelFont(20)
    assert widget.fontsize == 20
    widget.setLabelFont(-5)
    assert widget.fontsize == 1

    # Test set background color
    from qtpy.QtGui import QColor, QPalette
    from qtpy import QtCore
    widget.set_background_color(QColor(QtCore.Qt.GlobalColor.black))
    assert widget.palette().color(QPalette.ColorRole.Window).name() == QColor(QtCore.Qt.GlobalColor.black).name()


def test_molecule_widget_clear():
    widget = MoleculeWidget()

    # create dummy atoms
    dummy_atom = Atomtuple('C1', 'C', 0.0, 0.0, 0.0, 0)
    widget.open_molecule([dummy_atom])
    assert len(widget.atoms) == 1

    assert widget.is_point_inside_atom(widget.atoms[0], 0, 0) == True
    assert widget.is_point_inside_atom(widget.atoms[0], 100, 100) == False

    widget.clear()
    assert len(widget.atoms) == 0


def test_molecule_widget_rotation_matrices():
    widget = MoleculeWidget()
    widget.x_angle = 3.14159 / 2  # 90 degrees approx
    widget.y_angle = 3.14159 / 2

    rx = widget.rotate_x()
    ry = widget.rotate_y()

    import numpy as np
    assert rx.shape == (3, 3)
    assert ry.shape == (3, 3)
    # just checking that they run and return a matrix
    assert isinstance(rx, np.ndarray)


def test_mouse_events_record_position():
    widget = MoleculeWidget()

    from qtpy.QtGui import QMouseEvent
    from qtpy.QtCore import QPointF
    from qtpy import QtCore

    event = QMouseEvent(QtCore.QEvent.Type.MouseButtonPress, QPointF(10.0, 20.0), QPointF(10.0, 20.0),
                        QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier)
    widget.mousePressEvent(event)

    assert widget._lastPos == QPointF(10.0, 20.0)
    assert widget._pressPos == QPointF(10.0, 20.0)
