#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from pathlib import Path
import gemmi

from FinalCif.cif.cif_file_io import CifContainer

cif = CifContainer(Path(r'D:/GitHub/StructureFinder/test-data/p-1_a.cif'))
st = gemmi.read_structure('D:/GitHub/StructureFinder/test-data/p-1_a.cif')
st.setup_entities()
ns = gemmi.NeighborSearch(st, st.cell, 5).populate()
#ns = gemmi.NeighborSearch(st, 3)#.populate()
#print(cif.atoms())
#st = gemmi.make_structure_from_block(cif.block)
#st = cif.atomic_struct 

#ns = gemmi.NeighborSearch(st, st.cell).populate()
for n_atom, atom in enumerate(st.sites):
    print(atom)
    if ns.find_site_neighbors(atom, 1.1, 3):
        ns.add_atom(atom, 0, 0, n_atom)

