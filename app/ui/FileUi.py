
from PyQt5.QtWidgets import QGroupBox, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from logic.AnalyzerLogic import *
import sys




class FileUi(QVBoxLayout):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.lastOpenedPath = ""
        self.LIST_MINIMUM_HEIGHT = 120
        self.LIST_MINIMUM_WIDTH = 680

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.grpResult = QGroupBox("Files and Paths")

        self.layoutSelectedPath = QVBoxLayout()
        self.layoutSelectedPathButton = QVBoxLayout()

        self.lstSelectedPath = QListWidget()
        self.btnRemoveFromList = QPushButton(icon = QIcon(iconPath + "delete.png"))
        self.btnRemoveFromList.setToolTip("Remove selected item from the list")
        self.btnRemoveFromList.setMinimumSize(24,24)
        self.btnRemoveFromList.setIconSize(QSize(24,24))

    def configSignals(self):
        self.btnRemoveFromList.clicked.connect(self.removeFromTheList)


    def configLayout(self):

        #layoutSelectedPath
        self.layoutSelectedPathButton.addWidget(self.btnRemoveFromList)
        self.layoutSelectedPathButton.setAlignment(Qt.AlignTop)

        self.lstSelectedPath.setMinimumHeight(self.LIST_MINIMUM_HEIGHT)
        self.lstSelectedPath.setMinimumWidth(self.LIST_MINIMUM_WIDTH)
        self.layoutSelectedPath.setAlignment(Qt.AlignTop)

        self.layoutSelectedPath.addWidget(self.lstSelectedPath)
        self.layoutSelectedPath.addLayout(self.layoutSelectedPathButton)


        self.grpResult.setLayout(self.layoutSelectedPath)

        self.addWidget(self.grpResult)
        #self.addLayout(self.layoutSelectedPath)


    def removeFromTheList(self):
        listItems=self.lstSelectedPath.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.lstSelectedPath.takeItem(self.lstSelectedPath.row(item))

    def getSelectedPaths(self):
        paths = list()
        items = self.lstSelectedPath.selectedItems()
        for item in items:
            paths.append(item.text())
        return paths
    
    def getAllPaths(self):
        paths = list()
        for i in range(self.lstSelectedPath.count()):
            paths.append(self.lstSelectedPath.item(i).text())
        return paths
    
    def onAddFileFolder(self, path):
        print(path)
        item = QListWidgetItem(path)
        self.lstSelectedPath.addItem(item)
