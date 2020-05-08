#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from typing import Union

import gemmi
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QSize
from PyQt5.QtWidgets import QTableView, QHeaderView

from cif.cif_file_io import CifContainer


class Loop():
    def __init__(self, cif: CifContainer, tableview: QTableView):
        self.table = tableview
        self.cif = cif
        self.headerlabels = []
        self.model: Union[TableModel, None] = None

    def make_model(self, loopnum: int):
        # get data from cif loop
        self.model = TableModel(self.get_data(loopnum), self.headerlabels)
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width = header.sectionSize(column) + 10
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width)

    def get_data(self, loopnum: int):
        data = []
        self.headerlabels = self.cif.loops[loopnum].tags
        for v in self.cif.block.find(self.headerlabels):
            data.append([gemmi.cif.as_string(x) for x in v])
        return data


class TableModel(QAbstractTableModel):
    def __init__(self, data, header):
        super(TableModel, self).__init__()
        self._data = data
        self._header = header

    def data(self, index: QModelIndex, role: int = None):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

        if role == Qt.SizeHintRole:
            return QSize(120, 50)

        if role == Qt.TextAlignmentRole:
            pass
            # value = self._data[index.row()][index.column()]
            # if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
            #    # Align right, vertical middle.
            #    return Qt.AlignVCenter + Qt.AlignRight

    def headerData(self, section, orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._header[section])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignLeft

    def rowCount(self, parent=None, *args, **kwargs):
        """
        The length of the outer list.
        """
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Tkes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        return len(self._data[0])
