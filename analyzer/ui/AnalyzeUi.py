
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
import sys
from PythonUtilityClasses.SystemUtility import *




class AnalyzeUi(QVBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.keepResult = False
        
    def initWidgets(self):
        self.layoutAnalyzerConfig = QHBoxLayout()
        self.layoutAnalyzerAnalyze = QHBoxLayout()

        self.btnAnalyzeAll = QPushButton("Analyze All")
        self.btnAnalyzeSelected = QPushButton("Analyze Selected")
        self.btnClearAnalyze = QPushButton("Clear Analyze")
        self.btnClearOutput = QPushButton("Clear Output")

        self.chkKeepAnalyze = QCheckBox("Keep the analyze result")
        self.chkKeepAnalyze.setEnabled(False)


    def configSignals(self):
        self.btnAnalyzeAll.clicked.connect(self.onAnalyzeAll)
        self.btnAnalyzeSelected.clicked.connect(self.onAnalyzeSelectedPaths)
        self.btnClearAnalyze.clicked.connect(self.onClearAnalyze)
        self.btnClearOutput.clicked.connect(self.onClearOutput)
        self.chkKeepAnalyze.toggled.connect(self.onClickedKeepResult) 


    def configLayout(self):
        #layoutAnalyzer
        self.layoutAnalyzerAnalyze.addWidget(self.btnAnalyzeAll)
        self.layoutAnalyzerAnalyze.addWidget(self.btnAnalyzeSelected)
        self.layoutAnalyzerAnalyze.addWidget(self.btnClearAnalyze)
        self.layoutAnalyzerAnalyze.addWidget(self.btnClearOutput)

        #layoutAnalyzerConfig
        self.layoutAnalyzerConfig.addWidget(self.chkKeepAnalyze)

        self.addLayout(self.layoutAnalyzerAnalyze)
        self.addLayout(self.layoutAnalyzerConfig)

    def connectToGetSelectedPaths(self, getSelectedPath):
        self.getSelectedPaths = getSelectedPath

    def connectToGetAllPaths(self, getAllPaths):
        self.getAllPaths = getAllPaths

    def onAnalyzeSelectedPaths(self):
        paths = self.getSelectedPaths()
        self.analyzerLogic.analyzeAll(paths)

    def onAnalyzeAll(self):
        paths = self.getAllPaths()
        self.analyzerLogic.analyzeAll(paths)

    def onClearAnalyze(self):
        self.analyzerLogic.clear()     

    def onClearOutput(self):
        files = SystemUtility().getListOfFiles(os.getcwd() + "/out/","*")
        #print(files)
        for file in files :
            if os.path.isfile(file):
                #print(file)
                SystemUtility().deleteFiles(file)

    def onClickedKeepResult(self):
        self.analyzerLogic.setKeepResult( self.sender().isChecked())