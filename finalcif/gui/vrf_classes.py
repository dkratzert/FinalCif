from qtpy import QtCore
from qtpy.QtCore import QSize, Qt
from qtpy.QtWidgets import QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, \
    QVBoxLayout, QWidget


class QHLine(QFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setFrameShape(QFrame.Shape.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        # gives a black line:
        # self.setFrameShadow(QFrame.Plain)
        self.setFrameShadow(QFrame.Shadow.Raised)


class VREF:
    """
    _vrf_PLAT699_DK_zucker2_0m
    ;
    PROBLEM: Missing _exptl_crystal_description Value .......     Please Do !
    RESPONSE: ...
    ;
    """

    def __init__(self):
        self.key = ''
        self.data_name = ''
        self._problem = 'PROBLEM: '
        self._response = 'RESPONSE: '

    @property
    def value(self):
        return self.__repr__()

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, txt) -> None:
        self._response = self.response + txt

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, txt) -> None:
        self._problem = self.problem + txt

    def __repr__(self):
        txt = (
            f"{self.problem}\n"
            f"{self.response}\n"
        )
        return txt

    def __str__(self):
        return self.__repr__()


class MyVRFContainer(QWidget):

    def __init__(self, form: dict, help: str, parent=None, is_multi_cif=False):
        """
        A Widget to display each validation response form.

        :param form: a dictionary with:
                    {'level':   'PLAT035_ALERT_1_B',
                     'data_name': 'DK_zucker2_0m',
                     'name':    '_vrf_PLAT035_DK_zucker2_0m',
                     'problem': '_chemical_absolute_configuration ...',
                     'alert_num': 'PLAT035'}
        :param parent: Parent widget
        """
        super().__init__(parent)
        self.is_multi_cif = is_multi_cif
        self.setParent(parent)
        self.form = form
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
        self.response_text_edit = QTextEdit()
        self.alert_label_box()
        self.problem_label_box()
        self.response_label_box()
        self.setAutoFillBackground(False)
        self.help = help
        self.show()

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
        level = self.form['level']
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
        num = self.form['alert_num'] if 'alert_num' in self.form else ''
        if self.is_multi_cif:
            name = "  --> {}".format(self.form['data_name'])
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
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        hlayout.addItem(spacerItem)
        hlayout.addWidget(self.helpbutton)
        self.mainVLayout.addWidget(frame)

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
        p_text_label.setText(self.form['problem'])
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
        hlayout.addWidget(self.response_text_edit)
        self.mainVLayout.addWidget(frame)


if __name__ == '__main__':
    from qtpy.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    form = {'level'    : 'PLAT035_ALERT_1_B',
            'name'     : '_vrf_PLAT035_DK_zucker2_0m',
            'data_name': 'DK_zucker2_0m',
            'problem'  : '_chemical_absolute_configuration Info  Not Given     Please Do '
                         '!  ',
            'alert_num': 'PLAT035'}
    web = MyVRFContainer(form, help='helptext', parent=None, is_multi_cif=True)
    app.exec()
    web.raise_()

    v = VREF()
    v.key = '_vrf_PLAT035_DK_zucker2_0m'
    v.problem = '_chemical_absolute_configuration Info  Not Given     Please Do '
    v.response = 'a response'

    print(v.value)
