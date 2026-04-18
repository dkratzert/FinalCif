from qtpy import QtCore
from qtpy.QtCore import QSize, Qt, Signal
from qtpy.QtGui import QColor, QPalette
from qtpy.QtWidgets import QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, \
    QVBoxLayout, QWidget

from finalcif.cif.vrf_entry import VRFEntry


class QHLine(QFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setFrameShape(QFrame.Shape.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        # gives a black line:
        # self.setFrameShadow(QFrame.Plain)
        self.setFrameShadow(QFrame.Shadow.Raised)


class MyVRFContainer(QWidget):
    # Emitted when the user clicks the Delete button; carries a reference to self.
    deleted = Signal(object)
    # Emitted when the user clicks the Templates button; carries the VRF key (str).
    template_requested = Signal(str)

    def __init__(self, vrf_entry: VRFEntry, help: str, parent=None, is_multi_cif=False):
        """
        A Widget to display each validation response form.

        :param vrf_entry: a VRFEntry dataclass instance holding key, data_name, problem,
                          response, alert_num, level, and source for this alert.
        :param help: help text shown in the Help dialog for this alert.
        :param parent: Parent widget.
        :param is_multi_cif: True when the document contains multiple data blocks.
        """
        super().__init__(parent)
        self.is_multi_cif = is_multi_cif
        self.setParent(parent)
        self.vrf_entry = vrf_entry
        # self.setMinimumWidth(400)
        self.mainVLayout = QVBoxLayout(self)
        self.setLayout(self.mainVLayout)
        # self.setStyleSheet('QWidget { border: 2px solid black }')
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        self.mainVLayout.addWidget(QHLine(self))
        # The button to get help for the respective alert:
        self.helpbutton = QPushButton('Help')
        self.helpbutton.clicked.connect(self.show_help)
        if not help.strip():
            self.helpbutton.setEnabled(False)
        self.deletebutton = QPushButton('Delete')
        self.deletebutton.clicked.connect(self._on_delete)
        self.templatesbutton = QPushButton('Templates')
        self.templatesbutton.clicked.connect(self._on_templates)
        self.response_text_edit = QTextEdit()
        self.alert_label_box()
        self.problem_label_box()
        self.response_label_box()
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('lightgray'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.help = help
        self.show()

    def _on_delete(self) -> None:
        self.deleted.emit(self)

    def _on_templates(self) -> None:
        self.template_requested.emit(self.vrf_entry.key)

    def show_help(self):
        dialog = QDialog(parent=self)
        layout = QVBoxLayout()
        label = QLabel(self.help, parent=dialog)
        layout.addWidget(label)
        label.adjustSize()
        dialog.setLayout(layout)
        dialog.adjustSize()
        # dialog.setFixedHeight(200)
        # dialog.setFixedWidth(200)
        dialog.show()

    def sizeHint(self) -> QSize:
        return QSize(400, 150)

    def alert_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 8, 4, 4)
        frame.setLayout(hlayout)
        # does not work:
        # frame.setStyleSheet('QFrame { padding: 0px; margin: 0px;}')
        label = QLabel()
        hlayout.addWidget(label)
        level = self.vrf_entry.level
        atype = level[-1] if len(level) > 1 else 'General A  Alert'
        color = 'lightgray'
        if atype == 'A':
            color = 'rgb(240, 88, 70)'  # 'red'
        elif atype == 'B':
            color = 'rgb(252, 119, 20)'
        elif atype == 'C':
            color = 'yellow'
        elif atype == 'G':
            color = 'green'
        if len(atype) == 1:
            atype = atype + '  Alert'
        num = self.vrf_entry.alert_num
        if self.is_multi_cif:
            name = "  --> {}".format(self.vrf_entry.data_name)
        else:
            name = ''
        label.setText(f"{atype} {num} {name}")
        style = f'QLabel {{ font-size: 12px; background-color: {color:s}; ' \
                'font-weight: bold;' \
                'border: 1px solid gray;' \
                'border-radius: 5px; ' \
                'margin: 0px;' \
                'padding: 4px;' \
                'opacity: 230;' \
                '}'
        label.setStyleSheet(style)
        # Source badge: shows whether the VRF came from CheckCIF or from the CIF file
        self.source_label = QLabel()
        self._apply_source_style(self.vrf_entry.source)
        hlayout.addWidget(self.source_label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        hlayout.addItem(spacerItem)
        hlayout.addWidget(self.templatesbutton)
        hlayout.addWidget(self.helpbutton)
        hlayout.addWidget(self.deletebutton)
        self.mainVLayout.addWidget(frame)

    def _apply_source_style(self, source: str) -> None:
        """Update the source badge label to reflect *source*."""
        if source == 'cif':
            self.source_label.setText('Saved in CIF')
            self.source_label.setStyleSheet(
                'QLabel { font-size: 10px; background-color: rgb(70, 160, 160);'
                ' color: white; border-radius: 3px; padding: 2px 5px; }'
            )
        else:
            self.source_label.setText('From CheckCIF')
            self.source_label.setStyleSheet(
                'QLabel { font-size: 10px; background-color: rgb(70, 110, 200);'
                ' color: white; border-radius: 3px; padding: 2px 5px; }'
            )

    def update_source(self, new_source: str) -> None:
        """Dynamically update the source badge (e.g. after a new CheckCIF run)."""
        self.vrf_entry.source = new_source
        self._apply_source_style(new_source)

    def problem_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 4, 4, 4)
        frame.setLayout(hlayout)
        p_label = QLabel()
        hlayout.addWidget(p_label, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        p_label.setText('Problem:   ')
        p_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        p_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold; }')
        p_text_label = QLabel()
        p_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        hlayout.addWidget(p_text_label)
        hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        p_text_label.setText(self.vrf_entry.problem)
        self.mainVLayout.addWidget(frame)

    def response_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 8, 4, 12)
        frame.setLayout(hlayout)
        resp_label = QLabel()
        hlayout.addWidget(resp_label, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        resp_label.setText('Response: ')
        resp_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold }')
        self.response_text_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if self.vrf_entry.response:
            self.response_text_edit.setPlainText(self.vrf_entry.response)
        hlayout.addWidget(self.response_text_edit)
        self.mainVLayout.addWidget(frame)


if __name__ == '__main__':
    from qtpy.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    entry = VRFEntry(
        key='_vrf_PLAT035_DK_zucker2_0m',
        data_name='DK_zucker2_0m',
        problem='_chemical_absolute_configuration Info  Not Given     Please Do !  ',
        response='?',
        alert_num='PLAT035',
        level='PLAT035_ALERT_1_B',
    )
    web = MyVRFContainer(entry, help='helptext', parent=None, is_multi_cif=True)
    app.exec()
    web.raise_()
