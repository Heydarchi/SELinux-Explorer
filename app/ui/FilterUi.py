
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox, QLabel
from PyQt5.QtWidgets import QCheckBox, QListWidget, QListWidgetItem, QRadioButton, QComboBox
from PyQt5.QtGui import QIcon
from logic.AnalyzerLogic import *
from logic.FilterResult import *
from ui.UiUtility import *
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

        self.cmbRuleType = QComboBox()
        self.grpLayout = QHBoxLayout()
        self.groupBox = QGroupBox("Filter Rules")

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
        self.layoutFilterEntry.addWidget(self.chbxExactWord)

        self.layoutFilterButtons.addWidget(self.btnAddFilterRule)
        self.layoutFilterButtons.addWidget(self.btnRemoveSelected)
        self.layoutFilterButtons.addWidget(self.btnClearFilterRules)
        self.layoutFilterButtons.addWidget(self.btnFilter)

        self.layoutUserInput.addWidget(self.lstFilterRules)
        self.layoutUserInput.addLayout(self.layoutFilterButtons)

        self.layoutLeft.addLayout(self.grpLayout)
        self.layoutLeft.addLayout(self.layoutFilterEntry)
        self.layoutLeft.addLayout(self.layoutFilterButtons)
        self.layoutLeft.addLayout(self.layoutUserInput)

        self.groupBox.setLayout(self.layoutLeft)
        self.addWidget(self.groupBox)

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
        print("self.selectedFilterType: ", self.selectedFilterType)
        rule.filterType = FilterRule.getFilterTypeFromStr(self.cmbRuleType.currentText())

        self.onGetFilter(rule)

    def onGetFilter(self, rule):
        self.lstRules.append(rule)
        item = QListWidgetItem(rule.keyword + "  =>   Rule: " + rule.filterType.name + ", ExactWord: " +  str(rule.exactWord ))
        self.lstFilterRules.addItem(item)

    def onRemoveSelected(self):
        index = self.lstFilterRules.currentRow()
        self.lstFilterRules.takeItem(index)
        del self.lstRules[index]

    def onIndexChanged(self, i):
        self.selectedFilterType = FilterRule.getFilterTypeFromStr(self.cmbRuleType.currentText())
        print("self.selectedFilterType: ", self.selectedFilterType)

    def getSelectedFilterType(self):
        return self.selectedFilterType

    def setSelectedFilterType(self, filterType):
        if type(filterType) !=  type(FilterType):
            filterType = FilterType.DOMAIN
        self.selectedFilterType = FilterType(filterType)

