import sys

import vtk
from PyQt5 import QtWidgets, QtCore
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from finalcif.cif.atoms import element2num, get_radius_from_element
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.misc import distance


class MoleculeWidget(QtWidgets.QWidget):
    def __init__(self, parent, cif: CifContainer):
        super().__init__(parent=parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        istyle = vtk.vtkInteractorStyleSwitch()
        istyle.SetCurrentStyleToTrackballCamera()

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vlayout.addWidget(self.vtkWidget)
        interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        interactor.SetInteractorStyle(istyle)

        # molecule = self.get_molecule()
        #molecule = self.add_atoms()

        # Does not work, why?
        """colors = vtk.vtkDoubleArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        colors.Allocate(3 * molecule.GetNumberOfAtoms() + 1)
        for i in range(molecule.GetNumberOfAtoms()):
            num = molecule.GetAtomAtomicNumber(i)
            # print(i, element2rgb[num2element[num]])
            colors.InsertNextTypedTuple(num2rgb[num])
            # colors.InsertNextTypedTuple((1, 1, 1))
            # print(element2rgb[num2element[num]])
        molecule.GetAtomData().AddArray(colors)"""

        self.mol_mapper = vtk.vtkMoleculeMapper()
        # Belongs to the non-working code above:
        # mol_mapper.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "Colors")
        # mol_mapper.SetInputArrayToProcess(0, 0, 0, 4, "Colors")
        #self.mol_mapper.SetInputData(molecule)
        self.mol_mapper.SetRenderAtoms(True)
        # self.mol_mapper.UseBallAndStickSettings()
        self.mol_mapper.UseLiquoriceStickSettings()
        self.mol_mapper.SetUseMultiCylindersForBonds(False)
        self.mol_mapper.SetBondRadius(0.07)
        self.mol_mapper.SetAtomicRadiusScaleFactor(0.25)
        self.mol_mapper.SetBondColorMode(1)
        self.mol_mapper.SetBondColor(80, 80, 80)

        mol_actor = vtk.vtkActor()
        mol_actor.SetMapper(self.mol_mapper)
        # mol_actor.GetProperty().SetAmbient(0.0)
        # mol_actor.GetProperty().SetDiffuse(1.0)
        # mol_actor.GetProperty().SetSpecular(0.0)
        # mol_actor.GetProperty().SetSpecularPower(40.0)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(mol_actor)
        self.renderer.SetBackground(255, 255, 255)
        self.renderer.SetLayer(0)
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().Zoom(1.6)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        interactor.Initialize()

    def add_atoms(self, cif):
        molecule = vtk.vtkMolecule()
        for atom in cif.atoms_orth:
            molecule.AppendAtom(element2num[atom.type], atom.x, atom.y, atom.z)
        self.make_bonds(molecule, cif)
        return molecule

    def redraw(self, cif: CifContainer):
        """
        Loads a different molecule.
        """
        molecule = self.add_atoms(cif)
        self.mol_mapper.SetInputData(molecule)
        self.renderer.ResetCamera()
        self.renderer.GetActiveCamera().Zoom(1.5)

    def make_bonds(self, molecule, cif: CifContainer, extra_param: float = 0.48) -> None:
        h_atoms = ('H', 'D')
        for num1, at1 in enumerate(cif.atoms_orth, 0):
            rad1 = get_radius_from_element(at1.type)
            for num2, at2 in enumerate(cif.atoms_orth, 0):
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

    render_widget = MoleculeWidget(None, cif)
    render_widget.redraw(cif)

    window.setCentralWidget(render_widget)
    window.setMinimumSize(500, 500)
    window.show()
    window.raise_()
    # render_widget.redraw(CifContainer('tests/examples/1979688.cif'))
    sys.exit(app.exec_())
