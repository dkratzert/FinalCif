# -*- coding: utf-8 -*-

# Python: from finalcif.ciforder.order import CifOrder

################################################################################
##
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QStackedWidget, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

from finalcif.ciforder.order import CifOrder
from finalcif.displaymol.molecule2D import MoleculeWidget
from finalcif.gui.block_combobox import ComboBoxWithContextMenu
from finalcif.gui.custom_classes import MyCifTable
from finalcif.gui.equipmenttable import MyEQTableWidget
from finalcif.gui.file_editor import QCodeEditor
from finalcif.gui.mainstackwidget import MyMainStackedWidget
from finalcif.gui.propertytable import MyPropTableWidget

class Ui_FinalCifWindow(object):
    def setupUi(self, FinalCifWindow):
        if not FinalCifWindow.objectName():
            FinalCifWindow.setObjectName(u"FinalCifWindow")
        FinalCifWindow.resize(1914, 860)
        self.Mainwidget = QWidget(FinalCifWindow)
        self.Mainwidget.setObjectName(u"Mainwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.Mainwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 0)
        self.splitter = QSplitter(self.Mainwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.LeftFrame = QFrame(self.splitter)
        self.LeftFrame.setObjectName(u"LeftFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LeftFrame.sizePolicy().hasHeightForWidth())
        self.LeftFrame.setSizePolicy(sizePolicy)
        self.LeftFrame.setFrameShape(QFrame.NoFrame)
        self.LeftFrame.setFrameShadow(QFrame.Plain)
        self.LeftFrame.setLineWidth(0)
        self.verticalLayout_5 = QVBoxLayout(self.LeftFrame)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 0, 3, 0)
        self.SelectCifFileGroupBox = QGroupBox(self.LeftFrame)
        self.SelectCifFileGroupBox.setObjectName(u"SelectCifFileGroupBox")
        self.SelectCifFileGroupBox.setFlat(False)
        self.verticalLayout_29 = QVBoxLayout(self.SelectCifFileGroupBox)
        self.verticalLayout_29.setSpacing(6)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(3, 3, 3, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(3, 0, 0, -1)
        self.SelectCif_LineEdit = QLineEdit(self.SelectCifFileGroupBox)
        self.SelectCif_LineEdit.setObjectName(u"SelectCif_LineEdit")

        self.horizontalLayout_12.addWidget(self.SelectCif_LineEdit)

        self.SelectCif_PushButton = QPushButton(self.SelectCifFileGroupBox)
        self.SelectCif_PushButton.setObjectName(u"SelectCif_PushButton")

        self.horizontalLayout_12.addWidget(self.SelectCif_PushButton)


        self.verticalLayout_29.addLayout(self.horizontalLayout_12)

        self.RecentComboBox = QComboBox(self.SelectCifFileGroupBox)
        self.RecentComboBox.addItem("")
        self.RecentComboBox.setObjectName(u"RecentComboBox")
        self.RecentComboBox.setMaxVisibleItems(15)

        self.verticalLayout_29.addWidget(self.RecentComboBox)


        self.verticalLayout_5.addWidget(self.SelectCifFileGroupBox)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(3, -1, 3, -1)
        self.searchMainTableLabel = QLabel(self.LeftFrame)
        self.searchMainTableLabel.setObjectName(u"searchMainTableLabel")

        self.horizontalLayout_8.addWidget(self.searchMainTableLabel)

        self.searchMainTableLineEdit = QLineEdit(self.LeftFrame)
        self.searchMainTableLineEdit.setObjectName(u"searchMainTableLineEdit")

        self.horizontalLayout_8.addWidget(self.searchMainTableLineEdit)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.TemplatesStackedWidget = QStackedWidget(self.LeftFrame)
        self.TemplatesStackedWidget.setObjectName(u"TemplatesStackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TemplatesStackedWidget.sizePolicy().hasHeightForWidth())
        self.TemplatesStackedWidget.setSizePolicy(sizePolicy1)
        self.TemplatesStackedWidget.setLineWidth(1)
        self.page_equipment = QWidget()
        self.page_equipment.setObjectName(u"page_equipment")
        self.verticalLayout_16 = QVBoxLayout(self.page_equipment)
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.EquipmentGroupBox = QGroupBox(self.page_equipment)
        self.EquipmentGroupBox.setObjectName(u"EquipmentGroupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(36)
        sizePolicy2.setHeightForWidth(self.EquipmentGroupBox.sizePolicy().hasHeightForWidth())
        self.EquipmentGroupBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.EquipmentGroupBox)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(6, 4, 6, 4)
        self.EquipmentTemplatesStackedWidget = QStackedWidget(self.EquipmentGroupBox)
        self.EquipmentTemplatesStackedWidget.setObjectName(u"EquipmentTemplatesStackedWidget")
        sizePolicy1.setHeightForWidth(self.EquipmentTemplatesStackedWidget.sizePolicy().hasHeightForWidth())
        self.EquipmentTemplatesStackedWidget.setSizePolicy(sizePolicy1)
        self.EquipmentSelectPage = QWidget()
        self.EquipmentSelectPage.setObjectName(u"EquipmentSelectPage")
        self.verticalLayout_19 = QVBoxLayout(self.EquipmentSelectPage)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 3, 0, 3)
        self.EquipmentTemplatesListWidget = QListWidget(self.EquipmentSelectPage)
        self.EquipmentTemplatesListWidget.setObjectName(u"EquipmentTemplatesListWidget")
        self.EquipmentTemplatesListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.EquipmentTemplatesListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.EquipmentTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_19.addWidget(self.EquipmentTemplatesListWidget)

        self.horizontalLayout_Buttons = QHBoxLayout()
        self.horizontalLayout_Buttons.setSpacing(6)
        self.horizontalLayout_Buttons.setObjectName(u"horizontalLayout_Buttons")
        self.NewEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.NewEquipmentTemplateButton.setObjectName(u"NewEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.NewEquipmentTemplateButton)

        self.EditEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.EditEquipmentTemplateButton.setObjectName(u"EditEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.EditEquipmentTemplateButton)

        self.ImportEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.ImportEquipmentTemplateButton.setObjectName(u"ImportEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.ImportEquipmentTemplateButton)


        self.verticalLayout_19.addLayout(self.horizontalLayout_Buttons)

        self.EquipmentTemplatesStackedWidget.addWidget(self.EquipmentSelectPage)
        self.EquipmentEditPage = QWidget()
        self.EquipmentEditPage.setObjectName(u"EquipmentEditPage")
        self.verticalLayout_21 = QVBoxLayout(self.EquipmentEditPage)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 3, 0, 3)
        self.EquipmentEditTableWidget = MyEQTableWidget(self.EquipmentEditPage)
        if (self.EquipmentEditTableWidget.columnCount() < 2):
            self.EquipmentEditTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.EquipmentEditTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.EquipmentEditTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.EquipmentEditTableWidget.rowCount() < 1):
            self.EquipmentEditTableWidget.setRowCount(1)
        self.EquipmentEditTableWidget.setObjectName(u"EquipmentEditTableWidget")
        self.EquipmentEditTableWidget.setAutoScroll(False)
        self.EquipmentEditTableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.EquipmentEditTableWidget.setAlternatingRowColors(False)
        self.EquipmentEditTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.EquipmentEditTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.EquipmentEditTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.EquipmentEditTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.EquipmentEditTableWidget.setSortingEnabled(True)
        self.EquipmentEditTableWidget.setRowCount(1)
        self.EquipmentEditTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.EquipmentEditTableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.EquipmentEditTableWidget.horizontalHeader().setDefaultSectionSize(210)
        self.EquipmentEditTableWidget.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.EquipmentEditTableWidget.horizontalHeader().setStretchLastSection(True)
        self.EquipmentEditTableWidget.verticalHeader().setVisible(False)
        self.EquipmentEditTableWidget.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_21.addWidget(self.EquipmentEditTableWidget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.DeleteEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.DeleteEquipmentButton.setObjectName(u"DeleteEquipmentButton")

        self.horizontalLayout_5.addWidget(self.DeleteEquipmentButton)

        self.SaveEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.SaveEquipmentButton.setObjectName(u"SaveEquipmentButton")

        self.horizontalLayout_5.addWidget(self.SaveEquipmentButton)

        self.CancelEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.CancelEquipmentButton.setObjectName(u"CancelEquipmentButton")

        self.horizontalLayout_5.addWidget(self.CancelEquipmentButton)

        self.ExportEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.ExportEquipmentButton.setObjectName(u"ExportEquipmentButton")

        self.horizontalLayout_5.addWidget(self.ExportEquipmentButton)


        self.verticalLayout_21.addLayout(self.horizontalLayout_5)

        self.EquipmentTemplatesStackedWidget.addWidget(self.EquipmentEditPage)

        self.verticalLayout_7.addWidget(self.EquipmentTemplatesStackedWidget)


        self.verticalLayout_16.addWidget(self.EquipmentGroupBox)

        self.line = QFrame(self.page_equipment)
        self.line.setObjectName(u"line")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy3)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_16.addWidget(self.line)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(6, 6, -1, 6)
        self.ImportCifPushButton = QPushButton(self.page_equipment)
        self.ImportCifPushButton.setObjectName(u"ImportCifPushButton")

        self.horizontalLayout_13.addWidget(self.ImportCifPushButton)


        self.verticalLayout_16.addLayout(self.horizontalLayout_13)

        self.line_5 = QFrame(self.page_equipment)
        self.line_5.setObjectName(u"line_5")
        sizePolicy3.setHeightForWidth(self.line_5.sizePolicy().hasHeightForWidth())
        self.line_5.setSizePolicy(sizePolicy3)
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_16.addWidget(self.line_5)

        self.groupBox_5 = QGroupBox(self.page_equipment)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(50)
        sizePolicy4.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy4)
        self.verticalLayout_35 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(6, 9, 6, 9)
        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(-1, -1, -1, 12)
        self.ADPTableCheckBox = QCheckBox(self.groupBox_5)
        self.ADPTableCheckBox.setObjectName(u"ADPTableCheckBox")
        self.ADPTableCheckBox.setChecked(True)

        self.gridLayout_26.addWidget(self.ADPTableCheckBox, 0, 1, 1, 1)

        self.ReportTextCheckBox = QCheckBox(self.groupBox_5)
        self.ReportTextCheckBox.setObjectName(u"ReportTextCheckBox")

        self.gridLayout_26.addWidget(self.ReportTextCheckBox, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, -1)
        self.PictureWidthLabel = QLabel(self.groupBox_5)
        self.PictureWidthLabel.setObjectName(u"PictureWidthLabel")

        self.horizontalLayout_6.addWidget(self.PictureWidthLabel)

        self.PictureWidthDoubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.PictureWidthDoubleSpinBox.setObjectName(u"PictureWidthDoubleSpinBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.PictureWidthDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.PictureWidthDoubleSpinBox.setSizePolicy(sizePolicy5)
        self.PictureWidthDoubleSpinBox.setMinimumSize(QSize(80, 0))
        self.PictureWidthDoubleSpinBox.setValue(7.000000000000000)

        self.horizontalLayout_6.addWidget(self.PictureWidthDoubleSpinBox)

        self.horizontalSpacer_20 = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_20)


        self.gridLayout_26.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.HAtomsCheckBox = QCheckBox(self.groupBox_5)
        self.HAtomsCheckBox.setObjectName(u"HAtomsCheckBox")

        self.gridLayout_26.addWidget(self.HAtomsCheckBox, 1, 0, 1, 2)

        self.UsePicometersCheckBox = QCheckBox(self.groupBox_5)
        self.UsePicometersCheckBox.setObjectName(u"UsePicometersCheckBox")

        self.gridLayout_26.addWidget(self.UsePicometersCheckBox, 2, 1, 1, 1)


        self.verticalLayout_35.addLayout(self.gridLayout_26)

        self.groupBox_6 = QGroupBox(self.groupBox_5)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy1.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 3, 6, 6)
        self.docxTemplatesListWidget = QListWidget(self.groupBox_6)
        font = QFont()
        font.setItalic(True)
        __qlistwidgetitem = QListWidgetItem(self.docxTemplatesListWidget)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        __qlistwidgetitem.setFont(font);
        self.docxTemplatesListWidget.setObjectName(u"docxTemplatesListWidget")
        self.docxTemplatesListWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.docxTemplatesListWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.docxTemplatesListWidget.setSelectionRectVisible(False)

        self.verticalLayout_2.addWidget(self.docxTemplatesListWidget)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, 0, -1)
        self.AddNewTemplPushButton = QPushButton(self.groupBox_6)
        self.AddNewTemplPushButton.setObjectName(u"AddNewTemplPushButton")

        self.horizontalLayout_14.addWidget(self.AddNewTemplPushButton)

        self.RemoveTemplPushButton = QPushButton(self.groupBox_6)
        self.RemoveTemplPushButton.setObjectName(u"RemoveTemplPushButton")

        self.horizontalLayout_14.addWidget(self.RemoveTemplPushButton)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_13)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout_2.addWidget(self.label)


        self.verticalLayout_35.addWidget(self.groupBox_6)


        self.verticalLayout_16.addWidget(self.groupBox_5)

        self.TemplatesStackedWidget.addWidget(self.page_equipment)
        self.page_loops = QWidget()
        self.page_loops.setObjectName(u"page_loops")
        self.verticalLayout_18 = QVBoxLayout(self.page_loops)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.LoopsGroupBox = QGroupBox(self.page_loops)
        self.LoopsGroupBox.setObjectName(u"LoopsGroupBox")
        self.LoopsGroupBox.setFlat(True)
        self.verticalLayout_17 = QVBoxLayout(self.LoopsGroupBox)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(6, 6, 6, 6)
        self.LoopTemplatesListWidget = QListWidget(self.LoopsGroupBox)
        self.LoopTemplatesListWidget.setObjectName(u"LoopTemplatesListWidget")
        self.LoopTemplatesListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.LoopTemplatesListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.LoopTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_17.addWidget(self.LoopTemplatesListWidget)

        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(-1, 6, -1, 6)
        self.ExportAuthorPushButton = QPushButton(self.LoopsGroupBox)
        self.ExportAuthorPushButton.setObjectName(u"ExportAuthorPushButton")

        self.gridLayout_24.addWidget(self.ExportAuthorPushButton, 0, 1, 1, 1)

        self.ImportAuthorPushButton = QPushButton(self.LoopsGroupBox)
        self.ImportAuthorPushButton.setObjectName(u"ImportAuthorPushButton")

        self.gridLayout_24.addWidget(self.ImportAuthorPushButton, 0, 2, 1, 1)

        self.DeleteLoopAuthorTemplateButton = QPushButton(self.LoopsGroupBox)
        self.DeleteLoopAuthorTemplateButton.setObjectName(u"DeleteLoopAuthorTemplateButton")

        self.gridLayout_24.addWidget(self.DeleteLoopAuthorTemplateButton, 0, 3, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_24)

        self.line_2 = QFrame(self.LoopsGroupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_17.addWidget(self.line_2)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_9)


        self.verticalLayout_18.addWidget(self.LoopsGroupBox)

        self.TemplatesStackedWidget.addWidget(self.page_loops)

        self.verticalLayout_5.addWidget(self.TemplatesStackedWidget)

        self.splitter.addWidget(self.LeftFrame)
        self.CifDataItemsFrame = QFrame(self.splitter)
        self.CifDataItemsFrame.setObjectName(u"CifDataItemsFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(80)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.CifDataItemsFrame.sizePolicy().hasHeightForWidth())
        self.CifDataItemsFrame.setSizePolicy(sizePolicy6)
        self.gridLayout_6 = QGridLayout(self.CifDataItemsFrame)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(3, 9, 6, 0)
        self.spacegroupLabel = QLabel(self.CifDataItemsFrame)
        self.spacegroupLabel.setObjectName(u"spacegroupLabel")

        self.gridLayout_6.addWidget(self.spacegroupLabel, 0, 4, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_10, 0, 9, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_12, 0, 6, 1, 1)

        self.datanameComboBox = ComboBoxWithContextMenu(self.CifDataItemsFrame)
        self.datanameComboBox.setObjectName(u"datanameComboBox")
        self.datanameComboBox.setEditable(True)
        self.datanameComboBox.setMaxVisibleItems(20)
        self.datanameComboBox.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.datanameComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.datanameComboBox.setMinimumContentsLength(20)
        self.datanameComboBox.setFrame(True)

        self.gridLayout_6.addWidget(self.datanameComboBox, 0, 1, 1, 1)

        self.appendCifPushButton = QPushButton(self.CifDataItemsFrame)
        self.appendCifPushButton.setObjectName(u"appendCifPushButton")

        self.gridLayout_6.addWidget(self.appendCifPushButton, 0, 2, 1, 1)

        self.CCDCNumLabel = QLabel(self.CifDataItemsFrame)
        self.CCDCNumLabel.setObjectName(u"CCDCNumLabel")

        self.gridLayout_6.addWidget(self.CCDCNumLabel, 0, 7, 1, 1)

        self.CCDCNumLineEdit = QTextEdit(self.CifDataItemsFrame)
        self.CCDCNumLineEdit.setObjectName(u"CCDCNumLineEdit")
        self.CCDCNumLineEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.CCDCNumLineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CCDCNumLineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CCDCNumLineEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.CCDCNumLineEdit.setTabChangesFocus(True)
        self.CCDCNumLineEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.CCDCNumLineEdit.setReadOnly(False)
        self.CCDCNumLineEdit.setAcceptRichText(False)

        self.gridLayout_6.addWidget(self.CCDCNumLineEdit, 0, 8, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_11, 0, 3, 1, 1)

        self.HelpPushButton = QPushButton(self.CifDataItemsFrame)
        self.HelpPushButton.setObjectName(u"HelpPushButton")

        self.gridLayout_6.addWidget(self.HelpPushButton, 0, 12, 1, 1)

        self.SumFormMainLineEdit = QTextEdit(self.CifDataItemsFrame)
        self.SumFormMainLineEdit.setObjectName(u"SumFormMainLineEdit")
        self.SumFormMainLineEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.SumFormMainLineEdit.setInputMethodHints(Qt.ImhNone)
        self.SumFormMainLineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SumFormMainLineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SumFormMainLineEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.SumFormMainLineEdit.setTabChangesFocus(True)
        self.SumFormMainLineEdit.setUndoRedoEnabled(False)
        self.SumFormMainLineEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.SumFormMainLineEdit.setReadOnly(True)

        self.gridLayout_6.addWidget(self.SumFormMainLineEdit, 0, 11, 1, 1)

        self.datanameLabel = QLabel(self.CifDataItemsFrame)
        self.datanameLabel.setObjectName(u"datanameLabel")

        self.gridLayout_6.addWidget(self.datanameLabel, 0, 0, 1, 1)

        self.SumFormMainLabel = QLabel(self.CifDataItemsFrame)
        self.SumFormMainLabel.setObjectName(u"SumFormMainLabel")

        self.gridLayout_6.addWidget(self.SumFormMainLabel, 0, 10, 1, 1)

        self.Spacegroup_top_LineEdit = QTextEdit(self.CifDataItemsFrame)
        self.Spacegroup_top_LineEdit.setObjectName(u"Spacegroup_top_LineEdit")
        self.Spacegroup_top_LineEdit.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.Spacegroup_top_LineEdit.setInputMethodHints(Qt.ImhNone)
        self.Spacegroup_top_LineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Spacegroup_top_LineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Spacegroup_top_LineEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.Spacegroup_top_LineEdit.setTabChangesFocus(True)
        self.Spacegroup_top_LineEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.Spacegroup_top_LineEdit.setReadOnly(True)
        self.Spacegroup_top_LineEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_6.addWidget(self.Spacegroup_top_LineEdit, 0, 5, 1, 1)

        self.MainStackedWidget = MyMainStackedWidget(self.CifDataItemsFrame)
        self.MainStackedWidget.setObjectName(u"MainStackedWidget")
        self.page_MainTable = QWidget()
        self.page_MainTable.setObjectName(u"page_MainTable")
        self.verticalLayout = QVBoxLayout(self.page_MainTable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 6, 0, 0)
        self.cif_main_table = MyCifTable(self.page_MainTable)
        if (self.cif_main_table.columnCount() < 3):
            self.cif_main_table.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.cif_main_table.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.cif_main_table.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.cif_main_table.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.cif_main_table.setObjectName(u"cif_main_table")
        self.cif_main_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.cif_main_table.setAutoScroll(False)
        self.cif_main_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.cif_main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cif_main_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.cif_main_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.cif_main_table.setShowGrid(True)
        self.cif_main_table.setGridStyle(Qt.SolidLine)
        self.cif_main_table.setSortingEnabled(False)
        self.cif_main_table.setWordWrap(True)
        self.cif_main_table.setCornerButtonEnabled(False)
        self.cif_main_table.setColumnCount(3)
        self.cif_main_table.horizontalHeader().setMinimumSectionSize(80)
        self.cif_main_table.horizontalHeader().setDefaultSectionSize(152)
        self.cif_main_table.horizontalHeader().setHighlightSections(False)
        self.cif_main_table.verticalHeader().setMinimumSectionSize(20)
        self.cif_main_table.verticalHeader().setDefaultSectionSize(25)
        self.cif_main_table.verticalHeader().setHighlightSections(True)

        self.verticalLayout.addWidget(self.cif_main_table)

        self.ButtonsHorizontalLayout = QHBoxLayout()
        self.ButtonsHorizontalLayout.setSpacing(6)
        self.ButtonsHorizontalLayout.setObjectName(u"ButtonsHorizontalLayout")
        self.groupBox = QGroupBox(self.page_MainTable)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(9)
        self.gridLayout_7.setVerticalSpacing(6)
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.SaveCifButton = QPushButton(self.groupBox)
        self.SaveCifButton.setObjectName(u"SaveCifButton")

        self.gridLayout_7.addWidget(self.SaveCifButton, 0, 0, 1, 1)

        self.ExploreDirButton = QPushButton(self.groupBox)
        self.ExploreDirButton.setObjectName(u"ExploreDirButton")

        self.gridLayout_7.addWidget(self.ExploreDirButton, 1, 0, 1, 1)

        self.DetailsPushButton = QPushButton(self.groupBox)
        self.DetailsPushButton.setObjectName(u"DetailsPushButton")

        self.gridLayout_7.addWidget(self.DetailsPushButton, 0, 1, 1, 1)

        self.AuthorEditPushButton = QPushButton(self.groupBox)
        self.AuthorEditPushButton.setObjectName(u"AuthorEditPushButton")

        self.gridLayout_7.addWidget(self.AuthorEditPushButton, 1, 1, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox)

        self.groupBox_checkcif = QGroupBox(self.page_MainTable)
        self.groupBox_checkcif.setObjectName(u"groupBox_checkcif")
        self.gridLayout_15 = QGridLayout(self.groupBox_checkcif)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(9)
        self.gridLayout_15.setVerticalSpacing(6)
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.LoopsPushButton = QPushButton(self.groupBox_checkcif)
        self.LoopsPushButton.setObjectName(u"LoopsPushButton")

        self.gridLayout_15.addWidget(self.LoopsPushButton, 1, 0, 1, 1)

        self.ReportPicPushButton = QPushButton(self.groupBox_checkcif)
        self.ReportPicPushButton.setObjectName(u"ReportPicPushButton")

        self.gridLayout_15.addWidget(self.ReportPicPushButton, 0, 1, 1, 1)

        self.SaveFullReportButton = QPushButton(self.groupBox_checkcif)
        self.SaveFullReportButton.setObjectName(u"SaveFullReportButton")

        self.gridLayout_15.addWidget(self.SaveFullReportButton, 1, 1, 1, 1)

        self.CheckcifStartButton = QPushButton(self.groupBox_checkcif)
        self.CheckcifStartButton.setObjectName(u"CheckcifStartButton")

        self.gridLayout_15.addWidget(self.CheckcifStartButton, 0, 0, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox_checkcif)

        self.groupBox_tables = QGroupBox(self.page_MainTable)
        self.groupBox_tables.setObjectName(u"groupBox_tables")
        self.gridLayout = QGridLayout(self.groupBox_tables)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.CODpushButton = QPushButton(self.groupBox_tables)
        self.CODpushButton.setObjectName(u"CODpushButton")

        self.gridLayout.addWidget(self.CODpushButton, 0, 0, 1, 1)

        self.ShredCifButton = QPushButton(self.groupBox_tables)
        self.ShredCifButton.setObjectName(u"ShredCifButton")

        self.gridLayout.addWidget(self.ShredCifButton, 0, 1, 1, 1)

        self.CCDCpushButton = QPushButton(self.groupBox_tables)
        self.CCDCpushButton.setObjectName(u"CCDCpushButton")

        self.gridLayout.addWidget(self.CCDCpushButton, 1, 0, 1, 1)

        self.OptionsPushButton = QPushButton(self.groupBox_tables)
        self.OptionsPushButton.setObjectName(u"OptionsPushButton")

        self.gridLayout.addWidget(self.OptionsPushButton, 1, 1, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox_tables)


        self.verticalLayout.addLayout(self.ButtonsHorizontalLayout)

        self.MainStackedWidget.addWidget(self.page_MainTable)
        self.page_FinalCif = QWidget()
        self.page_FinalCif.setObjectName(u"page_FinalCif")
        self.verticalLayout_3 = QVBoxLayout(self.page_FinalCif)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.FinalCifFilePlainTextEdit = QCodeEditor(self.page_FinalCif)
        self.FinalCifFilePlainTextEdit.setObjectName(u"FinalCifFilePlainTextEdit")
        self.FinalCifFilePlainTextEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.FinalCifFilePlainTextEdit)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.BackPushButton = QPushButton(self.page_FinalCif)
        self.BackPushButton.setObjectName(u"BackPushButton")
        self.BackPushButton.setMinimumSize(QSize(120, 0))

        self.gridLayout_10.addWidget(self.BackPushButton, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_10)

        self.MainStackedWidget.addWidget(self.page_FinalCif)
        self.page_molinfo = QWidget()
        self.page_molinfo.setObjectName(u"page_molinfo")
        self.gridLayout_3 = QGridLayout(self.page_molinfo)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.molGroupBox = QGroupBox(self.page_molinfo)
        self.molGroupBox.setObjectName(u"molGroupBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(55)
        sizePolicy7.setVerticalStretch(80)
        sizePolicy7.setHeightForWidth(self.molGroupBox.sizePolicy().hasHeightForWidth())
        self.molGroupBox.setSizePolicy(sizePolicy7)
        self.verticalLayout_8 = QVBoxLayout(self.molGroupBox)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(6, 3, 6, 8)
        self.render_widget = MoleculeWidget(self.molGroupBox)
        self.render_widget.setObjectName(u"render_widget")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.render_widget.sizePolicy().hasHeightForWidth())
        self.render_widget.setSizePolicy(sizePolicy8)

        self.verticalLayout_8.addWidget(self.render_widget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.growCheckBox = QCheckBox(self.molGroupBox)
        self.growCheckBox.setObjectName(u"growCheckBox")
        self.growCheckBox.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_7.addWidget(self.growCheckBox)

        self.labelsCheckBox = QCheckBox(self.molGroupBox)
        self.labelsCheckBox.setObjectName(u"labelsCheckBox")
        self.labelsCheckBox.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_7.addWidget(self.labelsCheckBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.drawImagePushButton = QPushButton(self.molGroupBox)
        self.drawImagePushButton.setObjectName(u"drawImagePushButton")

        self.horizontalLayout_7.addWidget(self.drawImagePushButton)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_23)


        self.verticalLayout_8.addLayout(self.horizontalLayout_7)


        self.gridLayout_3.addWidget(self.molGroupBox, 0, 0, 1, 1)

        self.groupBox_9 = QGroupBox(self.page_molinfo)
        self.groupBox_9.setObjectName(u"groupBox_9")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(45)
        sizePolicy9.setVerticalStretch(80)
        sizePolicy9.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy9)
        self.verticalLayout_41 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.shelx_TextEdit = QPlainTextEdit(self.groupBox_9)
        self.shelx_TextEdit.setObjectName(u"shelx_TextEdit")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(90)
        sizePolicy10.setHeightForWidth(self.shelx_TextEdit.sizePolicy().hasHeightForWidth())
        self.shelx_TextEdit.setSizePolicy(sizePolicy10)
        font1 = QFont()
        font1.setFamilies([u"Courier New"])
        font1.setPointSize(11)
        self.shelx_TextEdit.setFont(font1)
        self.shelx_TextEdit.setFrameShape(QFrame.NoFrame)
        self.shelx_TextEdit.setFrameShadow(QFrame.Plain)
        self.shelx_TextEdit.setUndoRedoEnabled(False)
        self.shelx_TextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.shelx_TextEdit.setReadOnly(True)

        self.verticalLayout_41.addWidget(self.shelx_TextEdit)

        self.shelx_warn_TextEdit = QPlainTextEdit(self.groupBox_9)
        self.shelx_warn_TextEdit.setObjectName(u"shelx_warn_TextEdit")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(10)
        sizePolicy11.setHeightForWidth(self.shelx_warn_TextEdit.sizePolicy().hasHeightForWidth())
        self.shelx_warn_TextEdit.setSizePolicy(sizePolicy11)
        font2 = QFont()
        font2.setFamilies([u"Courier New"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.shelx_warn_TextEdit.setFont(font2)
        self.shelx_warn_TextEdit.setUndoRedoEnabled(False)
        self.shelx_warn_TextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.shelx_warn_TextEdit.setReadOnly(True)

        self.verticalLayout_41.addWidget(self.shelx_warn_TextEdit)


        self.gridLayout_3.addWidget(self.groupBox_9, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.page_molinfo)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(20)
        sizePolicy12.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy12)
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.zLabel = QLabel(self.groupBox_3)
        self.zLabel.setObjectName(u"zLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.zLabel)

        self.zLineEdit = QLineEdit(self.groupBox_3)
        self.zLineEdit.setObjectName(u"zLineEdit")
        self.zLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.zLineEdit)

        self.temperatureLabel = QLabel(self.groupBox_3)
        self.temperatureLabel.setObjectName(u"temperatureLabel")
        self.temperatureLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.temperatureLabel)

        self.temperatureLineEdit = QLineEdit(self.groupBox_3)
        self.temperatureLineEdit.setObjectName(u"temperatureLineEdit")
        self.temperatureLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.temperatureLineEdit)

        self.wR2Label = QLabel(self.groupBox_3)
        self.wR2Label.setObjectName(u"wR2Label")
        font3 = QFont()
        font3.setBold(False)
        font3.setItalic(False)
        self.wR2Label.setFont(font3)
        self.wR2Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.wR2Label)

        self.wR2LineEdit = QLineEdit(self.groupBox_3)
        self.wR2LineEdit.setObjectName(u"wR2LineEdit")
        self.wR2LineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.wR2LineEdit)

        self.r1Label = QLabel(self.groupBox_3)
        self.r1Label.setObjectName(u"r1Label")
        self.r1Label.setFont(font3)
        self.r1Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.r1Label)

        self.r1LineEdit = QLineEdit(self.groupBox_3)
        self.r1LineEdit.setObjectName(u"r1LineEdit")
        self.r1LineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.r1LineEdit)

        self.goofLabel = QLabel(self.groupBox_3)
        self.goofLabel.setObjectName(u"goofLabel")
        self.goofLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.goofLabel)

        self.goofLineEdit = QLineEdit(self.groupBox_3)
        self.goofLineEdit.setObjectName(u"goofLineEdit")
        self.goofLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.goofLineEdit)

        self.maxShiftLabel = QLabel(self.groupBox_3)
        self.maxShiftLabel.setObjectName(u"maxShiftLabel")
        self.maxShiftLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.maxShiftLabel)

        self.maxShiftLineEdit = QLineEdit(self.groupBox_3)
        self.maxShiftLineEdit.setObjectName(u"maxShiftLineEdit")
        self.maxShiftLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.maxShiftLineEdit)

        self.completeLabel = QLabel(self.groupBox_3)
        self.completeLabel.setObjectName(u"completeLabel")
        font4 = QFont()
        font4.setBold(False)
        self.completeLabel.setFont(font4)
        self.completeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.completeLabel)

        self.completeLineEdit = QLineEdit(self.groupBox_3)
        self.completeLineEdit.setObjectName(u"completeLineEdit")
        self.completeLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.completeLineEdit)


        self.gridLayout_4.addLayout(self.formLayout_3, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_24, 0, 7, 1, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.reflTotalLabel = QLabel(self.groupBox_3)
        self.reflTotalLabel.setObjectName(u"reflTotalLabel")
        self.reflTotalLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.reflTotalLabel)

        self.reflTotalLineEdit = QLineEdit(self.groupBox_3)
        self.reflTotalLineEdit.setObjectName(u"reflTotalLineEdit")
        self.reflTotalLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.reflTotalLineEdit)

        self.refl2sigmaLabel = QLabel(self.groupBox_3)
        self.refl2sigmaLabel.setObjectName(u"refl2sigmaLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.refl2sigmaLabel)

        self.refl2sigmaLineEdit = QLineEdit(self.groupBox_3)
        self.refl2sigmaLineEdit.setObjectName(u"refl2sigmaLineEdit")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.refl2sigmaLineEdit)

        self.uniqReflLabel = QLabel(self.groupBox_3)
        self.uniqReflLabel.setObjectName(u"uniqReflLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.uniqReflLabel)

        self.uniqReflLineEdit = QLineEdit(self.groupBox_3)
        self.uniqReflLineEdit.setObjectName(u"uniqReflLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.uniqReflLineEdit)

        self.numParametersLabel = QLabel(self.groupBox_3)
        self.numParametersLabel.setObjectName(u"numParametersLabel")
        self.numParametersLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.numParametersLabel)

        self.numParametersLineEdit = QLineEdit(self.groupBox_3)
        self.numParametersLineEdit.setObjectName(u"numParametersLineEdit")
        self.numParametersLineEdit.setMinimumSize(QSize(0, 0))
        self.numParametersLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.numParametersLineEdit)

        self.dataReflnsLabel = QLabel(self.groupBox_3)
        self.dataReflnsLabel.setObjectName(u"dataReflnsLabel")
        self.dataReflnsLabel.setFont(font4)
        self.dataReflnsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.dataReflnsLabel)

        self.dataReflnsLineEdit = QLineEdit(self.groupBox_3)
        self.dataReflnsLineEdit.setObjectName(u"dataReflnsLineEdit")
        self.dataReflnsLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.dataReflnsLineEdit)

        self.wavelengthLabel = QLabel(self.groupBox_3)
        self.wavelengthLabel.setObjectName(u"wavelengthLabel")
        self.wavelengthLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.wavelengthLabel)

        self.wavelengthLineEdit = QLineEdit(self.groupBox_3)
        self.wavelengthLineEdit.setObjectName(u"wavelengthLineEdit")
        self.wavelengthLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.wavelengthLineEdit)

        self.flackXLabel = QLabel(self.groupBox_3)
        self.flackXLabel.setObjectName(u"flackXLabel")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.flackXLabel)

        self.flackXLineEdit = QLineEdit(self.groupBox_3)
        self.flackXLineEdit.setObjectName(u"flackXLineEdit")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.flackXLineEdit)


        self.gridLayout_4.addLayout(self.formLayout_2, 0, 6, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy13)
        self.gridLayout_9 = QGridLayout(self.groupBox_4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.cellField = QLabel(self.groupBox_4)
        self.cellField.setObjectName(u"cellField")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.cellField.sizePolicy().hasHeightForWidth())
        self.cellField.setSizePolicy(sizePolicy14)
        self.cellField.setMinimumSize(QSize(0, 75))
        self.cellField.setBaseSize(QSize(0, 75))
        self.cellField.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.cellField.setAutoFillBackground(False)
        self.cellField.setStyleSheet(u"border-color: rgb(53, 53, 53);")
        self.cellField.setFrameShape(QFrame.NoFrame)
        self.cellField.setFrameShadow(QFrame.Plain)
        self.cellField.setTextFormat(Qt.RichText)
        self.cellField.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_9.addWidget(self.cellField, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 0, 5, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.peakLabel = QLabel(self.groupBox_3)
        self.peakLabel.setObjectName(u"peakLabel")
        self.peakLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.peakLabel)

        self.peakLineEdit = QLineEdit(self.groupBox_3)
        self.peakLineEdit.setObjectName(u"peakLineEdit")
        self.peakLineEdit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.peakLineEdit)

        self.rintLabel = QLabel(self.groupBox_3)
        self.rintLabel.setObjectName(u"rintLabel")
        self.rintLabel.setFont(font4)
        self.rintLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.rintLabel)

        self.rintLineEdit = QLineEdit(self.groupBox_3)
        self.rintLineEdit.setObjectName(u"rintLineEdit")
        self.rintLineEdit.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.rintLineEdit)

        self.rsigmaLabel = QLabel(self.groupBox_3)
        self.rsigmaLabel.setObjectName(u"rsigmaLabel")
        self.rsigmaLabel.setFont(font4)
        self.rsigmaLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.rsigmaLabel)

        self.rsigmaLineEdit = QLineEdit(self.groupBox_3)
        self.rsigmaLineEdit.setObjectName(u"rsigmaLineEdit")
        self.rsigmaLineEdit.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.rsigmaLineEdit)

        self.numRestraintsLabel = QLabel(self.groupBox_3)
        self.numRestraintsLabel.setObjectName(u"numRestraintsLabel")
        self.numRestraintsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.numRestraintsLabel)

        self.numRestraintsLineEdit = QLineEdit(self.groupBox_3)
        self.numRestraintsLineEdit.setObjectName(u"numRestraintsLineEdit")
        self.numRestraintsLineEdit.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.numRestraintsLineEdit)

        self.thetaMaxLabel = QLabel(self.groupBox_3)
        self.thetaMaxLabel.setObjectName(u"thetaMaxLabel")
        self.thetaMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.thetaMaxLabel)

        self.thetaMaxLineEdit = QLineEdit(self.groupBox_3)
        self.thetaMaxLineEdit.setObjectName(u"thetaMaxLineEdit")
        self.thetaMaxLineEdit.setReadOnly(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.thetaMaxLineEdit)

        self.thetaFullLabel = QLabel(self.groupBox_3)
        self.thetaFullLabel.setObjectName(u"thetaFullLabel")
        self.thetaFullLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.thetaFullLabel)

        self.thetaFullLineEdit = QLineEdit(self.groupBox_3)
        self.thetaFullLineEdit.setObjectName(u"thetaFullLineEdit")
        self.thetaFullLineEdit.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.thetaFullLineEdit)

        self.dLabel = QLabel(self.groupBox_3)
        self.dLabel.setObjectName(u"dLabel")
        self.dLabel.setFont(font4)
        self.dLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.dLabel)

        self.dLineEdit = QLineEdit(self.groupBox_3)
        self.dLineEdit.setObjectName(u"dLineEdit")
        self.dLineEdit.setReadOnly(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.dLineEdit)


        self.gridLayout_4.addLayout(self.formLayout, 0, 4, 1, 1)

        self.BackpushButtonDetails = QPushButton(self.groupBox_3)
        self.BackpushButtonDetails.setObjectName(u"BackpushButtonDetails")
        sizePolicy5.setHeightForWidth(self.BackpushButtonDetails.sizePolicy().hasHeightForWidth())
        self.BackpushButtonDetails.setSizePolicy(sizePolicy5)

        self.gridLayout_4.addWidget(self.BackpushButtonDetails, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_22, 0, 1, 1, 1)

        self.SourcesPushButton = QPushButton(self.groupBox_3)
        self.SourcesPushButton.setObjectName(u"SourcesPushButton")
        sizePolicy5.setHeightForWidth(self.SourcesPushButton.sizePolicy().hasHeightForWidth())
        self.SourcesPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_4.addWidget(self.SourcesPushButton, 2, 7, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_3, 1, 0, 1, 3)

        self.MainStackedWidget.addWidget(self.page_molinfo)
        self.page_Sources = QWidget()
        self.page_Sources.setObjectName(u"page_Sources")
        self.gridLayout_11 = QGridLayout(self.page_Sources)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.horizontalSpacer_9 = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_9, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.page_Sources)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.SourcesTableWidget = QTableWidget(self.groupBox_2)
        if (self.SourcesTableWidget.columnCount() < 3):
            self.SourcesTableWidget.setColumnCount(3)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.SourcesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.SourcesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.SourcesTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        self.SourcesTableWidget.setObjectName(u"SourcesTableWidget")
        self.SourcesTableWidget.setWordWrap(False)
        self.SourcesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.SourcesTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.SourcesTableWidget)


        self.gridLayout_11.addWidget(self.groupBox_2, 0, 1, 1, 3)

        self.BackSourcesPushButton = QPushButton(self.page_Sources)
        self.BackSourcesPushButton.setObjectName(u"BackSourcesPushButton")
        sizePolicy5.setHeightForWidth(self.BackSourcesPushButton.sizePolicy().hasHeightForWidth())
        self.BackSourcesPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_11.addWidget(self.BackSourcesPushButton, 1, 2, 1, 2)

        self.MainStackedWidget.addWidget(self.page_Sources)
        self.page_options = QWidget()
        self.page_options.setObjectName(u"page_options")
        self.gridLayout_12 = QGridLayout(self.page_options)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.BackFromOptionspPushButton = QPushButton(self.page_options)
        self.BackFromOptionspPushButton.setObjectName(u"BackFromOptionspPushButton")
        sizePolicy5.setHeightForWidth(self.BackFromOptionspPushButton.sizePolicy().hasHeightForWidth())
        self.BackFromOptionspPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_12.addWidget(self.BackFromOptionspPushButton, 7, 0, 1, 1)

        self.groupBox_COD = QGroupBox(self.page_options)
        self.groupBox_COD.setObjectName(u"groupBox_COD")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy15.setHorizontalStretch(50)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.groupBox_COD.sizePolicy().hasHeightForWidth())
        self.groupBox_COD.setSizePolicy(sizePolicy15)
        self.formLayout_6 = QFormLayout(self.groupBox_COD)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setContentsMargins(-1, 12, -1, -1)
        self.label_7 = QLabel(self.groupBox_COD)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_6.setWidget(0, QFormLayout.SpanningRole, self.label_7)

        self.CODURLTextedit = QLineEdit(self.groupBox_COD)
        self.CODURLTextedit.setObjectName(u"CODURLTextedit")
        sizePolicy3.setHeightForWidth(self.CODURLTextedit.sizePolicy().hasHeightForWidth())
        self.CODURLTextedit.setSizePolicy(sizePolicy3)
        self.CODURLTextedit.setMinimumSize(QSize(300, 0))

        self.formLayout_6.setWidget(1, QFormLayout.SpanningRole, self.CODURLTextedit)


        self.gridLayout_12.addWidget(self.groupBox_COD, 2, 2, 1, 1)

        self.groupBox_7 = QGroupBox(self.page_options)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.formLayout_4 = QFormLayout(self.groupBox_7)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_4.setWidget(0, QFormLayout.SpanningRole, self.label_4)

        self.CheckCIFServerURLTextedit = QLineEdit(self.groupBox_7)
        self.CheckCIFServerURLTextedit.setObjectName(u"CheckCIFServerURLTextedit")
        sizePolicy3.setHeightForWidth(self.CheckCIFServerURLTextedit.sizePolicy().hasHeightForWidth())
        self.CheckCIFServerURLTextedit.setSizePolicy(sizePolicy3)
        self.CheckCIFServerURLTextedit.setMinimumSize(QSize(300, 0))

        self.formLayout_4.setWidget(1, QFormLayout.SpanningRole, self.CheckCIFServerURLTextedit)


        self.gridLayout_12.addWidget(self.groupBox_7, 0, 2, 1, 1)

        self.groupBox_8 = QGroupBox(self.page_options)
        self.groupBox_8.setObjectName(u"groupBox_8")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy16.setHorizontalStretch(15)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy16)
        self.verticalLayout_34 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.ExportAllTemplatesPushButton = QPushButton(self.groupBox_8)
        self.ExportAllTemplatesPushButton.setObjectName(u"ExportAllTemplatesPushButton")

        self.verticalLayout_34.addWidget(self.ExportAllTemplatesPushButton, 0, Qt.AlignLeft)

        self.label_18 = QLabel(self.groupBox_8)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_34.addWidget(self.label_18)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_34.addItem(self.verticalSpacer)

        self.ImportAllTemplatesPushButton = QPushButton(self.groupBox_8)
        self.ImportAllTemplatesPushButton.setObjectName(u"ImportAllTemplatesPushButton")

        self.verticalLayout_34.addWidget(self.ImportAllTemplatesPushButton, 0, Qt.AlignLeft)

        self.label_17 = QLabel(self.groupBox_8)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_34.addWidget(self.label_17)


        self.gridLayout_12.addWidget(self.groupBox_8, 0, 1, 1, 1)

        self.groupBox_10 = QGroupBox(self.page_options)
        self.groupBox_10.setObjectName(u"groupBox_10")
        sizePolicy16.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy16)
        self.verticalLayout_37 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.trackChangesCifCheckBox = QCheckBox(self.groupBox_10)
        self.trackChangesCifCheckBox.setObjectName(u"trackChangesCifCheckBox")

        self.verticalLayout_37.addWidget(self.trackChangesCifCheckBox)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_37.addItem(self.verticalSpacer_14)


        self.gridLayout_12.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.cifOrderWidget = CifOrder(self.page_options)
        self.cifOrderWidget.setObjectName(u"cifOrderWidget")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy17.setHorizontalStretch(30)
        sizePolicy17.setVerticalStretch(2)
        sizePolicy17.setHeightForWidth(self.cifOrderWidget.sizePolicy().hasHeightForWidth())
        self.cifOrderWidget.setSizePolicy(sizePolicy17)

        self.gridLayout_12.addWidget(self.cifOrderWidget, 2, 0, 5, 2)

        self.PropertiesGroupBox = QGroupBox(self.page_options)
        self.PropertiesGroupBox.setObjectName(u"PropertiesGroupBox")
        sizePolicy18 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy18.setHorizontalStretch(50)
        sizePolicy18.setVerticalStretch(2)
        sizePolicy18.setHeightForWidth(self.PropertiesGroupBox.sizePolicy().hasHeightForWidth())
        self.PropertiesGroupBox.setSizePolicy(sizePolicy18)
        self.verticalLayout_6 = QVBoxLayout(self.PropertiesGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.PropertiesTemplatesStackedWidget = QStackedWidget(self.PropertiesGroupBox)
        self.PropertiesTemplatesStackedWidget.setObjectName(u"PropertiesTemplatesStackedWidget")
        self.PropertiesSelectPage = QWidget()
        self.PropertiesSelectPage.setObjectName(u"PropertiesSelectPage")
        self.verticalLayout_20 = QVBoxLayout(self.PropertiesSelectPage)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 3, 0, 3)
        self.PropertiesTemplatesListWidget = QListWidget(self.PropertiesSelectPage)
        self.PropertiesTemplatesListWidget.setObjectName(u"PropertiesTemplatesListWidget")
        self.PropertiesTemplatesListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.PropertiesTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_20.addWidget(self.PropertiesTemplatesListWidget)

        self.horizontalLayout_Buttons2 = QHBoxLayout()
        self.horizontalLayout_Buttons2.setObjectName(u"horizontalLayout_Buttons2")
        self.EditPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.EditPropertyTemplateButton.setObjectName(u"EditPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.EditPropertyTemplateButton)

        self.NewPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.NewPropertyTemplateButton.setObjectName(u"NewPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.NewPropertyTemplateButton)

        self.ImportPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.ImportPropertyTemplateButton.setObjectName(u"ImportPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.ImportPropertyTemplateButton)


        self.verticalLayout_20.addLayout(self.horizontalLayout_Buttons2)

        self.PropertiesTemplatesStackedWidget.addWidget(self.PropertiesSelectPage)
        self.PropertiesEditPage = QWidget()
        self.PropertiesEditPage.setObjectName(u"PropertiesEditPage")
        self.verticalLayout_22 = QVBoxLayout(self.PropertiesEditPage)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 3, 0, 3)
        self.KeywordVerticalLayout = QVBoxLayout()
        self.KeywordVerticalLayout.setObjectName(u"KeywordVerticalLayout")
        self.cifKeywordLB = QLabel(self.PropertiesEditPage)
        self.cifKeywordLB.setObjectName(u"cifKeywordLB")

        self.KeywordVerticalLayout.addWidget(self.cifKeywordLB)

        self.cifKeywordLineEdit = QLineEdit(self.PropertiesEditPage)
        self.cifKeywordLineEdit.setObjectName(u"cifKeywordLineEdit")

        self.KeywordVerticalLayout.addWidget(self.cifKeywordLineEdit)


        self.verticalLayout_22.addLayout(self.KeywordVerticalLayout)

        self.PropertiesEditTableWidget = MyPropTableWidget(self.PropertiesEditPage)
        if (self.PropertiesEditTableWidget.columnCount() < 1):
            self.PropertiesEditTableWidget.setColumnCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.PropertiesEditTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        if (self.PropertiesEditTableWidget.rowCount() < 1):
            self.PropertiesEditTableWidget.setRowCount(1)
        self.PropertiesEditTableWidget.setObjectName(u"PropertiesEditTableWidget")
        self.PropertiesEditTableWidget.setAutoScroll(False)
        self.PropertiesEditTableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.PropertiesEditTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.PropertiesEditTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.PropertiesEditTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.PropertiesEditTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.PropertiesEditTableWidget.setRowCount(1)
        self.PropertiesEditTableWidget.horizontalHeader().setVisible(False)
        self.PropertiesEditTableWidget.horizontalHeader().setMinimumSectionSize(90)
        self.PropertiesEditTableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.PropertiesEditTableWidget.horizontalHeader().setStretchLastSection(True)
        self.PropertiesEditTableWidget.verticalHeader().setVisible(False)
        self.PropertiesEditTableWidget.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_22.addWidget(self.PropertiesEditTableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.DeletePropertiesButton = QPushButton(self.PropertiesEditPage)
        self.DeletePropertiesButton.setObjectName(u"DeletePropertiesButton")
        sizePolicy19 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy19.setHorizontalStretch(1)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.DeletePropertiesButton.sizePolicy().hasHeightForWidth())
        self.DeletePropertiesButton.setSizePolicy(sizePolicy19)

        self.horizontalLayout.addWidget(self.DeletePropertiesButton)

        self.SavePropertiesButton = QPushButton(self.PropertiesEditPage)
        self.SavePropertiesButton.setObjectName(u"SavePropertiesButton")
        sizePolicy20 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy20.setHorizontalStretch(1)
        sizePolicy20.setVerticalStretch(0)
        sizePolicy20.setHeightForWidth(self.SavePropertiesButton.sizePolicy().hasHeightForWidth())
        self.SavePropertiesButton.setSizePolicy(sizePolicy20)

        self.horizontalLayout.addWidget(self.SavePropertiesButton)

        self.CancelPropertiesButton = QPushButton(self.PropertiesEditPage)
        self.CancelPropertiesButton.setObjectName(u"CancelPropertiesButton")
        sizePolicy19.setHeightForWidth(self.CancelPropertiesButton.sizePolicy().hasHeightForWidth())
        self.CancelPropertiesButton.setSizePolicy(sizePolicy19)

        self.horizontalLayout.addWidget(self.CancelPropertiesButton)

        self.ExportPropertyButton = QPushButton(self.PropertiesEditPage)
        self.ExportPropertyButton.setObjectName(u"ExportPropertyButton")

        self.horizontalLayout.addWidget(self.ExportPropertyButton)


        self.verticalLayout_22.addLayout(self.horizontalLayout)

        self.PropertiesTemplatesStackedWidget.addWidget(self.PropertiesEditPage)

        self.verticalLayout_6.addWidget(self.PropertiesTemplatesStackedWidget)


        self.gridLayout_12.addWidget(self.PropertiesGroupBox, 3, 2, 4, 1)

        self.MainStackedWidget.addWidget(self.page_options)
        self.page_Loops = QWidget()
        self.page_Loops.setObjectName(u"page_Loops")
        self.verticalLayout_9 = QVBoxLayout(self.page_Loops)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, 12, -1, -1)
        self.LoopsTabWidget = QTabWidget(self.page_Loops)
        self.LoopsTabWidget.setObjectName(u"LoopsTabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_16 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.verticalSpacer_16, 0, 1, 1, 1)

        self.authorEditTabWidget = QTabWidget(self.tab_2)
        self.authorEditTabWidget.setObjectName(u"authorEditTabWidget")
        sizePolicy21 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy21.setHorizontalStretch(45)
        sizePolicy21.setVerticalStretch(0)
        sizePolicy21.setHeightForWidth(self.authorEditTabWidget.sizePolicy().hasHeightForWidth())
        self.authorEditTabWidget.setSizePolicy(sizePolicy21)
        self.page_publication = QWidget()
        self.page_publication.setObjectName(u"page_publication")
        self.verticalLayout_23 = QVBoxLayout(self.page_publication)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_20 = QLabel(self.page_publication)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_24.addWidget(self.label_20)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_34 = QLabel(self.page_publication)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_34, 5, 0, 1, 1)

        self.footnote_label = QLabel(self.page_publication)
        self.footnote_label.setObjectName(u"footnote_label")
        self.footnote_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.footnote_label, 7, 0, 1, 1)

        self.label_21 = QLabel(self.page_publication)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 2, 0, 1, 1)

        self.label_28 = QLabel(self.page_publication)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setScaledContents(False)

        self.gridLayout_5.addWidget(self.label_28, 2, 2, 1, 1)

        self.PhoneLineEdit = QLineEdit(self.page_publication)
        self.PhoneLineEdit.setObjectName(u"PhoneLineEdit")

        self.gridLayout_5.addWidget(self.PhoneLineEdit, 4, 1, 1, 1)

        self.ContactAuthorCheckBox = QCheckBox(self.page_publication)
        self.ContactAuthorCheckBox.setObjectName(u"ContactAuthorCheckBox")

        self.gridLayout_5.addWidget(self.ContactAuthorCheckBox, 1, 1, 1, 1)

        self.label_22 = QLabel(self.page_publication)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_22.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_22, 0, 0, 1, 1)

        self.EmailLabel = QLabel(self.page_publication)
        self.EmailLabel.setObjectName(u"EmailLabel")
        self.EmailLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.EmailLabel, 3, 0, 1, 1)

        self.FootNoteLineEdit = QLineEdit(self.page_publication)
        self.FootNoteLineEdit.setObjectName(u"FootNoteLineEdit")

        self.gridLayout_5.addWidget(self.FootNoteLineEdit, 7, 1, 1, 1)

        self.label_27 = QLabel(self.page_publication)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setScaledContents(False)

        self.gridLayout_5.addWidget(self.label_27, 0, 2, 1, 1)

        self.PhoneLabel = QLabel(self.page_publication)
        self.PhoneLabel.setObjectName(u"PhoneLabel")
        self.PhoneLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.PhoneLabel, 4, 0, 1, 1)

        self.AddressTextedit = QTextEdit(self.page_publication)
        self.AddressTextedit.setObjectName(u"AddressTextedit")

        self.gridLayout_5.addWidget(self.AddressTextedit, 2, 1, 1, 1)

        self.FullNameLineEdit = QLineEdit(self.page_publication)
        self.FullNameLineEdit.setObjectName(u"FullNameLineEdit")

        self.gridLayout_5.addWidget(self.FullNameLineEdit, 0, 1, 1, 1)

        self.EMailLineEdit = QLineEdit(self.page_publication)
        self.EMailLineEdit.setObjectName(u"EMailLineEdit")

        self.gridLayout_5.addWidget(self.EMailLineEdit, 3, 1, 1, 1)

        self.ORCIDLineEdit = QLineEdit(self.page_publication)
        self.ORCIDLineEdit.setObjectName(u"ORCIDLineEdit")

        self.gridLayout_5.addWidget(self.ORCIDLineEdit, 5, 1, 1, 1)

        self.label_36 = QLabel(self.page_publication)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_36, 6, 0, 1, 1)

        self.IUCRIDLineEdit = QLineEdit(self.page_publication)
        self.IUCRIDLineEdit.setObjectName(u"IUCRIDLineEdit")

        self.gridLayout_5.addWidget(self.IUCRIDLineEdit, 6, 1, 1, 1)


        self.verticalLayout_24.addLayout(self.gridLayout_5)


        self.verticalLayout_23.addLayout(self.verticalLayout_24)

        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.SaveAuthorLoopToTemplateButton = QPushButton(self.page_publication)
        self.SaveAuthorLoopToTemplateButton.setObjectName(u"SaveAuthorLoopToTemplateButton")

        self.verticalLayout_32.addWidget(self.SaveAuthorLoopToTemplateButton, 0, Qt.AlignRight)

        self.AddThisAuthorToLoopPushButton = QPushButton(self.page_publication)
        self.AddThisAuthorToLoopPushButton.setObjectName(u"AddThisAuthorToLoopPushButton")

        self.verticalLayout_32.addWidget(self.AddThisAuthorToLoopPushButton)


        self.verticalLayout_23.addLayout(self.verticalLayout_32)

        self.authorEditTabWidget.addTab(self.page_publication, "")
        self.page_audit = QWidget()
        self.page_audit.setObjectName(u"page_audit")
        self.verticalLayout_40 = QVBoxLayout(self.page_audit)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.label_23 = QLabel(self.page_audit)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_38.addWidget(self.label_23)

        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.label_29 = QLabel(self.page_audit)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setScaledContents(False)

        self.gridLayout_25.addWidget(self.label_29, 0, 2, 1, 1)

        self.label_24 = QLabel(self.page_audit)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_24.setOpenExternalLinks(True)

        self.gridLayout_25.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_30 = QLabel(self.page_audit)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setScaledContents(False)

        self.gridLayout_25.addWidget(self.label_30, 2, 2, 1, 1)

        self.EmailLabel_cif = QLabel(self.page_audit)
        self.EmailLabel_cif.setObjectName(u"EmailLabel_cif")
        self.EmailLabel_cif.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_25.addWidget(self.EmailLabel_cif, 3, 0, 1, 1)

        self.PhoneLineEdit_cif = QLineEdit(self.page_audit)
        self.PhoneLineEdit_cif.setObjectName(u"PhoneLineEdit_cif")

        self.gridLayout_25.addWidget(self.PhoneLineEdit_cif, 4, 1, 1, 1)

        self.ContactAuthorCheckBox_cif = QCheckBox(self.page_audit)
        self.ContactAuthorCheckBox_cif.setObjectName(u"ContactAuthorCheckBox_cif")

        self.gridLayout_25.addWidget(self.ContactAuthorCheckBox_cif, 1, 1, 1, 1)

        self.AddressTextedit_cif = QTextEdit(self.page_audit)
        self.AddressTextedit_cif.setObjectName(u"AddressTextedit_cif")

        self.gridLayout_25.addWidget(self.AddressTextedit_cif, 2, 1, 1, 1)

        self.label_25 = QLabel(self.page_audit)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_25.addWidget(self.label_25, 2, 0, 1, 1)

        self.FullNameLineEdit_cif = QLineEdit(self.page_audit)
        self.FullNameLineEdit_cif.setObjectName(u"FullNameLineEdit_cif")

        self.gridLayout_25.addWidget(self.FullNameLineEdit_cif, 0, 1, 1, 1)

        self.PhoneLabel_cif = QLabel(self.page_audit)
        self.PhoneLabel_cif.setObjectName(u"PhoneLabel_cif")
        self.PhoneLabel_cif.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_25.addWidget(self.PhoneLabel_cif, 4, 0, 1, 1)

        self.EMailLineEdit_cif = QLineEdit(self.page_audit)
        self.EMailLineEdit_cif.setObjectName(u"EMailLineEdit_cif")

        self.gridLayout_25.addWidget(self.EMailLineEdit_cif, 3, 1, 1, 1)

        self.label_16 = QLabel(self.page_audit)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_25.addWidget(self.label_16, 6, 0, 1, 3)

        self.label_19 = QLabel(self.page_audit)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_25.addWidget(self.label_19, 7, 0, 1, 3)

        self.label_13 = QLabel(self.page_audit)
        self.label_13.setObjectName(u"label_13")
        sizePolicy22 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy22.setHorizontalStretch(0)
        sizePolicy22.setVerticalStretch(0)
        sizePolicy22.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy22)
        self.label_13.setWordWrap(True)

        self.gridLayout_25.addWidget(self.label_13, 5, 1, 1, 2)


        self.verticalLayout_38.addLayout(self.gridLayout_25)


        self.verticalLayout_40.addLayout(self.verticalLayout_38)

        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.SaveAuthorLoopToTemplateButton_cif = QPushButton(self.page_audit)
        self.SaveAuthorLoopToTemplateButton_cif.setObjectName(u"SaveAuthorLoopToTemplateButton_cif")

        self.verticalLayout_39.addWidget(self.SaveAuthorLoopToTemplateButton_cif, 0, Qt.AlignRight)

        self.AddThisAuthorToLoopPushButton_cif = QPushButton(self.page_audit)
        self.AddThisAuthorToLoopPushButton_cif.setObjectName(u"AddThisAuthorToLoopPushButton_cif")
        sizePolicy23 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy23.setHorizontalStretch(0)
        sizePolicy23.setVerticalStretch(0)
        sizePolicy23.setHeightForWidth(self.AddThisAuthorToLoopPushButton_cif.sizePolicy().hasHeightForWidth())
        self.AddThisAuthorToLoopPushButton_cif.setSizePolicy(sizePolicy23)

        self.verticalLayout_39.addWidget(self.AddThisAuthorToLoopPushButton_cif)


        self.verticalLayout_40.addLayout(self.verticalLayout_39)

        self.authorEditTabWidget.addTab(self.page_audit, "")

        self.gridLayout_2.addWidget(self.authorEditTabWidget, 2, 1, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_21, 2, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_10, 3, 1, 1, 1)

        self.frame_2 = QFrame(self.tab_2)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy24 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy24.setHorizontalStretch(55)
        sizePolicy24.setVerticalStretch(0)
        sizePolicy24.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy24)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout_2.addWidget(self.frame_2, 2, 2, 1, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_15, 1, 1, 1, 1)

        self.LoopsTabWidget.addTab(self.tab_2, "")

        self.verticalLayout_9.addWidget(self.LoopsTabWidget)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.revertLoopsPushButton = QPushButton(self.page_Loops)
        self.revertLoopsPushButton.setObjectName(u"revertLoopsPushButton")

        self.gridLayout_16.addWidget(self.revertLoopsPushButton, 0, 2, 1, 1)

        self.BackFromLoopsPushButton = QPushButton(self.page_Loops)
        self.BackFromLoopsPushButton.setObjectName(u"BackFromLoopsPushButton")
        sizePolicy5.setHeightForWidth(self.BackFromLoopsPushButton.sizePolicy().hasHeightForWidth())
        self.BackFromLoopsPushButton.setSizePolicy(sizePolicy5)
        self.BackFromLoopsPushButton.setMinimumSize(QSize(120, 0))

        self.gridLayout_16.addWidget(self.BackFromLoopsPushButton, 0, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_16.addItem(self.verticalSpacer_7, 3, 0, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_15, 0, 1, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_16, 0, 3, 1, 1)

        self.newLoopPushButton = QPushButton(self.page_Loops)
        self.newLoopPushButton.setObjectName(u"newLoopPushButton")

        self.gridLayout_16.addWidget(self.newLoopPushButton, 0, 4, 1, 1)

        self.deleteLoopButton = QPushButton(self.page_Loops)
        self.deleteLoopButton.setObjectName(u"deleteLoopButton")

        self.gridLayout_16.addWidget(self.deleteLoopButton, 3, 4, 1, 1)


        self.verticalLayout_9.addLayout(self.gridLayout_16)

        self.MainStackedWidget.addWidget(self.page_Loops)
        self.page_checkcif = QWidget()
        self.page_checkcif.setObjectName(u"page_checkcif")
        self.gridLayout_8 = QGridLayout(self.page_checkcif)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.CheckCIFResultsTabWidget = QTabWidget(self.page_checkcif)
        self.CheckCIFResultsTabWidget.setObjectName(u"CheckCIFResultsTabWidget")
        sizePolicy25 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy25.setHorizontalStretch(0)
        sizePolicy25.setVerticalStretch(4)
        sizePolicy25.setHeightForWidth(self.CheckCIFResultsTabWidget.sizePolicy().hasHeightForWidth())
        self.CheckCIFResultsTabWidget.setSizePolicy(sizePolicy25)
        self.CheckCIFResultsTabWidget.setDocumentMode(False)
        self.CheckCIFResultsTabWidget.setTabBarAutoHide(False)
        self.platon_page = QWidget()
        self.platon_page.setObjectName(u"platon_page")
        self.verticalLayout_11 = QVBoxLayout(self.platon_page)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.CheckcifPlaintextEdit = QPlainTextEdit(self.platon_page)
        self.CheckcifPlaintextEdit.setObjectName(u"CheckcifPlaintextEdit")
        self.CheckcifPlaintextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.CheckcifPlaintextEdit.setReadOnly(True)
        self.CheckcifPlaintextEdit.setPlainText(u"")
        self.CheckcifPlaintextEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_11.addWidget(self.CheckcifPlaintextEdit)

        self.CheckCIFResultsTabWidget.addTab(self.platon_page, "")
        self.html_page = QWidget()
        self.html_page.setObjectName(u"html_page")
        self.verticalLayout_12 = QVBoxLayout(self.html_page)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.ResponsesTabWidget = QTabWidget(self.html_page)
        self.ResponsesTabWidget.setObjectName(u"ResponsesTabWidget")
        self.ResponsesTabWidget.setTabPosition(QTabWidget.South)
        self.ResponsesTabWidget.setMovable(False)
        self.htmlTabwidgetPage = QWidget()
        self.htmlTabwidgetPage.setObjectName(u"htmlTabwidgetPage")
        self.verticalLayout_14 = QVBoxLayout(self.htmlTabwidgetPage)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.htmlCHeckCifGridLayout = QGridLayout()
        self.htmlCHeckCifGridLayout.setObjectName(u"htmlCHeckCifGridLayout")

        self.verticalLayout_14.addLayout(self.htmlCHeckCifGridLayout)

        self.ResponsesTabWidget.addTab(self.htmlTabwidgetPage, "")
        self.ResponsesTabWidgetPage2 = QWidget()
        self.ResponsesTabWidgetPage2.setObjectName(u"ResponsesTabWidgetPage2")
        self.verticalLayout_15 = QVBoxLayout(self.ResponsesTabWidgetPage2)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.responseFormsListWidget = QListWidget(self.ResponsesTabWidgetPage2)
        self.responseFormsListWidget.setObjectName(u"responseFormsListWidget")
        self.responseFormsListWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.responseFormsListWidget.setAutoScroll(False)
        self.responseFormsListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.responseFormsListWidget.setProperty(u"showDropIndicator", False)
        self.responseFormsListWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout_15.addWidget(self.responseFormsListWidget)

        self.label_6 = QLabel(self.ResponsesTabWidgetPage2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_15.addWidget(self.label_6)

        self.frame = QFrame(self.ResponsesTabWidgetPage2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.SavePushButton = QPushButton(self.frame)
        self.SavePushButton.setObjectName(u"SavePushButton")

        self.horizontalLayout_2.addWidget(self.SavePushButton)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_19)


        self.verticalLayout_15.addWidget(self.frame)

        self.ResponsesTabWidget.addTab(self.ResponsesTabWidgetPage2, "")

        self.verticalLayout_12.addWidget(self.ResponsesTabWidget)

        self.CheckCIFResultsTabWidget.addTab(self.html_page, "")
        self.pdf_page = QWidget()
        self.pdf_page.setObjectName(u"pdf_page")
        self.verticalLayout_13 = QVBoxLayout(self.pdf_page)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_5 = QLabel(self.pdf_page)
        self.label_5.setObjectName(u"label_5")
        sizePolicy26 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy26.setHorizontalStretch(0)
        sizePolicy26.setVerticalStretch(0)
        sizePolicy26.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy26)
        self.label_5.setMinimumSize(QSize(0, 20))

        self.verticalLayout_13.addWidget(self.label_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_4)

        self.CheckCIFResultsTabWidget.addTab(self.pdf_page, "")
        self.ckf_page = QWidget()
        self.ckf_page.setObjectName(u"ckf_page")
        self.verticalLayout_36 = QVBoxLayout(self.ckf_page)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(3, 3, 3, 3)
        self.ckf_textedit = QPlainTextEdit(self.ckf_page)
        self.ckf_textedit.setObjectName(u"ckf_textedit")
        font5 = QFont()
        font5.setFamilies([u"Courier New"])
        font5.setPointSize(10)
        self.ckf_textedit.setFont(font5)
        self.ckf_textedit.setReadOnly(True)
        self.ckf_textedit.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_36.addWidget(self.ckf_textedit)

        self.CheckCIFResultsTabWidget.addTab(self.ckf_page, "")

        self.gridLayout_8.addWidget(self.CheckCIFResultsTabWidget, 1, 0, 1, 8)

        self.groupBox_71 = QGroupBox(self.page_checkcif)
        self.groupBox_71.setObjectName(u"groupBox_71")
        sizePolicy27 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy27.setHorizontalStretch(0)
        sizePolicy27.setVerticalStretch(1)
        sizePolicy27.setHeightForWidth(self.groupBox_71.sizePolicy().hasHeightForWidth())
        self.groupBox_71.setSizePolicy(sizePolicy27)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_71)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 6, 0, 0)
        self.CheckCifLogPlainTextEdit = QPlainTextEdit(self.groupBox_71)
        self.CheckCifLogPlainTextEdit.setObjectName(u"CheckCifLogPlainTextEdit")
        self.CheckCifLogPlainTextEdit.setTabChangesFocus(True)
        self.CheckCifLogPlainTextEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.CheckCifLogPlainTextEdit)


        self.gridLayout_8.addWidget(self.groupBox_71, 0, 0, 1, 8)

        self.groupBox_checkcif_2 = QGroupBox(self.page_checkcif)
        self.groupBox_checkcif_2.setObjectName(u"groupBox_checkcif_2")
        self.gridLayout_14 = QGridLayout(self.groupBox_checkcif_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.CheckcifPDFOnlineButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifPDFOnlineButton.setObjectName(u"CheckcifPDFOnlineButton")

        self.gridLayout_14.addWidget(self.CheckcifPDFOnlineButton, 1, 2, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.structfactCheckBox = QCheckBox(self.groupBox_checkcif_2)
        self.structfactCheckBox.setObjectName(u"structfactCheckBox")

        self.horizontalLayout_9.addWidget(self.structfactCheckBox)

        self.fullIucrCheckBox = QCheckBox(self.groupBox_checkcif_2)
        self.fullIucrCheckBox.setObjectName(u"fullIucrCheckBox")

        self.horizontalLayout_9.addWidget(self.fullIucrCheckBox)


        self.gridLayout_14.addLayout(self.horizontalLayout_9, 2, 0, 1, 3)

        self.CheckcifButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifButton.setObjectName(u"CheckcifButton")

        self.gridLayout_14.addWidget(self.CheckcifButton, 1, 0, 1, 1)

        self.CheckcifHTMLOnlineButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifHTMLOnlineButton.setObjectName(u"CheckcifHTMLOnlineButton")

        self.gridLayout_14.addWidget(self.CheckcifHTMLOnlineButton, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_checkcif_2, 4, 5, 4, 1)

        self.ButtonFrame = QFrame(self.page_checkcif)
        self.ButtonFrame.setObjectName(u"ButtonFrame")
        self.ButtonFrame.setFrameShape(QFrame.NoFrame)
        self.ButtonFrame.setFrameShadow(QFrame.Raised)
        self.ButtonFrame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.ButtonFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_8.addWidget(self.ButtonFrame, 2, 0, 1, 7)

        self.horizontalSpacer = QSpacerItem(225, 47, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 4, 6, 3, 1)

        self.BackFromPlatonPushButton = QPushButton(self.page_checkcif)
        self.BackFromPlatonPushButton.setObjectName(u"BackFromPlatonPushButton")
        self.BackFromPlatonPushButton.setMinimumSize(QSize(160, 0))

        self.gridLayout_8.addWidget(self.BackFromPlatonPushButton, 5, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(13, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_2, 5, 1, 1, 2)

        self.horizontalSpacer_17 = QSpacerItem(13, 47, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_17, 4, 4, 3, 1)

        self.MainStackedWidget.addWidget(self.page_checkcif)
        self.page_cod = QWidget()
        self.page_cod.setObjectName(u"page_cod")
        self.gridLayout_17 = QGridLayout(self.page_cod)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.frame_for_radiobuttons = QFrame(self.page_cod)
        self.frame_for_radiobuttons.setObjectName(u"frame_for_radiobuttons")
        self.frame_for_radiobuttons.setFrameShape(QFrame.StyledPanel)
        self.frame_for_radiobuttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_for_radiobuttons)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_radiobuttons = QHBoxLayout()
        self.horizontalLayout_radiobuttons.setObjectName(u"horizontalLayout_radiobuttons")
        self.personalDepositRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.personalDepositRadioButton.setObjectName(u"personalDepositRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.personalDepositRadioButton)

        self.prepublicationDepositRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.prepublicationDepositRadioButton.setObjectName(u"prepublicationDepositRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.prepublicationDepositRadioButton)

        self.publishedDepositionRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.publishedDepositionRadioButton.setObjectName(u"publishedDepositionRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.publishedDepositionRadioButton)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_radiobuttons.addItem(self.horizontalSpacer_31)


        self.verticalLayout_28.addLayout(self.horizontalLayout_radiobuttons)


        self.gridLayout_22.addWidget(self.frame_for_radiobuttons, 0, 1, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, -1, 9, -1)
        self.depositorUsername = QLabel(self.page_cod)
        self.depositorUsername.setObjectName(u"depositorUsername")

        self.gridLayout_19.addWidget(self.depositorUsername, 0, 0, 1, 1)

        self.label_9 = QLabel(self.page_cod)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_19.addWidget(self.label_9, 2, 0, 1, 1)

        self.depositorPasswordLineEdit = QLineEdit(self.page_cod)
        self.depositorPasswordLineEdit.setObjectName(u"depositorPasswordLineEdit")
        self.depositorPasswordLineEdit.setEchoMode(QLineEdit.Password)

        self.gridLayout_19.addWidget(self.depositorPasswordLineEdit, 1, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, -1, -1)
        self.depositHKLcheckBox = QCheckBox(self.page_cod)
        self.depositHKLcheckBox.setObjectName(u"depositHKLcheckBox")

        self.horizontalLayout_11.addWidget(self.depositHKLcheckBox)

        self.Upload_hkl_pushButton = QPushButton(self.page_cod)
        self.Upload_hkl_pushButton.setObjectName(u"Upload_hkl_pushButton")
        sizePolicy5.setHeightForWidth(self.Upload_hkl_pushButton.sizePolicy().hasHeightForWidth())
        self.Upload_hkl_pushButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_11.addWidget(self.Upload_hkl_pushButton)


        self.gridLayout_19.addLayout(self.horizontalLayout_11, 3, 1, 1, 1)

        self.userEmailLineEdit = QLineEdit(self.page_cod)
        self.userEmailLineEdit.setObjectName(u"userEmailLineEdit")
        self.userEmailLineEdit.setInputMethodHints(Qt.ImhEmailCharactersOnly|Qt.ImhLowercaseOnly|Qt.ImhNoAutoUppercase)

        self.gridLayout_19.addWidget(self.userEmailLineEdit, 2, 1, 1, 1)

        self.depositorUsernameLineEdit = QLineEdit(self.page_cod)
        self.depositorUsernameLineEdit.setObjectName(u"depositorUsernameLineEdit")

        self.gridLayout_19.addWidget(self.depositorUsernameLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.page_cod)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextFormat(Qt.RichText)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.gridLayout_19.addWidget(self.label_2, 0, 2, 4, 1)

        self.depositorPasswordLabel = QLabel(self.page_cod)
        self.depositorPasswordLabel.setObjectName(u"depositorPasswordLabel")

        self.gridLayout_19.addWidget(self.depositorPasswordLabel, 1, 0, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_19, 1, 1, 1, 1)

        self.depositionOptionsStackedWidget = QStackedWidget(self.page_cod)
        self.depositionOptionsStackedWidget.setObjectName(u"depositionOptionsStackedWidget")
        self.depositionOptionsStackedWidget.setFrameShape(QFrame.NoFrame)
        self.depositionOptionsStackedWidget.setFrameShadow(QFrame.Raised)
        self.depositionOptionsStackedWidget.setLineWidth(1)
        self.page_personal = QWidget()
        self.page_personal.setObjectName(u"page_personal")
        self.verticalLayout_30 = QVBoxLayout(self.page_personal)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 12, 0, -1)
        self.label_10 = QLabel(self.page_personal)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setTextFormat(Qt.RichText)

        self.verticalLayout_30.addWidget(self.label_10)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.horizontalSpacer_30 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_30, 0, 2, 1, 1)

        self.ContactAuthorLabel = QLabel(self.page_personal)
        self.ContactAuthorLabel.setObjectName(u"ContactAuthorLabel")

        self.gridLayout_20.addWidget(self.ContactAuthorLabel, 1, 0, 1, 1)

        self.authorsFullNamePersonalLabel = QLabel(self.page_personal)
        self.authorsFullNamePersonalLabel.setObjectName(u"authorsFullNamePersonalLabel")

        self.gridLayout_20.addWidget(self.authorsFullNamePersonalLabel, 0, 0, 1, 1)

        self.authorEditorPushButton = QPushButton(self.page_personal)
        self.authorEditorPushButton.setObjectName(u"authorEditorPushButton")
        sizePolicy5.setHeightForWidth(self.authorEditorPushButton.sizePolicy().hasHeightForWidth())
        self.authorEditorPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_20.addWidget(self.authorEditorPushButton, 0, 1, 1, 1)

        self.ContactAuthorLineEdit = QLineEdit(self.page_personal)
        self.ContactAuthorLineEdit.setObjectName(u"ContactAuthorLineEdit")
        self.ContactAuthorLineEdit.setReadOnly(True)

        self.gridLayout_20.addWidget(self.ContactAuthorLineEdit, 1, 1, 1, 1)

        self.ContactEmailLineEdit = QLineEdit(self.page_personal)
        self.ContactEmailLineEdit.setObjectName(u"ContactEmailLineEdit")
        self.ContactEmailLineEdit.setReadOnly(True)

        self.gridLayout_20.addWidget(self.ContactEmailLineEdit, 2, 1, 1, 1)

        self.label_12 = QLabel(self.page_personal)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_20.addWidget(self.label_12, 2, 0, 1, 1)


        self.verticalLayout_30.addLayout(self.gridLayout_20)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_12)

        self.depositionOptionsStackedWidget.addWidget(self.page_personal)
        self.page_prepublication = QWidget()
        self.page_prepublication.setObjectName(u"page_prepublication")
        self.verticalLayout_25 = QVBoxLayout(self.page_prepublication)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.horizontalSpacer_29 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_29, 0, 2, 1, 1)

        self.embargoTimeInMonthsSpinBox = QSpinBox(self.page_prepublication)
        self.embargoTimeInMonthsSpinBox.setObjectName(u"embargoTimeInMonthsSpinBox")
        self.embargoTimeInMonthsSpinBox.setMinimum(6)
        self.embargoTimeInMonthsSpinBox.setMaximum(12)

        self.gridLayout_21.addWidget(self.embargoTimeInMonthsSpinBox, 1, 1, 1, 1)

        self.label_8 = QLabel(self.page_prepublication)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_21.addWidget(self.label_8, 1, 2, 1, 1)

        self.journalNameLineEdit = QLineEdit(self.page_prepublication)
        self.journalNameLineEdit.setObjectName(u"journalNameLineEdit")

        self.gridLayout_21.addWidget(self.journalNameLineEdit, 0, 1, 1, 1)

        self.embargoTimeInMonthsLabel = QLabel(self.page_prepublication)
        self.embargoTimeInMonthsLabel.setObjectName(u"embargoTimeInMonthsLabel")

        self.gridLayout_21.addWidget(self.embargoTimeInMonthsLabel, 1, 0, 1, 1)

        self.journalMameLabel = QLabel(self.page_prepublication)
        self.journalMameLabel.setObjectName(u"journalMameLabel")

        self.gridLayout_21.addWidget(self.journalMameLabel, 0, 0, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_21)

        self.gridLayout_author_prepubl = QGridLayout()
        self.gridLayout_author_prepubl.setObjectName(u"gridLayout_author_prepubl")
        self.horizontalSpacer_35 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_author_prepubl.addItem(self.horizontalSpacer_35, 0, 3, 1, 1)

        self.authorsFullNamePersonalLabel_2 = QLabel(self.page_prepublication)
        self.authorsFullNamePersonalLabel_2.setObjectName(u"authorsFullNamePersonalLabel_2")

        self.gridLayout_author_prepubl.addWidget(self.authorsFullNamePersonalLabel_2, 0, 1, 1, 1)

        self.ContactAuthorLineEdit_2 = QLineEdit(self.page_prepublication)
        self.ContactAuthorLineEdit_2.setObjectName(u"ContactAuthorLineEdit_2")
        self.ContactAuthorLineEdit_2.setReadOnly(True)

        self.gridLayout_author_prepubl.addWidget(self.ContactAuthorLineEdit_2, 1, 2, 1, 1)

        self.authorEditorPushButton_2 = QPushButton(self.page_prepublication)
        self.authorEditorPushButton_2.setObjectName(u"authorEditorPushButton_2")
        sizePolicy5.setHeightForWidth(self.authorEditorPushButton_2.sizePolicy().hasHeightForWidth())
        self.authorEditorPushButton_2.setSizePolicy(sizePolicy5)

        self.gridLayout_author_prepubl.addWidget(self.authorEditorPushButton_2, 0, 2, 1, 1)

        self.ContactAuthorLabel_2 = QLabel(self.page_prepublication)
        self.ContactAuthorLabel_2.setObjectName(u"ContactAuthorLabel_2")

        self.gridLayout_author_prepubl.addWidget(self.ContactAuthorLabel_2, 1, 1, 1, 1)

        self.label_15 = QLabel(self.page_prepublication)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_author_prepubl.addWidget(self.label_15, 2, 1, 1, 1)

        self.ContactEmailLineEdit_2 = QLineEdit(self.page_prepublication)
        self.ContactEmailLineEdit_2.setObjectName(u"ContactEmailLineEdit_2")
        self.ContactEmailLineEdit_2.setReadOnly(True)

        self.gridLayout_author_prepubl.addWidget(self.ContactEmailLineEdit_2, 2, 2, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_author_prepubl)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_13)

        self.depositionOptionsStackedWidget.addWidget(self.page_prepublication)
        self.page_published = QWidget()
        self.page_published.setObjectName(u"page_published")
        self.verticalLayout_27 = QVBoxLayout(self.page_published)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_23 = QGridLayout()
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.publication_doi_lineedit = QLineEdit(self.page_published)
        self.publication_doi_lineedit.setObjectName(u"publication_doi_lineedit")

        self.gridLayout_23.addWidget(self.publication_doi_lineedit, 1, 1, 1, 1)

        self.cod_database_code_Label = QLabel(self.page_published)
        self.cod_database_code_Label.setObjectName(u"cod_database_code_Label")

        self.gridLayout_23.addWidget(self.cod_database_code_Label, 1, 0, 1, 1)

        self.horizontalSpacer_32 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_32, 1, 3, 1, 1)

        self.label_11 = QLabel(self.page_published)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_23.addWidget(self.label_11, 0, 0, 1, 2)

        self.GetDOIPushButton = QPushButton(self.page_published)
        self.GetDOIPushButton.setObjectName(u"GetDOIPushButton")

        self.gridLayout_23.addWidget(self.GetDOIPushButton, 1, 2, 1, 1)


        self.verticalLayout_27.addLayout(self.gridLayout_23)

        self.DOIResolveTextLabel = QLabel(self.page_published)
        self.DOIResolveTextLabel.setObjectName(u"DOIResolveTextLabel")
        self.DOIResolveTextLabel.setTextFormat(Qt.PlainText)
        self.DOIResolveTextLabel.setWordWrap(True)

        self.verticalLayout_27.addWidget(self.DOIResolveTextLabel)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_14 = QLabel(self.page_published)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setTextFormat(Qt.RichText)

        self.verticalLayout_26.addWidget(self.label_14)


        self.verticalLayout_27.addLayout(self.verticalLayout_26)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_27.addItem(self.verticalSpacer_11)

        self.depositionOptionsStackedWidget.addWidget(self.page_published)
        self.page_deposition_output = QWidget()
        self.page_deposition_output.setObjectName(u"page_deposition_output")
        self.verticalLayout_31 = QVBoxLayout(self.page_deposition_output)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(0, -1, 0, 0)
        self.label_deposition_output = QLabel(self.page_deposition_output)
        self.label_deposition_output.setObjectName(u"label_deposition_output")

        self.verticalLayout_31.addWidget(self.label_deposition_output)

        self.depositOutputTextBrowser = QTextBrowser(self.page_deposition_output)
        self.depositOutputTextBrowser.setObjectName(u"depositOutputTextBrowser")
        self.depositOutputTextBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.depositOutputTextBrowser.setAutoFormatting(QTextEdit.AutoAll)
        self.depositOutputTextBrowser.setOpenExternalLinks(True)

        self.verticalLayout_31.addWidget(self.depositOutputTextBrowser)

        self.depositionOptionsStackedWidget.addWidget(self.page_deposition_output)

        self.gridLayout_22.addWidget(self.depositionOptionsStackedWidget, 4, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_22, 0, 1, 1, 1)

        self.StructuresListGroupBox = QGroupBox(self.page_cod)
        self.StructuresListGroupBox.setObjectName(u"StructuresListGroupBox")
        sizePolicy28 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy28.setHorizontalStretch(0)
        sizePolicy28.setVerticalStretch(0)
        sizePolicy28.setHeightForWidth(self.StructuresListGroupBox.sizePolicy().hasHeightForWidth())
        self.StructuresListGroupBox.setSizePolicy(sizePolicy28)
        self.StructuresListGroupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.gridLayout_18 = QGridLayout(self.StructuresListGroupBox)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.refreshDepositListPushButton = QPushButton(self.StructuresListGroupBox)
        self.refreshDepositListPushButton.setObjectName(u"refreshDepositListPushButton")
        self.refreshDepositListPushButton.setEnabled(False)
        self.refreshDepositListPushButton.setCheckable(False)
        self.refreshDepositListPushButton.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.refreshDepositListPushButton, 1, 1, 1, 1)

        self.horizontalSpacer_33 = QSpacerItem(1, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_33, 1, 0, 1, 1)

        self.horizontalSpacer_34 = QSpacerItem(1, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_34, 1, 2, 1, 1)

        self.CODtableWidget = QTableWidget(self.StructuresListGroupBox)
        if (self.CODtableWidget.columnCount() < 3):
            self.CODtableWidget.setColumnCount(3)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.CODtableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.CODtableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.CODtableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        self.CODtableWidget.setObjectName(u"CODtableWidget")
        self.CODtableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.CODtableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.CODtableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.CODtableWidget.setSortingEnabled(True)
        self.CODtableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.CODtableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.CODtableWidget.horizontalHeader().setStretchLastSection(False)
        self.CODtableWidget.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_18.addWidget(self.CODtableWidget, 0, 0, 1, 3)


        self.gridLayout_17.addWidget(self.StructuresListGroupBox, 0, 0, 1, 1, Qt.AlignHCenter)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.BackFromDepositPushButton = QPushButton(self.page_cod)
        self.BackFromDepositPushButton.setObjectName(u"BackFromDepositPushButton")
        self.BackFromDepositPushButton.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_10.addWidget(self.BackFromDepositPushButton)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_27)

        self.depositCIFpushButton = QPushButton(self.page_cod)
        self.depositCIFpushButton.setObjectName(u"depositCIFpushButton")

        self.horizontalLayout_10.addWidget(self.depositCIFpushButton)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_28)


        self.gridLayout_17.addLayout(self.horizontalLayout_10, 1, 0, 1, 2)

        self.MainStackedWidget.addWidget(self.page_cod)
        self.page_textTemplate = QWidget()
        self.page_textTemplate.setObjectName(u"page_textTemplate")
        self.verticalLayout_33 = QVBoxLayout(self.page_textTemplate)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.MainStackedWidget.addWidget(self.page_textTemplate)

        self.gridLayout_6.addWidget(self.MainStackedWidget, 2, 0, 1, 13)

        self.splitter.addWidget(self.CifDataItemsFrame)

        self.horizontalLayout_4.addWidget(self.splitter)

        FinalCifWindow.setCentralWidget(self.Mainwidget)
        self.statusBar = QStatusBar(FinalCifWindow)
        self.statusBar.setObjectName(u"statusBar")
        FinalCifWindow.setStatusBar(self.statusBar)
        QWidget.setTabOrder(self.publishedDepositionRadioButton, self.prepublicationDepositRadioButton)
        QWidget.setTabOrder(self.prepublicationDepositRadioButton, self.SelectCif_PushButton)
        QWidget.setTabOrder(self.SelectCif_PushButton, self.EditEquipmentTemplateButton)
        QWidget.setTabOrder(self.EditEquipmentTemplateButton, self.ImportEquipmentTemplateButton)
        QWidget.setTabOrder(self.ImportEquipmentTemplateButton, self.DeleteEquipmentButton)
        QWidget.setTabOrder(self.DeleteEquipmentButton, self.SaveEquipmentButton)
        QWidget.setTabOrder(self.SaveEquipmentButton, self.CancelEquipmentButton)
        QWidget.setTabOrder(self.CancelEquipmentButton, self.ExportEquipmentButton)
        QWidget.setTabOrder(self.ExportEquipmentButton, self.EditPropertyTemplateButton)
        QWidget.setTabOrder(self.EditPropertyTemplateButton, self.NewPropertyTemplateButton)
        QWidget.setTabOrder(self.NewPropertyTemplateButton, self.ImportPropertyTemplateButton)
        QWidget.setTabOrder(self.ImportPropertyTemplateButton, self.cifKeywordLineEdit)
        QWidget.setTabOrder(self.cifKeywordLineEdit, self.DeletePropertiesButton)
        QWidget.setTabOrder(self.DeletePropertiesButton, self.SavePropertiesButton)
        QWidget.setTabOrder(self.SavePropertiesButton, self.CancelPropertiesButton)
        QWidget.setTabOrder(self.CancelPropertiesButton, self.ExportPropertyButton)
        QWidget.setTabOrder(self.ExportPropertyButton, self.LoopTemplatesListWidget)
        QWidget.setTabOrder(self.LoopTemplatesListWidget, self.HelpPushButton)
        QWidget.setTabOrder(self.HelpPushButton, self.cif_main_table)
        QWidget.setTabOrder(self.cif_main_table, self.SaveCifButton)
        QWidget.setTabOrder(self.SaveCifButton, self.ExploreDirButton)
        QWidget.setTabOrder(self.ExploreDirButton, self.DetailsPushButton)
        QWidget.setTabOrder(self.DetailsPushButton, self.LoopsPushButton)
        QWidget.setTabOrder(self.LoopsPushButton, self.ReportPicPushButton)
        QWidget.setTabOrder(self.ReportPicPushButton, self.SaveFullReportButton)
        QWidget.setTabOrder(self.SaveFullReportButton, self.CheckcifStartButton)
        QWidget.setTabOrder(self.CheckcifStartButton, self.CODpushButton)
        QWidget.setTabOrder(self.CODpushButton, self.ShredCifButton)
        QWidget.setTabOrder(self.ShredCifButton, self.CCDCpushButton)
        QWidget.setTabOrder(self.CCDCpushButton, self.OptionsPushButton)
        QWidget.setTabOrder(self.OptionsPushButton, self.FinalCifFilePlainTextEdit)
        QWidget.setTabOrder(self.FinalCifFilePlainTextEdit, self.BackPushButton)
        QWidget.setTabOrder(self.BackPushButton, self.reflTotalLineEdit)
        QWidget.setTabOrder(self.reflTotalLineEdit, self.refl2sigmaLineEdit)
        QWidget.setTabOrder(self.refl2sigmaLineEdit, self.uniqReflLineEdit)
        QWidget.setTabOrder(self.uniqReflLineEdit, self.numParametersLineEdit)
        QWidget.setTabOrder(self.numParametersLineEdit, self.dataReflnsLineEdit)
        QWidget.setTabOrder(self.dataReflnsLineEdit, self.wavelengthLineEdit)
        QWidget.setTabOrder(self.wavelengthLineEdit, self.flackXLineEdit)
        QWidget.setTabOrder(self.flackXLineEdit, self.zLineEdit)
        QWidget.setTabOrder(self.zLineEdit, self.temperatureLineEdit)
        QWidget.setTabOrder(self.temperatureLineEdit, self.wR2LineEdit)
        QWidget.setTabOrder(self.wR2LineEdit, self.r1LineEdit)
        QWidget.setTabOrder(self.r1LineEdit, self.goofLineEdit)
        QWidget.setTabOrder(self.goofLineEdit, self.maxShiftLineEdit)
        QWidget.setTabOrder(self.maxShiftLineEdit, self.peakLineEdit)
        QWidget.setTabOrder(self.peakLineEdit, self.rintLineEdit)
        QWidget.setTabOrder(self.rintLineEdit, self.rsigmaLineEdit)
        QWidget.setTabOrder(self.rsigmaLineEdit, self.numRestraintsLineEdit)
        QWidget.setTabOrder(self.numRestraintsLineEdit, self.thetaMaxLineEdit)
        QWidget.setTabOrder(self.thetaMaxLineEdit, self.thetaFullLineEdit)
        QWidget.setTabOrder(self.thetaFullLineEdit, self.dLineEdit)
        QWidget.setTabOrder(self.dLineEdit, self.SourcesTableWidget)
        QWidget.setTabOrder(self.SourcesTableWidget, self.BackSourcesPushButton)
        QWidget.setTabOrder(self.BackSourcesPushButton, self.BackFromOptionspPushButton)
        QWidget.setTabOrder(self.BackFromOptionspPushButton, self.CheckCIFServerURLTextedit)
        QWidget.setTabOrder(self.CheckCIFServerURLTextedit, self.PictureWidthDoubleSpinBox)
        QWidget.setTabOrder(self.PictureWidthDoubleSpinBox, self.LoopsTabWidget)
        QWidget.setTabOrder(self.LoopsTabWidget, self.revertLoopsPushButton)
        QWidget.setTabOrder(self.revertLoopsPushButton, self.BackFromLoopsPushButton)
        QWidget.setTabOrder(self.BackFromLoopsPushButton, self.CheckCifLogPlainTextEdit)
        QWidget.setTabOrder(self.CheckCifLogPlainTextEdit, self.CheckcifButton)
        QWidget.setTabOrder(self.CheckcifButton, self.CheckcifPDFOnlineButton)
        QWidget.setTabOrder(self.CheckcifPDFOnlineButton, self.CheckcifHTMLOnlineButton)
        QWidget.setTabOrder(self.CheckcifHTMLOnlineButton, self.CheckCIFResultsTabWidget)
        QWidget.setTabOrder(self.CheckCIFResultsTabWidget, self.CheckcifPlaintextEdit)
        QWidget.setTabOrder(self.CheckcifPlaintextEdit, self.ResponsesTabWidget)
        QWidget.setTabOrder(self.ResponsesTabWidget, self.responseFormsListWidget)
        QWidget.setTabOrder(self.responseFormsListWidget, self.SavePushButton)
        QWidget.setTabOrder(self.SavePushButton, self.EquipmentEditTableWidget)
        QWidget.setTabOrder(self.EquipmentEditTableWidget, self.PropertiesTemplatesListWidget)
        QWidget.setTabOrder(self.PropertiesTemplatesListWidget, self.EquipmentTemplatesListWidget)
        QWidget.setTabOrder(self.EquipmentTemplatesListWidget, self.RecentComboBox)
        QWidget.setTabOrder(self.RecentComboBox, self.PropertiesEditTableWidget)
        QWidget.setTabOrder(self.PropertiesEditTableWidget, self.NewEquipmentTemplateButton)
        QWidget.setTabOrder(self.NewEquipmentTemplateButton, self.ExportAuthorPushButton)
        QWidget.setTabOrder(self.ExportAuthorPushButton, self.ImportAuthorPushButton)
        QWidget.setTabOrder(self.ImportAuthorPushButton, self.DeleteLoopAuthorTemplateButton)
        QWidget.setTabOrder(self.DeleteLoopAuthorTemplateButton, self.SumFormMainLineEdit)
        QWidget.setTabOrder(self.SumFormMainLineEdit, self.Spacegroup_top_LineEdit)
        QWidget.setTabOrder(self.Spacegroup_top_LineEdit, self.CCDCNumLineEdit)
        QWidget.setTabOrder(self.CCDCNumLineEdit, self.BackpushButtonDetails)
        QWidget.setTabOrder(self.BackpushButtonDetails, self.completeLineEdit)
        QWidget.setTabOrder(self.completeLineEdit, self.personalDepositRadioButton)
        QWidget.setTabOrder(self.personalDepositRadioButton, self.CODtableWidget)
        QWidget.setTabOrder(self.CODtableWidget, self.journalNameLineEdit)
        QWidget.setTabOrder(self.journalNameLineEdit, self.FullNameLineEdit)
        QWidget.setTabOrder(self.FullNameLineEdit, self.ContactAuthorCheckBox)
        QWidget.setTabOrder(self.ContactAuthorCheckBox, self.AddressTextedit)
        QWidget.setTabOrder(self.AddressTextedit, self.EMailLineEdit)
        QWidget.setTabOrder(self.EMailLineEdit, self.PhoneLineEdit)
        QWidget.setTabOrder(self.PhoneLineEdit, self.ORCIDLineEdit)
        QWidget.setTabOrder(self.ORCIDLineEdit, self.IUCRIDLineEdit)
        QWidget.setTabOrder(self.IUCRIDLineEdit, self.FootNoteLineEdit)
        QWidget.setTabOrder(self.FootNoteLineEdit, self.SaveAuthorLoopToTemplateButton)
        QWidget.setTabOrder(self.SaveAuthorLoopToTemplateButton, self.AddThisAuthorToLoopPushButton)
        QWidget.setTabOrder(self.AddThisAuthorToLoopPushButton, self.drawImagePushButton)
        QWidget.setTabOrder(self.drawImagePushButton, self.ExportAllTemplatesPushButton)
        QWidget.setTabOrder(self.ExportAllTemplatesPushButton, self.ImportAllTemplatesPushButton)
        QWidget.setTabOrder(self.ImportAllTemplatesPushButton, self.ReportTextCheckBox)
        QWidget.setTabOrder(self.ReportTextCheckBox, self.HAtomsCheckBox)
        QWidget.setTabOrder(self.HAtomsCheckBox, self.CODURLTextedit)
        QWidget.setTabOrder(self.CODURLTextedit, self.trackChangesCifCheckBox)
        QWidget.setTabOrder(self.trackChangesCifCheckBox, self.authorEditTabWidget)
        QWidget.setTabOrder(self.authorEditTabWidget, self.depositorUsernameLineEdit)
        QWidget.setTabOrder(self.depositorUsernameLineEdit, self.depositorPasswordLineEdit)
        QWidget.setTabOrder(self.depositorPasswordLineEdit, self.SelectCif_LineEdit)
        QWidget.setTabOrder(self.SelectCif_LineEdit, self.growCheckBox)
        QWidget.setTabOrder(self.growCheckBox, self.labelsCheckBox)
        QWidget.setTabOrder(self.labelsCheckBox, self.FullNameLineEdit_cif)
        QWidget.setTabOrder(self.FullNameLineEdit_cif, self.ContactAuthorCheckBox_cif)
        QWidget.setTabOrder(self.ContactAuthorCheckBox_cif, self.AddressTextedit_cif)
        QWidget.setTabOrder(self.AddressTextedit_cif, self.EMailLineEdit_cif)
        QWidget.setTabOrder(self.EMailLineEdit_cif, self.PhoneLineEdit_cif)
        QWidget.setTabOrder(self.PhoneLineEdit_cif, self.SaveAuthorLoopToTemplateButton_cif)
        QWidget.setTabOrder(self.SaveAuthorLoopToTemplateButton_cif, self.AddThisAuthorToLoopPushButton_cif)
        QWidget.setTabOrder(self.AddThisAuthorToLoopPushButton_cif, self.newLoopPushButton)
        QWidget.setTabOrder(self.newLoopPushButton, self.structfactCheckBox)
        QWidget.setTabOrder(self.structfactCheckBox, self.fullIucrCheckBox)
        QWidget.setTabOrder(self.fullIucrCheckBox, self.BackFromPlatonPushButton)
        QWidget.setTabOrder(self.BackFromPlatonPushButton, self.depositHKLcheckBox)
        QWidget.setTabOrder(self.depositHKLcheckBox, self.Upload_hkl_pushButton)
        QWidget.setTabOrder(self.Upload_hkl_pushButton, self.userEmailLineEdit)
        QWidget.setTabOrder(self.userEmailLineEdit, self.authorEditorPushButton)
        QWidget.setTabOrder(self.authorEditorPushButton, self.ContactAuthorLineEdit)
        QWidget.setTabOrder(self.ContactAuthorLineEdit, self.ContactEmailLineEdit)
        QWidget.setTabOrder(self.ContactEmailLineEdit, self.embargoTimeInMonthsSpinBox)
        QWidget.setTabOrder(self.embargoTimeInMonthsSpinBox, self.ContactAuthorLineEdit_2)
        QWidget.setTabOrder(self.ContactAuthorLineEdit_2, self.authorEditorPushButton_2)
        QWidget.setTabOrder(self.authorEditorPushButton_2, self.ContactEmailLineEdit_2)
        QWidget.setTabOrder(self.ContactEmailLineEdit_2, self.publication_doi_lineedit)
        QWidget.setTabOrder(self.publication_doi_lineedit, self.GetDOIPushButton)
        QWidget.setTabOrder(self.GetDOIPushButton, self.depositOutputTextBrowser)
        QWidget.setTabOrder(self.depositOutputTextBrowser, self.refreshDepositListPushButton)
        QWidget.setTabOrder(self.refreshDepositListPushButton, self.BackFromDepositPushButton)
        QWidget.setTabOrder(self.BackFromDepositPushButton, self.depositCIFpushButton)
        QWidget.setTabOrder(self.depositCIFpushButton, self.datanameComboBox)
        QWidget.setTabOrder(self.datanameComboBox, self.appendCifPushButton)

        self.retranslateUi(FinalCifWindow)

        self.TemplatesStackedWidget.setCurrentIndex(0)
        self.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.MainStackedWidget.setCurrentIndex(5)
        self.PropertiesTemplatesStackedWidget.setCurrentIndex(1)
        self.LoopsTabWidget.setCurrentIndex(0)
        self.authorEditTabWidget.setCurrentIndex(1)
        self.CheckCIFResultsTabWidget.setCurrentIndex(3)
        self.ResponsesTabWidget.setCurrentIndex(1)
        self.depositionOptionsStackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(FinalCifWindow)
    # setupUi

    def retranslateUi(self, FinalCifWindow):
        FinalCifWindow.setWindowTitle(QCoreApplication.translate("FinalCifWindow", u"FinalCif", None))
        self.SelectCifFileGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"CIF File", None))
        self.SelectCif_LineEdit.setPlaceholderText(QCoreApplication.translate("FinalCifWindow", u"Select a .cif file first.", None))
        self.SelectCif_PushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Select File", None))
        self.RecentComboBox.setItemText(0, QCoreApplication.translate("FinalCifWindow", u"Recent Files", None))

        self.RecentComboBox.setCurrentText(QCoreApplication.translate("FinalCifWindow", u"Recent Files", None))
        self.searchMainTableLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Search Key", None))
        self.searchMainTableLineEdit.setPlaceholderText(QCoreApplication.translate("FinalCifWindow", u"Find a CIF keyword in the main table", None))
        self.EquipmentGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"Equipment Templates", None))
