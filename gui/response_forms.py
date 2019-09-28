# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/daniel/GitHub/FinalCif/./gui/response_forms.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(613, 514)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.helpFrame = QtWidgets.QFrame(Dialog)
        self.helpFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.helpFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.helpFrame.setObjectName("helpFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.helpFrame)
        self.horizontalLayout_2.setContentsMargins(6, 6, -1, 12)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.helpFrame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.helpFrame, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.responseFormsListWidget = QtWidgets.QListWidget(self.groupBox)
        self.responseFormsListWidget.setObjectName("responseFormsListWidget")
        self.verticalLayout.addWidget(self.responseFormsListWidget)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Validation Response Forms"))
        self.label.setText(_translate("Dialog", "Every form you fill out will be written to the cif file."))
        self.pushButton_3.setText(_translate("Dialog", "Request Forms"))
        self.pushButton.setText(_translate("Dialog", "Save Response Forms"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.groupBox.setTitle(_translate("Dialog", "List of Alerts"))
