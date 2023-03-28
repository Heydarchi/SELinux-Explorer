
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QGroupBox, QLabel
from PyQt5.QtWidgets import QCheckBox, QListWidget, QListWidgetItem, QRadioButton, QComboBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from AnalyzerLogic import *
from FilterResult import *
from ui.UiUtility import *
import sys
from PythonUtilityClasses.SystemUtility import *




class FilterUi(QHBoxLayout):
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
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_MAX_WIDTH = 360        
        self.BTN_WIDTH = 24        
        self.BTN_HEIGHT = 24        
        self.selectedFilterType = None

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.layoutUserInput = QHBoxLayout()
        self.layoutFilterEntry = QHBoxLayout()
        self.layoutFilterButtons = QVBoxLayout()

        self.layoutLeft = QVBoxLayout()

        self.lblPattern = QLabel("Pattern")
        self.lblFilterType = QLabel("Rule type")
        self.edtPattern = QLineEdit()

        self.btnFilter =UiUtility.createButton("Generate output", QIcon(iconPath + "filter.png"), self.BTN_WIDTH, self.BTN_HEIGHT)        
        self.btnAddFilterRule =UiUtility.createButton("Add a new filter", QIcon(iconPath + "add.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btnClearFilterRules =UiUtility.createButton("Clear all the filters", QIcon(iconPath + "broom.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btnRemoveSelected =UiUtility.createButton("Remove the selected filter", QIcon(iconPath + "minus.png"), self.BTN_WIDTH, self.BTN_HEIGHT)

        self.lstFilterRules = QListWidget()

        self.chbxExactWord = QCheckBox("Exact Word")
        self.rdDomain = QRadioButton("Domain")
        self.rdFilename = QRadioButton("File name")
        self.rdClassType = QRadioButton("Type def(Class type)")
        self.rdPermission = QRadioButton("Permission")

        self.cmbRuleType = QComboBox()
        self.grpLayout = QHBoxLayout()

        for filterType in FilterType:
            self.cmbRuleType.addItem(filterType.name)        

    def configSignals(self):
        self.btnFilter.clicked.connect(self.onFilter)
        self.btnAddFilterRule.clicked.connect(self.onAddFilterRule)
        self.btnClearFilterRules.clicked.connect(self.onClearFilterRules)
        self.btnRemoveSelected.clicked.connect(self.onRemoveSelected)
        self.cmbRuleType.currentIndexChanged.connect(self.onIndexChanged)

    def configLayout(self):
        #layoutAnalyzer
        self.grpLayout.addWidget(self.lblFilterType)
        self.grpLayout.addWidget(self.cmbRuleType)

        #layoutAnalyzerConfig
        self.layoutFilterEntry.addWidget(self.lblPattern)
        self.layoutFilterEntry.addWidget(self.edtPattern)

        self.layoutFilterButtons.addWidget(self.btnAddFilterRule)
        self.layoutFilterButtons.addWidget(self.btnRemoveSelected)
        self.layoutFilterButtons.addWidget(self.btnClearFilterRules)
        self.layoutFilterButtons.addWidget(self.btnFilter)

        self.layoutUserInput.addWidget(self.lstFilterRules)
        self.layoutUserInput.addLayout(self.layoutFilterButtons)

        self.layoutLeft.addLayout(self.grpLayout)
        self.layoutLeft.addLayout(self.layoutFilterEntry)
        self.layoutLeft.addWidget(self.chbxExactWord)
        self.layoutLeft.addLayout(self.layoutFilterButtons)
        self.layoutLeft.addLayout(self.layoutUserInput)

        self.addLayout(self.layoutLeft)

    def onFilter(self):
        #if self.selectedFilterType == FilterType.DOMAIN:
            fileName, filteredPolicyFile = FilterResult().filter(self.lstRules, self.analyzerLogic.listOfPolicyFiles)
            print(fileName)
            self.analyzerLogic.onAnalyzeFinished(filteredPolicyFile)

    def onClearFilterRules(self):
        self.lstRules.clear()
        self.lstFilterRules.clear()

    def onAddFilterRule(self):
        rule = FilterRule()
        rule.exactWord = self.chbxExactWord.isChecked()
        rule.keyword = self.edtPattern.text().strip()
        rule.filterType = FilterType(self.selectedFilterType)
        self.lstRules.append(rule)

        item = QListWidgetItem(rule.keyword + "  =>   Rule: " + rule.filterType.name + ", ExactWord: " +  str(rule.exactWord ))
        self.lstFilterRules.addItem(item)

    def onRemoveSelected(self):
        index = self.lstFilterRules.currentRow()
        self.lstFilterRules.takeItem(index)
        del self.lstRules[index]

    def onIndexChanged(self, i):
        for filterType in FilterType:
            if self.cmbRuleType.currentText == filterType.name:
                self.selectedFilterType = filterType
                break

    def getSelectedFilterType(self):
        return self.selectedFilterType

    def setSelectedFilterType(self, filterType):
        if type(filterType) !=  type(FilterType):
            filterType = FilterType.DOMAIN
        self.selectedFilterType = FilterType(filterType)

