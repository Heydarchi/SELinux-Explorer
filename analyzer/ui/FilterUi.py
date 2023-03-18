
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGroupBox, QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
from FilterResult import *
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

        self.chbxExactWord = QCheckBox("Exact Word")
        self.chbxDomain = QCheckBox("Domain")
        self.chbxFilename = QCheckBox("File name")
        self.chbxClassType = QCheckBox("Type def(Class type)")
        self.chbxPermission = QCheckBox("Permission")
        self.grpLayout = QHBoxLayout()
        self.grpFilterOption = QGroupBox("Filter options")

    def configSignals(self):
        self.btnFilter.clicked.connect(self.onFilter)

    def configLayout(self):
        #layoutAnalyzer
        self.grpLayout.addWidget(self.chbxDomain)
        self.grpLayout.addWidget(self.chbxFilename)
        self.grpLayout.addWidget(self.chbxClassType)
        self.grpLayout.addWidget(self.chbxPermission)
        self.grpFilterOption.setLayout(self.grpLayout)

        #layoutAnalyzerConfig
        self.layoutFilterEntry.addWidget(self.lblPattern)
        self.layoutFilterEntry.addWidget(self.edtPattern)
        self.layoutFilterEntry.addWidget(self.chbxExactWord)
        self.layoutFilterEntry.addWidget(self.btnFilter)
        self.layoutFilterOption.addWidget(self.grpFilterOption)
        self.addLayout(self.layoutFilterOption)
        self.addLayout(self.layoutFilterEntry)

    def onFilter(self):
        if self.isDomaineSelected():
            fileName = FilterResult().filterDomain(self.edtPattern.text(), self.analyzerLogic.listOfPolicyFiles, self.chbxExactWord.isChecked())
            print(fileName)
            self.analyzerLogic.onAnalyzeFinished()

    def isClassTypeSelected(self):
        return self.chbxClassType.isChecked()
    
    def isDomaineSelected(self):
        return self.chbxDomain.isChecked()
    
    def isFilenameSelected(self):
        return self.chbxFilename.isChecked()
    
    def isPermissionSelected(self):
        return self.chbxPermission.isChecked()
        
    def setClassTypeSelected(self, state):
        self.chbxClassType.setChecked(state)

    def setDomainSelected(self, state):
        self.chbxDomain.setChecked(state)

    def setFilenameSelected(self, state):
        self.chbxFilename.setChecked(state)

    def setPermissionSelected(self, state):
        self.chbxPermission.setChecked(state)

