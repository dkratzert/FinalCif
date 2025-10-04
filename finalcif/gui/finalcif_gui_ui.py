
# Python: from finalcif.ciforder.order import CifOrder

################################################################################
##
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
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

class Ui_FinalCifWindow:
    def setupUi(self, FinalCifWindow):
        if not FinalCifWindow.objectName():
            FinalCifWindow.setObjectName("FinalCifWindow")
        FinalCifWindow.resize(1446, 860)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FinalCifWindow.sizePolicy().hasHeightForWidth())
        FinalCifWindow.setSizePolicy(sizePolicy)
        self.Mainwidget = QWidget(FinalCifWindow)
        self.Mainwidget.setObjectName("Mainwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.Mainwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 0)
        self.splitter = QSplitter(self.Mainwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.LeftFrame = QFrame(self.splitter)
        self.LeftFrame.setObjectName("LeftFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(9)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LeftFrame.sizePolicy().hasHeightForWidth())
        self.LeftFrame.setSizePolicy(sizePolicy1)
        self.LeftFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.LeftFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.LeftFrame.setLineWidth(0)
        self.verticalLayout_5 = QVBoxLayout(self.LeftFrame)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 0, 3, 0)
        self.SelectCifFileGroupBox = QGroupBox(self.LeftFrame)
        self.SelectCifFileGroupBox.setObjectName("SelectCifFileGroupBox")
        self.SelectCifFileGroupBox.setFlat(False)
        self.verticalLayout_29 = QVBoxLayout(self.SelectCifFileGroupBox)
        self.verticalLayout_29.setSpacing(6)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(3, 3, 3, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(3, 0, 0, -1)
        self.SelectCif_LineEdit = QLineEdit(self.SelectCifFileGroupBox)
        self.SelectCif_LineEdit.setObjectName("SelectCif_LineEdit")

        self.horizontalLayout_12.addWidget(self.SelectCif_LineEdit)

        self.SelectCif_PushButton = QPushButton(self.SelectCifFileGroupBox)
        self.SelectCif_PushButton.setObjectName("SelectCif_PushButton")

        self.horizontalLayout_12.addWidget(self.SelectCif_PushButton)


        self.verticalLayout_29.addLayout(self.horizontalLayout_12)

        self.RecentComboBox = QComboBox(self.SelectCifFileGroupBox)
        self.RecentComboBox.addItem("")
        self.RecentComboBox.setObjectName("RecentComboBox")
        self.RecentComboBox.setMaxVisibleItems(15)

        self.verticalLayout_29.addWidget(self.RecentComboBox)


        self.verticalLayout_5.addWidget(self.SelectCifFileGroupBox)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(3, -1, 3, -1)
        self.searchMainTableLabel = QLabel(self.LeftFrame)
        self.searchMainTableLabel.setObjectName("searchMainTableLabel")

        self.horizontalLayout_8.addWidget(self.searchMainTableLabel)

        self.searchMainTableLineEdit = QLineEdit(self.LeftFrame)
        self.searchMainTableLineEdit.setObjectName("searchMainTableLineEdit")

        self.horizontalLayout_8.addWidget(self.searchMainTableLineEdit)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.TemplatesStackedWidget = QStackedWidget(self.LeftFrame)
        self.TemplatesStackedWidget.setObjectName("TemplatesStackedWidget")
        sizePolicy.setHeightForWidth(self.TemplatesStackedWidget.sizePolicy().hasHeightForWidth())
        self.TemplatesStackedWidget.setSizePolicy(sizePolicy)
        self.TemplatesStackedWidget.setLineWidth(1)
        self.page_equipment = QWidget()
        self.page_equipment.setObjectName("page_equipment")
        self.verticalLayout_16 = QVBoxLayout(self.page_equipment)
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.EquipmentGroupBox = QGroupBox(self.page_equipment)
        self.EquipmentGroupBox.setObjectName("EquipmentGroupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(36)
        sizePolicy2.setHeightForWidth(self.EquipmentGroupBox.sizePolicy().hasHeightForWidth())
        self.EquipmentGroupBox.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.EquipmentGroupBox)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(6, 4, 6, 4)
        self.EquipmentTemplatesStackedWidget = QStackedWidget(self.EquipmentGroupBox)
        self.EquipmentTemplatesStackedWidget.setObjectName("EquipmentTemplatesStackedWidget")
        sizePolicy.setHeightForWidth(self.EquipmentTemplatesStackedWidget.sizePolicy().hasHeightForWidth())
        self.EquipmentTemplatesStackedWidget.setSizePolicy(sizePolicy)
        self.EquipmentSelectPage = QWidget()
        self.EquipmentSelectPage.setObjectName("EquipmentSelectPage")
        self.verticalLayout_19 = QVBoxLayout(self.EquipmentSelectPage)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 3, 0, 3)
        self.EquipmentTemplatesListWidget = QListWidget(self.EquipmentSelectPage)
        self.EquipmentTemplatesListWidget.setObjectName("EquipmentTemplatesListWidget")
        self.EquipmentTemplatesListWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.EquipmentTemplatesListWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.EquipmentTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_19.addWidget(self.EquipmentTemplatesListWidget)

        self.horizontalLayout_Buttons = QHBoxLayout()
        self.horizontalLayout_Buttons.setSpacing(6)
        self.horizontalLayout_Buttons.setObjectName("horizontalLayout_Buttons")
        self.NewEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.NewEquipmentTemplateButton.setObjectName("NewEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.NewEquipmentTemplateButton)

        self.EditEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.EditEquipmentTemplateButton.setObjectName("EditEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.EditEquipmentTemplateButton)

        self.ImportEquipmentTemplateButton = QPushButton(self.EquipmentSelectPage)
        self.ImportEquipmentTemplateButton.setObjectName("ImportEquipmentTemplateButton")

        self.horizontalLayout_Buttons.addWidget(self.ImportEquipmentTemplateButton)


        self.verticalLayout_19.addLayout(self.horizontalLayout_Buttons)

        self.EquipmentTemplatesStackedWidget.addWidget(self.EquipmentSelectPage)
        self.EquipmentEditPage = QWidget()
        self.EquipmentEditPage.setObjectName("EquipmentEditPage")
        self.verticalLayout_21 = QVBoxLayout(self.EquipmentEditPage)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
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
        self.EquipmentEditTableWidget.setObjectName("EquipmentEditTableWidget")
        self.EquipmentEditTableWidget.setAutoScroll(False)
        self.EquipmentEditTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.EquipmentEditTableWidget.setAlternatingRowColors(False)
        self.EquipmentEditTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.EquipmentEditTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.EquipmentEditTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.EquipmentEditTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.EquipmentEditTableWidget.setSortingEnabled(True)
        self.EquipmentEditTableWidget.setRowCount(1)
        self.EquipmentEditTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.EquipmentEditTableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.EquipmentEditTableWidget.horizontalHeader().setDefaultSectionSize(210)
        self.EquipmentEditTableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.EquipmentEditTableWidget.horizontalHeader().setStretchLastSection(True)
        self.EquipmentEditTableWidget.verticalHeader().setVisible(False)
        self.EquipmentEditTableWidget.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_21.addWidget(self.EquipmentEditTableWidget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.DeleteEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.DeleteEquipmentButton.setObjectName("DeleteEquipmentButton")

        self.horizontalLayout_5.addWidget(self.DeleteEquipmentButton)

        self.SaveEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.SaveEquipmentButton.setObjectName("SaveEquipmentButton")

        self.horizontalLayout_5.addWidget(self.SaveEquipmentButton)

        self.CancelEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.CancelEquipmentButton.setObjectName("CancelEquipmentButton")

        self.horizontalLayout_5.addWidget(self.CancelEquipmentButton)

        self.ExportEquipmentButton = QPushButton(self.EquipmentEditPage)
        self.ExportEquipmentButton.setObjectName("ExportEquipmentButton")

        self.horizontalLayout_5.addWidget(self.ExportEquipmentButton)


        self.verticalLayout_21.addLayout(self.horizontalLayout_5)

        self.EquipmentTemplatesStackedWidget.addWidget(self.EquipmentEditPage)

        self.verticalLayout_7.addWidget(self.EquipmentTemplatesStackedWidget)


        self.verticalLayout_16.addWidget(self.EquipmentGroupBox)

        self.line = QFrame(self.page_equipment)
        self.line.setObjectName("line")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy3)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_16.addWidget(self.line)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(6, 6, -1, 6)
        self.ImportCifPushButton = QPushButton(self.page_equipment)
        self.ImportCifPushButton.setObjectName("ImportCifPushButton")

        self.horizontalLayout_13.addWidget(self.ImportCifPushButton)


        self.verticalLayout_16.addLayout(self.horizontalLayout_13)

        self.line_5 = QFrame(self.page_equipment)
        self.line_5.setObjectName("line_5")
        sizePolicy3.setHeightForWidth(self.line_5.sizePolicy().hasHeightForWidth())
        self.line_5.setSizePolicy(sizePolicy3)
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_16.addWidget(self.line_5)

        self.groupBox_5 = QGroupBox(self.page_equipment)
        self.groupBox_5.setObjectName("groupBox_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(50)
        sizePolicy4.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy4)
        self.verticalLayout_35 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(6, 9, 6, 9)
        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.gridLayout_26.setContentsMargins(-1, -1, -1, 12)
        self.ADPTableCheckBox = QCheckBox(self.groupBox_5)
        self.ADPTableCheckBox.setObjectName("ADPTableCheckBox")
        self.ADPTableCheckBox.setChecked(True)

        self.gridLayout_26.addWidget(self.ADPTableCheckBox, 0, 1, 1, 1)

        self.ReportTextCheckBox = QCheckBox(self.groupBox_5)
        self.ReportTextCheckBox.setObjectName("ReportTextCheckBox")

        self.gridLayout_26.addWidget(self.ReportTextCheckBox, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, -1)
        self.PictureWidthLabel = QLabel(self.groupBox_5)
        self.PictureWidthLabel.setObjectName("PictureWidthLabel")

        self.horizontalLayout_6.addWidget(self.PictureWidthLabel)

        self.PictureWidthDoubleSpinBox = QDoubleSpinBox(self.groupBox_5)
        self.PictureWidthDoubleSpinBox.setObjectName("PictureWidthDoubleSpinBox")
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
        self.HAtomsCheckBox.setObjectName("HAtomsCheckBox")

        self.gridLayout_26.addWidget(self.HAtomsCheckBox, 1, 0, 1, 2)

        self.UsePicometersCheckBox = QCheckBox(self.groupBox_5)
        self.UsePicometersCheckBox.setObjectName("UsePicometersCheckBox")

        self.gridLayout_26.addWidget(self.UsePicometersCheckBox, 2, 1, 1, 1)


        self.verticalLayout_35.addLayout(self.gridLayout_26)

        self.groupBox_6 = QGroupBox(self.groupBox_5)
        self.groupBox_6.setObjectName("groupBox_6")
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 3, 6, 6)
        self.docxTemplatesListWidget = QListWidget(self.groupBox_6)
        font = QFont()
        font.setItalic(True)
        __qlistwidgetitem = QListWidgetItem(self.docxTemplatesListWidget)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        __qlistwidgetitem.setFont(font)
        self.docxTemplatesListWidget.setObjectName("docxTemplatesListWidget")
        self.docxTemplatesListWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.docxTemplatesListWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.docxTemplatesListWidget.setSelectionRectVisible(False)

        self.verticalLayout_2.addWidget(self.docxTemplatesListWidget)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, 0, -1)
        self.AddNewTemplPushButton = QPushButton(self.groupBox_6)
        self.AddNewTemplPushButton.setObjectName("AddNewTemplPushButton")

        self.horizontalLayout_14.addWidget(self.AddNewTemplPushButton)

        self.RemoveTemplPushButton = QPushButton(self.groupBox_6)
        self.RemoveTemplPushButton.setObjectName("RemoveTemplPushButton")

        self.horizontalLayout_14.addWidget(self.RemoveTemplPushButton)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_13)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName("label")
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.verticalLayout_2.addWidget(self.label)


        self.verticalLayout_35.addWidget(self.groupBox_6)


        self.verticalLayout_16.addWidget(self.groupBox_5)

        self.TemplatesStackedWidget.addWidget(self.page_equipment)
        self.page_loops = QWidget()
        self.page_loops.setObjectName("page_loops")
        self.verticalLayout_18 = QVBoxLayout(self.page_loops)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.LoopsGroupBox = QGroupBox(self.page_loops)
        self.LoopsGroupBox.setObjectName("LoopsGroupBox")
        self.LoopsGroupBox.setFlat(True)
        self.verticalLayout_17 = QVBoxLayout(self.LoopsGroupBox)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(6, 6, 6, 6)
        self.LoopTemplatesListWidget = QListWidget(self.LoopsGroupBox)
        self.LoopTemplatesListWidget.setObjectName("LoopTemplatesListWidget")
        self.LoopTemplatesListWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.LoopTemplatesListWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.LoopTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_17.addWidget(self.LoopTemplatesListWidget)

        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.gridLayout_24.setContentsMargins(-1, 6, -1, 6)
        self.ExportAuthorPushButton = QPushButton(self.LoopsGroupBox)
        self.ExportAuthorPushButton.setObjectName("ExportAuthorPushButton")

        self.gridLayout_24.addWidget(self.ExportAuthorPushButton, 0, 1, 1, 1)

        self.ImportAuthorPushButton = QPushButton(self.LoopsGroupBox)
        self.ImportAuthorPushButton.setObjectName("ImportAuthorPushButton")

        self.gridLayout_24.addWidget(self.ImportAuthorPushButton, 0, 2, 1, 1)

        self.DeleteLoopAuthorTemplateButton = QPushButton(self.LoopsGroupBox)
        self.DeleteLoopAuthorTemplateButton.setObjectName("DeleteLoopAuthorTemplateButton")

        self.gridLayout_24.addWidget(self.DeleteLoopAuthorTemplateButton, 0, 3, 1, 1)


        self.verticalLayout_17.addLayout(self.gridLayout_24)

        self.line_2 = QFrame(self.LoopsGroupBox)
        self.line_2.setObjectName("line_2")
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
        self.CifDataItemsFrame.setObjectName("CifDataItemsFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(7)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.CifDataItemsFrame.sizePolicy().hasHeightForWidth())
        self.CifDataItemsFrame.setSizePolicy(sizePolicy6)
        self.gridLayout_6 = QGridLayout(self.CifDataItemsFrame)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.setContentsMargins(3, 9, 6, 0)
        self.spacegroupLabel = QLabel(self.CifDataItemsFrame)
        self.spacegroupLabel.setObjectName("spacegroupLabel")

        self.gridLayout_6.addWidget(self.spacegroupLabel, 0, 4, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_10, 0, 9, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_12, 0, 6, 1, 1)

        self.datanameComboBox = ComboBoxWithContextMenu(self.CifDataItemsFrame)
        self.datanameComboBox.setObjectName("datanameComboBox")
        self.datanameComboBox.setEditable(True)
        self.datanameComboBox.setMaxVisibleItems(20)
        self.datanameComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)
        self.datanameComboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.datanameComboBox.setMinimumContentsLength(20)
        self.datanameComboBox.setFrame(True)

        self.gridLayout_6.addWidget(self.datanameComboBox, 0, 1, 1, 1)

        self.appendCifPushButton = QPushButton(self.CifDataItemsFrame)
        self.appendCifPushButton.setObjectName("appendCifPushButton")

        self.gridLayout_6.addWidget(self.appendCifPushButton, 0, 2, 1, 1)

        self.CCDCNumLabel = QLabel(self.CifDataItemsFrame)
        self.CCDCNumLabel.setObjectName("CCDCNumLabel")

        self.gridLayout_6.addWidget(self.CCDCNumLabel, 0, 7, 1, 1)

        self.CCDCNumLineEdit = QTextEdit(self.CifDataItemsFrame)
        self.CCDCNumLineEdit.setObjectName("CCDCNumLineEdit")
        self.CCDCNumLineEdit.viewport().setProperty("cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.CCDCNumLineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CCDCNumLineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CCDCNumLineEdit.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.CCDCNumLineEdit.setTabChangesFocus(True)
        self.CCDCNumLineEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.CCDCNumLineEdit.setReadOnly(False)
        self.CCDCNumLineEdit.setAcceptRichText(False)

        self.gridLayout_6.addWidget(self.CCDCNumLineEdit, 0, 8, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_11, 0, 3, 1, 1)

        self.HelpPushButton = QPushButton(self.CifDataItemsFrame)
        self.HelpPushButton.setObjectName("HelpPushButton")

        self.gridLayout_6.addWidget(self.HelpPushButton, 0, 12, 1, 1)

        self.SumFormMainLineEdit = QTextEdit(self.CifDataItemsFrame)
        self.SumFormMainLineEdit.setObjectName("SumFormMainLineEdit")
        self.SumFormMainLineEdit.viewport().setProperty("cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.SumFormMainLineEdit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.SumFormMainLineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SumFormMainLineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SumFormMainLineEdit.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.SumFormMainLineEdit.setTabChangesFocus(True)
        self.SumFormMainLineEdit.setUndoRedoEnabled(False)
        self.SumFormMainLineEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.SumFormMainLineEdit.setReadOnly(True)

        self.gridLayout_6.addWidget(self.SumFormMainLineEdit, 0, 11, 1, 1)

        self.datanameLabel = QLabel(self.CifDataItemsFrame)
        self.datanameLabel.setObjectName("datanameLabel")

        self.gridLayout_6.addWidget(self.datanameLabel, 0, 0, 1, 1)

        self.SumFormMainLabel = QLabel(self.CifDataItemsFrame)
        self.SumFormMainLabel.setObjectName("SumFormMainLabel")

        self.gridLayout_6.addWidget(self.SumFormMainLabel, 0, 10, 1, 1)

        self.Spacegroup_top_LineEdit = QTextEdit(self.CifDataItemsFrame)
        self.Spacegroup_top_LineEdit.setObjectName("Spacegroup_top_LineEdit")
        self.Spacegroup_top_LineEdit.viewport().setProperty("cursor", QCursor(Qt.CursorShape.IBeamCursor))
        self.Spacegroup_top_LineEdit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.Spacegroup_top_LineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Spacegroup_top_LineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Spacegroup_top_LineEdit.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.Spacegroup_top_LineEdit.setTabChangesFocus(True)
        self.Spacegroup_top_LineEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.Spacegroup_top_LineEdit.setReadOnly(True)
        self.Spacegroup_top_LineEdit.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_6.addWidget(self.Spacegroup_top_LineEdit, 0, 5, 1, 1)

        self.MainStackedWidget = MyMainStackedWidget(self.CifDataItemsFrame)
        self.MainStackedWidget.setObjectName("MainStackedWidget")
        self.page_MainTable = QWidget()
        self.page_MainTable.setObjectName("page_MainTable")
        self.verticalLayout = QVBoxLayout(self.page_MainTable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.cif_main_table.setObjectName("cif_main_table")
        self.cif_main_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.cif_main_table.setAutoScroll(False)
        self.cif_main_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.cif_main_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cif_main_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cif_main_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cif_main_table.setShowGrid(True)
        self.cif_main_table.setGridStyle(Qt.PenStyle.SolidLine)
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
        self.ButtonsHorizontalLayout.setObjectName("ButtonsHorizontalLayout")
        self.groupBox = QGroupBox(self.page_MainTable)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(9)
        self.gridLayout_7.setVerticalSpacing(6)
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.SaveCifButton = QPushButton(self.groupBox)
        self.SaveCifButton.setObjectName("SaveCifButton")

        self.gridLayout_7.addWidget(self.SaveCifButton, 0, 0, 1, 1)

        self.ExploreDirButton = QPushButton(self.groupBox)
        self.ExploreDirButton.setObjectName("ExploreDirButton")

        self.gridLayout_7.addWidget(self.ExploreDirButton, 1, 0, 1, 1)

        self.DetailsPushButton = QPushButton(self.groupBox)
        self.DetailsPushButton.setObjectName("DetailsPushButton")

        self.gridLayout_7.addWidget(self.DetailsPushButton, 0, 1, 1, 1)

        self.AuthorEditPushButton = QPushButton(self.groupBox)
        self.AuthorEditPushButton.setObjectName("AuthorEditPushButton")

        self.gridLayout_7.addWidget(self.AuthorEditPushButton, 1, 1, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox)

        self.groupBox_checkcif = QGroupBox(self.page_MainTable)
        self.groupBox_checkcif.setObjectName("groupBox_checkcif")
        self.gridLayout_15 = QGridLayout(self.groupBox_checkcif)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(9)
        self.gridLayout_15.setVerticalSpacing(6)
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.LoopsPushButton = QPushButton(self.groupBox_checkcif)
        self.LoopsPushButton.setObjectName("LoopsPushButton")

        self.gridLayout_15.addWidget(self.LoopsPushButton, 1, 0, 1, 1)

        self.ReportPicPushButton = QPushButton(self.groupBox_checkcif)
        self.ReportPicPushButton.setObjectName("ReportPicPushButton")

        self.gridLayout_15.addWidget(self.ReportPicPushButton, 0, 1, 1, 1)

        self.SaveFullReportButton = QPushButton(self.groupBox_checkcif)
        self.SaveFullReportButton.setObjectName("SaveFullReportButton")

        self.gridLayout_15.addWidget(self.SaveFullReportButton, 1, 1, 1, 1)

        self.CheckcifStartButton = QPushButton(self.groupBox_checkcif)
        self.CheckcifStartButton.setObjectName("CheckcifStartButton")

        self.gridLayout_15.addWidget(self.CheckcifStartButton, 0, 0, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox_checkcif)

        self.groupBox_tables = QGroupBox(self.page_MainTable)
        self.groupBox_tables.setObjectName("groupBox_tables")
        self.gridLayout = QGridLayout(self.groupBox_tables)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.CODpushButton = QPushButton(self.groupBox_tables)
        self.CODpushButton.setObjectName("CODpushButton")

        self.gridLayout.addWidget(self.CODpushButton, 0, 0, 1, 1)

        self.ShredCifButton = QPushButton(self.groupBox_tables)
        self.ShredCifButton.setObjectName("ShredCifButton")

        self.gridLayout.addWidget(self.ShredCifButton, 0, 1, 1, 1)

        self.CCDCpushButton = QPushButton(self.groupBox_tables)
        self.CCDCpushButton.setObjectName("CCDCpushButton")

        self.gridLayout.addWidget(self.CCDCpushButton, 1, 0, 1, 1)

        self.OptionsPushButton = QPushButton(self.groupBox_tables)
        self.OptionsPushButton.setObjectName("OptionsPushButton")

        self.gridLayout.addWidget(self.OptionsPushButton, 1, 1, 1, 1)


        self.ButtonsHorizontalLayout.addWidget(self.groupBox_tables)


        self.verticalLayout.addLayout(self.ButtonsHorizontalLayout)

        self.MainStackedWidget.addWidget(self.page_MainTable)
        self.page_FinalCif = QWidget()
        self.page_FinalCif.setObjectName("page_FinalCif")
        self.verticalLayout_3 = QVBoxLayout(self.page_FinalCif)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.FinalCifFilePlainTextEdit = QCodeEditor(self.page_FinalCif)
        self.FinalCifFilePlainTextEdit.setObjectName("FinalCifFilePlainTextEdit")
        self.FinalCifFilePlainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.FinalCifFilePlainTextEdit)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.BackPushButton = QPushButton(self.page_FinalCif)
        self.BackPushButton.setObjectName("BackPushButton")
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
        self.page_molinfo.setObjectName("page_molinfo")
        self.gridLayout_3 = QGridLayout(self.page_molinfo)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.molGroupBox = QGroupBox(self.page_molinfo)
        self.molGroupBox.setObjectName("molGroupBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(55)
        sizePolicy7.setVerticalStretch(80)
        sizePolicy7.setHeightForWidth(self.molGroupBox.sizePolicy().hasHeightForWidth())
        self.molGroupBox.setSizePolicy(sizePolicy7)
        self.verticalLayout_8 = QVBoxLayout(self.molGroupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(6, 3, 6, 8)
        self.render_widget = MoleculeWidget(self.molGroupBox)
        self.render_widget.setObjectName("render_widget")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.render_widget.sizePolicy().hasHeightForWidth())
        self.render_widget.setSizePolicy(sizePolicy8)

        self.verticalLayout_8.addWidget(self.render_widget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.growCheckBox = QCheckBox(self.molGroupBox)
        self.growCheckBox.setObjectName("growCheckBox")
        self.growCheckBox.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_7.addWidget(self.growCheckBox)

        self.labelsCheckBox = QCheckBox(self.molGroupBox)
        self.labelsCheckBox.setObjectName("labelsCheckBox")
        self.labelsCheckBox.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_7.addWidget(self.labelsCheckBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.drawImagePushButton = QPushButton(self.molGroupBox)
        self.drawImagePushButton.setObjectName("drawImagePushButton")

        self.horizontalLayout_7.addWidget(self.drawImagePushButton)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_23)


        self.verticalLayout_8.addLayout(self.horizontalLayout_7)


        self.gridLayout_3.addWidget(self.molGroupBox, 0, 0, 1, 1)

        self.groupBox_9 = QGroupBox(self.page_molinfo)
        self.groupBox_9.setObjectName("groupBox_9")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(45)
        sizePolicy9.setVerticalStretch(80)
        sizePolicy9.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy9)
        self.verticalLayout_41 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.shelx_TextEdit = QPlainTextEdit(self.groupBox_9)
        self.shelx_TextEdit.setObjectName("shelx_TextEdit")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(90)
        sizePolicy10.setHeightForWidth(self.shelx_TextEdit.sizePolicy().hasHeightForWidth())
        self.shelx_TextEdit.setSizePolicy(sizePolicy10)
        font1 = QFont()
        font1.setFamilies(["Courier New"])
        self.shelx_TextEdit.setFont(font1)
        self.shelx_TextEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.shelx_TextEdit.setFrameShadow(QFrame.Shadow.Plain)
        self.shelx_TextEdit.setUndoRedoEnabled(False)
        self.shelx_TextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.shelx_TextEdit.setReadOnly(True)

        self.verticalLayout_41.addWidget(self.shelx_TextEdit)

        self.shelx_warn_TextEdit = QPlainTextEdit(self.groupBox_9)
        self.shelx_warn_TextEdit.setObjectName("shelx_warn_TextEdit")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(10)
        sizePolicy11.setHeightForWidth(self.shelx_warn_TextEdit.sizePolicy().hasHeightForWidth())
        self.shelx_warn_TextEdit.setSizePolicy(sizePolicy11)
        font2 = QFont()
        font2.setFamilies(["Courier New"])
        font2.setBold(True)
        self.shelx_warn_TextEdit.setFont(font2)
        self.shelx_warn_TextEdit.setUndoRedoEnabled(False)
        self.shelx_warn_TextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.shelx_warn_TextEdit.setReadOnly(True)

        self.verticalLayout_41.addWidget(self.shelx_warn_TextEdit)


        self.gridLayout_3.addWidget(self.groupBox_9, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.page_molinfo)
        self.groupBox_3.setObjectName("groupBox_3")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(20)
        sizePolicy12.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy12)
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.zLabel = QLabel(self.groupBox_3)
        self.zLabel.setObjectName("zLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.zLabel)

        self.zLineEdit = QLineEdit(self.groupBox_3)
        self.zLineEdit.setObjectName("zLineEdit")
        self.zLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.zLineEdit)

        self.temperatureLabel = QLabel(self.groupBox_3)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.temperatureLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.temperatureLabel)

        self.temperatureLineEdit = QLineEdit(self.groupBox_3)
        self.temperatureLineEdit.setObjectName("temperatureLineEdit")
        self.temperatureLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.temperatureLineEdit)

        self.wR2Label = QLabel(self.groupBox_3)
        self.wR2Label.setObjectName("wR2Label")
        font3 = QFont()
        font3.setBold(False)
        font3.setItalic(False)
        self.wR2Label.setFont(font3)
        self.wR2Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.wR2Label)

        self.wR2LineEdit = QLineEdit(self.groupBox_3)
        self.wR2LineEdit.setObjectName("wR2LineEdit")
        self.wR2LineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.wR2LineEdit)

        self.r1Label = QLabel(self.groupBox_3)
        self.r1Label.setObjectName("r1Label")
        self.r1Label.setFont(font3)
        self.r1Label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.r1Label)

        self.r1LineEdit = QLineEdit(self.groupBox_3)
        self.r1LineEdit.setObjectName("r1LineEdit")
        self.r1LineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.r1LineEdit)

        self.goofLabel = QLabel(self.groupBox_3)
        self.goofLabel.setObjectName("goofLabel")
        self.goofLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.goofLabel)

        self.goofLineEdit = QLineEdit(self.groupBox_3)
        self.goofLineEdit.setObjectName("goofLineEdit")
        self.goofLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.goofLineEdit)

        self.maxShiftLabel = QLabel(self.groupBox_3)
        self.maxShiftLabel.setObjectName("maxShiftLabel")
        self.maxShiftLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.maxShiftLabel)

        self.maxShiftLineEdit = QLineEdit(self.groupBox_3)
        self.maxShiftLineEdit.setObjectName("maxShiftLineEdit")
        self.maxShiftLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.FieldRole, self.maxShiftLineEdit)

        self.completeLabel = QLabel(self.groupBox_3)
        self.completeLabel.setObjectName("completeLabel")
        font4 = QFont()
        font4.setBold(False)
        self.completeLabel.setFont(font4)
        self.completeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.LabelRole, self.completeLabel)

        self.completeLineEdit = QLineEdit(self.groupBox_3)
        self.completeLineEdit.setObjectName("completeLineEdit")
        self.completeLineEdit.setReadOnly(True)

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.FieldRole, self.completeLineEdit)


        self.gridLayout_4.addLayout(self.formLayout_3, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_24, 0, 7, 1, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.reflTotalLabel = QLabel(self.groupBox_3)
        self.reflTotalLabel.setObjectName("reflTotalLabel")
        self.reflTotalLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.reflTotalLabel)

        self.reflTotalLineEdit = QLineEdit(self.groupBox_3)
        self.reflTotalLineEdit.setObjectName("reflTotalLineEdit")
        self.reflTotalLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.reflTotalLineEdit)

        self.refl2sigmaLabel = QLabel(self.groupBox_3)
        self.refl2sigmaLabel.setObjectName("refl2sigmaLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.refl2sigmaLabel)

        self.refl2sigmaLineEdit = QLineEdit(self.groupBox_3)
        self.refl2sigmaLineEdit.setObjectName("refl2sigmaLineEdit")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.refl2sigmaLineEdit)

        self.uniqReflLabel = QLabel(self.groupBox_3)
        self.uniqReflLabel.setObjectName("uniqReflLabel")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.uniqReflLabel)

        self.uniqReflLineEdit = QLineEdit(self.groupBox_3)
        self.uniqReflLineEdit.setObjectName("uniqReflLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.uniqReflLineEdit)

        self.numParametersLabel = QLabel(self.groupBox_3)
        self.numParametersLabel.setObjectName("numParametersLabel")
        self.numParametersLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.numParametersLabel)

        self.numParametersLineEdit = QLineEdit(self.groupBox_3)
        self.numParametersLineEdit.setObjectName("numParametersLineEdit")
        self.numParametersLineEdit.setMinimumSize(QSize(0, 0))
        self.numParametersLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.numParametersLineEdit)

        self.dataReflnsLabel = QLabel(self.groupBox_3)
        self.dataReflnsLabel.setObjectName("dataReflnsLabel")
        self.dataReflnsLabel.setFont(font4)
        self.dataReflnsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.dataReflnsLabel)

        self.dataReflnsLineEdit = QLineEdit(self.groupBox_3)
        self.dataReflnsLineEdit.setObjectName("dataReflnsLineEdit")
        self.dataReflnsLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.dataReflnsLineEdit)

        self.wavelengthLabel = QLabel(self.groupBox_3)
        self.wavelengthLabel.setObjectName("wavelengthLabel")
        self.wavelengthLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.wavelengthLabel)

        self.wavelengthLineEdit = QLineEdit(self.groupBox_3)
        self.wavelengthLineEdit.setObjectName("wavelengthLineEdit")
        self.wavelengthLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.wavelengthLineEdit)

        self.flackXLabel = QLabel(self.groupBox_3)
        self.flackXLabel.setObjectName("flackXLabel")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.LabelRole, self.flackXLabel)

        self.flackXLineEdit = QLineEdit(self.groupBox_3)
        self.flackXLineEdit.setObjectName("flackXLineEdit")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.FieldRole, self.flackXLineEdit)


        self.gridLayout_4.addLayout(self.formLayout_2, 0, 6, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName("groupBox_4")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy13)
        self.gridLayout_9 = QGridLayout(self.groupBox_4)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.cellField = QLabel(self.groupBox_4)
        self.cellField.setObjectName("cellField")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.cellField.sizePolicy().hasHeightForWidth())
        self.cellField.setSizePolicy(sizePolicy14)
        self.cellField.setMinimumSize(QSize(0, 75))
        self.cellField.setBaseSize(QSize(0, 75))
        self.cellField.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.cellField.setAutoFillBackground(False)
        self.cellField.setStyleSheet("border-color: rgb(53, 53, 53);")
        self.cellField.setFrameShape(QFrame.Shape.NoFrame)
        self.cellField.setFrameShadow(QFrame.Shadow.Plain)
        self.cellField.setTextFormat(Qt.TextFormat.RichText)
        self.cellField.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.gridLayout_9.addWidget(self.cellField, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 0, 5, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.peakLabel = QLabel(self.groupBox_3)
        self.peakLabel.setObjectName("peakLabel")
        self.peakLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.peakLabel)

        self.peakLineEdit = QLineEdit(self.groupBox_3)
        self.peakLineEdit.setObjectName("peakLineEdit")
        self.peakLineEdit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.peakLineEdit)

        self.rintLabel = QLabel(self.groupBox_3)
        self.rintLabel.setObjectName("rintLabel")
        self.rintLabel.setFont(font4)
        self.rintLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.rintLabel)

        self.rintLineEdit = QLineEdit(self.groupBox_3)
        self.rintLineEdit.setObjectName("rintLineEdit")
        self.rintLineEdit.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rintLineEdit)

        self.rsigmaLabel = QLabel(self.groupBox_3)
        self.rsigmaLabel.setObjectName("rsigmaLabel")
        self.rsigmaLabel.setFont(font4)
        self.rsigmaLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.rsigmaLabel)

        self.rsigmaLineEdit = QLineEdit(self.groupBox_3)
        self.rsigmaLineEdit.setObjectName("rsigmaLineEdit")
        self.rsigmaLineEdit.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.rsigmaLineEdit)

        self.numRestraintsLabel = QLabel(self.groupBox_3)
        self.numRestraintsLabel.setObjectName("numRestraintsLabel")
        self.numRestraintsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.numRestraintsLabel)

        self.numRestraintsLineEdit = QLineEdit(self.groupBox_3)
        self.numRestraintsLineEdit.setObjectName("numRestraintsLineEdit")
        self.numRestraintsLineEdit.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.numRestraintsLineEdit)

        self.thetaMaxLabel = QLabel(self.groupBox_3)
        self.thetaMaxLabel.setObjectName("thetaMaxLabel")
        self.thetaMaxLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.thetaMaxLabel)

        self.thetaMaxLineEdit = QLineEdit(self.groupBox_3)
        self.thetaMaxLineEdit.setObjectName("thetaMaxLineEdit")
        self.thetaMaxLineEdit.setReadOnly(True)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.thetaMaxLineEdit)

        self.thetaFullLabel = QLabel(self.groupBox_3)
        self.thetaFullLabel.setObjectName("thetaFullLabel")
        self.thetaFullLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.thetaFullLabel)

        self.thetaFullLineEdit = QLineEdit(self.groupBox_3)
        self.thetaFullLineEdit.setObjectName("thetaFullLineEdit")
        self.thetaFullLineEdit.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.thetaFullLineEdit)

        self.dLabel = QLabel(self.groupBox_3)
        self.dLabel.setObjectName("dLabel")
        self.dLabel.setFont(font4)
        self.dLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.dLabel)

        self.dLineEdit = QLineEdit(self.groupBox_3)
        self.dLineEdit.setObjectName("dLineEdit")
        self.dLineEdit.setReadOnly(True)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.dLineEdit)


        self.gridLayout_4.addLayout(self.formLayout, 0, 4, 1, 1)

        self.BackpushButtonDetails = QPushButton(self.groupBox_3)
        self.BackpushButtonDetails.setObjectName("BackpushButtonDetails")
        sizePolicy5.setHeightForWidth(self.BackpushButtonDetails.sizePolicy().hasHeightForWidth())
        self.BackpushButtonDetails.setSizePolicy(sizePolicy5)

        self.gridLayout_4.addWidget(self.BackpushButtonDetails, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_22, 0, 1, 1, 1)

        self.SourcesPushButton = QPushButton(self.groupBox_3)
        self.SourcesPushButton.setObjectName("SourcesPushButton")
        sizePolicy5.setHeightForWidth(self.SourcesPushButton.sizePolicy().hasHeightForWidth())
        self.SourcesPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_4.addWidget(self.SourcesPushButton, 2, 7, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_3, 1, 0, 1, 3)

        self.MainStackedWidget.addWidget(self.page_molinfo)
        self.page_Sources = QWidget()
        self.page_Sources.setObjectName("page_Sources")
        self.gridLayout_11 = QGridLayout(self.page_Sources)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.horizontalSpacer_9 = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_9, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.page_Sources)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")

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
        self.SourcesTableWidget.setObjectName("SourcesTableWidget")
        self.SourcesTableWidget.setWordWrap(False)
        self.SourcesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.SourcesTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.SourcesTableWidget)


        self.gridLayout_11.addWidget(self.groupBox_2, 0, 1, 1, 3)

        self.BackSourcesPushButton = QPushButton(self.page_Sources)
        self.BackSourcesPushButton.setObjectName("BackSourcesPushButton")
        sizePolicy5.setHeightForWidth(self.BackSourcesPushButton.sizePolicy().hasHeightForWidth())
        self.BackSourcesPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_11.addWidget(self.BackSourcesPushButton, 1, 2, 1, 2)

        self.MainStackedWidget.addWidget(self.page_Sources)
        self.page_options = QWidget()
        self.page_options.setObjectName("page_options")
        self.gridLayout_12 = QGridLayout(self.page_options)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.BackFromOptionspPushButton = QPushButton(self.page_options)
        self.BackFromOptionspPushButton.setObjectName("BackFromOptionspPushButton")
        sizePolicy5.setHeightForWidth(self.BackFromOptionspPushButton.sizePolicy().hasHeightForWidth())
        self.BackFromOptionspPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_12.addWidget(self.BackFromOptionspPushButton, 7, 0, 1, 1)

        self.groupBox_COD = QGroupBox(self.page_options)
        self.groupBox_COD.setObjectName("groupBox_COD")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy15.setHorizontalStretch(50)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.groupBox_COD.sizePolicy().hasHeightForWidth())
        self.groupBox_COD.setSizePolicy(sizePolicy15)
        self.formLayout_6 = QFormLayout(self.groupBox_COD)
        self.formLayout_6.setObjectName("formLayout_6")
        self.formLayout_6.setContentsMargins(-1, 12, -1, -1)
        self.label_7 = QLabel(self.groupBox_COD)
        self.label_7.setObjectName("label_7")

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.label_7)

        self.CODURLTextedit = QLineEdit(self.groupBox_COD)
        self.CODURLTextedit.setObjectName("CODURLTextedit")
        sizePolicy3.setHeightForWidth(self.CODURLTextedit.sizePolicy().hasHeightForWidth())
        self.CODURLTextedit.setSizePolicy(sizePolicy3)
        self.CODURLTextedit.setMinimumSize(QSize(300, 0))

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.CODURLTextedit)


        self.gridLayout_12.addWidget(self.groupBox_COD, 2, 2, 1, 1)

        self.groupBox_71 = QGroupBox(self.page_options)
        self.groupBox_71.setObjectName("groupBox_71")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy16.setHorizontalStretch(20)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.groupBox_71.sizePolicy().hasHeightForWidth())
        self.groupBox_71.setSizePolicy(sizePolicy16)
        self.formLayout_4 = QFormLayout(self.groupBox_71)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_4 = QLabel(self.groupBox_71)
        self.label_4.setObjectName("label_4")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.label_4)

        self.CheckCIFServerURLTextedit = QLineEdit(self.groupBox_71)
        self.CheckCIFServerURLTextedit.setObjectName("CheckCIFServerURLTextedit")
        sizePolicy3.setHeightForWidth(self.CheckCIFServerURLTextedit.sizePolicy().hasHeightForWidth())
        self.CheckCIFServerURLTextedit.setSizePolicy(sizePolicy3)
        self.CheckCIFServerURLTextedit.setMinimumSize(QSize(300, 0))

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.CheckCIFServerURLTextedit)


        self.gridLayout_12.addWidget(self.groupBox_71, 0, 2, 1, 1)

        self.groupBox_8 = QGroupBox(self.page_options)
        self.groupBox_8.setObjectName("groupBox_8")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy17.setHorizontalStretch(15)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy17)
        self.verticalLayout_34 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.ExportAllTemplatesPushButton = QPushButton(self.groupBox_8)
        self.ExportAllTemplatesPushButton.setObjectName("ExportAllTemplatesPushButton")

        self.verticalLayout_34.addWidget(self.ExportAllTemplatesPushButton, 0, Qt.AlignmentFlag.AlignLeft)

        self.label_18 = QLabel(self.groupBox_8)
        self.label_18.setObjectName("label_18")

        self.verticalLayout_34.addWidget(self.label_18)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_34.addItem(self.verticalSpacer)

        self.ImportAllTemplatesPushButton = QPushButton(self.groupBox_8)
        self.ImportAllTemplatesPushButton.setObjectName("ImportAllTemplatesPushButton")

        self.verticalLayout_34.addWidget(self.ImportAllTemplatesPushButton, 0, Qt.AlignmentFlag.AlignLeft)

        self.label_17 = QLabel(self.groupBox_8)
        self.label_17.setObjectName("label_17")

        self.verticalLayout_34.addWidget(self.label_17)


        self.gridLayout_12.addWidget(self.groupBox_8, 0, 1, 1, 1)

        self.groupBox_10 = QGroupBox(self.page_options)
        self.groupBox_10.setObjectName("groupBox_10")
        sizePolicy17.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy17)
        self.verticalLayout_37 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.trackChangesCifCheckBox = QCheckBox(self.groupBox_10)
        self.trackChangesCifCheckBox.setObjectName("trackChangesCifCheckBox")

        self.verticalLayout_37.addWidget(self.trackChangesCifCheckBox)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.textSizeSpinBox = QSpinBox(self.groupBox_10)
        self.textSizeSpinBox.setObjectName("textSizeSpinBox")

        self.horizontalLayout_15.addWidget(self.textSizeSpinBox)

        self.label_26 = QLabel(self.groupBox_10)
        self.label_26.setObjectName("label_26")

        self.horizontalLayout_15.addWidget(self.label_26)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_6)


        self.verticalLayout_37.addLayout(self.horizontalLayout_15)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_37.addItem(self.verticalSpacer_14)


        self.gridLayout_12.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.cifOrderWidget = CifOrder(self.page_options)
        self.cifOrderWidget.setObjectName("cifOrderWidget")
        sizePolicy18 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy18.setHorizontalStretch(30)
        sizePolicy18.setVerticalStretch(2)
        sizePolicy18.setHeightForWidth(self.cifOrderWidget.sizePolicy().hasHeightForWidth())
        self.cifOrderWidget.setSizePolicy(sizePolicy18)

        self.gridLayout_12.addWidget(self.cifOrderWidget, 2, 0, 5, 2)

        self.PropertiesGroupBox = QGroupBox(self.page_options)
        self.PropertiesGroupBox.setObjectName("PropertiesGroupBox")
        sizePolicy19 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy19.setHorizontalStretch(50)
        sizePolicy19.setVerticalStretch(2)
        sizePolicy19.setHeightForWidth(self.PropertiesGroupBox.sizePolicy().hasHeightForWidth())
        self.PropertiesGroupBox.setSizePolicy(sizePolicy19)
        self.verticalLayout_6 = QVBoxLayout(self.PropertiesGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.PropertiesTemplatesStackedWidget = QStackedWidget(self.PropertiesGroupBox)
        self.PropertiesTemplatesStackedWidget.setObjectName("PropertiesTemplatesStackedWidget")
        self.PropertiesSelectPage = QWidget()
        self.PropertiesSelectPage.setObjectName("PropertiesSelectPage")
        self.verticalLayout_20 = QVBoxLayout(self.PropertiesSelectPage)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 3, 0, 3)
        self.PropertiesTemplatesListWidget = QListWidget(self.PropertiesSelectPage)
        self.PropertiesTemplatesListWidget.setObjectName("PropertiesTemplatesListWidget")
        self.PropertiesTemplatesListWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.PropertiesTemplatesListWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_20.addWidget(self.PropertiesTemplatesListWidget)

        self.horizontalLayout_Buttons2 = QHBoxLayout()
        self.horizontalLayout_Buttons2.setObjectName("horizontalLayout_Buttons2")
        self.EditPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.EditPropertyTemplateButton.setObjectName("EditPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.EditPropertyTemplateButton)

        self.NewPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.NewPropertyTemplateButton.setObjectName("NewPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.NewPropertyTemplateButton)

        self.ImportPropertyTemplateButton = QPushButton(self.PropertiesSelectPage)
        self.ImportPropertyTemplateButton.setObjectName("ImportPropertyTemplateButton")

        self.horizontalLayout_Buttons2.addWidget(self.ImportPropertyTemplateButton)


        self.verticalLayout_20.addLayout(self.horizontalLayout_Buttons2)

        self.PropertiesTemplatesStackedWidget.addWidget(self.PropertiesSelectPage)
        self.PropertiesEditPage = QWidget()
        self.PropertiesEditPage.setObjectName("PropertiesEditPage")
        self.verticalLayout_22 = QVBoxLayout(self.PropertiesEditPage)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 3, 0, 3)
        self.KeywordVerticalLayout = QVBoxLayout()
        self.KeywordVerticalLayout.setObjectName("KeywordVerticalLayout")
        self.cifKeywordLB = QLabel(self.PropertiesEditPage)
        self.cifKeywordLB.setObjectName("cifKeywordLB")

        self.KeywordVerticalLayout.addWidget(self.cifKeywordLB)

        self.cifKeywordLineEdit = QLineEdit(self.PropertiesEditPage)
        self.cifKeywordLineEdit.setObjectName("cifKeywordLineEdit")

        self.KeywordVerticalLayout.addWidget(self.cifKeywordLineEdit)


        self.verticalLayout_22.addLayout(self.KeywordVerticalLayout)

        self.PropertiesEditTableWidget = MyPropTableWidget(self.PropertiesEditPage)
        if (self.PropertiesEditTableWidget.columnCount() < 1):
            self.PropertiesEditTableWidget.setColumnCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.PropertiesEditTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        if (self.PropertiesEditTableWidget.rowCount() < 1):
            self.PropertiesEditTableWidget.setRowCount(1)
        self.PropertiesEditTableWidget.setObjectName("PropertiesEditTableWidget")
        self.PropertiesEditTableWidget.setAutoScroll(False)
        self.PropertiesEditTableWidget.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.PropertiesEditTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.PropertiesEditTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.PropertiesEditTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.PropertiesEditTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.PropertiesEditTableWidget.setRowCount(1)
        self.PropertiesEditTableWidget.horizontalHeader().setVisible(False)
        self.PropertiesEditTableWidget.horizontalHeader().setMinimumSectionSize(90)
        self.PropertiesEditTableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.PropertiesEditTableWidget.horizontalHeader().setStretchLastSection(True)
        self.PropertiesEditTableWidget.verticalHeader().setVisible(False)
        self.PropertiesEditTableWidget.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout_22.addWidget(self.PropertiesEditTableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DeletePropertiesButton = QPushButton(self.PropertiesEditPage)
        self.DeletePropertiesButton.setObjectName("DeletePropertiesButton")
        sizePolicy20 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy20.setHorizontalStretch(1)
        sizePolicy20.setVerticalStretch(0)
        sizePolicy20.setHeightForWidth(self.DeletePropertiesButton.sizePolicy().hasHeightForWidth())
        self.DeletePropertiesButton.setSizePolicy(sizePolicy20)

        self.horizontalLayout.addWidget(self.DeletePropertiesButton)

        self.SavePropertiesButton = QPushButton(self.PropertiesEditPage)
        self.SavePropertiesButton.setObjectName("SavePropertiesButton")
        sizePolicy21 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy21.setHorizontalStretch(1)
        sizePolicy21.setVerticalStretch(0)
        sizePolicy21.setHeightForWidth(self.SavePropertiesButton.sizePolicy().hasHeightForWidth())
        self.SavePropertiesButton.setSizePolicy(sizePolicy21)

        self.horizontalLayout.addWidget(self.SavePropertiesButton)

        self.CancelPropertiesButton = QPushButton(self.PropertiesEditPage)
        self.CancelPropertiesButton.setObjectName("CancelPropertiesButton")
        sizePolicy20.setHeightForWidth(self.CancelPropertiesButton.sizePolicy().hasHeightForWidth())
        self.CancelPropertiesButton.setSizePolicy(sizePolicy20)

        self.horizontalLayout.addWidget(self.CancelPropertiesButton)

        self.ExportPropertyButton = QPushButton(self.PropertiesEditPage)
        self.ExportPropertyButton.setObjectName("ExportPropertyButton")

        self.horizontalLayout.addWidget(self.ExportPropertyButton)


        self.verticalLayout_22.addLayout(self.horizontalLayout)

        self.PropertiesTemplatesStackedWidget.addWidget(self.PropertiesEditPage)

        self.verticalLayout_6.addWidget(self.PropertiesTemplatesStackedWidget)


        self.gridLayout_12.addWidget(self.PropertiesGroupBox, 3, 2, 4, 1)

        self.MainStackedWidget.addWidget(self.page_options)
        self.page_Loops = QWidget()
        self.page_Loops.setObjectName("page_Loops")
        self.verticalLayout_9 = QVBoxLayout(self.page_Loops)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, 12, -1, -1)
        self.LoopsTabWidget = QTabWidget(self.page_Loops)
        self.LoopsTabWidget.setObjectName("LoopsTabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalSpacer_16 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.verticalSpacer_16, 0, 1, 1, 1)

        self.authorEditTabWidget = QTabWidget(self.tab_2)
        self.authorEditTabWidget.setObjectName("authorEditTabWidget")
        sizePolicy22 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy22.setHorizontalStretch(45)
        sizePolicy22.setVerticalStretch(0)
        sizePolicy22.setHeightForWidth(self.authorEditTabWidget.sizePolicy().hasHeightForWidth())
        self.authorEditTabWidget.setSizePolicy(sizePolicy22)
        self.page_publication = QWidget()
        self.page_publication.setObjectName("page_publication")
        self.verticalLayout_23 = QVBoxLayout(self.page_publication)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.label_20 = QLabel(self.page_publication)
        self.label_20.setObjectName("label_20")

        self.verticalLayout_24.addWidget(self.label_20)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_34 = QLabel(self.page_publication)
        self.label_34.setObjectName("label_34")
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_34, 5, 0, 1, 1)

        self.footnote_label = QLabel(self.page_publication)
        self.footnote_label.setObjectName("footnote_label")
        self.footnote_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.footnote_label, 7, 0, 1, 1)

        self.label_21 = QLabel(self.page_publication)
        self.label_21.setObjectName("label_21")
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 2, 0, 1, 1)

        self.label_28 = QLabel(self.page_publication)
        self.label_28.setObjectName("label_28")
        self.label_28.setScaledContents(False)

        self.gridLayout_5.addWidget(self.label_28, 2, 2, 1, 1)

        self.PhoneLineEdit = QLineEdit(self.page_publication)
        self.PhoneLineEdit.setObjectName("PhoneLineEdit")

        self.gridLayout_5.addWidget(self.PhoneLineEdit, 4, 1, 1, 1)

        self.ContactAuthorCheckBox = QCheckBox(self.page_publication)
        self.ContactAuthorCheckBox.setObjectName("ContactAuthorCheckBox")

        self.gridLayout_5.addWidget(self.ContactAuthorCheckBox, 1, 1, 1, 1)

        self.label_22 = QLabel(self.page_publication)
        self.label_22.setObjectName("label_22")
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_22.setOpenExternalLinks(True)

        self.gridLayout_5.addWidget(self.label_22, 0, 0, 1, 1)

        self.EmailLabel = QLabel(self.page_publication)
        self.EmailLabel.setObjectName("EmailLabel")
        self.EmailLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.EmailLabel, 3, 0, 1, 1)

        self.FootNoteLineEdit = QLineEdit(self.page_publication)
        self.FootNoteLineEdit.setObjectName("FootNoteLineEdit")

        self.gridLayout_5.addWidget(self.FootNoteLineEdit, 7, 1, 1, 1)

        self.label_27 = QLabel(self.page_publication)
        self.label_27.setObjectName("label_27")
        self.label_27.setScaledContents(False)

        self.gridLayout_5.addWidget(self.label_27, 0, 2, 1, 1)

        self.PhoneLabel = QLabel(self.page_publication)
        self.PhoneLabel.setObjectName("PhoneLabel")
        self.PhoneLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.PhoneLabel, 4, 0, 1, 1)

        self.AddressTextedit = QTextEdit(self.page_publication)
        self.AddressTextedit.setObjectName("AddressTextedit")

        self.gridLayout_5.addWidget(self.AddressTextedit, 2, 1, 1, 1)

        self.FullNameLineEdit = QLineEdit(self.page_publication)
        self.FullNameLineEdit.setObjectName("FullNameLineEdit")

        self.gridLayout_5.addWidget(self.FullNameLineEdit, 0, 1, 1, 1)

        self.EMailLineEdit = QLineEdit(self.page_publication)
        self.EMailLineEdit.setObjectName("EMailLineEdit")

        self.gridLayout_5.addWidget(self.EMailLineEdit, 3, 1, 1, 1)

        self.ORCIDLineEdit = QLineEdit(self.page_publication)
        self.ORCIDLineEdit.setObjectName("ORCIDLineEdit")

        self.gridLayout_5.addWidget(self.ORCIDLineEdit, 5, 1, 1, 1)

        self.label_36 = QLabel(self.page_publication)
        self.label_36.setObjectName("label_36")
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_36, 6, 0, 1, 1)

        self.IUCRIDLineEdit = QLineEdit(self.page_publication)
        self.IUCRIDLineEdit.setObjectName("IUCRIDLineEdit")

        self.gridLayout_5.addWidget(self.IUCRIDLineEdit, 6, 1, 1, 1)


        self.verticalLayout_24.addLayout(self.gridLayout_5)


        self.verticalLayout_23.addLayout(self.verticalLayout_24)

        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.SaveAuthorLoopToTemplateButton = QPushButton(self.page_publication)
        self.SaveAuthorLoopToTemplateButton.setObjectName("SaveAuthorLoopToTemplateButton")

        self.verticalLayout_32.addWidget(self.SaveAuthorLoopToTemplateButton, 0, Qt.AlignmentFlag.AlignRight)

        self.AddThisAuthorToLoopPushButton = QPushButton(self.page_publication)
        self.AddThisAuthorToLoopPushButton.setObjectName("AddThisAuthorToLoopPushButton")

        self.verticalLayout_32.addWidget(self.AddThisAuthorToLoopPushButton)


        self.verticalLayout_23.addLayout(self.verticalLayout_32)

        self.authorEditTabWidget.addTab(self.page_publication, "")
        self.page_audit = QWidget()
        self.page_audit.setObjectName("page_audit")
        self.verticalLayout_40 = QVBoxLayout(self.page_audit)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.label_23 = QLabel(self.page_audit)
        self.label_23.setObjectName("label_23")

        self.verticalLayout_38.addWidget(self.label_23)

        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.label_29 = QLabel(self.page_audit)
        self.label_29.setObjectName("label_29")
        self.label_29.setScaledContents(False)

        self.gridLayout_25.addWidget(self.label_29, 0, 2, 1, 1)

        self.label_24 = QLabel(self.page_audit)
        self.label_24.setObjectName("label_24")
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_24.setOpenExternalLinks(True)

        self.gridLayout_25.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_30 = QLabel(self.page_audit)
        self.label_30.setObjectName("label_30")
        self.label_30.setScaledContents(False)

        self.gridLayout_25.addWidget(self.label_30, 2, 2, 1, 1)

        self.EmailLabel_cif = QLabel(self.page_audit)
        self.EmailLabel_cif.setObjectName("EmailLabel_cif")
        self.EmailLabel_cif.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_25.addWidget(self.EmailLabel_cif, 3, 0, 1, 1)

        self.PhoneLineEdit_cif = QLineEdit(self.page_audit)
        self.PhoneLineEdit_cif.setObjectName("PhoneLineEdit_cif")

        self.gridLayout_25.addWidget(self.PhoneLineEdit_cif, 4, 1, 1, 1)

        self.ContactAuthorCheckBox_cif = QCheckBox(self.page_audit)
        self.ContactAuthorCheckBox_cif.setObjectName("ContactAuthorCheckBox_cif")

        self.gridLayout_25.addWidget(self.ContactAuthorCheckBox_cif, 1, 1, 1, 1)

        self.AddressTextedit_cif = QTextEdit(self.page_audit)
        self.AddressTextedit_cif.setObjectName("AddressTextedit_cif")

        self.gridLayout_25.addWidget(self.AddressTextedit_cif, 2, 1, 1, 1)

        self.label_25 = QLabel(self.page_audit)
        self.label_25.setObjectName("label_25")
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_25.addWidget(self.label_25, 2, 0, 1, 1)

        self.FullNameLineEdit_cif = QLineEdit(self.page_audit)
        self.FullNameLineEdit_cif.setObjectName("FullNameLineEdit_cif")

        self.gridLayout_25.addWidget(self.FullNameLineEdit_cif, 0, 1, 1, 1)

        self.PhoneLabel_cif = QLabel(self.page_audit)
        self.PhoneLabel_cif.setObjectName("PhoneLabel_cif")
        self.PhoneLabel_cif.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_25.addWidget(self.PhoneLabel_cif, 4, 0, 1, 1)

        self.EMailLineEdit_cif = QLineEdit(self.page_audit)
        self.EMailLineEdit_cif.setObjectName("EMailLineEdit_cif")

        self.gridLayout_25.addWidget(self.EMailLineEdit_cif, 3, 1, 1, 1)

        self.label_16 = QLabel(self.page_audit)
        self.label_16.setObjectName("label_16")

        self.gridLayout_25.addWidget(self.label_16, 6, 0, 1, 3)

        self.label_19 = QLabel(self.page_audit)
        self.label_19.setObjectName("label_19")

        self.gridLayout_25.addWidget(self.label_19, 7, 0, 1, 3)

        self.label_13 = QLabel(self.page_audit)
        self.label_13.setObjectName("label_13")
        sizePolicy23 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy23.setHorizontalStretch(0)
        sizePolicy23.setVerticalStretch(0)
        sizePolicy23.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy23)
        self.label_13.setWordWrap(True)

        self.gridLayout_25.addWidget(self.label_13, 5, 1, 1, 2)


        self.verticalLayout_38.addLayout(self.gridLayout_25)


        self.verticalLayout_40.addLayout(self.verticalLayout_38)

        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.SaveAuthorLoopToTemplateButton_cif = QPushButton(self.page_audit)
        self.SaveAuthorLoopToTemplateButton_cif.setObjectName("SaveAuthorLoopToTemplateButton_cif")

        self.verticalLayout_39.addWidget(self.SaveAuthorLoopToTemplateButton_cif, 0, Qt.AlignmentFlag.AlignRight)

        self.AddThisAuthorToLoopPushButton_cif = QPushButton(self.page_audit)
        self.AddThisAuthorToLoopPushButton_cif.setObjectName("AddThisAuthorToLoopPushButton_cif")
        sizePolicy24 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy24.setHorizontalStretch(0)
        sizePolicy24.setVerticalStretch(0)
        sizePolicy24.setHeightForWidth(self.AddThisAuthorToLoopPushButton_cif.sizePolicy().hasHeightForWidth())
        self.AddThisAuthorToLoopPushButton_cif.setSizePolicy(sizePolicy24)

        self.verticalLayout_39.addWidget(self.AddThisAuthorToLoopPushButton_cif)


        self.verticalLayout_40.addLayout(self.verticalLayout_39)

        self.authorEditTabWidget.addTab(self.page_audit, "")

        self.gridLayout_2.addWidget(self.authorEditTabWidget, 2, 1, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_21, 2, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_10, 3, 1, 1, 1)

        self.frame_2 = QFrame(self.tab_2)
        self.frame_2.setObjectName("frame_2")
        sizePolicy25 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy25.setHorizontalStretch(55)
        sizePolicy25.setVerticalStretch(0)
        sizePolicy25.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy25)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.frame_2, 2, 2, 1, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_15, 1, 1, 1, 1)

        self.LoopsTabWidget.addTab(self.tab_2, "")

        self.verticalLayout_9.addWidget(self.LoopsTabWidget)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.revertLoopsPushButton = QPushButton(self.page_Loops)
        self.revertLoopsPushButton.setObjectName("revertLoopsPushButton")

        self.gridLayout_16.addWidget(self.revertLoopsPushButton, 0, 2, 1, 1)

        self.BackFromLoopsPushButton = QPushButton(self.page_Loops)
        self.BackFromLoopsPushButton.setObjectName("BackFromLoopsPushButton")
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
        self.newLoopPushButton.setObjectName("newLoopPushButton")

        self.gridLayout_16.addWidget(self.newLoopPushButton, 0, 4, 1, 1)

        self.deleteLoopButton = QPushButton(self.page_Loops)
        self.deleteLoopButton.setObjectName("deleteLoopButton")

        self.gridLayout_16.addWidget(self.deleteLoopButton, 3, 4, 1, 1)


        self.verticalLayout_9.addLayout(self.gridLayout_16)

        self.MainStackedWidget.addWidget(self.page_Loops)
        self.page_checkcif = QWidget()
        self.page_checkcif.setObjectName("page_checkcif")
        self.gridLayout_8 = QGridLayout(self.page_checkcif)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.CheckCIFResultsTabWidget = QTabWidget(self.page_checkcif)
        self.CheckCIFResultsTabWidget.setObjectName("CheckCIFResultsTabWidget")
        sizePolicy26 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy26.setHorizontalStretch(0)
        sizePolicy26.setVerticalStretch(4)
        sizePolicy26.setHeightForWidth(self.CheckCIFResultsTabWidget.sizePolicy().hasHeightForWidth())
        self.CheckCIFResultsTabWidget.setSizePolicy(sizePolicy26)
        self.CheckCIFResultsTabWidget.setDocumentMode(False)
        self.CheckCIFResultsTabWidget.setTabBarAutoHide(False)
        self.platon_page = QWidget()
        self.platon_page.setObjectName("platon_page")
        self.verticalLayout_11 = QVBoxLayout(self.platon_page)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.CheckcifPlaintextEdit = QPlainTextEdit(self.platon_page)
        self.CheckcifPlaintextEdit.setObjectName("CheckcifPlaintextEdit")
        self.CheckcifPlaintextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.CheckcifPlaintextEdit.setReadOnly(True)
        self.CheckcifPlaintextEdit.setPlainText("")
        self.CheckcifPlaintextEdit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_11.addWidget(self.CheckcifPlaintextEdit)

        self.CheckCIFResultsTabWidget.addTab(self.platon_page, "")
        self.html_page = QWidget()
        self.html_page.setObjectName("html_page")
        self.verticalLayout_12 = QVBoxLayout(self.html_page)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.ResponsesTabWidget = QTabWidget(self.html_page)
        self.ResponsesTabWidget.setObjectName("ResponsesTabWidget")
        self.ResponsesTabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.ResponsesTabWidget.setMovable(False)
        self.htmlTabwidgetPage = QWidget()
        self.htmlTabwidgetPage.setObjectName("htmlTabwidgetPage")
        self.verticalLayout_14 = QVBoxLayout(self.htmlTabwidgetPage)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.htmlCHeckCifGridLayout = QGridLayout()
        self.htmlCHeckCifGridLayout.setObjectName("htmlCHeckCifGridLayout")

        self.verticalLayout_14.addLayout(self.htmlCHeckCifGridLayout)

        self.ResponsesTabWidget.addTab(self.htmlTabwidgetPage, "")
        self.ResponsesTabWidgetPage2 = QWidget()
        self.ResponsesTabWidgetPage2.setObjectName("ResponsesTabWidgetPage2")
        self.verticalLayout_15 = QVBoxLayout(self.ResponsesTabWidgetPage2)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.responseFormsListWidget = QListWidget(self.ResponsesTabWidgetPage2)
        self.responseFormsListWidget.setObjectName("responseFormsListWidget")
        self.responseFormsListWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.responseFormsListWidget.setAutoScroll(False)
        self.responseFormsListWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.responseFormsListWidget.setProperty("showDropIndicator", False)
        self.responseFormsListWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.verticalLayout_15.addWidget(self.responseFormsListWidget)

        self.label_6 = QLabel(self.ResponsesTabWidgetPage2)
        self.label_6.setObjectName("label_6")

        self.verticalLayout_15.addWidget(self.label_6)

        self.frame = QFrame(self.ResponsesTabWidgetPage2)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.SavePushButton = QPushButton(self.frame)
        self.SavePushButton.setObjectName("SavePushButton")

        self.horizontalLayout_2.addWidget(self.SavePushButton)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_19)


        self.verticalLayout_15.addWidget(self.frame)

        self.ResponsesTabWidget.addTab(self.ResponsesTabWidgetPage2, "")

        self.verticalLayout_12.addWidget(self.ResponsesTabWidget)

        self.CheckCIFResultsTabWidget.addTab(self.html_page, "")
        self.pdf_page = QWidget()
        self.pdf_page.setObjectName("pdf_page")
        self.verticalLayout_13 = QVBoxLayout(self.pdf_page)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_5 = QLabel(self.pdf_page)
        self.label_5.setObjectName("label_5")
        sizePolicy27 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy27.setHorizontalStretch(0)
        sizePolicy27.setVerticalStretch(0)
        sizePolicy27.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy27)
        self.label_5.setMinimumSize(QSize(0, 20))

        self.verticalLayout_13.addWidget(self.label_5)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_4)

        self.CheckCIFResultsTabWidget.addTab(self.pdf_page, "")
        self.ckf_page = QWidget()
        self.ckf_page.setObjectName("ckf_page")
        self.verticalLayout_36 = QVBoxLayout(self.ckf_page)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(3, 3, 3, 3)
        self.ckf_textedit = QPlainTextEdit(self.ckf_page)
        self.ckf_textedit.setObjectName("ckf_textedit")
        self.ckf_textedit.setFont(font1)
        self.ckf_textedit.setReadOnly(True)
        self.ckf_textedit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_36.addWidget(self.ckf_textedit)

        self.CheckCIFResultsTabWidget.addTab(self.ckf_page, "")

        self.gridLayout_8.addWidget(self.CheckCIFResultsTabWidget, 1, 0, 1, 8)

        self.groupBox_7 = QGroupBox(self.page_checkcif)
        self.groupBox_7.setObjectName("groupBox_7")
        sizePolicy28 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy28.setHorizontalStretch(0)
        sizePolicy28.setVerticalStretch(1)
        sizePolicy28.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy28)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 6, 0, 0)
        self.CheckCifLogPlainTextEdit = QPlainTextEdit(self.groupBox_7)
        self.CheckCifLogPlainTextEdit.setObjectName("CheckCifLogPlainTextEdit")
        self.CheckCifLogPlainTextEdit.setTabChangesFocus(True)
        self.CheckCifLogPlainTextEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.CheckCifLogPlainTextEdit)


        self.gridLayout_8.addWidget(self.groupBox_7, 0, 0, 1, 8)

        self.groupBox_checkcif_2 = QGroupBox(self.page_checkcif)
        self.groupBox_checkcif_2.setObjectName("groupBox_checkcif_2")
        self.gridLayout_14 = QGridLayout(self.groupBox_checkcif_2)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.CheckcifPDFOnlineButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifPDFOnlineButton.setObjectName("CheckcifPDFOnlineButton")

        self.gridLayout_14.addWidget(self.CheckcifPDFOnlineButton, 1, 2, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.structfactCheckBox = QCheckBox(self.groupBox_checkcif_2)
        self.structfactCheckBox.setObjectName("structfactCheckBox")

        self.horizontalLayout_9.addWidget(self.structfactCheckBox)

        self.fullIucrCheckBox = QCheckBox(self.groupBox_checkcif_2)
        self.fullIucrCheckBox.setObjectName("fullIucrCheckBox")

        self.horizontalLayout_9.addWidget(self.fullIucrCheckBox)

        self.checkDuplicatesCheckBox = QCheckBox(self.groupBox_checkcif_2)
        self.checkDuplicatesCheckBox.setObjectName("checkDuplicatesCheckBox")
        self.checkDuplicatesCheckBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.checkDuplicatesCheckBox)


        self.gridLayout_14.addLayout(self.horizontalLayout_9, 2, 0, 1, 3)

        self.CheckcifButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifButton.setObjectName("CheckcifButton")

        self.gridLayout_14.addWidget(self.CheckcifButton, 1, 0, 1, 1)

        self.CheckcifHTMLOnlineButton = QPushButton(self.groupBox_checkcif_2)
        self.CheckcifHTMLOnlineButton.setObjectName("CheckcifHTMLOnlineButton")

        self.gridLayout_14.addWidget(self.CheckcifHTMLOnlineButton, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_checkcif_2, 4, 5, 4, 1)

        self.ButtonFrame = QFrame(self.page_checkcif)
        self.ButtonFrame.setObjectName("ButtonFrame")
        self.ButtonFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ButtonFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.ButtonFrame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.ButtonFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_8.addWidget(self.ButtonFrame, 2, 0, 1, 7)

        self.horizontalSpacer = QSpacerItem(225, 47, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 4, 6, 3, 1)

        self.BackFromPlatonPushButton = QPushButton(self.page_checkcif)
        self.BackFromPlatonPushButton.setObjectName("BackFromPlatonPushButton")
        self.BackFromPlatonPushButton.setMinimumSize(QSize(160, 0))

        self.gridLayout_8.addWidget(self.BackFromPlatonPushButton, 5, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(13, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_2, 5, 1, 1, 2)

        self.horizontalSpacer_17 = QSpacerItem(13, 47, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_17, 4, 4, 3, 1)

        self.MainStackedWidget.addWidget(self.page_checkcif)
        self.page_cod = QWidget()
        self.page_cod.setObjectName("page_cod")
        self.gridLayout_17 = QGridLayout(self.page_cod)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.frame_for_radiobuttons = QFrame(self.page_cod)
        self.frame_for_radiobuttons.setObjectName("frame_for_radiobuttons")
        self.frame_for_radiobuttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_for_radiobuttons.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_for_radiobuttons)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_radiobuttons = QHBoxLayout()
        self.horizontalLayout_radiobuttons.setObjectName("horizontalLayout_radiobuttons")
        self.personalDepositRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.personalDepositRadioButton.setObjectName("personalDepositRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.personalDepositRadioButton)

        self.prepublicationDepositRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.prepublicationDepositRadioButton.setObjectName("prepublicationDepositRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.prepublicationDepositRadioButton)

        self.publishedDepositionRadioButton = QRadioButton(self.frame_for_radiobuttons)
        self.publishedDepositionRadioButton.setObjectName("publishedDepositionRadioButton")

        self.horizontalLayout_radiobuttons.addWidget(self.publishedDepositionRadioButton)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_radiobuttons.addItem(self.horizontalSpacer_31)


        self.verticalLayout_28.addLayout(self.horizontalLayout_radiobuttons)


        self.gridLayout_22.addWidget(self.frame_for_radiobuttons, 0, 1, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, -1, 9, -1)
        self.depositorUsername = QLabel(self.page_cod)
        self.depositorUsername.setObjectName("depositorUsername")

        self.gridLayout_19.addWidget(self.depositorUsername, 0, 0, 1, 1)

        self.label_9 = QLabel(self.page_cod)
        self.label_9.setObjectName("label_9")

        self.gridLayout_19.addWidget(self.label_9, 2, 0, 1, 1)

        self.depositorPasswordLineEdit = QLineEdit(self.page_cod)
        self.depositorPasswordLineEdit.setObjectName("depositorPasswordLineEdit")
        self.depositorPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout_19.addWidget(self.depositorPasswordLineEdit, 1, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, -1, -1)
        self.depositHKLcheckBox = QCheckBox(self.page_cod)
        self.depositHKLcheckBox.setObjectName("depositHKLcheckBox")

        self.horizontalLayout_11.addWidget(self.depositHKLcheckBox)

        self.Upload_hkl_pushButton = QPushButton(self.page_cod)
        self.Upload_hkl_pushButton.setObjectName("Upload_hkl_pushButton")
        sizePolicy5.setHeightForWidth(self.Upload_hkl_pushButton.sizePolicy().hasHeightForWidth())
        self.Upload_hkl_pushButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_11.addWidget(self.Upload_hkl_pushButton)


        self.gridLayout_19.addLayout(self.horizontalLayout_11, 3, 1, 1, 1)

        self.userEmailLineEdit = QLineEdit(self.page_cod)
        self.userEmailLineEdit.setObjectName("userEmailLineEdit")
        self.userEmailLineEdit.setInputMethodHints(Qt.InputMethodHint.ImhEmailCharactersOnly|Qt.InputMethodHint.ImhLowercaseOnly|Qt.InputMethodHint.ImhNoAutoUppercase)

        self.gridLayout_19.addWidget(self.userEmailLineEdit, 2, 1, 1, 1)

        self.depositorUsernameLineEdit = QLineEdit(self.page_cod)
        self.depositorUsernameLineEdit.setObjectName("depositorUsernameLineEdit")

        self.gridLayout_19.addWidget(self.depositorUsernameLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.page_cod)
        self.label_2.setObjectName("label_2")
        self.label_2.setTextFormat(Qt.TextFormat.RichText)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.gridLayout_19.addWidget(self.label_2, 0, 2, 4, 1)

        self.depositorPasswordLabel = QLabel(self.page_cod)
        self.depositorPasswordLabel.setObjectName("depositorPasswordLabel")

        self.gridLayout_19.addWidget(self.depositorPasswordLabel, 1, 0, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_19, 1, 1, 1, 1)

        self.depositionOptionsStackedWidget = QStackedWidget(self.page_cod)
        self.depositionOptionsStackedWidget.setObjectName("depositionOptionsStackedWidget")
        self.depositionOptionsStackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.depositionOptionsStackedWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.depositionOptionsStackedWidget.setLineWidth(1)
        self.page_personal = QWidget()
        self.page_personal.setObjectName("page_personal")
        self.verticalLayout_30 = QVBoxLayout(self.page_personal)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 12, 0, -1)
        self.label_10 = QLabel(self.page_personal)
        self.label_10.setObjectName("label_10")
        self.label_10.setTextFormat(Qt.TextFormat.RichText)

        self.verticalLayout_30.addWidget(self.label_10)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.horizontalSpacer_30 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_30, 0, 2, 1, 1)

        self.ContactAuthorLabel = QLabel(self.page_personal)
        self.ContactAuthorLabel.setObjectName("ContactAuthorLabel")

        self.gridLayout_20.addWidget(self.ContactAuthorLabel, 1, 0, 1, 1)

        self.authorsFullNamePersonalLabel = QLabel(self.page_personal)
        self.authorsFullNamePersonalLabel.setObjectName("authorsFullNamePersonalLabel")

        self.gridLayout_20.addWidget(self.authorsFullNamePersonalLabel, 0, 0, 1, 1)

        self.authorEditorPushButton = QPushButton(self.page_personal)
        self.authorEditorPushButton.setObjectName("authorEditorPushButton")
        sizePolicy5.setHeightForWidth(self.authorEditorPushButton.sizePolicy().hasHeightForWidth())
        self.authorEditorPushButton.setSizePolicy(sizePolicy5)

        self.gridLayout_20.addWidget(self.authorEditorPushButton, 0, 1, 1, 1)

        self.ContactAuthorLineEdit = QLineEdit(self.page_personal)
        self.ContactAuthorLineEdit.setObjectName("ContactAuthorLineEdit")
        self.ContactAuthorLineEdit.setReadOnly(True)

        self.gridLayout_20.addWidget(self.ContactAuthorLineEdit, 1, 1, 1, 1)

        self.ContactEmailLineEdit = QLineEdit(self.page_personal)
        self.ContactEmailLineEdit.setObjectName("ContactEmailLineEdit")
        self.ContactEmailLineEdit.setReadOnly(True)

        self.gridLayout_20.addWidget(self.ContactEmailLineEdit, 2, 1, 1, 1)

        self.label_12 = QLabel(self.page_personal)
        self.label_12.setObjectName("label_12")

        self.gridLayout_20.addWidget(self.label_12, 2, 0, 1, 1)


        self.verticalLayout_30.addLayout(self.gridLayout_20)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_12)

        self.depositionOptionsStackedWidget.addWidget(self.page_personal)
        self.page_prepublication = QWidget()
        self.page_prepublication.setObjectName("page_prepublication")
        self.verticalLayout_25 = QVBoxLayout(self.page_prepublication)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.horizontalSpacer_29 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_29, 0, 2, 1, 1)

        self.embargoTimeInMonthsSpinBox = QSpinBox(self.page_prepublication)
        self.embargoTimeInMonthsSpinBox.setObjectName("embargoTimeInMonthsSpinBox")
        self.embargoTimeInMonthsSpinBox.setMinimum(6)
        self.embargoTimeInMonthsSpinBox.setMaximum(12)

        self.gridLayout_21.addWidget(self.embargoTimeInMonthsSpinBox, 1, 1, 1, 1)

        self.label_8 = QLabel(self.page_prepublication)
        self.label_8.setObjectName("label_8")

        self.gridLayout_21.addWidget(self.label_8, 1, 2, 1, 1)

        self.journalNameLineEdit = QLineEdit(self.page_prepublication)
        self.journalNameLineEdit.setObjectName("journalNameLineEdit")

        self.gridLayout_21.addWidget(self.journalNameLineEdit, 0, 1, 1, 1)

        self.embargoTimeInMonthsLabel = QLabel(self.page_prepublication)
        self.embargoTimeInMonthsLabel.setObjectName("embargoTimeInMonthsLabel")

        self.gridLayout_21.addWidget(self.embargoTimeInMonthsLabel, 1, 0, 1, 1)

        self.journalMameLabel = QLabel(self.page_prepublication)
        self.journalMameLabel.setObjectName("journalMameLabel")

        self.gridLayout_21.addWidget(self.journalMameLabel, 0, 0, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_21)

        self.gridLayout_author_prepubl = QGridLayout()
        self.gridLayout_author_prepubl.setObjectName("gridLayout_author_prepubl")
        self.horizontalSpacer_35 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_author_prepubl.addItem(self.horizontalSpacer_35, 0, 3, 1, 1)

        self.authorsFullNamePersonalLabel_2 = QLabel(self.page_prepublication)
        self.authorsFullNamePersonalLabel_2.setObjectName("authorsFullNamePersonalLabel_2")

        self.gridLayout_author_prepubl.addWidget(self.authorsFullNamePersonalLabel_2, 0, 1, 1, 1)

        self.ContactAuthorLineEdit_2 = QLineEdit(self.page_prepublication)
        self.ContactAuthorLineEdit_2.setObjectName("ContactAuthorLineEdit_2")
        self.ContactAuthorLineEdit_2.setReadOnly(True)

        self.gridLayout_author_prepubl.addWidget(self.ContactAuthorLineEdit_2, 1, 2, 1, 1)

        self.authorEditorPushButton_2 = QPushButton(self.page_prepublication)
        self.authorEditorPushButton_2.setObjectName("authorEditorPushButton_2")
        sizePolicy5.setHeightForWidth(self.authorEditorPushButton_2.sizePolicy().hasHeightForWidth())
        self.authorEditorPushButton_2.setSizePolicy(sizePolicy5)

        self.gridLayout_author_prepubl.addWidget(self.authorEditorPushButton_2, 0, 2, 1, 1)

        self.ContactAuthorLabel_2 = QLabel(self.page_prepublication)
        self.ContactAuthorLabel_2.setObjectName("ContactAuthorLabel_2")

        self.gridLayout_author_prepubl.addWidget(self.ContactAuthorLabel_2, 1, 1, 1, 1)

        self.label_15 = QLabel(self.page_prepublication)
        self.label_15.setObjectName("label_15")

        self.gridLayout_author_prepubl.addWidget(self.label_15, 2, 1, 1, 1)

        self.ContactEmailLineEdit_2 = QLineEdit(self.page_prepublication)
        self.ContactEmailLineEdit_2.setObjectName("ContactEmailLineEdit_2")
        self.ContactEmailLineEdit_2.setReadOnly(True)

        self.gridLayout_author_prepubl.addWidget(self.ContactEmailLineEdit_2, 2, 2, 1, 1)


        self.verticalLayout_25.addLayout(self.gridLayout_author_prepubl)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_13)

        self.depositionOptionsStackedWidget.addWidget(self.page_prepublication)
        self.page_published = QWidget()
        self.page_published.setObjectName("page_published")
        self.verticalLayout_27 = QVBoxLayout(self.page_published)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_23 = QGridLayout()
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.publication_doi_lineedit = QLineEdit(self.page_published)
        self.publication_doi_lineedit.setObjectName("publication_doi_lineedit")

        self.gridLayout_23.addWidget(self.publication_doi_lineedit, 1, 1, 1, 1)

        self.cod_database_code_Label = QLabel(self.page_published)
        self.cod_database_code_Label.setObjectName("cod_database_code_Label")

        self.gridLayout_23.addWidget(self.cod_database_code_Label, 1, 0, 1, 1)

        self.horizontalSpacer_32 = QSpacerItem(80, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_32, 1, 3, 1, 1)

        self.label_11 = QLabel(self.page_published)
        self.label_11.setObjectName("label_11")

        self.gridLayout_23.addWidget(self.label_11, 0, 0, 1, 2)

        self.GetDOIPushButton = QPushButton(self.page_published)
        self.GetDOIPushButton.setObjectName("GetDOIPushButton")

        self.gridLayout_23.addWidget(self.GetDOIPushButton, 1, 2, 1, 1)


        self.verticalLayout_27.addLayout(self.gridLayout_23)

        self.DOIResolveTextLabel = QLabel(self.page_published)
        self.DOIResolveTextLabel.setObjectName("DOIResolveTextLabel")
        self.DOIResolveTextLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.DOIResolveTextLabel.setWordWrap(True)

        self.verticalLayout_27.addWidget(self.DOIResolveTextLabel)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_14 = QLabel(self.page_published)
        self.label_14.setObjectName("label_14")
        self.label_14.setTextFormat(Qt.TextFormat.RichText)

        self.verticalLayout_26.addWidget(self.label_14)


        self.verticalLayout_27.addLayout(self.verticalLayout_26)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_27.addItem(self.verticalSpacer_11)

        self.depositionOptionsStackedWidget.addWidget(self.page_published)
        self.page_deposition_output = QWidget()
        self.page_deposition_output.setObjectName("page_deposition_output")
        self.verticalLayout_31 = QVBoxLayout(self.page_deposition_output)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.verticalLayout_31.setContentsMargins(0, -1, 0, 0)
        self.label_deposition_output = QLabel(self.page_deposition_output)
        self.label_deposition_output.setObjectName("label_deposition_output")

        self.verticalLayout_31.addWidget(self.label_deposition_output)

        self.depositOutputTextBrowser = QTextBrowser(self.page_deposition_output)
        self.depositOutputTextBrowser.setObjectName("depositOutputTextBrowser")
        self.depositOutputTextBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.depositOutputTextBrowser.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.depositOutputTextBrowser.setOpenExternalLinks(True)

        self.verticalLayout_31.addWidget(self.depositOutputTextBrowser)

        self.depositionOptionsStackedWidget.addWidget(self.page_deposition_output)

        self.gridLayout_22.addWidget(self.depositionOptionsStackedWidget, 4, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_22, 0, 1, 1, 1)

        self.StructuresListGroupBox = QGroupBox(self.page_cod)
        self.StructuresListGroupBox.setObjectName("StructuresListGroupBox")
        sizePolicy29 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy29.setHorizontalStretch(0)
        sizePolicy29.setVerticalStretch(0)
        sizePolicy29.setHeightForWidth(self.StructuresListGroupBox.sizePolicy().hasHeightForWidth())
        self.StructuresListGroupBox.setSizePolicy(sizePolicy29)
        self.StructuresListGroupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gridLayout_18 = QGridLayout(self.StructuresListGroupBox)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.refreshDepositListPushButton = QPushButton(self.StructuresListGroupBox)
        self.refreshDepositListPushButton.setObjectName("refreshDepositListPushButton")
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
        self.CODtableWidget.setObjectName("CODtableWidget")
        self.CODtableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.CODtableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.CODtableWidget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.CODtableWidget.setSortingEnabled(True)
        self.CODtableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.CODtableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.CODtableWidget.horizontalHeader().setStretchLastSection(False)
        self.CODtableWidget.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_18.addWidget(self.CODtableWidget, 0, 0, 1, 3)


        self.gridLayout_17.addWidget(self.StructuresListGroupBox, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.BackFromDepositPushButton = QPushButton(self.page_cod)
        self.BackFromDepositPushButton.setObjectName("BackFromDepositPushButton")
        self.BackFromDepositPushButton.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_10.addWidget(self.BackFromDepositPushButton)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_27)

        self.depositCIFpushButton = QPushButton(self.page_cod)
        self.depositCIFpushButton.setObjectName("depositCIFpushButton")

        self.horizontalLayout_10.addWidget(self.depositCIFpushButton)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_28)


        self.gridLayout_17.addLayout(self.horizontalLayout_10, 1, 0, 1, 2)

        self.MainStackedWidget.addWidget(self.page_cod)
        self.page_textTemplate = QWidget()
        self.page_textTemplate.setObjectName("page_textTemplate")
        self.verticalLayout_33 = QVBoxLayout(self.page_textTemplate)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.MainStackedWidget.addWidget(self.page_textTemplate)

        self.gridLayout_6.addWidget(self.MainStackedWidget, 2, 0, 1, 13)

        self.splitter.addWidget(self.CifDataItemsFrame)

        self.horizontalLayout_4.addWidget(self.splitter)

        FinalCifWindow.setCentralWidget(self.Mainwidget)
        self.statusBar = QStatusBar(FinalCifWindow)
        self.statusBar.setObjectName("statusBar")
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
        QWidget.setTabOrder(self.CODURLTextedit, self.authorEditTabWidget)
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
        self.MainStackedWidget.setCurrentIndex(6)
        self.PropertiesTemplatesStackedWidget.setCurrentIndex(1)
        self.LoopsTabWidget.setCurrentIndex(0)
        self.authorEditTabWidget.setCurrentIndex(1)
        self.CheckCIFResultsTabWidget.setCurrentIndex(3)
        self.ResponsesTabWidget.setCurrentIndex(1)
        self.depositionOptionsStackedWidget.setCurrentIndex(3)

    # setupUi

    def retranslateUi(self, FinalCifWindow):
        FinalCifWindow.setWindowTitle(QCoreApplication.translate("FinalCifWindow", "FinalCif", None))
        self.SelectCifFileGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "CIF File", None))
        self.SelectCif_LineEdit.setPlaceholderText(QCoreApplication.translate("FinalCifWindow", "Select a .cif file first.", None))
        self.SelectCif_PushButton.setText(QCoreApplication.translate("FinalCifWindow", "Select File", None))
        self.RecentComboBox.setItemText(0, QCoreApplication.translate("FinalCifWindow", "Recent Files", None))

        self.RecentComboBox.setCurrentText(QCoreApplication.translate("FinalCifWindow", "Recent Files", None))
        self.searchMainTableLabel.setText(QCoreApplication.translate("FinalCifWindow", "Search Key", None))
        self.searchMainTableLineEdit.setPlaceholderText(QCoreApplication.translate("FinalCifWindow", "Find a CIF keyword in the main table", None))
        self.EquipmentGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "Equipment Templates", None))
