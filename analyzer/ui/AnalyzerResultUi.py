
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,QTableWidgetItem
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
        self.TABLE_MAX_WIDTH = 240  

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.tblResult = QTableWidget()
        self.layoutButton = QHBoxLayout()
        self.grpLayout = QVBoxLayout()

        self.btnAddSelected = QPushButton(icon = QIcon(iconPath + "add.png"))
        self.btnAddSelected.setToolTip("Add to the filters")
        self.btnAddSelected.setMinimumSize(24,24)
        self.btnAddSelected.setIconSize(QSize(24,24))

        self.tblResult.setColumnCount(2)
        self.tblResult.setMaximumWidth(self.TABLE_MAX_WIDTH)
        self.tblResult.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

    def configSignals(self):
        self.btnAddSelected.clicked.connect(self.onAddSelectedFile)
        self.tblResult.itemClicked.connect(self.onSelectedResult) 

        #self.analyzerLogic.setUiUpdateSignal(self.onAnalyzeFinished)

    def configLayout(self):
        self.layoutButton.addWidget(self.btnAddSelected)

        self.grpLayout.addWidget(self.tblResult)
        self.grpLayout.addLayout(self.layoutButton)

        self.addLayout(self.grpLayout)

    def onAddSelectedFile(self):
        '''items = self.tblResult.selectedItems()
        for item in items:
            path = item.text()'''
        pass

    def onResultAdded(self, lstRules):
        '''item = QListWidgetItem(filePath)
        self.tblResult.addItem(item)'''
        pass

    def onAnalyzeFinished(self):
        '''self.tblResult.clear()
        for file in self.analyzerLogic.listOfDiagrams:
            self.tblResult.addItem(QListWidgetItem(file))'''
        pass

    def onSelectedResult(self):
        listItems=self.tblResult.selectedItems()
        if len(listItems) > 0:
            self.diagram = DiagramWindow(listItems[0].text())
            self.diagram.show()

    def onDispose(self):
        if self.diagram != None :
            self.diagram.close()