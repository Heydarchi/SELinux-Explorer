
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QGroupBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *
from logic.FilterResult import *



class AnalyzerResultUi(QVBoxLayout):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        self.diagram = None
        self.resultPolicyFiles = None
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 2
        self.COL_TITLE_WIDTH = 320
        self.COL_TYPE_WIDTH = 140
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + self.COL_TYPE_WIDTH + self.MARGIN
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1

    def initWidgets(self):
        iconPath = './ui/icons/'

        self.tblResult = QTableWidget()
        self.layoutButton = QHBoxLayout()
        self.layoutFilter = QHBoxLayout()
        self.groupBox = QGroupBox("Analyzer result")
        self.grpLayout = QVBoxLayout()

        self.btnAddSelected = QPushButton(icon = QIcon(iconPath + "down-arrow.png"))
        self.btnAddSelected.setToolTip("Add to the filters")
        self.btnAddSelected.setMinimumSize(24,24)
        self.btnAddSelected.setIconSize(QSize(24,24))

        self.cmbFilter = QComboBox()
        self.cmbFilter.addItem("ALL")
        for filterType in FilterType:
            self.cmbFilter.addItem(filterType.name)

        self.lblFilterType = QLabel("Filter type")

        self.tblResult.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tblResult.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tblResult.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tblResult.setColumnWidth(self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tblResult.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tblResult.setSelectionMode(QTableWidget.SingleSelection)
        self.tblResult.setSelectionBehavior(QTableWidget.SelectRows)

    def configSignals(self):
        self.btnAddSelected.clicked.connect(self.onAddSelectedFilter)
        self.analyzerLogic.setUiUpdateAnalyzerDataSignal(self.onAnalyzeFinished)
        self.cmbFilter.currentIndexChanged.connect(self.onFilterChanged)

    def configLayout(self):
        self.layoutFilter.addWidget(self.lblFilterType)
        self.layoutFilter.addWidget(self.cmbFilter)

        self.layoutButton.addWidget(self.btnAddSelected)

        self.grpLayout.addLayout(self.layoutFilter)
        self.grpLayout.addWidget(self.tblResult)
        self.grpLayout.addLayout(self.layoutButton)

        self.groupBox.setLayout(self.grpLayout)

        self.addWidget(self.groupBox)

    def onAddSelectedFilter(self):
        row = self.tblResult.currentRow()
        rule = FilterRule()
        rule.exactWord = False
        rule.keyword = self.tblResult.item(row, self.COL_TITLE_INDEX).text() 
        rule.filterType =FilterRule.getFilterTypeFromStr(self.tblResult.item(row, self.COL_TYPE_INDEX).text())
        self.sendToFilterUi(rule)

    def onResultAdded(self, lstRules):
        '''item = QListWidgetItem(filePath)
        self.tblResult.addItem(item)'''
        pass

    def onAnalyzeFinished(self, policyFiles):
        if policyFiles == None:
            return
        print("onAnalyzeFinished: ", len(policyFiles))
        self.resultPolicyFiles = policyFiles
        self.onFilterChanged()


    def collectDomainRule(self, policyFiles):
        domainRules = []
        for policyFile in policyFiles:
            if policyFile == None:
                return

            for typeDef in policyFile.typeDef:
                if typeDef.name.strip() != "":
                    domainRules.append(FilterRule(FilterType.DOMAIN, typeDef.name, False))

            for seApps in policyFile.seApps:
                if seApps.domain.strip() != "":
                    domainRules.append(FilterRule(FilterType.DOMAIN, seApps.domain, False))

            for context in policyFile.contexts:
                if context.domainName.strip() != "":
                    domainRules.append(FilterRule(FilterType.DOMAIN, context.domainName, False))

        return domainRules

    def collectFilePathRule(self, policyFiles):
        filePathRules = []
        for policyFile in policyFiles:
            if policyFile == None:
                return

            for seApps in policyFile.seApps:
                if seApps.name.strip() != "":
                    filePathRules.append(FilterRule(FilterType.FILE_PATH, seApps.name, False))

            for context in policyFile.contexts:
                if context.pathName.strip() != "":
                    filePathRules.append(FilterRule(FilterType.FILE_PATH, context.pathName, False))

        return filePathRules

    def collectFileNameRule(self, policyFiles):
        fileNameRules = []
        for policyFile in policyFiles:
            if policyFile == None:
                return

            if policyFile.fileName.strip() !="" :
                fileNameRules.append(FilterRule(FilterType.FILE_NAME, policyFile.fileName, False))
        return fileNameRules

    def collectPermissionRule(self, policyFiles):
        permissionRules = []
        for policyFile in policyFiles:
            if policyFile == None:
                return

            for rule in policyFile.rules:
                if len(rule.permissions) > 0:
                    for permission in rule.permissions:
                        permissionRules.append(FilterRule(FilterType.PERMISSION, permission, False))

        permissionRules = list(set(permissionRules))
        return permissionRules

    def onDispose(self):
        if self.diagram != None :
            self.diagram.close()

    def connectToFilterUi(self, onAddFilterEvent):
        self.sendToFilterUi = onAddFilterEvent

    def onFilterChanged(self):
        "Filter the result table based on the selected filter type, If it's ALL, show all the results"
        lstRules = []
        if self.cmbFilter.currentText() == "ALL":
            lstRules.extend(self.collectDomainRule(self.resultPolicyFiles))
            lstRules.extend(self.collectFilePathRule(self.resultPolicyFiles))
            lstRules.extend(self.collectPermissionRule(self.resultPolicyFiles))
            lstRules.extend(self.collectFileNameRule(self.resultPolicyFiles))
        elif self.cmbFilter.currentText() == FilterType.DOMAIN.name:
            lstRules.extend(self.collectDomainRule(self.resultPolicyFiles))
        elif self.cmbFilter.currentText() == FilterType.FILE_PATH.name:
            lstRules.extend(self.collectFilePathRule(self.resultPolicyFiles))
        elif self.cmbFilter.currentText() == FilterType.FILE_NAME.name:
            lstRules.extend(self.collectFileNameRule(self.resultPolicyFiles))
        elif self.cmbFilter.currentText() == FilterType.PERMISSION.name:
            lstRules.extend(self.collectPermissionRule(self.resultPolicyFiles))

        self.updateTable(lstRules)


    def updateTable(self, lstRules):
        self.clearTable()
        self.tblResult.setRowCount(len(lstRules))
        for i in range(len(lstRules)):
            self.tblResult.setItem(i, self.COL_TITLE_INDEX, QTableWidgetItem(lstRules[i].keyword))
            self.tblResult.setItem(i, self.COL_TYPE_INDEX, QTableWidgetItem(lstRules[i].filterType.name))
    def clearTable(self):
        self.tblResult.clear()
        self.tblResult.setRowCount(0)