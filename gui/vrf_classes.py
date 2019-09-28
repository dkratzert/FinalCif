from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QFrame, \
    QLineEdit, QTextEdit


class MyVRFContainer(QWidget):

    def __init__(self, form: dict, parent=None):
        """
        A Widget to display each validation response form.
        #TODO: test what happens if form is empty or contains garbage

        :param form: a dictionary with:
                    {'level':   'PLAT035_ALERT_1_B',
                     'name':    '_vrf_PLAT035_DK_zucker2_0m',
                     'problem': '_chemical_absolute_configuration ...',
                     'alert_num': 'PLAT035'}
        :param parent: Parent widget
        """
        super().__init__(parent)
        self.form = form
        #self.setMinimumWidth(400)
        self.color = 'red'  # TODO: get colr from alert type
        self.mainVLayout = QVBoxLayout(self)
        self.setLayout(self.mainVLayout)
        #self.setStyleSheet('QWidget { border: 2px solid black }')
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setSpacing(0)
        # The button to get help for the respective alert:
        self.helpbutton = QPushButton('Help')
        self.alert_label_box()
        self.problem_label_box()
        self.response_label_box()
        #
        self.show()

    def alert_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 4, 4, 4)
        frame.setLayout(hlayout)
        # does not work:
        #frame.setStyleSheet('QFrame { padding: 0px; margin: 0px;}')
        label = QLabel()
        hlayout.addWidget(label)
        level = self.form['level']
        type = level[-1] if len(level) > 1 else 'General Alert'
        num = self.form['alert_num'] if 'alert_num' in self.form else ''
        label.setText( "{} alert {}".format(type, num))
        style = 'QLabel {{ font-size: 12px; background-color: {:s}; ' \
                          'border: 2px solid black;' \
                          'border-radius: 5px; ' \
                          'margin: 0px;' \
                          'padding: 4px;' \
                '}}'.format(self.color)
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
        #p_label.setAlignment()
        p_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold; }')
        p_text_label = QLabel()
        hlayout.addWidget(p_text_label)
        p_text_label.setText(self.form['problem'])
        self.mainVLayout.addWidget(frame)

    def response_label_box(self):
        frame = QFrame()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(4, 4, 4, 4)
        frame.setLayout(hlayout)
        resp_label = QLabel()
        hlayout.addWidget(resp_label, 0, Qt.AlignTop)
        resp_label.setText('Response: ')
        resp_label.setStyleSheet('QLabel { font-size: 12px; font-weight: bold }')
        response_text_edit = QTextEdit()
        hlayout.addWidget(response_text_edit)
        self.mainVLayout.addWidget(frame)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    form = {'level'     : 'PLAT035_ALERT_1_B',
            'name'      : '_vrf_PLAT035_DK_zucker2_0m',
            'problem'   : '_chemical_absolute_configuration Info  Not Given     Please Do '
                          '!  ',
            'alert_num': 'PLAT035'}
    web = MyVRFContainer(form)
    app.exec_()
    web.raise_()