#if QT_CONFIG(tooltip)
        self.EquipmentTemplatesListWidget.setToolTip(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Each entry can have a list of key/value pairs. For example a Diffractometer model can have a list of features.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.NewEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"New Template", None))
        self.EditEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Edit Template", None))
        self.ImportEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Import Template", None))
        ___qtablewidgetitem = self.EquipmentEditTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FinalCifWindow", u"key", None));
        ___qtablewidgetitem1 = self.EquipmentEditTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FinalCifWindow", u"value", None));
        self.DeleteEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", u"Delete Template", None))
        self.SaveEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", u"Save", None))
        self.CancelEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", u"Cancel", None))
        self.ExportEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", u"Export", None))
        self.ImportCifPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Import .cif, .pcf, .cif_od, .cfx or .sqf file", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("FinalCifWindow", u"Report Options", None))
        self.ADPTableCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Add ADP table", None))
        self.ReportTextCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"No report text in structure report", None))
        self.PictureWidthLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Picture width [cm]", None))
        self.HAtomsCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"No bonds and angles to hydrogen atoms", None))
        self.UsePicometersCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Use picometers", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("FinalCifWindow", u"Report Templates:", None))

        __sortingEnabled = self.docxTemplatesListWidget.isSortingEnabled()
        self.docxTemplatesListWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.docxTemplatesListWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("FinalCifWindow", u"Use FinalCif default template", None));
        self.docxTemplatesListWidget.setSortingEnabled(__sortingEnabled)

        self.AddNewTemplPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Add New Template", None))
        self.RemoveTemplPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Remove Selected", None))
        self.label.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Get more templates here:  <a href=\"https://github.com/dkratzert/FinalCif\"><span style=\" text-decoration: underline; color:#0068da;\">https://github.com/dkratzert/FinalCif</span></a></p></body></html>", None))
        self.LoopsGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"Author Templates", None))
        self.ExportAuthorPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Export Author as File", None))
        self.ImportAuthorPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Import Author", None))
        self.DeleteLoopAuthorTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Delete Author", None))
        self.spacegroupLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Space-Group Type", None))
        self.appendCifPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Append CIF", None))
        self.CCDCNumLabel.setText(QCoreApplication.translate("FinalCifWindow", u"CCDC Number", None))
        self.HelpPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Help", None))
        self.datanameLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Data Name", None))
        self.SumFormMainLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Sum Formula", None))
        ___qtablewidgetitem2 = self.cif_main_table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FinalCifWindow", u"CIF Value", None));
        ___qtablewidgetitem3 = self.cif_main_table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FinalCifWindow", u"From Data Source", None));
        ___qtablewidgetitem4 = self.cif_main_table.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FinalCifWindow", u"Own Data", None));
        self.groupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.SaveCifButton.setToolTip(QCoreApplication.translate("FinalCifWindow", u"Saves the CIF file to name-finalcif.cif", None))
