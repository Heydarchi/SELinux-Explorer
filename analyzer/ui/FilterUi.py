
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGroupBox, QLabel
from PyQt5.QtWidgets import QCheckBox, QListWidget, QListWidgetItem, QRadioButton
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
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.lstRules = list()

    def initWidgets(self):
        self.layoutFilterOption = QHBoxLayout()
        self.layoutFilterEntry = QHBoxLayout()
        self.layoutFilterButtons = QHBoxLayout()

        self.lblPattern = QLabel("Pattern")
        self.edtPattern = QLineEdit()
        self.btnFilter = QPushButton("Filter")
        self.btnAddFilterRule = QPushButton("Add")
        self.btnClearFilterRules = QPushButton("Clear Filters")
        self.btnRemoveSelected = QPushButton("Remove Selected")

        self.lstFilterRules = QListWidget()

        self.chbxExactWord = QCheckBox("Exact Word")
        self.rdDomain = QRadioButton("Domain")
        self.rdFilename = QRadioButton("File name")
        self.rdClassType = QRadioButton("Type def(Class type)")
        self.rdPermission = QRadioButton("Permission")
        self.grpLayout = QHBoxLayout()
        self.grpFilterOption = QGroupBox("Filter options")

    def configSignals(self):
        self.btnFilter.clicked.connect(self.onFilter)
        self.btnAddFilterRule.clicked.connect(self.onAddFilterRule)
        self.btnClearFilterRules.clicked.connect(self.onClearFilterRules)
        self.btnRemoveSelected.clicked.connect(self.onRemoveSelected)

    def configLayout(self):
        #layoutAnalyzer
        self.grpLayout.addWidget(self.rdDomain)
        self.grpLayout.addWidget(self.rdFilename)
        self.grpLayout.addWidget(self.rdClassType)
        self.grpLayout.addWidget(self.rdPermission)
        self.grpFilterOption.setLayout(self.grpLayout)

        #layoutAnalyzerConfig
        self.layoutFilterEntry.addWidget(self.lblPattern)
        self.layoutFilterEntry.addWidget(self.edtPattern)
        self.layoutFilterEntry.addWidget(self.chbxExactWord)
        self.layoutFilterEntry.addWidget(self.btnAddFilterRule)
        self.layoutFilterOption.addWidget(self.grpFilterOption)
        self.layoutFilterButtons.addWidget(self.btnRemoveSelected)
        self.layoutFilterButtons.addWidget(self.btnClearFilterRules)
        self.layoutFilterButtons.addWidget(self.btnFilter)

        self.addLayout(self.layoutFilterOption)
        self.addLayout(self.layoutFilterEntry)
        self.addWidget(self.lstFilterRules)
        self.addLayout(self.layoutFilterButtons)

    def onFilter(self):
        if self.isDomaineSelected():
            fileName = FilterResult().filter(self.lstRules, self.analyzerLogic.listOfPolicyFiles)
            print(fileName)
            self.analyzerLogic.onAnalyzeFinished()

    def onClearFilterRules(self):
        self.lstRules.clear()
        self.lstFilterRules.clear()

    def onAddFilterRule(self):
        rule = FilterRule()
        rule.exactWord = self.chbxExactWord.isChecked()
        rule.keyword = self.edtPattern.text().strip()
        if self.isDomaineSelected():
            rule.filterType = FilterType.DOMAIN

        if self.isFilenameSelected():
            rule.filterType = FilterType.FILE_NAME

        if self.isClassTypeSelected():
            rule.filterType = FilterType.TYPE_DEF

        if self.isPermissionSelected():
            rule.filterType = FilterType.PERMISSION

        self.lstRules.append(rule)

        item = QListWidgetItem(rule.keyword + "  =>   Rule: " + rule.filterType.name + ", ExactWord: " +  str(rule.exactWord ))
        self.lstFilterRules.addItem(item)

    def onRemoveSelected(self):
        index = self.lstFilterRules.currentRow()
        self.lstFilterRules.takeItem(index)
        del self.lstRules[index]

    def isClassTypeSelected(self):
        return self.rdClassType.isChecked()
    
    def isDomaineSelected(self):
        return self.rdDomain.isChecked()
    
    def isFilenameSelected(self):
        return self.rdFilename.isChecked()
    
    def isPermissionSelected(self):
        return self.rdPermission.isChecked()
        
    def setClassTypeSelected(self, state):
        self.rdClassType.setChecked(state)

    def setDomainSelected(self, state):
        self.rdDomain.setChecked(state)

    def setFilenameSelected(self, state):
        self.rdFilename.setChecked(state)

    def setPermissionSelected(self, state):
        self.rdPermission.setChecked(state)

