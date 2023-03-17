
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QGroupBox
from AnalyzerLogic import *
import sys
from PythonUtilityClasses.SystemUtility import *


class ResultUi(QVBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initWidgets()
        self.configSignals()
        self.configLayout()


    def initWidgets(self):
        self.lstResults = QListWidget()
        self.btnDeleteSelected = QPushButton("Delete selected")
        self.btnDeleteAll = QPushButton("Delete All")
        self.layoutButton = QHBoxLayout()
        self.grpLayout = QVBoxLayout()
        self.grpResult = QGroupBox("Results")

    def configSignals(self):
        self.btnDeleteSelected.clicked.connect(self.onDeleteSelectedFile)
        self.btnDeleteAll.clicked.connect(self.onDeleteAllFile)

    def configLayout(self):
        self.layoutButton.addWidget(self.btnDeleteSelected)
        self.layoutButton.addWidget(self.btnDeleteAll)

        self.grpLayout.addWidget(self.lstResults)
        self.grpLayout.addLayout(self.layoutButton)
        self.grpResult.setLayout(self.grpLayout)

        self.addWidget(self.grpResult)

    def onDeleteSelectedFile(self):
        pass
    
    def onDeleteAllFile(self):
        pass