#if QT_CONFIG(tooltip)
        self.EquipmentTemplatesListWidget.setToolTip(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Each entry can have a list of key/value pairs. For example a Diffractometer model can have a list of features.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.NewEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "New Template", None))
        self.EditEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Edit Template", None))
        self.ImportEquipmentTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Import Template", None))
        ___qtablewidgetitem = self.EquipmentEditTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FinalCifWindow", "key", None))
        ___qtablewidgetitem1 = self.EquipmentEditTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FinalCifWindow", "value", None))
        self.DeleteEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", "Delete Template", None))
        self.SaveEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", "Save", None))
        self.CancelEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", "Cancel", None))
        self.ExportEquipmentButton.setText(QCoreApplication.translate("FinalCifWindow", "Export", None))
        self.ImportCifPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Import .cif, .pcf, .cif_od, .cfx or .sqf file", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("FinalCifWindow", "Report Options", None))
        self.ADPTableCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Add ADP table", None))
        self.ReportTextCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "No report text in structure report", None))
        self.PictureWidthLabel.setText(QCoreApplication.translate("FinalCifWindow", "Picture width [cm]", None))
        self.HAtomsCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "No bonds and angles to hydrogen atoms", None))
        self.UsePicometersCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Use picometers", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("FinalCifWindow", "Report Templates:", None))

        __sortingEnabled = self.docxTemplatesListWidget.isSortingEnabled()
        self.docxTemplatesListWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.docxTemplatesListWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("FinalCifWindow", "Use FinalCif default template", None))
        self.docxTemplatesListWidget.setSortingEnabled(__sortingEnabled)

        self.AddNewTemplPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Add New Template", None))
        self.RemoveTemplPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Remove Selected", None))
        self.label.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Get more templates here:  <a href=\"https://github.com/dkratzert/FinalCif\"><span style=\" text-decoration: underline; color:#0068da;\">https://github.com/dkratzert/FinalCif</span></a></p></body></html>", None))
        self.LoopsGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "Author Templates", None))
        self.ExportAuthorPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Export Author as File", None))
        self.ImportAuthorPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Import Author", None))
        self.DeleteLoopAuthorTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Delete Author", None))
        self.spacegroupLabel.setText(QCoreApplication.translate("FinalCifWindow", "Space-Group Type", None))
        self.appendCifPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Append CIF", None))
        self.CCDCNumLabel.setText(QCoreApplication.translate("FinalCifWindow", "CCDC Number", None))
        self.HelpPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Help", None))
        self.datanameLabel.setText(QCoreApplication.translate("FinalCifWindow", "Data Name", None))
        self.SumFormMainLabel.setText(QCoreApplication.translate("FinalCifWindow", "Sum Formula", None))
        ___qtablewidgetitem2 = self.cif_main_table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FinalCifWindow", "CIF Value", None))
        ___qtablewidgetitem3 = self.cif_main_table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FinalCifWindow", "From Data Source", None))
        ___qtablewidgetitem4 = self.cif_main_table.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FinalCifWindow", "Own Data", None))
        self.groupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.SaveCifButton.setToolTip(QCoreApplication.translate("FinalCifWindow", "Saves the CIF file to name-finalcif.cif", None))
