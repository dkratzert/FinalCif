# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_key_dialog_ui.ui'
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
from qtpy.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_AddKeyWindow(object):
    def setupUi(self, AddKeyWindow):
        if not AddKeyWindow.objectName():
            AddKeyWindow.setObjectName(u"AddKeyWindow")
        AddKeyWindow.resize(528, 445)
        self.centralwidget = QWidget(AddKeyWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchLabel = QLabel(self.centralwidget)
        self.searchLabel.setObjectName(u"searchLabel")

        self.horizontalLayout.addWidget(self.searchLabel)

        self.searchLineEdit = QLineEdit(self.centralwidget)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout.addWidget(self.searchLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.keysListWidget = QListWidget(self.centralwidget)
        self.keysListWidget.setObjectName(u"keysListWidget")
        self.keysListWidget.setProperty(u"showDropIndicator", False)
        self.keysListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.keysListWidget.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.verticalLayout.addWidget(self.keysListWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.addKeyPushButton = QPushButton(self.centralwidget)
        self.addKeyPushButton.setObjectName(u"addKeyPushButton")

        self.horizontalLayout_2.addWidget(self.addKeyPushButton)

        self.cancelPushButton = QPushButton(self.centralwidget)
        self.cancelPushButton.setObjectName(u"cancelPushButton")

        self.horizontalLayout_2.addWidget(self.cancelPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        AddKeyWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AddKeyWindow)

        QMetaObject.connectSlotsByName(AddKeyWindow)
    # setupUi

    def retranslateUi(self, AddKeyWindow):
        AddKeyWindow.setWindowTitle(QCoreApplication.translate("AddKeyWindow", u"Add CIF Keyword", None))
        self.searchLabel.setText(QCoreApplication.translate("AddKeyWindow", u"Search", None))
        self.addKeyPushButton.setText(QCoreApplication.translate("AddKeyWindow", u"Add Key(s)", None))
        self.cancelPushButton.setText(QCoreApplication.translate("AddKeyWindow", u"Close", None))
    # retranslateUi

