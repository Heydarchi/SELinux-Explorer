
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from AnalyzerLogic import *
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

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.layoutSelectedPath = QHBoxLayout()
        self.layoutSelectedPathButton = QVBoxLayout()

        self.lstSelectedPath = QListWidget()
        self.btnRemoveFromList = QPushButton(icon = QIcon(iconPath + "minus.png"))
        self.btnRemoveFromList.setToolTip("Remove selected item from the list")
        self.btnRemoveFromList.setMinimumSize(24,24)
        self.btnRemoveFromList.setIconSize(QSize(24,24))

    def configSignals(self):
        self.btnRemoveFromList.clicked.connect(self.removeFromTheList)


    def configLayout(self):

        #layoutSelectedPath
        self.layoutSelectedPathButton.addWidget(self.btnRemoveFromList)
        self.layoutSelectedPathButton.setAlignment(Qt.AlignTop)

        self.lstSelectedPath.setFixedHeight(120)
        self.layoutSelectedPath.setAlignment(Qt.AlignTop)

        self.layoutSelectedPath.addWidget(self.lstSelectedPath)
        self.layoutSelectedPath.addLayout(self.layoutSelectedPathButton)

        self.addLayout(self.layoutSelectedPath)


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