#endif // QT_CONFIG(tooltip)
        self.SaveCifButton.setText(QCoreApplication.translate("FinalCifWindow", "Save CIF File", None))
#if QT_CONFIG(tooltip)
        self.ExploreDirButton.setToolTip(QCoreApplication.translate("FinalCifWindow", "Saves the CIF file to name-finalcif.cif", None))
#endif // QT_CONFIG(tooltip)
        self.ExploreDirButton.setText(QCoreApplication.translate("FinalCifWindow", "Explore Directory", None))
        self.DetailsPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Show Details", None))
        self.AuthorEditPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Author Editor", None))
        self.groupBox_checkcif.setTitle("")
        self.LoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Edit Loops", None))
        self.ReportPicPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Picture for Report", None))
        self.SaveFullReportButton.setText(QCoreApplication.translate("FinalCifWindow", "Make Tables", None))
        self.CheckcifStartButton.setText(QCoreApplication.translate("FinalCifWindow", "CheckCIF", None))
        self.groupBox_tables.setTitle("")
        self.CODpushButton.setText(QCoreApplication.translate("FinalCifWindow", "COD Deposit", None))
        self.ShredCifButton.setText(QCoreApplication.translate("FinalCifWindow", "Extract .hkl/.res File", None))
        self.CCDCpushButton.setText(QCoreApplication.translate("FinalCifWindow", "CCDC Deposit", None))
        self.OptionsPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Options", None))
        self.BackPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.molGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "Molecule", None))
        self.growCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Grow Structure", None))
        self.labelsCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Show Labels", None))
        self.drawImagePushButton.setText(QCoreApplication.translate("FinalCifWindow", "Use as Image for Report", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("FinalCifWindow", "Shelx File", None))
        self.shelx_TextEdit.setPlainText(QCoreApplication.translate("FinalCifWindow", "No Shelx file available", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("FinalCifWindow", "Properties", None))
        self.zLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Z</p></body></html>", None))
        self.temperatureLabel.setText(QCoreApplication.translate("FinalCifWindow", "Temperature [K]", None))
        self.wR2Label.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-style:italic;\">wR</span><span style=\" vertical-align:sub;\">2 </span>[all ref.]</p></body></html>", None))
        self.r1Label.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">1 </span>[<span style=\" font-style:italic;\">I </span>&gt; 2\u03c3(<span style=\" font-style:italic;\">I</span>)]</p></body></html>", None))
        self.goofLabel.setText(QCoreApplication.translate("FinalCifWindow", "Goof", None))
        self.maxShiftLabel.setText(QCoreApplication.translate("FinalCifWindow", "Max Shift/esd", None))
        self.completeLabel.setText(QCoreApplication.translate("FinalCifWindow", "complete [%]", None))
        self.reflTotalLabel.setText(QCoreApplication.translate("FinalCifWindow", "Measured Refl.", None))
        self.refl2sigmaLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Data with [<span style=\" font-style:italic;\">I </span>&gt; 2\u03c3(<span style=\" font-style:italic;\">I</span>)]</p></body></html>", None))
        self.uniqReflLabel.setText(QCoreApplication.translate("FinalCifWindow", "Independent Refl.", None))
        self.numParametersLabel.setText(QCoreApplication.translate("FinalCifWindow", "Parameters", None))
        self.dataReflnsLabel.setText(QCoreApplication.translate("FinalCifWindow", "Data/Parameters", None))
        self.wavelengthLabel.setText(QCoreApplication.translate("FinalCifWindow", "Wavelength [\u00c5]", None))
        self.flackXLabel.setText(QCoreApplication.translate("FinalCifWindow", "Flack x", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("FinalCifWindow", "Unit Cell", None))
        self.cellField.setText("")
        self.peakLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Peak/Hole [e\u00c5<span style=\" vertical-align:super;\">-3</span>]</p></body></html>", None))
        self.rintLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">int</span></p></body></html>", None))
        self.rsigmaLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-style:italic;\">R</span><span style=\" vertical-align:sub;\">\u03c3</span></p></body></html>", None))
        self.numRestraintsLabel.setText(QCoreApplication.translate("FinalCifWindow", "Restraints", None))
        self.thetaMaxLabel.setText(QCoreApplication.translate("FinalCifWindow", "\u03b8(max) [\u00b0]", None))
        self.thetaFullLabel.setText(QCoreApplication.translate("FinalCifWindow", "\u03b8(full) [\u00b0]", None))
        self.dLabel.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>Resolution [\u00c5]</p></body></html>", None))
        self.BackpushButtonDetails.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.SourcesPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Data Sources", None))
        self.groupBox_2.setTitle("")
        self.label_3.setText(QCoreApplication.translate("FinalCifWindow", "The list of data sources shows the origin of CIF items automatically collected by FinalCif. \n"
"\n"
"Uncheck items in order to ignore the respective data source.\n"
"The data source will be ignored until next program restart.", None))
        ___qtablewidgetitem5 = self.SourcesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FinalCifWindow", "CIF Item", None))
        ___qtablewidgetitem6 = self.SourcesTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("FinalCifWindow", "Data Source", None))
        self.BackSourcesPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.BackFromOptionspPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to Main Table", None))
        self.groupBox_COD.setTitle(QCoreApplication.translate("FinalCifWindow", "Crystallography Open Database Server", None))
        self.label_7.setText(QCoreApplication.translate("FinalCifWindow", "COD deposit URL:", None))
        self.CODURLTextedit.setText(QCoreApplication.translate("FinalCifWindow", "https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl", None))
        self.groupBox_71.setTitle(QCoreApplication.translate("FinalCifWindow", "CheckCIF Server", None))
        self.label_4.setText(QCoreApplication.translate("FinalCifWindow", "Change this URL if the CheckCIF server URL changes:", None))
        self.CheckCIFServerURLTextedit.setText(QCoreApplication.translate("FinalCifWindow", "https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("FinalCifWindow", "Export", None))
        self.ExportAllTemplatesPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Export all Templates", None))
        self.label_18.setText(QCoreApplication.translate("FinalCifWindow", "Exports all templates from Equipment, Properties,\n"
" Authors and Text snippets to a single file.", None))
        self.ImportAllTemplatesPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Import all Templates", None))
        self.label_17.setText(QCoreApplication.translate("FinalCifWindow", "Imports all templates from a template file.", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("FinalCifWindow", "General Options", None))
        self.trackChangesCifCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Track CIF changes in separate file\n"
" \"[name]-finalcif_changes.cif\".", None))
        self.label_26.setText(QCoreApplication.translate("FinalCifWindow", "Application font size", None))
        self.PropertiesGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "Property Templates", None))
