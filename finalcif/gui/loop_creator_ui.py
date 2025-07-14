# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loop_creator_ui.ui'
##
##
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_LoopCreator(object):
    def setupUi(self, LoopCreator):
        if not LoopCreator.objectName():
            LoopCreator.setObjectName(u"LoopCreator")
        LoopCreator.resize(800, 600)
        self.horizontalLayout_2 = QHBoxLayout(LoopCreator)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(LoopCreator)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(LoopCreator)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.searchLineEdit = QLineEdit(LoopCreator)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout.addWidget(self.searchLineEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.availableKeysListWidget = QListWidget(LoopCreator)
        self.availableKeysListWidget.setObjectName(u"availableKeysListWidget")

        self.verticalLayout_2.addWidget(self.availableKeysListWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.rightPushButton = QPushButton(LoopCreator)
        self.rightPushButton.setObjectName(u"rightPushButton")

        self.verticalLayout.addWidget(self.rightPushButton)

        self.leftPushButton = QPushButton(LoopCreator)
        self.leftPushButton.setObjectName(u"leftPushButton")

        self.verticalLayout.addWidget(self.leftPushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(LoopCreator)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(LoopCreator)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.newLoopKeysListWidget = QListWidget(LoopCreator)
        self.newLoopKeysListWidget.setObjectName(u"newLoopKeysListWidget")

        self.verticalLayout_3.addWidget(self.newLoopKeysListWidget)

        self.saveLoopPushButton = QPushButton(LoopCreator)
        self.saveLoopPushButton.setObjectName(u"saveLoopPushButton")

        self.verticalLayout_3.addWidget(self.saveLoopPushButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(LoopCreator)

        QMetaObject.connectSlotsByName(LoopCreator)
    # setupUi

    def retranslateUi(self, LoopCreator):
        LoopCreator.setWindowTitle(QCoreApplication.translate("LoopCreator", u"LoopCreator", None))
        self.label_2.setText(QCoreApplication.translate("LoopCreator", u"<html><head/><body><p><span style=\" font-size:18pt;\">Available CIF keywords</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("LoopCreator", u"Search a Key", None))
        self.rightPushButton.setText(QCoreApplication.translate("LoopCreator", u"-->", None))
        self.leftPushButton.setText(QCoreApplication.translate("LoopCreator", u"<--", None))
        self.label_3.setText(QCoreApplication.translate("LoopCreator", u"<html><head/><body><p><span style=\" font-size:18pt;\">New Loop Header</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("LoopCreator", u"Add CIF keys in order to create a new loop", None))
        self.saveLoopPushButton.setText(QCoreApplication.translate("LoopCreator", u"Save new Loop", None))
    # retranslateUi

