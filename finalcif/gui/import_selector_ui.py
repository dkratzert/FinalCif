# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_selector_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_importSelectMainWindow(object):
    def setupUi(self, importSelectMainWindow):
        if not importSelectMainWindow.objectName():
            importSelectMainWindow.setObjectName(u"importSelectMainWindow")
        importSelectMainWindow.resize(800, 600)
        self.centralwidget = QWidget(importSelectMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.importInfoLabel = QLabel(self.centralwidget)
        self.importInfoLabel.setObjectName(u"importInfoLabel")

        self.verticalLayout.addWidget(self.importInfoLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 10, 10, -1)
        self.importTable_keys = QTableWidget(self.centralwidget)
        if (self.importTable_keys.columnCount() < 1):
            self.importTable_keys.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.importTable_keys.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.importTable_keys.setObjectName(u"importTable_keys")
        self.importTable_keys.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.importTable_keys)

        self.importTable_loops = QTableWidget(self.centralwidget)
        if (self.importTable_loops.columnCount() < 1):
            self.importTable_loops.setColumnCount(1)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.importTable_loops.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        self.importTable_loops.setObjectName(u"importTable_loops")
        self.importTable_loops.verticalHeader().setVisible(False)

        self.horizontalLayout_2.addWidget(self.importTable_loops)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.importSelectedPushbutton = QPushButton(self.centralwidget)
        self.importSelectedPushbutton.setObjectName(u"importSelectedPushbutton")

        self.horizontalLayout.addWidget(self.importSelectedPushbutton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.selectOnlyNewPB = QPushButton(self.centralwidget)
        self.selectOnlyNewPB.setObjectName(u"selectOnlyNewPB")

        self.horizontalLayout.addWidget(self.selectOnlyNewPB)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.saveSelectionPushbutton = QPushButton(self.centralwidget)
        self.saveSelectionPushbutton.setObjectName(u"saveSelectionPushbutton")

        self.horizontalLayout.addWidget(self.saveSelectionPushbutton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        importSelectMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(importSelectMainWindow)

        QMetaObject.connectSlotsByName(importSelectMainWindow)
    # setupUi

    def retranslateUi(self, importSelectMainWindow):
        importSelectMainWindow.setWindowTitle(QCoreApplication.translate("importSelectMainWindow", u"Select import items", None))
        self.importInfoLabel.setText("")
        ___qtablewidgetitem = self.importTable_keys.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("importSelectMainWindow", u"keys", None));
        ___qtablewidgetitem1 = self.importTable_loops.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("importSelectMainWindow", u"loops", None));
        self.importSelectedPushbutton.setText(QCoreApplication.translate("importSelectMainWindow", u"Import Selected", None))
        self.selectOnlyNewPB.setText(QCoreApplication.translate("importSelectMainWindow", u"Select Only New Data", None))
        self.saveSelectionPushbutton.setText(QCoreApplication.translate("importSelectMainWindow", u"Save current Selection", None))
    # retranslateUi