#endif // QT_CONFIG(tooltip)
        self.SaveCifButton.setText(QCoreApplication.translate("FinalCifWindow", u"Save CIF File", None))
#if QT_CONFIG(tooltip)
        self.ExploreDirButton.setToolTip(QCoreApplication.translate("FinalCifWindow", u"Saves the CIF file to name-finalcif.cif", None))
#endif // QT_CONFIG(tooltip)
        self.ExploreDirButton.setText(QCoreApplication.translate("FinalCifWindow", u"Explore Directory", None))
        self.DetailsPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Show Details", None))
        self.AuthorEditPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Author Editor", None))
        self.groupBox_checkcif.setTitle("")
        self.LoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Edit Loops", None))
        self.ReportPicPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Picture for Report", None))
        self.SaveFullReportButton.setText(QCoreApplication.translate("FinalCifWindow", u"Make Tables", None))
        self.CheckcifStartButton.setText(QCoreApplication.translate("FinalCifWindow", u"CheckCIF", None))
        self.groupBox_tables.setTitle("")
        self.CODpushButton.setText(QCoreApplication.translate("FinalCifWindow", u"COD Deposit", None))
        self.ShredCifButton.setText(QCoreApplication.translate("FinalCifWindow", u"Extract .hkl/.res File", None))
        self.CCDCpushButton.setText(QCoreApplication.translate("FinalCifWindow", u"CCDC Deposit", None))
        self.OptionsPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Options", None))
        self.BackPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.molGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"Molecule", None))
        self.growCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Grow Structure", None))
        self.labelsCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Show Labels", None))
        self.drawImagePushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Use as Image for Report", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("FinalCifWindow", u"Shelx File", None))
        self.shelx_TextEdit.setPlainText(QCoreApplication.translate("FinalCifWindow", u"No Shelx file available", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("FinalCifWindow", u"Properties", None))
        self.zLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Z</p></body></html>", None))
        self.temperatureLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Temperature [K]", None))
        self.wR2Label.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">wR</span><span style=\" vertical-align:sub;\">2 </span>[all ref.]</p></body></html>", None))
        self.r1Label.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">1 </span>[<span style=\" font-style:italic;\">I </span>&gt; 2\u03c3(<span style=\" font-style:italic;\">I</span>)]</p></body></html>", None))
        self.goofLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Goof", None))
        self.maxShiftLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Max Shift/esd", None))
        self.completeLabel.setText(QCoreApplication.translate("FinalCifWindow", u"complete [%]", None))
        self.reflTotalLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Measured Refl.", None))
        self.refl2sigmaLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Data with [<span style=\" font-style:italic;\">I </span>&gt; 2\u03c3(<span style=\" font-style:italic;\">I</span>)]</p></body></html>", None))
        self.uniqReflLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Independent Refl.", None))
        self.numParametersLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Parameters", None))
        self.dataReflnsLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Data/Parameters", None))
        self.wavelengthLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Wavelength [\u00c5]", None))
        self.flackXLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Flack x", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("FinalCifWindow", u"Unit Cell", None))
        self.cellField.setText("")
        self.peakLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Peak/Hole [e\u00c5<span style=\" vertical-align:super;\">-3</span>]</p></body></html>", None))
        self.rintLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">int</span></p></body></html>", None))
        self.rsigmaLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">\u03c3</span></p></body></html>", None))
        self.numRestraintsLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Restraints", None))
        self.thetaMaxLabel.setText(QCoreApplication.translate("FinalCifWindow", u"\u03b8(max) [\u00b0]", None))
        self.thetaFullLabel.setText(QCoreApplication.translate("FinalCifWindow", u"\u03b8(full) [\u00b0]", None))
        self.dLabel.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>Resolution [\u00c5]</p></body></html>", None))
        self.BackpushButtonDetails.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.SourcesPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Data Sources", None))
        self.groupBox_2.setTitle("")
        self.label_3.setText(QCoreApplication.translate("FinalCifWindow", u"The list of data sources shows the origin of CIF items automatically collected by FinalCif. \n"
"\n"
"Uncheck items in order to ignore the respective data source.\n"
"The data source will be ignored until next program restart.", None))
        ___qtablewidgetitem5 = self.SourcesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FinalCifWindow", u"CIF Item", None));
        ___qtablewidgetitem6 = self.SourcesTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("FinalCifWindow", u"Data Source", None));
        self.BackSourcesPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.BackFromOptionspPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to Main Table", None))
        self.groupBox_COD.setTitle(QCoreApplication.translate("FinalCifWindow", u"Crystallography Open Database Server", None))
        self.label_7.setText(QCoreApplication.translate("FinalCifWindow", u"COD deposit URL:", None))
        self.CODURLTextedit.setText(QCoreApplication.translate("FinalCifWindow", u"https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("FinalCifWindow", u"CheckCIF Server", None))
        self.label_4.setText(QCoreApplication.translate("FinalCifWindow", u"Change this URL if the CheckCIF server URL changes:", None))
        self.CheckCIFServerURLTextedit.setText(QCoreApplication.translate("FinalCifWindow", u"https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("FinalCifWindow", u"Export", None))
        self.ExportAllTemplatesPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Export all Templates", None))
        self.label_18.setText(QCoreApplication.translate("FinalCifWindow", u"Exports all templates from Equipment, Properties,\n"
" Authors and Text snippets to a single file.", None))
        self.ImportAllTemplatesPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Import all Templates", None))
        self.label_17.setText(QCoreApplication.translate("FinalCifWindow", u"Imports all templates from a template file.", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("FinalCifWindow", u"General Options", None))
        self.trackChangesCifCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Track CIF changes in separate file\n"
" \"[name]-finalcif_changes.cif\".", None))
        self.PropertiesGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"Property Templates", None))
#if QT_CONFIG(tooltip)
        self.PropertiesTemplatesListWidget.setToolTip(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>A list of common properties like </p><p>_exptl_crystal_colour: yellow, red, blue, ...</p><p>Lists defined here will appear as dropdown menus in the main Table.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.EditPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Edit Template", None))
        self.NewPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"New Template", None))
        self.ImportPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Import", None))
        self.cifKeywordLB.setText(QCoreApplication.translate("FinalCifWindow", u"CIF keyword:", None))
        self.DeletePropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", u"Delete Template", None))
        self.SavePropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", u"Save", None))
        self.CancelPropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", u"Cancel", None))
        self.ExportPropertyButton.setText(QCoreApplication.translate("FinalCifWindow", u"Export", None))
        self.label_20.setText(QCoreApplication.translate("FinalCifWindow", u"Details about the author(s) of a manuscript submitted for publication.\n"
"Contact authors should always also appear as regular authors.", None))
        self.label_34.setText(QCoreApplication.translate("FinalCifWindow", u"ORCID", None))
        self.footnote_label.setText(QCoreApplication.translate("FinalCifWindow", u"footnote", None))
        self.label_21.setText(QCoreApplication.translate("FinalCifWindow", u"Adresss", None))
        self.label_28.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" color:#666666;\">The adress of an author</span></p><p><span style=\" color:#666666;\">Department<br/>Institute<br/>Street<br/>City and postcode<br/>COUNTRY</span></p></body></html>", None))
        self.ContactAuthorCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"This is a contact author", None))
        self.label_22.setText(QCoreApplication.translate("FinalCifWindow", u"Full Name", None))
        self.EmailLabel.setText(QCoreApplication.translate("FinalCifWindow", u"e-mail", None))
        self.label_27.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" color:#666666;\">Family name, first name</span></p></body></html>", None))
        self.PhoneLabel.setText(QCoreApplication.translate("FinalCifWindow", u"phone number", None))
        self.label_36.setText(QCoreApplication.translate("FinalCifWindow", u"IUCr Id", None))
        self.SaveAuthorLoopToTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", u"Save Author as Template", None))
        self.AddThisAuthorToLoopPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Add Publication Author to CIF Loop", None))
        self.authorEditTabWidget.setTabText(self.authorEditTabWidget.indexOf(self.page_publication), QCoreApplication.translate("FinalCifWindow", u"Publication Authors", None))
        self.label_23.setText(QCoreApplication.translate("FinalCifWindow", u"Details about the author(s) of this CIF data block (most often the crystallographer).\n"
"Contact authors should always also appear as regular authors.", None))
        self.label_29.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" color:#666666;\">Family name, first name</span></p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("FinalCifWindow", u"Full Name", None))
        self.label_30.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" color:#666666;\">The adress of an author</span></p><p><span style=\" color:#666666;\">Department<br/>Institute<br/>Street<br/>City and postcode<br/>COUNTRY</span></p></body></html>", None))
        self.EmailLabel_cif.setText(QCoreApplication.translate("FinalCifWindow", u"e-mail", None))
        self.ContactAuthorCheckBox_cif.setText(QCoreApplication.translate("FinalCifWindow", u"This is a contact author", None))
        self.label_25.setText(QCoreApplication.translate("FinalCifWindow", u"Adresss", None))
        self.PhoneLabel_cif.setText(QCoreApplication.translate("FinalCifWindow", u"phone number", None))
        self.label_16.setText("")
        self.label_19.setText("")
        self.label_13.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" color:#666666;\">Audit authors have less possibilities than publication authors.</span></p></body></html>", None))
        self.SaveAuthorLoopToTemplateButton_cif.setText(QCoreApplication.translate("FinalCifWindow", u"Save Author as Template", None))
        self.AddThisAuthorToLoopPushButton_cif.setText(QCoreApplication.translate("FinalCifWindow", u"Add Audit Author to CIF Loop", None))
        self.authorEditTabWidget.setTabText(self.authorEditTabWidget.indexOf(self.page_audit), QCoreApplication.translate("FinalCifWindow", u"Audit (CIF) Authors", None))
        self.LoopsTabWidget.setTabText(self.LoopsTabWidget.indexOf(self.tab_2), QCoreApplication.translate("FinalCifWindow", u"Author Editor", None))
        self.revertLoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Revert Changes", None))
        self.BackFromLoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.newLoopPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Add New Loop", None))
        self.deleteLoopButton.setText(QCoreApplication.translate("FinalCifWindow", u"Delete Loop", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.platon_page), QCoreApplication.translate("FinalCifWindow", u"PLATON CheckCIF result", None))
        self.ResponsesTabWidget.setTabText(self.ResponsesTabWidget.indexOf(self.htmlTabwidgetPage), QCoreApplication.translate("FinalCifWindow", u"html report", None))
        self.label_6.setText(QCoreApplication.translate("FinalCifWindow", u"Every form you fill out will be written to the cif file.", None))
        self.SavePushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Save Response Forms", None))
        self.ResponsesTabWidget.setTabText(self.ResponsesTabWidget.indexOf(self.ResponsesTabWidgetPage2), QCoreApplication.translate("FinalCifWindow", u"checkcif alerts", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.html_page), QCoreApplication.translate("FinalCifWindow", u"html CheckCIF result", None))
        self.label_5.setText(QCoreApplication.translate("FinalCifWindow", u"The resulting PDF file will be displayed in an external program after CheckCIF has completed.", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.pdf_page), QCoreApplication.translate("FinalCifWindow", u"PDF CheckCIF result", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.ckf_page), QCoreApplication.translate("FinalCifWindow", u"Structure Factor Report", None))
        self.groupBox_71.setTitle(QCoreApplication.translate("FinalCifWindow", u"CheckCIF log messages", None))
        self.groupBox_checkcif_2.setTitle("")
        self.CheckcifPDFOnlineButton.setText(QCoreApplication.translate("FinalCifWindow", u"Checkcif Online PDF", None))
        self.structfactCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"without structure factors (faster but not complete)", None))
        self.fullIucrCheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"Full IUCr publication validation", None))
        self.CheckcifButton.setText(QCoreApplication.translate("FinalCifWindow", u"CheckCif Offline", None))
        self.CheckcifHTMLOnlineButton.setText(QCoreApplication.translate("FinalCifWindow", u"Checkcif Online HTML", None))
        self.BackFromPlatonPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.personalDepositRadioButton.setText(QCoreApplication.translate("FinalCifWindow", u"personal (private) communication", None))
        self.prepublicationDepositRadioButton.setText(QCoreApplication.translate("FinalCifWindow", u"prepublication", None))
        self.publishedDepositionRadioButton.setText(QCoreApplication.translate("FinalCifWindow", u"already published", None))
        self.depositorUsername.setText(QCoreApplication.translate("FinalCifWindow", u"depositor's username", None))
        self.label_9.setText(QCoreApplication.translate("FinalCifWindow", u"depsoitor's e-mail", None))
        self.depositHKLcheckBox.setText(QCoreApplication.translate("FinalCifWindow", u"deposit included hkl data or", None))
        self.Upload_hkl_pushButton.setText(QCoreApplication.translate("FinalCifWindow", u"choose different hkl file", None))
        self.label_2.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p>You need to have a COD account <br/>in order to deposit a cif file. </p><p><a href=\"http://crystallography.net/cod/\"><span style=\" text-decoration: underline; color:#094fd1;\">Signup here for a new account</span></a></p></body></html>", None))
        self.depositorPasswordLabel.setText(QCoreApplication.translate("FinalCifWindow", u"depositor's password", None))
        self.label_10.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">A personal communication to the COD makes the uploaded CIF publicly available.</span></p></body></html>", None))
        self.ContactAuthorLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Publication author for contact by the COD:", None))
        self.authorsFullNamePersonalLabel.setText(QCoreApplication.translate("FinalCifWindow", u"The current CIF does not contain enough author \n"
"information please add a publication author:", None))
        self.authorEditorPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Author Editor", None))
        self.label_12.setText(QCoreApplication.translate("FinalCifWindow", u"Email address for contact by the COD:", None))
        self.label_8.setText(QCoreApplication.translate("FinalCifWindow", u"(6-12 months)", None))
        self.embargoTimeInMonthsLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Hold period in months (embargo time)", None))
        self.journalMameLabel.setText(QCoreApplication.translate("FinalCifWindow", u"Intended journal name (not mandatory)", None))
        self.authorsFullNamePersonalLabel_2.setText(QCoreApplication.translate("FinalCifWindow", u"The current CIF does not contain all author information \n"
"please add a publication author:", None))
        self.authorEditorPushButton_2.setText(QCoreApplication.translate("FinalCifWindow", u"Author Editor", None))
        self.ContactAuthorLabel_2.setText(QCoreApplication.translate("FinalCifWindow", u"Publication author for contact by the COD:", None))
        self.label_15.setText(QCoreApplication.translate("FinalCifWindow", u"Email address for contact by the COD:", None))
        self.cod_database_code_Label.setText(QCoreApplication.translate("FinalCifWindow", u"Publication DOI:", None))
        self.label_11.setText(QCoreApplication.translate("FinalCifWindow", u"Insert the DOI of the publication to which the uploaded CIF belongs.", None))
        self.GetDOIPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Get Citation", None))
        self.DOIResolveTextLabel.setText("")
        self.label_14.setText(QCoreApplication.translate("FinalCifWindow", u"<html><head/><body><p><span style=\" font-weight:600; color:#a50000;\">Files from commercial databases should not be uploaded without permission!</span></p></body></html>", None))
        self.label_deposition_output.setText(QCoreApplication.translate("FinalCifWindow", u"Deposition Output:", None))
        self.StructuresListGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", u"List of deposited structures", None))
        self.refreshDepositListPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Enter username and password", None))
        ___qtablewidgetitem7 = self.CODtableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("FinalCifWindow", u"ID", None));
        ___qtablewidgetitem8 = self.CODtableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("FinalCifWindow", u"Date", None));
        ___qtablewidgetitem9 = self.CODtableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("FinalCifWindow", u"Time", None));
        self.BackFromDepositPushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Back to CIF Table", None))
        self.depositCIFpushButton.setText(QCoreApplication.translate("FinalCifWindow", u"Deposit CIF", None))
    # retranslateUi

