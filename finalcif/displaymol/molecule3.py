"""To be used with PDB files from NMR. The script reads a PDB file containing
several models and calculates standard deviation of the positions of heavy
atoms (C, N, O). The standard deviations are visualised as semi-transparent
ellipsoids (vtkTensorGlyphs) plotted against the average structure (in tube
representation."""
import sys
from typing import Generator, Any

import numpy
import vtk
from PyQt5 import QtWidgets
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from finalcif.cif.cif_file_io import CifContainer


class MoleculeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.painter = None
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)
        istyle = vtk.vtkInteractorStyleSwitch()
        istyle.SetCurrentStyleToTrackballCamera()
        #interactor = vtk.vtkRenderWindowInteractor()
        #interactor.SetRenderWindow(window)

        #self.frame = QtWidgets.QFrame()
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        #self.vlayout.addWidget(self.vtkWidget)
        self.vlayout.addWidget(self.vtkWidget)
        interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        interactor.SetInteractorStyle(istyle)

        #self.atoms: List[Atom] = []

        symdict = {"N": 7, "C": 6, "O": 8, "H": 1}
        coords = []
        symbols = []
        pdbf = open("finalcif/displaymol/2evq.pdb")
        line = pdbf.readline()
        natoms = 0
        while line[:6] != "MODEL ":
            line = pdbf.readline()
        while line:
            modelno = int(line[6:])
            line = pdbf.readline()
            i = 0
            while line[:6] != "ENDMDL":
                sym = line[12:16].strip()
                if sym[:1] in ["N", "C", "O"]:
                    if modelno == 1:
                        coords.append([[], [], []])
                        natoms += 1
                        symbols.append(symdict[sym[0]])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords[i][0].append(x)
                    coords[i][1].append(y)
                    coords[i][2].append(z)
                    i += 1
                line = pdbf.readline()
            while line and line[:6] != "MODEL ":
                line = pdbf.readline()
        pdbf.close()

        coords = numpy.array(coords)
        averaged = numpy.mean(coords, axis=2)
        """
        stddev = numpy.std(coords, axis=2)
        
        atom_points = vtk.vtkPoints()
        atom_points.SetNumberOfPoints(natoms)
        
        tensors = vtk.vtkFloatArray()
        tensors.SetNumberOfComponents(9)
        tensors.SetNumberOfTuples(natoms)
        tensors.SetName("ellipsoids")
        
        for i in range(natoms):
            a = averaged[i]
            atom_points.InsertPoint(i, a[0], a[1], a[2])
            r = stddev[i] * 3.0
            tensors.SetTuple(i, (r[0], 0.0, 0.0,
                                 0.0, r[1], 0.0,
                                 0.0, 0.0, r[2]))
        
        grid = vtk.vtkUnstructuredGrid()
        grid.SetPoints(atom_points)
        grid.GetPointData().SetTensors(tensors)
        
        sphere = vtk.vtkSphereSource()
        sphere.SetPhiResolution(16)
        sphere.SetThetaResolution(16)
        
        ellipsoids = vtk.vtkTensorGlyph()
        ellipsoids.SetInputData(grid)
        ellipsoids.SetSourceConnection(sphere.GetOutputPort())
        
        ellMapper = vtk.vtkPolyDataMapper()
        ellMapper.SetInputConnection(ellipsoids.GetOutputPort())
        
        ellActor = vtk.vtkActor()
        ellActor.SetMapper(ellMapper)
        #ellActor.GetProperty().SetOpacity(0.3)
        """
        molecule = vtk.vtkMolecule()

        for i in range(natoms):
            s = symbols[i]
            a = averaged[i]
            molecule.AppendAtom(s, a[0], a[1], a[2])

        for i in range(natoms):
            a = averaged[i]
            for j in range(i + 1, natoms):
                b = averaged[j]
                d = numpy.sqrt(numpy.sum((a - b) ** 2))
                if d < 1.7:
                    molecule.AppendBond(i, j, 1)

        molMapper = vtk.vtkMoleculeMapper()
        # molMapper.UseLiquoriceStickSettings()
        molMapper.SetInputData(molecule)
        molMapper.SetRenderAtoms(True)
        # molMapper.SetAtomicRadiusType()
        # molMapper.SetAtomicRadiusTypeToUnitRadius()
        molMapper.UseBallAndStickSettings()  # .SetRenderAtoms(True)
        molMapper.SetUseMultiCylindersForBonds(False)
        molMapper.SetBondRadius(0.07)
        molMapper.SetAtomicRadiusScaleFactor(0.2)
        molMapper.SetBondColorMode(0)
        molMapper.SetBondColor(80, 80, 80)

        molActor = vtk.vtkActor()
        molActor.SetMapper(molMapper)

        renderer = vtk.vtkRenderer()
        renderer.AddActor(molActor)
        # renderer.AddActor(ellActor)
        renderer.SetBackground(255,255,255)
        renderer.SetLayer(0)
        self.vtkWidget.GetRenderWindow().AddRenderer(renderer)


        #window = vtk.vtkRenderWindow()
        #window.AddRenderer(renderer)
        #window.SetSize(1800, 1800)




        #interactor.Initialize()
        #interactor.Start()
        #self.frame.setLayout(self.vlayout)
        #self.setCentralWidget(self.frame)
        #self.setLayout(self.vlayout)
        #self.show()
        interactor.Initialize()


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
    render_widget = MoleculeWidget()#cif.atoms_orth)
    # add and show
    window.setCentralWidget(render_widget)
    window.setMinimumSize(300, 300)
    window.show()
    window.raise_()
    # start the event loop
    sys.exit(app.exec_())