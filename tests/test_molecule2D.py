import pytest
from finalcif.displaymol.molecule2D import calc_volume, MoleculeWidget, RenderItem
from finalcif.displaymol.sdm import Atomtuple

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

from qtpy import QtWidgets

def test_molecule_widget_creation():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    widget = MoleculeWidget()
    assert widget.atoms_size == 12
    assert widget.fontsize == 13
    assert widget.bond_width == 3
    assert widget.labels is True
    assert widget.show_adps is True
    assert widget.bond_drawer == widget._draw_bond_rounded

from finalcif.cif.cif_file_io import CifContainer
from qtpy.QtCore import Qt

def test_molecule_widget_with_cif():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])

    cif = CifContainer(r'D:\_DEV\GitHub\FinalCif\tests\examples\1979688_small.cif')
    adp_dict = {dp.label: (dp.U11, dp.U22, dp.U33, dp.U23, dp.U13, dp.U12) for dp in cif.displacement_parameters()}

    widget = MoleculeWidget()
    widget.resize(800, 600)
    widget.open_molecule(list(cif.atoms_orth), cif.cell[:6], adp_dict)
    widget.show()

    assert len(widget.atoms) == 94

    # Ensure grabbing the widget content as pixmap (invoking paintEvent) does not crash
    pixmap = widget.grab()
    assert not pixmap.isNull()

    # Test setting parameters and re-drawing
    widget.labels = False
    widget.show_adps = False
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

