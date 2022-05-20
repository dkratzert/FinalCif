import sys

import vtk
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QSurfaceFormat
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkDomainsChemistry import vtkPeriodicTable

from finalcif.cif.atoms import element2num, get_radius_from_element, num2rgb
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.misc import distance


# Some say this makes it more compatible to old hardware, but I am not sure:
# vtkmodules.qt.QVTKRWIBase = 'QGLWidget'


class MoleculeWidget(QtWidgets.QWidget):
    """
    This widget is currently unused in FinalCif.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        vtk.vtkObject.GlobalWarningDisplayOff()
        self.initialized = False
        QSurfaceFormat.defaultFormat().setProfile(QSurfaceFormat.CompatibilityProfile)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        istyle = vtk.vtkInteractorStyleSwitch()
        istyle.SetCurrentStyleToTrackballCamera()
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(istyle)
        self.mol_mapper = vtk.vtkMoleculeMapper()
        lut = self._modify_color_lookup_table()
        self.mol_mapper.SetLookupTable(lut)
        self.mol_mapper.SetRenderAtoms(True)
        # self.mol_mapper.UseBallAndStickSettings()
        self.mol_mapper.UseLiquoriceStickSettings()
        self.mol_mapper.SetUseMultiCylindersForBonds(False)
        self.mol_mapper.SetBondRadius(0.065)
        self.mol_mapper.SetAtomicRadiusScaleFactor(0.27)
        self.mol_mapper.SetBondColorMode(0)
        self.mol_mapper.SetBondColor(80, 80, 80)
        mol_actor = vtk.vtkActor()
        mol_actor.SetMapper(self.mol_mapper)
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(mol_actor)
        self.renderer.SetBackground(255, 255, 255)
        self.renderer.SetLayer(0)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

    def _modify_color_lookup_table(self):
        lut = vtk.vtkLookupTable()
        vtkPeriodicTable().GetDefaultLUT(lut)
        # Replace existing lut with own table:
        for num, color in num2rgb.items():
            lut.SetTableValue(num, *color)
        return lut

    def _add_atoms(self, atoms):
        molecule = vtk.vtkMolecule()
        for atom in atoms:
            molecule.AppendAtom(element2num[atom.type], atom.x, atom.y, atom.z)
        self._make_bonds(molecule, list(atoms))
        return molecule

    def draw(self, atoms):
        """
        Loads a different molecule.
        """
        molecule = self._add_atoms(atoms)
        self.mol_mapper.SetInputData(molecule)
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().Zoom(1.7)
        self.interactor.Render()

    def _make_bonds(self, molecule, atoms, extra_param: float = 0.48) -> None:
        h_atoms = ('H', 'D')
        for num1, at1 in enumerate(atoms, 0):
            rad1 = get_radius_from_element(at1.type)
            for num2, at2 in enumerate(atoms, 0):
                if at1.part * at2.part != 0 and at1.part != at2.part:
                    continue
                if at1.label == at2.label:
                    continue
                d = distance(at1.x, at1.y, at1.z, at2.x, at2.y, at2.z)
                if d > 4.0:  # makes bonding faster (longer bonds do not exist)
                    continue
                rad2 = get_radius_from_element(at2.type)
                if (rad1 + rad2) + extra_param > d > 0:
                    if at1.type in h_atoms and at2.type in h_atoms:
                        continue
                    molecule.AppendBond(num1, num2, 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    # cif = CifContainer('tests/examples/1979688.cif')
    cif = CifContainer('test-data/p21c.cif')

    render_widget = MoleculeWidget(None)
    render_widget.draw(atoms=[x for x in cif.atoms_orth])

    window.setCentralWidget(render_widget)
    window.setMinimumSize(500, 500)
    window.show()
    window.raise_()
    # render_widget.redraw(CifContainer('tests/examples/1979688.cif'))
    sys.exit(app.exec_())
