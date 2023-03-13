
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGroupBox, QRadioButton, QLabel
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
import sys
from PythonUtilityClasses.SystemUtility import *




class FilterUi(QVBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initWidgets()
        self.configSignals()
        self.configLayout()


    def initWidgets(self):
        self.layoutFilterOption = QHBoxLayout()
        self.layoutFilterEntry = QHBoxLayout()

        self.lblPattern = QLabel("Pattern")
        self.edtPattern = QLineEdit()
        self.btnFilter = QPushButton("Filter")

        self.rdbBtnDomain = QRadioButton("Domain")
        self.rdbBtnFilename = QRadioButton("File name")
        self.rdbBtnClassType = QRadioButton("Type def(Class type)")
        self.rdbBtnPermission = QRadioButton("Permission")
        self.grpLayout = QHBoxLayout()
        self.grpFilterOption = QGroupBox("Filter options")

    def configSignals(self):
        pass

    def configLayout(self):
        #layoutAnalyzer
        self.grpLayout.addWidget(self.rdbBtnDomain)
        self.grpLayout.addWidget(self.rdbBtnFilename)
        self.grpLayout.addWidget(self.rdbBtnClassType)
        self.grpLayout.addWidget(self.rdbBtnPermission)
        self.grpFilterOption.setLayout(self.grpLayout)

        #layoutAnalyzerConfig
        self.layoutFilterEntry.addWidget(self.lblPattern)
        self.layoutFilterEntry.addWidget(self.edtPattern)
        self.layoutFilterEntry.addWidget(self.btnFilter)
        self.layoutFilterOption.addWidget(self.grpFilterOption)
        self.addLayout(self.layoutFilterOption)
        self.addLayout(self.layoutFilterEntry)
