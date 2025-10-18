# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from qtpy.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MultitableWindow(object):
    def setupUi(self, MultitableWindow):
        if not MultitableWindow.objectName():
            MultitableWindow.setObjectName(u"MultitableWindow")
        MultitableWindow.resize(809, 588)
        self.Mainwidget = QWidget(MultitableWindow)
        self.Mainwidget.setObjectName(u"Mainwidget")
        self.gridLayout = QGridLayout(self.Mainwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cif_files_button = QPushButton(self.Mainwidget)
        self.cif_files_button.setObjectName(u"cif_files_button")

        self.gridLayout.addWidget(self.cif_files_button, 0, 0, 1, 1)

        self.report_button = QPushButton(self.Mainwidget)
        self.report_button.setObjectName(u"report_button")

        self.gridLayout.addWidget(self.report_button, 0, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.removeButton = QPushButton(self.Mainwidget)
        self.removeButton.setObjectName(u"removeButton")

        self.gridLayout.addWidget(self.removeButton, 0, 4, 1, 1)

        self.splitter_2 = QSplitter(self.Mainwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Vertical)
        self.groupBox = QGroupBox(self.splitter_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.CifFileListListWidget = QListWidget(self.groupBox)
        self.CifFileListListWidget.setObjectName(u"CifFileListListWidget")
        self.CifFileListListWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.CifFileListListWidget.setDefaultDropAction(Qt.CopyAction)
        self.CifFileListListWidget.setAlternatingRowColors(True)

        self.verticalLayout.addWidget(self.CifFileListListWidget)

        self.splitter_2.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.OutputTextEdit = QTextEdit(self.groupBox_2)
        self.OutputTextEdit.setObjectName(u"OutputTextEdit")
        sizePolicy.setHeightForWidth(self.OutputTextEdit.sizePolicy().hasHeightForWidth())
        self.OutputTextEdit.setSizePolicy(sizePolicy)
        self.OutputTextEdit.setMinimumSize(QSize(0, 0))
        self.OutputTextEdit.setReadOnly(True)
        self.OutputTextEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.OutputTextEdit)

        self.splitter_2.addWidget(self.groupBox_2)

        self.gridLayout.addWidget(self.splitter_2, 1, 0, 2, 5)

        MultitableWindow.setCentralWidget(self.Mainwidget)

        self.retranslateUi(MultitableWindow)
    # setupUi

    def retranslateUi(self, MultitableWindow):
        MultitableWindow.setWindowTitle(QCoreApplication.translate("MultitableWindow", u"Mutitable", None))
        self.cif_files_button.setText(QCoreApplication.translate("MultitableWindow", u"Select CIF files", None))
        self.report_button.setText(QCoreApplication.translate("MultitableWindow", u"Generate Report", None))
#if QT_CONFIG(tooltip)
        self.removeButton.setToolTip(QCoreApplication.translate("MultitableWindow", u"<html><head/><body><p>Removes the currently selected file from the list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.removeButton.setText(QCoreApplication.translate("MultitableWindow", u"Remove Current File", None))
        self.groupBox.setTitle(QCoreApplication.translate("MultitableWindow", u"Files List", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MultitableWindow", u"Program Output", None))
    # retranslateUi

