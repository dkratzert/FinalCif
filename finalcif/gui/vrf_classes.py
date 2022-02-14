from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, \
    QVBoxLayout, QWidget


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        # self.setFrameShadow(QFrame.Sunken)
        # gives a black line:
        # self.setFrameShadow(QFrame.Plain)
        self.setFrameShadow(QFrame.Raised)


class VREF():
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
    def response(self, txt):
        self._response = self.response + txt

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, txt):
        self._problem = self.problem + txt

    def __repr__(self):
        txt = (
            "{}\n"
            "{}\n".format(self.problem, self.response)
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
        self.mainVLayout.addWidget(QHLine())
        # The button to get help for the respective alert:
        self.helpbutton = QPushButton('Help')
        self.helpbutton.clicked.connect(self.show_help)
        self.response_text_edit = QTextEdit()
        self.alert_label_box()
        self.problem_label_box()
        self.response_label_box()
        self.setAutoFillBackground(False)
        self.help = help
        #
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
        type = level[-1] if len(level) > 1 else 'General A  Alert'
        color = 'lightgray'
        if type == 'A':
            color = 'rgb(240, 88, 70)'  # 'red'
        elif type == 'B':
            color = 'rgb(252, 119, 20)'
        elif type == 'C':
            color = 'yellow'
        elif type == 'G':
            color = 'green'
        if len(type) == 1:
            type = type + '  Alert'
        num = self.form['alert_num'] if 'alert_num' in self.form else ''
        if self.is_multi_cif:
            name = "  --> {}".format(self.form['data_name'])
        else:
            name = ''
        label.setText("{} {} {}".format(type, num, name))
        style = 'QLabel {{ font-size: 12px; background-color: {:s}; ' \
                'font-weight: bold;' \
                'border: 1px solid gray;' \
                'border-radius: 5px; ' \
                'margin: 0px;' \
                'padding: 4px;' \
                'opacity: 230;' \
                '}}'.format(color)
        label.setStyleSheet(style)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hlayout.addItem(spacerItem)
        hlayout.addWidget(self.helpbutton)
        self.mainVLayout.addWidget(frame)

    def problem_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 4, 4, 4)
        frame.setLayout(hlayout)
        p_label = QLabel()
        hlayout.addWidget(p_label, 0, Qt.AlignTop)
        p_label.setText('Problem:   ')
        p_label.setAlignment(Qt.AlignLeft)
        p_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold; }')
        p_text_label = QLabel()
        p_text_label.setAlignment(Qt.AlignLeft)
        hlayout.addWidget(p_text_label)
        hlayout.setAlignment(Qt.AlignLeft)
        p_text_label.setText(self.form['problem'])
        self.mainVLayout.addWidget(frame)

    def response_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 8, 4, 12)
        frame.setLayout(hlayout)
        resp_label = QLabel()
        hlayout.addWidget(resp_label, 0, Qt.AlignTop)
        resp_label.setText('Response: ')
        resp_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold }')
        self.response_text_edit.setFocusPolicy(Qt.StrongFocus)
        hlayout.addWidget(self.response_text_edit)
        self.mainVLayout.addWidget(frame)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    form = {'level'    : 'PLAT035_ALERT_1_B',
            'name'     : '_vrf_PLAT035_DK_zucker2_0m',
            'data_name': 'DK_zucker2_0m',
            'problem'  : '_chemical_absolute_configuration Info  Not Given     Please Do '
                         '!  ',
            'alert_num': 'PLAT035'}
    web = MyVRFContainer(form, help='helptext', parent=None, is_multi_cif=True)
    app.exec_()
    web.raise_()

    v = VREF()
    v.key = '_vrf_PLAT035_DK_zucker2_0m'
    v.problem = '_chemical_absolute_configuration Info  Not Given     Please Do '
    v.response = 'a response'

    print(v.value)
