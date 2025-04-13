# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_templates_ui.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from finalcif.gui.spell_check_edit import SpellTextEdit

class Ui_TextTemplatesWidget(object):
    def setupUi(self, TextTemplatesWidget):
        if not TextTemplatesWidget.objectName():
            TextTemplatesWidget.setObjectName(u"TextTemplatesWidget")
        TextTemplatesWidget.resize(883, 610)
        self.verticalLayout_3 = QVBoxLayout(TextTemplatesWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, -1, -1, 6)
        self.cifKeyLabel = QLabel(TextTemplatesWidget)
        self.cifKeyLabel.setObjectName(u"cifKeyLabel")

        self.horizontalLayout.addWidget(self.cifKeyLabel)

        self.cifKeyLineEdit = QLineEdit(TextTemplatesWidget)
        self.cifKeyLineEdit.setObjectName(u"cifKeyLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.cifKeyLineEdit.sizePolicy().hasHeightForWidth())
        self.cifKeyLineEdit.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        self.cifKeyLineEdit.setFont(font)
        self.cifKeyLineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.cifKeyLineEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.TemplatesListGroupBox = QGroupBox(TextTemplatesWidget)
        self.TemplatesListGroupBox.setObjectName(u"TemplatesListGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(50)
        sizePolicy1.setHeightForWidth(self.TemplatesListGroupBox.sizePolicy().hasHeightForWidth())
        self.TemplatesListGroupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.TemplatesListGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 6, -1, 6)
        self.templatesListWidget = QListWidget(self.TemplatesListGroupBox)
        self.templatesListWidget.setObjectName(u"templatesListWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(60)
        sizePolicy2.setHeightForWidth(self.templatesListWidget.sizePolicy().hasHeightForWidth())
        self.templatesListWidget.setSizePolicy(sizePolicy2)
        self.templatesListWidget.setFrameShape(QFrame.NoFrame)
        self.templatesListWidget.setFrameShadow(QFrame.Plain)
        self.templatesListWidget.setLineWidth(0)
        self.templatesListWidget.setAutoScroll(False)
        self.templatesListWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.templatesListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.templatesListWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.templatesListWidget.setResizeMode(QListView.Adjust)

        self.verticalLayout.addWidget(self.templatesListWidget)


        self.horizontalLayout_2.addWidget(self.TemplatesListGroupBox)

        self.combinedTestGroupBox = QGroupBox(TextTemplatesWidget)
        self.combinedTestGroupBox.setObjectName(u"combinedTestGroupBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(40)
        sizePolicy3.setHeightForWidth(self.combinedTestGroupBox.sizePolicy().hasHeightForWidth())
        self.combinedTestGroupBox.setSizePolicy(sizePolicy3)
        self.verticalLayout_4 = QVBoxLayout(self.combinedTestGroupBox)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(12, 6, 12, 6)
        self.plainTextEdit = SpellTextEdit(self.combinedTestGroupBox)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy4)
        self.plainTextEdit.setFrameShadow(QFrame.Plain)
        self.plainTextEdit.setLineWidth(0)
        self.plainTextEdit.setBackgroundVisible(False)

        self.verticalLayout_4.addWidget(self.plainTextEdit)


        self.horizontalLayout_2.addWidget(self.combinedTestGroupBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.applaTextHorizontalLayout = QHBoxLayout()
        self.applaTextHorizontalLayout.setObjectName(u"applaTextHorizontalLayout")
        self.applyTextPushButton = QPushButton(TextTemplatesWidget)
        self.applyTextPushButton.setObjectName(u"applyTextPushButton")

        self.applaTextHorizontalLayout.addWidget(self.applyTextPushButton)

        self.cancelTextPushButton = QPushButton(TextTemplatesWidget)
        self.cancelTextPushButton.setObjectName(u"cancelTextPushButton")

        self.applaTextHorizontalLayout.addWidget(self.cancelTextPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.applaTextHorizontalLayout.addItem(self.horizontalSpacer)

        self.savePushButton = QPushButton(TextTemplatesWidget)
        self.savePushButton.setObjectName(u"savePushButton")

        self.applaTextHorizontalLayout.addWidget(self.savePushButton)

        self.importPushButton = QPushButton(TextTemplatesWidget)
        self.importPushButton.setObjectName(u"importPushButton")

        self.applaTextHorizontalLayout.addWidget(self.importPushButton)

        self.exportTextPushButton = QPushButton(TextTemplatesWidget)
        self.exportTextPushButton.setObjectName(u"exportTextPushButton")

        self.applaTextHorizontalLayout.addWidget(self.exportTextPushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.applaTextHorizontalLayout.addItem(self.horizontalSpacer_2)

        self.deletePushButton = QPushButton(TextTemplatesWidget)
        self.deletePushButton.setObjectName(u"deletePushButton")

        self.applaTextHorizontalLayout.addWidget(self.deletePushButton)


        self.verticalLayout_3.addLayout(self.applaTextHorizontalLayout)


        self.retranslateUi(TextTemplatesWidget)

        QMetaObject.connectSlotsByName(TextTemplatesWidget)
    # setupUi

    def retranslateUi(self, TextTemplatesWidget):
        TextTemplatesWidget.setWindowTitle(QCoreApplication.translate("TextTemplatesWidget", u"TextTemplatesWidget", None))
        self.cifKeyLabel.setText(QCoreApplication.translate("TextTemplatesWidget", u"CIF key:", None))
        self.cifKeyLineEdit.setText("")
        self.TemplatesListGroupBox.setTitle(QCoreApplication.translate("TextTemplatesWidget", u"Select template(s)", None))
        self.combinedTestGroupBox.setTitle(QCoreApplication.translate("TextTemplatesWidget", u"Combined text", None))
        self.plainTextEdit.setPlaceholderText(QCoreApplication.translate("TextTemplatesWidget", u"The text of the selected templates is added here in the order of selection.", None))
        self.applyTextPushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Apply Text", None))
        self.cancelTextPushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Cancel", None))
        self.savePushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Save as Template", None))
        self.importPushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Import Template", None))
        self.exportTextPushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Export to CIF", None))
        self.deletePushButton.setText(QCoreApplication.translate("TextTemplatesWidget", u"Delete Template", None))
    # retranslateUi

