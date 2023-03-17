
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
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
        self.layoutPath = QHBoxLayout()
        self.layoutSelectedPath = QHBoxLayout()
        self.layoutSelectedPathButton = QVBoxLayout()

        self.lblPath = QLabel("Path")
        self.lblSelectedPath = QLabel("Selected Path")
        self.edtCurrentSelectedPath = QLineEdit()

        self.lstSelectedPath = QListWidget()

        self.btnBrowseFile = QPushButton("Browse File")
        self.btnBrowseFolder = QPushButton("Browse Folder")
        self.btnAddToList = QPushButton("Add to")
        self.btnRemoveFromList = QPushButton("Remove from")


    def configSignals(self):
        self.btnBrowseFile.clicked.connect(self.browseFilePath)
        self.btnBrowseFolder.clicked.connect(self.browseFolderPath)
        self.btnAddToList.clicked.connect(self.addSelectedPathToList)
        self.btnRemoveFromList.clicked.connect(self.removeFromTheList)


    def configLayout(self):
        #layoutPath
        self.edtCurrentSelectedPath.setFixedWidth(500)
        self.edtCurrentSelectedPath.setReadOnly(True)

        self.layoutPath.addWidget(self.lblPath)
        self.layoutPath.addWidget(self.edtCurrentSelectedPath)
        self.layoutPath.addWidget(self.btnBrowseFile)
        self.layoutPath.addWidget(self.btnBrowseFolder)
        self.layoutPath.addStretch()

        #layoutSelectedPath
        self.layoutSelectedPathButton.addWidget(self.btnAddToList)
        self.layoutSelectedPathButton.addWidget(self.btnRemoveFromList)

        self.lblSelectedPath.setAlignment(Qt.AlignTop)
        self.lstSelectedPath.setFixedHeight(120)
        self.layoutSelectedPath.setAlignment(Qt.AlignTop)

        self.layoutSelectedPath.addLayout(self.layoutSelectedPathButton)
        self.layoutSelectedPath.addWidget(self.lstSelectedPath)

        self.addLayout(self.layoutPath)
        self.addLayout(self.layoutSelectedPath)


    def browseFilePath(self):
        dlg = QFileDialog(directory = self.lastOpenedPath)
        if dlg.exec_():
            self.edtCurrentSelectedPath.setText(dlg.selectedFiles()[0])
            self.lastOpenedPath = self.edtCurrentSelectedPath.text()

    def browseFolderPath(self):
        self.edtCurrentSelectedPath.setText(QFileDialog(directory = self.lastOpenedPath).getExistingDirectory(self.mainWindow, 'Hey! Select a Folder', options=QFileDialog.ShowDirsOnly))
        self.lastOpenedPath = self.edtCurrentSelectedPath.text()

    def addSelectedPathToList(self):
        item = QListWidgetItem(self.edtCurrentSelectedPath.text())
        print(self.edtCurrentSelectedPath.text())
        self.lstSelectedPath.addItem(item)

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