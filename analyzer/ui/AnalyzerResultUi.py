
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,QTableWidgetItem, QGroupBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDesktopWidget
from AnalyzerLogic import *
import sys
from PythonUtilityClasses.SystemUtility import *
from FilterResult import *



class AnalyzerResultUi(QVBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.diagram = None
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 3
        self.COL_TITLE_WIDTH = 320
        self.COL_TYPE_WIDTH = 140
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + self.COL_TYPE_WIDTH + self.MARGIN
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1
        self.COL_TYPE_ENUM_INDEX = 2

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.tblResult = QTableWidget()
        self.layoutButton = QHBoxLayout()
        self.groupBox = QGroupBox("Analyzer result")
        self.grpLayout = QVBoxLayout()

        self.btnAddSelected = QPushButton(icon = QIcon(iconPath + "add.png"))
        self.btnAddSelected.setToolTip("Add to the filters")
        self.btnAddSelected.setMinimumSize(24,24)
        self.btnAddSelected.setIconSize(QSize(24,24))

        self.tblResult.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tblResult.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tblResult.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tblResult.setColumnWidth(self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tblResult.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tblResult.setColumnHidden(self.COL_TYPE_ENUM_INDEX, True)


    def configSignals(self):
        self.btnAddSelected.clicked.connect(self.onAddSelectedFilter)
        #self.tblResult.itemClicked.connect(self.onSelectedResult) 

        self.analyzerLogic.setUiUpdateAnalyzerDataSignal(self.onAnalyzeFinished)

    def configLayout(self):
        self.layoutButton.addWidget(self.btnAddSelected)

        self.grpLayout.addWidget(self.tblResult)
        self.grpLayout.addLayout(self.layoutButton)

        self.groupBox.setLayout(self.grpLayout)

        self.addWidget(self.groupBox)

    def onAddSelectedFilter(self):
        row = self.tblResult.currentRow()
        rule = FilterRule()
        rule.exactWord = False
        rule.keyword = self.tblResult.item(row, self.COL_TITLE_INDEX).text() 
        rule.filterType = FilterType(int(self.tblResult.item(row, self.COL_TYPE_ENUM_INDEX).text()))
        self.sendToFilterUi(rule)

    def onResultAdded(self, lstRules):
        '''item = QListWidgetItem(filePath)
        self.tblResult.addItem(item)'''
        pass

    def onAnalyzeFinished(self, policyFiles):
        if policyFiles == None:
            self.tblResult.clear()
            self.tblResult.setRowCount(0)

            return

        for policyFile in policyFiles:
            if policyFile == None:
                self.tblResult.clear()
                self.tblResult.setRowCount(0)
                return
            
            for typeDef in policyFile.typeDef:
                if typeDef.name.strip() != "":
                    index = self.tblResult.rowCount()
                    self.tblResult.insertRow(index)
                    self.tblResult.setItem(index , self.COL_TITLE_INDEX, QTableWidgetItem(typeDef.name))
                    self.tblResult.setItem(index , self.COL_TYPE_INDEX, QTableWidgetItem(FilterType.DOMAIN.name))
                    self.tblResult.setItem(index , self.COL_TYPE_ENUM_INDEX, QTableWidgetItem(str(FilterType.DOMAIN.value)))

            for seApps in policyFile.seApps:
                if seApps.domain.strip() != "":
                    index = self.tblResult.rowCount()
                    self.tblResult.insertRow(index)
                    self.tblResult.setItem(index , self.COL_TITLE_INDEX, QTableWidgetItem(seApps.domain))
                    self.tblResult.setItem(index , self.COL_TYPE_INDEX, QTableWidgetItem(FilterType.DOMAIN.name))
                    self.tblResult.setItem(index , self.COL_TYPE_ENUM_INDEX, QTableWidgetItem(str(FilterType.DOMAIN.value)))

            for context in policyFile.contexts:
                if context.domainName.strip() != "":
                    index = self.tblResult.rowCount()
                    self.tblResult.insertRow(index)
                    self.tblResult.setItem(index , self.COL_TITLE_INDEX, QTableWidgetItem(context.domainName))
                    self.tblResult.setItem(index , self.COL_TYPE_INDEX, QTableWidgetItem(FilterType.DOMAIN.name))
                    self.tblResult.setItem(index , self.COL_TYPE_ENUM_INDEX, QTableWidgetItem(str(FilterType.DOMAIN.value)))

            for context in policyFile.contexts:
                if context.pathName.strip() != "":
                    index = self.tblResult.rowCount()
                    self.tblResult.insertRow(index)
                    self.tblResult.setItem(index , self.COL_TITLE_INDEX, QTableWidgetItem(context.pathName))
                    self.tblResult.setItem(index , self.COL_TYPE_INDEX, QTableWidgetItem(FilterType.FILE_NAME.name))
                    self.tblResult.setItem(index , self.COL_TYPE_ENUM_INDEX, QTableWidgetItem(str(FilterType.FILE_NAME.value)))


    def onDispose(self):
        if self.diagram != None :
            self.diagram.close()

    def connectToFilterUi(self, onAddFilterEvent):
        self.sendToFilterUi = onAddFilterEvent