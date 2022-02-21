"""To be used with PDB files from NMR. The script reads a PDB file containing
several models and calculates standard deviation of the positions of heavy
atoms (C, N, O). The standard deviations are visualised as semi-transparent
ellipsoids (vtkTensorGlyphs) plotted against the average structure (in tube
representation."""
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

        self.cif = cif

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
        molecule = self.add_atoms()

        """ Does not work, why?
        colors = vtk.vtkDoubleArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        colors.Allocate(3 * molecule.GetNumberOfAtoms()+1)
        for i in range(molecule.GetNumberOfAtoms()):
            num = molecule.GetAtomAtomicNumber(i)
            #print(i, element2rgb[num2element[num]])
            colors.InsertNextTypedTuple(element2rgb[num2element[num]])
            #colors.InsertNextTypedTuple((1, 1, 1))
            #print(element2rgb[num2element[num]])
        molecule.GetAtomData().AddArray(colors)
        # molMapper.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "Colors")
        # molMapper.SetInputArrayToProcess(0, 0, 0, 4, "Colors")
        """

        molMapper = vtk.vtkMoleculeMapper()
        molMapper.SetInputData(molecule)
        molMapper.SetRenderAtoms(True)
        molMapper.UseBallAndStickSettings()
        molMapper.SetUseMultiCylindersForBonds(False)
        molMapper.SetBondRadius(0.07)
        molMapper.SetAtomicRadiusScaleFactor(0.2)
        molMapper.SetBondColorMode(0)
        molMapper.SetBondColor(80, 80, 80)

        molActor = vtk.vtkActor()
        molActor.SetMapper(molMapper)

        renderer = vtk.vtkRenderer()
        renderer.AddActor(molActor)
        renderer.SetBackground(255, 255, 255)
        renderer.SetLayer(0)
        renderer.ResetCamera()
        renderer.GetActiveCamera().Zoom(1.6)
        self.vtkWidget.GetRenderWindow().AddRenderer(renderer)
        interactor.Initialize()

    def add_atoms(self):
        molecule = vtk.vtkMolecule()
        for atom in self.cif.atoms_orth:
            vatom = molecule.AppendAtom(element2num[atom.type], atom.x, atom.y, atom.z)
        self.make_bonds(molecule)
        return molecule

    def make_bonds(self, molecule, extra_param: float = 0.48) -> None:
        h_atoms = ('H', 'D')
        for num1, at1 in enumerate(self.cif.atoms_orth, 0):
            rad1 = get_radius_from_element(at1.type)
            for num2, at2 in enumerate(self.cif.atoms_orth, 0):
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
    # Molecule(atoms).draw()
    app = QtWidgets.QApplication(sys.argv)
    # create our new Qt MainWindow
    window = QtWidgets.QMainWindow()
    # create our new custom VTK Qt widget
    # shx = Shelxfile()
    # shx.read_file('tests/examples/1979688-finalcif.res')
    # atoms = [x.cart_coords for x in shx.atoms]
    cif = CifContainer('tests/examples/1979688.cif')
    render_widget = MoleculeWidget(None, cif)  # cif.atoms_orth)
    # add and show
    window.setCentralWidget(render_widget)
    window.setMinimumSize(500, 500)
    window.show()
    window.raise_()
    # start the event loop
    sys.exit(app.exec_())
