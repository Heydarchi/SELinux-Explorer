
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox, QLabel
from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QTableWidget, QComboBox
from PyQt5.QtGui import QIcon
from logic.AnalyzerLogic import *
from logic.FilterResult import *
from ui.UiUtility import *
from PythonUtilityClasses.SystemUtility import *
from AppSetting import *



class FilterUi(QHBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initVariables()
        self.initLayout()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.lstRules = list()
        self.BTN_WIDTH = 28
        self.BTN_HEIGHT = 48
        self.selectedFilterType = None
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 3
        self.COL_TITLE_WIDTH = 320
        self.COL_TYPE_WIDTH = 140
        self.COL_EXACT_WORD_WIDTH = 100
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + self.COL_TYPE_WIDTH + self.MARGIN + self.COL_EXACT_WORD_WIDTH
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1
        self.COL_EXACT_WORD_INDEX = 2

    def initWidgets(self):
        self.tblRule = QTableWidget()
        self.lblPattern = QLabel("Pattern")
        self.lblFilterType = QLabel("Rule type")
        self.edtPattern = QLineEdit()

        self.btnFilter =UiUtility.createButton("Generate output", QIcon(ICON_PATH + "filter.png"), self.BTN_WIDTH, self.BTN_HEIGHT)        
        self.btnAddFilterRule =UiUtility.createButton("Add a new filter", QIcon(ICON_PATH + "add.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btnClearFilterRules =UiUtility.createButton("Clear all the filters", QIcon(ICON_PATH + "broom.png"), self.BTN_WIDTH, self.BTN_HEIGHT)
        self.btnRemoveSelected =UiUtility.createButton("Remove the selected filter", QIcon(ICON_PATH + "minus.png"), self.BTN_WIDTH, self.BTN_HEIGHT)


        self.chbxExactWord = QCheckBox("Exact Word")

        self.cmbRuleType = QComboBox()
        self.groupBox = QGroupBox("Filter Rules")

        for filterType in FilterType:
            self.cmbRuleType.addItem(filterType.name)   
            
        self.tblRule.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tblRule.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tblRule.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tblRule.setColumnWidth(self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tblRule.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tblRule.setColumnWidth(self.COL_EXACT_WORD_INDEX, self.COL_EXACT_WORD_WIDTH)
        self.tblRule.setSelectionMode(QTableWidget.SingleSelection)
        self.tblRule.setSelectionBehavior(QTableWidget.SelectRows)

    def initLayout(self):
        self.layoutLeft = QVBoxLayout()
        self.layoutFilterEntry = QHBoxLayout()
        self.layoutFilterButtons = QVBoxLayout()
        self.layoutUserInput = QHBoxLayout()
        self.grpLayout = QHBoxLayout()


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

        self.layoutUserInput.addWidget(self.tblRule)
        self.layoutUserInput.addLayout(self.layoutFilterButtons)

        self.layoutLeft.addLayout(self.grpLayout)
        self.layoutLeft.addLayout(self.layoutFilterEntry)
        self.layoutLeft.addLayout(self.layoutFilterButtons)
        self.layoutLeft.addLayout(self.layoutUserInput)

        self.groupBox.setMinimumWidth(self.TABLE_MIN_WIDTH + 3 * self.BTN_WIDTH )
        self.groupBox.setLayout(self.layoutLeft)
        self.addWidget(self.groupBox)


    def onFilter(self):
        #if self.selectedFilterType == FilterType.DOMAIN:
            fileName, filteredPolicyFile = FilterResult().filter(self.lstRules, self.analyzerLogic.listOfPolicyFiles)
            print(fileName)
            self.analyzerLogic.onAnalyzeFinished(filteredPolicyFile)

    def onClearFilterRules(self):
        self.lstRules.clear()
        self.tblRule.clear()
        self.tblRule.setRowCount(0)

    def onAddFilterRule(self):
        rule = FilterRule()
        rule.exactWord = self.chbxExactWord.isChecked()
        rule.keyword = self.edtPattern.text().strip()
        print("self.selectedFilterType: ", self.selectedFilterType)
        rule.filterType = FilterRule.getFilterTypeFromStr(self.cmbRuleType.currentText())

        self.onGetFilter(rule)

    def onGetFilter(self, rule):
        self.lstRules.append(rule)
        index = self.tblRule.rowCount()
        self.tblRule.setRowCount(index + 1)
        self.tblRule.setItem(index, self.COL_TITLE_INDEX, QTableWidgetItem(rule.keyword.strip()))
        self.tblRule.setItem(index, self.COL_TYPE_INDEX, QTableWidgetItem(rule.filterType.name.strip()))
        self.tblRule.setItem(index, self.COL_EXACT_WORD_INDEX, QTableWidgetItem(str(rule.exactWord)))
    def onRemoveSelected(self):
        row = self.tblRule.currentRow()
        index = self.tblRule.selectedIndexes()[0].row()
        print("index: ", index)
        print("selectedIndex: ", self.tblRule.selectedIndexes())
        self.tblRule.removeRow(row)
        print("self.lstRules: ", self.lstRules)
        del self.lstRules[index]
        print("self.lstRules: ", self.lstRules)

    def onIndexChanged(self, i):
        self.selectedFilterType = FilterRule.getFilterTypeFromStr(self.cmbRuleType.currentText())
        print("self.selectedFilterType: ", self.selectedFilterType)

    def getSelectedFilterType(self):
        return self.selectedFilterType

    def setSelectedFilterType(self, filterType):
        if type(filterType) !=  type(FilterType):
            filterType = FilterType.DOMAIN
        self.selectedFilterType = FilterType(filterType)