#if QT_CONFIG(tooltip)
        self.PropertiesTemplatesListWidget.setToolTip(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>A list of common properties like </p><p>_exptl_crystal_colour: yellow, red, blue, ...</p><p>Lists defined here will appear as dropdown menus in the main Table.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.EditPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Edit Template", None))
        self.NewPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "New Template", None))
        self.ImportPropertyTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Import", None))
        self.cifKeywordLB.setText(QCoreApplication.translate("FinalCifWindow", "CIF keyword:", None))
        self.DeletePropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", "Delete Template", None))
        self.SavePropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", "Save", None))
        self.CancelPropertiesButton.setText(QCoreApplication.translate("FinalCifWindow", "Cancel", None))
        self.ExportPropertyButton.setText(QCoreApplication.translate("FinalCifWindow", "Export", None))
        self.label_20.setText(QCoreApplication.translate("FinalCifWindow", "Details about the author(s) of a manuscript submitted for publication.\n"
"Contact authors should always also appear as regular authors.", None))
        self.label_34.setText(QCoreApplication.translate("FinalCifWindow", "ORCID", None))
        self.footnote_label.setText(QCoreApplication.translate("FinalCifWindow", "footnote", None))
        self.label_21.setText(QCoreApplication.translate("FinalCifWindow", "Adresss", None))
        self.label_28.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" color:#666666;\">The adress of an author</span></p><p><span style=\" color:#666666;\">Department<br/>Institute<br/>Street<br/>City and postcode<br/>COUNTRY</span></p></body></html>", None))
        self.ContactAuthorCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "This is a contact author", None))
        self.label_22.setText(QCoreApplication.translate("FinalCifWindow", "Full Name", None))
        self.EmailLabel.setText(QCoreApplication.translate("FinalCifWindow", "e-mail", None))
        self.label_27.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" color:#666666;\">Family name, first name</span></p></body></html>", None))
        self.PhoneLabel.setText(QCoreApplication.translate("FinalCifWindow", "phone number", None))
        self.label_36.setText(QCoreApplication.translate("FinalCifWindow", "IUCr Id", None))
        self.SaveAuthorLoopToTemplateButton.setText(QCoreApplication.translate("FinalCifWindow", "Save Author as Template", None))
        self.AddThisAuthorToLoopPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Add Publication Author to CIF Loop", None))
        self.authorEditTabWidget.setTabText(self.authorEditTabWidget.indexOf(self.page_publication), QCoreApplication.translate("FinalCifWindow", "Publication Authors", None))
        self.label_23.setText(QCoreApplication.translate("FinalCifWindow", "Details about the author(s) of this CIF data block (most often the crystallographer).\n"
"Contact authors should always also appear as regular authors.", None))
        self.label_29.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" color:#666666;\">Family name, first name</span></p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("FinalCifWindow", "Full Name", None))
        self.label_30.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" color:#666666;\">The adress of an author</span></p><p><span style=\" color:#666666;\">Department<br/>Institute<br/>Street<br/>City and postcode<br/>COUNTRY</span></p></body></html>", None))
        self.EmailLabel_cif.setText(QCoreApplication.translate("FinalCifWindow", "e-mail", None))
        self.ContactAuthorCheckBox_cif.setText(QCoreApplication.translate("FinalCifWindow", "This is a contact author", None))
        self.label_25.setText(QCoreApplication.translate("FinalCifWindow", "Adresss", None))
        self.PhoneLabel_cif.setText(QCoreApplication.translate("FinalCifWindow", "phone number", None))
        self.label_16.setText("")
        self.label_19.setText("")
        self.label_13.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" color:#666666;\">Audit authors have less possibilities than publication authors.</span></p></body></html>", None))
        self.SaveAuthorLoopToTemplateButton_cif.setText(QCoreApplication.translate("FinalCifWindow", "Save Author as Template", None))
        self.AddThisAuthorToLoopPushButton_cif.setText(QCoreApplication.translate("FinalCifWindow", "Add Audit Author to CIF Loop", None))
        self.authorEditTabWidget.setTabText(self.authorEditTabWidget.indexOf(self.page_audit), QCoreApplication.translate("FinalCifWindow", "Audit (CIF) Authors", None))
        self.LoopsTabWidget.setTabText(self.LoopsTabWidget.indexOf(self.tab_2), QCoreApplication.translate("FinalCifWindow", "Author Editor", None))
        self.revertLoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Revert Changes", None))
        self.BackFromLoopsPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.newLoopPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Add New Loop", None))
        self.deleteLoopButton.setText(QCoreApplication.translate("FinalCifWindow", "Delete Loop", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.platon_page), QCoreApplication.translate("FinalCifWindow", "PLATON CheckCIF result", None))
        self.ResponsesTabWidget.setTabText(self.ResponsesTabWidget.indexOf(self.htmlTabwidgetPage), QCoreApplication.translate("FinalCifWindow", "html report", None))
        self.label_6.setText(QCoreApplication.translate("FinalCifWindow", "Every form you fill out will be written to the cif file.", None))
        self.SavePushButton.setText(QCoreApplication.translate("FinalCifWindow", "Save Response Forms", None))
        self.ResponsesTabWidget.setTabText(self.ResponsesTabWidget.indexOf(self.ResponsesTabWidgetPage2), QCoreApplication.translate("FinalCifWindow", "checkcif alerts", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.html_page), QCoreApplication.translate("FinalCifWindow", "html CheckCIF result", None))
        self.label_5.setText(QCoreApplication.translate("FinalCifWindow", "The resulting PDF file will be displayed in an external program after CheckCIF has completed.", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.pdf_page), QCoreApplication.translate("FinalCifWindow", "PDF CheckCIF result", None))
        self.CheckCIFResultsTabWidget.setTabText(self.CheckCIFResultsTabWidget.indexOf(self.ckf_page), QCoreApplication.translate("FinalCifWindow", "Structure Factor Report", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("FinalCifWindow", "CheckCIF log messages", None))
        self.groupBox_checkcif_2.setTitle("")
        self.CheckcifPDFOnlineButton.setText(QCoreApplication.translate("FinalCifWindow", "Checkcif Online PDF", None))
        self.structfactCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "without structure factors (faster but not complete)", None))
        self.fullIucrCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Full IUCr publication validation", None))
        self.checkDuplicatesCheckBox.setText(QCoreApplication.translate("FinalCifWindow", "Check for duplicates in CSD", None))
        self.CheckcifButton.setText(QCoreApplication.translate("FinalCifWindow", "CheckCif Offline", None))
        self.CheckcifHTMLOnlineButton.setText(QCoreApplication.translate("FinalCifWindow", "Checkcif Online HTML", None))
        self.BackFromPlatonPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.personalDepositRadioButton.setText(QCoreApplication.translate("FinalCifWindow", "personal (private) communication", None))
        self.prepublicationDepositRadioButton.setText(QCoreApplication.translate("FinalCifWindow", "prepublication", None))
        self.publishedDepositionRadioButton.setText(QCoreApplication.translate("FinalCifWindow", "already published", None))
        self.depositorUsername.setText(QCoreApplication.translate("FinalCifWindow", "depositor's username", None))
        self.label_9.setText(QCoreApplication.translate("FinalCifWindow", "depsoitor's e-mail", None))
        self.depositHKLcheckBox.setText(QCoreApplication.translate("FinalCifWindow", "deposit included hkl data or", None))
        self.Upload_hkl_pushButton.setText(QCoreApplication.translate("FinalCifWindow", "choose different hkl file", None))
        self.label_2.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p>You need to have a COD account <br/>in order to deposit a cif file. </p><p><a href=\"http://crystallography.net/cod/\"><span style=\" text-decoration: underline; color:#094fd1;\">Signup here for a new account</span></a></p></body></html>", None))
        self.depositorPasswordLabel.setText(QCoreApplication.translate("FinalCifWindow", "depositor's password", None))
        self.label_10.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-weight:600;\">A personal communication to the COD makes the uploaded CIF publicly available.</span></p></body></html>", None))
        self.ContactAuthorLabel.setText(QCoreApplication.translate("FinalCifWindow", "Publication author for contact by the COD:", None))
        self.authorsFullNamePersonalLabel.setText(QCoreApplication.translate("FinalCifWindow", "The current CIF does not contain enough author \n"
"information please add a publication author:", None))
        self.authorEditorPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Author Editor", None))
        self.label_12.setText(QCoreApplication.translate("FinalCifWindow", "Email address for contact by the COD:", None))
        self.label_8.setText(QCoreApplication.translate("FinalCifWindow", "(6-12 months)", None))
        self.embargoTimeInMonthsLabel.setText(QCoreApplication.translate("FinalCifWindow", "Hold period in months (embargo time)", None))
        self.journalMameLabel.setText(QCoreApplication.translate("FinalCifWindow", "Intended journal name (not mandatory)", None))
        self.authorsFullNamePersonalLabel_2.setText(QCoreApplication.translate("FinalCifWindow", "The current CIF does not contain all author information \n"
"please add a publication author:", None))
        self.authorEditorPushButton_2.setText(QCoreApplication.translate("FinalCifWindow", "Author Editor", None))
        self.ContactAuthorLabel_2.setText(QCoreApplication.translate("FinalCifWindow", "Publication author for contact by the COD:", None))
        self.label_15.setText(QCoreApplication.translate("FinalCifWindow", "Email address for contact by the COD:", None))
        self.cod_database_code_Label.setText(QCoreApplication.translate("FinalCifWindow", "Publication DOI:", None))
        self.label_11.setText(QCoreApplication.translate("FinalCifWindow", "Insert the DOI of the publication to which the uploaded CIF belongs.", None))
        self.GetDOIPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Get Citation", None))
        self.DOIResolveTextLabel.setText("")
        self.label_14.setText(QCoreApplication.translate("FinalCifWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#a50000;\">Files from commercial databases should not be uploaded without permission!</span></p></body></html>", None))
        self.label_deposition_output.setText(QCoreApplication.translate("FinalCifWindow", "Deposition Output:", None))
        self.StructuresListGroupBox.setTitle(QCoreApplication.translate("FinalCifWindow", "List of deposited structures", None))
        self.refreshDepositListPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Enter username and password", None))
        ___qtablewidgetitem7 = self.CODtableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("FinalCifWindow", "ID", None))
        ___qtablewidgetitem8 = self.CODtableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("FinalCifWindow", "Date", None))
        ___qtablewidgetitem9 = self.CODtableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("FinalCifWindow", "Time", None))
        self.BackFromDepositPushButton.setText(QCoreApplication.translate("FinalCifWindow", "Back to CIF Table", None))
        self.depositCIFpushButton.setText(QCoreApplication.translate("FinalCifWindow", "Deposit CIF", None))
    # retranslateUi

