# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/daniel/GitHub/FinalCif/./gui/response_forms.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResponseFormsEditor(object):
    def setupUi(self, ResponseFormsEditor):
        ResponseFormsEditor.setObjectName("ResponseFormsEditor")
        ResponseFormsEditor.resize(613, 514)
        ResponseFormsEditor.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(ResponseFormsEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonFrame = QtWidgets.QFrame(ResponseFormsEditor)
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonFrame.setLineWidth(0)
        self.ButtonFrame.setObjectName("ButtonFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ButtonFrame)
        self.horizontalLayout.setContentsMargins(12, 0, -1, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SavePushButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.SavePushButton.setObjectName("SavePushButton")
        self.horizontalLayout.addWidget(self.SavePushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.CancelPushButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.CancelPushButton.setObjectName("CancelPushButton")
        self.horizontalLayout.addWidget(self.CancelPushButton)
        self.gridLayout.addWidget(self.ButtonFrame, 3, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(ResponseFormsEditor)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.responseFormsListWidget = QtWidgets.QListWidget(self.groupBox)
        self.responseFormsListWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.responseFormsListWidget.setAutoScroll(False)
        self.responseFormsListWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.responseFormsListWidget.setProperty("showDropIndicator", False)
        self.responseFormsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.responseFormsListWidget.setObjectName("responseFormsListWidget")
        self.verticalLayout.addWidget(self.responseFormsListWidget)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.helpFrame = QtWidgets.QFrame(ResponseFormsEditor)
        self.helpFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.helpFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.helpFrame.setObjectName("helpFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.helpFrame)
        self.horizontalLayout_2.setContentsMargins(6, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.helpFrame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.helpFrame, 2, 0, 1, 1)

        self.retranslateUi(ResponseFormsEditor)
        QtCore.QMetaObject.connectSlotsByName(ResponseFormsEditor)

    def retranslateUi(self, ResponseFormsEditor):
        _translate = QtCore.QCoreApplication.translate
        ResponseFormsEditor.setWindowTitle(_translate("ResponseFormsEditor", "Validation Response Forms"))
        self.SavePushButton.setText(_translate("ResponseFormsEditor", "Save Response Forms"))
        self.CancelPushButton.setText(_translate("ResponseFormsEditor", "Cancel"))
        self.groupBox.setTitle(_translate("ResponseFormsEditor", "List of CheckCif Alerts"))
        self.label.setText(_translate("ResponseFormsEditor", "Every form you fill out will be written to the cif file."))
