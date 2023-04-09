
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGroupBox, QLabel, QCheckBox, QLineEdit
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *
from logic.FilterResult import *
from ui.UiUtility import *
from AppSetting import *
from model.PolicyEntities import *


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
        self.resultPolicyFile = None
        self.TABLE_MINIMUM_HEIGHT = 240
        self.TABLE_COLUMNS_NUMBER = 2
        self.COL_TITLE_WIDTH = 420
        self.COL_TYPE_WIDTH = 140
        self.MARGIN = 20
        self.TABLE_MIN_WIDTH = self.COL_TITLE_WIDTH + \
                               self.COL_TYPE_WIDTH + self.MARGIN
        self.COL_TITLE_INDEX = 0
        self.COL_TYPE_INDEX = 1
        self.lastRulesResult = list()
        self.BTN_WIDTH = 28
        self.BTN_HEIGHT = 28

    def initWidgets(self):
        self.lblSearch = QLabel("Search")
        self.edtSearch = QLineEdit()
        self.chkCaseSensitive = QCheckBox("Case sensitive")
        self.btnResetSearch = UiUtility.createButton(
            "Reset search",
            ICON_PATH + "reset_green.png",
            self.BTN_WIDTH,
            self.BTN_HEIGHT)
        self.tblResult = QTableWidget()
        self.layoutButton = QHBoxLayout()
        self.layoutFilter = QHBoxLayout()
        self.groupBox = QGroupBox("Analyzer result")
        self.grpLayout = QVBoxLayout()
        self.layoutSearch = QHBoxLayout()

        self.chkCaseSensitive.setChecked(False)

        self.btnAddSelected = UiUtility.createButton(
            "Add to the filters",
            ICON_PATH + "down-arrow.png",
            self.BTN_WIDTH,
            self.BTN_HEIGHT)

        self.cmbFilter = QComboBox()
        self.cmbFilter.addItem("ALL")
        for filterType in FilterType:
            self.cmbFilter.addItem(filterType.name)

        self.lblFilterType = QLabel("Filter type")

        self.tblResult.setColumnCount(self.TABLE_COLUMNS_NUMBER)
        self.tblResult.setMinimumWidth(self.TABLE_MIN_WIDTH)
        self.tblResult.setMinimumHeight(self.TABLE_MINIMUM_HEIGHT)

        self.tblResult.setColumnWidth(
            self.COL_TITLE_INDEX, self.COL_TITLE_WIDTH)
        self.tblResult.setColumnWidth(self.COL_TYPE_INDEX, self.COL_TYPE_WIDTH)
        self.tblResult.setSelectionMode(QTableWidget.SingleSelection)
        self.tblResult.setSelectionBehavior(QTableWidget.SelectRows)

    def configSignals(self):
        self.btnAddSelected.clicked.connect(self.onAddSelectedFilter)
        self.analyzerLogic.setUiUpdateAnalyzerDataSignal(
            self.onAnalyzeFinished)
        self.cmbFilter.currentIndexChanged.connect(self.onFilterChanged)
        self.edtSearch.textChanged.connect(self.onSeachTextChanged)
        self.btnResetSearch.clicked.connect(self.onResetSearch)
        self.chkCaseSensitive.clicked.connect(self.onCaseSensitiveChanged)

    def configLayout(self):
        self.layoutSearch.addWidget(self.lblSearch)
        self.layoutSearch.addWidget(self.edtSearch)
        self.layoutSearch.addWidget(self.chkCaseSensitive)
        self.layoutSearch.addWidget(self.btnResetSearch)

        self.layoutFilter.addWidget(self.lblFilterType)
        self.layoutFilter.addWidget(self.cmbFilter)

        self.layoutButton.addWidget(self.btnAddSelected)

        self.grpLayout.addLayout(self.layoutSearch)
        self.grpLayout.addLayout(self.layoutFilter)
        self.grpLayout.addWidget(self.tblResult)
        self.grpLayout.addLayout(self.layoutButton)

        self.groupBox.setLayout(self.grpLayout)

        self.addWidget(self.groupBox)

    def onCaseSensitiveChanged(self):
        self.onSeachTextChanged()

    def onAddSelectedFilter(self):
        row = self.tblResult.currentRow()
        rule = FilterRule()
        rule.exactWord = UiUtility.askQuestion(
            self.mainWindow, "Exact word",
            "Do you want to add the exact word?")
        rule.keyword = self.tblResult.item(
            row, self.COL_TITLE_INDEX).text().strip()
        rule.filterType = FilterRule.getFilterTypeFromStr(
            self.tblResult.item(row, self.COL_TYPE_INDEX).text().strip())
        self.sendToFilterUi(rule)

    def onResultAdded(self, lstRules):
        '''item = QListWidgetItem(filePath)
        self.tblResult.addItem(item)'''
        pass

    def onAnalyzeFinished(self, refPolicyFile):
        print("onAnalyzeFinished")
        if refPolicyFile is None:
            refPolicyFile = PolicyFiles()
        self.resultPolicyFile = refPolicyFile
        self.onFilterChanged()

    def onSeachTextChanged(self):
        lstRules = []
        if self.edtSearch.text().strip() != "":
            lstRules = self.searchResult(
                self.lastRulesResult,
                self.edtSearch.text().strip(),
                self.chkCaseSensitive.isChecked())
        else:
            lstRules = self.lastRulesResult
        self.updateTable(lstRules)

    def onResetSearch(self):
        self.edtSearch.setText("")

    def collectDomainRule(self, policyFile):
        domainRules = []
        if policyFile is None:
            return

        for typeDef in policyFile.typeDef:
            if typeDef.name.strip() != "":
                domainRules.append(
                    FilterRule(
                        FilterType.DOMAIN,
                        typeDef.name,
                        False))

        for seApps in policyFile.seApps:
            if seApps.domain.strip() != "":
                domainRules.append(
                    FilterRule(
                        FilterType.DOMAIN,
                        seApps.domain,
                        False))

        for context in policyFile.contexts:
            if context.domainName.strip() != "":
                domainRules.append(
                    FilterRule(
                        FilterType.DOMAIN,
                        context.domainName,
                        False))

        for attribute in policyFile.attribute:
            if attribute.name.strip() != "":
                domainRules.append(
                    FilterRule(
                        FilterType.DOMAIN,
                        attribute.name,
                        False))

        domainRules = list(set(domainRules))
        return domainRules

    def collectFilePathRule(self, policyFile):
        filePathRules = []
        if policyFile is None:
            return

        for seApps in policyFile.seApps:
            if seApps.name.strip() != "":
                filePathRules.append(
                    FilterRule(
                        FilterType.FILE_PATH,
                        seApps.name,
                        False))

        for context in policyFile.contexts:
            if context.pathName.strip() != "":
                filePathRules.append(
                    FilterRule(
                        FilterType.FILE_PATH,
                        context.pathName,
                        False))

        filePathRules = list(set(filePathRules))
        return filePathRules

    def collectPermissionRule(self, policyFile):
        permissionRules = []
        if policyFile is None:
            return

        for rule in policyFile.rules:
            if len(rule.permissions) > 0:
                for permission in rule.permissions:
                    permissionRules.append(
                        FilterRule(
                            FilterType.PERMISSION,
                            permission,
                            False))

        for macro in policyFile.macros:
            if len(macro.rules) > 0:
                for rule in macro.rules:
                    for permission in rule.permissions:
                        permissionRules.append(
                            FilterRule(
                                FilterType.PERMISSION,
                                permission,
                                False))

        permissionRules = list(set(permissionRules))
        return permissionRules

    def collectClassType(self, policyFile):
        classTypeRules = []
        if policyFile is None:
            return

        for typeDef in policyFile.typeDef:
            for type in typeDef.types:
                if type.strip() != "":
                    classTypeRules.append(
                        FilterRule(
                            FilterType.CLASS_TYPE,
                            type,
                            False))

        for context in policyFile.contexts:
            for type in context.typeDef.types:
                if type.strip() != "":
                    classTypeRules.append(
                        FilterRule(
                            FilterType.CLASS_TYPE,
                            type,
                            False))

        for rule in policyFile.rules:
            if rule.classType.strip() != "":
                classTypeRules.append(
                    FilterRule(
                        FilterType.CLASS_TYPE,
                        rule.classType,
                        False))

        classTypeRules = list(set(classTypeRules))
        return classTypeRules

    def onDispose(self):
        if self.diagram is not None:
            self.diagram.close()

    def connectToFilterUi(self, onAddFilterEvent):
        self.sendToFilterUi = onAddFilterEvent

    def onFilterChanged(self):
        '''Filter the result table based on the selected filter type,
        If it's ALL, show all the results'''
        # print("onFilterChanged")
        lstRules = []
        if self.cmbFilter.currentText() == "ALL":
            lstRules.extend(self.collectDomainRule(self.resultPolicyFile))
            lstRules.extend(self.collectFilePathRule(self.resultPolicyFile))
            lstRules.extend(self.collectPermissionRule(self.resultPolicyFile))
            lstRules.extend(self.collectClassType(self.resultPolicyFile))
        elif self.cmbFilter.currentText() == FilterType.DOMAIN.name:
            lstRules.extend(self.collectDomainRule(self.resultPolicyFile))
        elif self.cmbFilter.currentText() == FilterType.FILE_PATH.name:
            lstRules.extend(self.collectFilePathRule(self.resultPolicyFile))
        elif self.cmbFilter.currentText() == FilterType.PERMISSION.name:
            lstRules.extend(self.collectPermissionRule(self.resultPolicyFile))
        elif self.cmbFilter.currentText() == FilterType.CLASS_TYPE.name:
            lstRules.extend(self.collectClassType(self.resultPolicyFile))

        self.lastRulesResult = lstRules
        # print("Total rules: " + str(len(lstRules)))
        if self.edtSearch.text().strip() != "":
            lstRules = self.searchResult(
                lstRules,
                self.edtSearch.text().strip(),
                self.chkCaseSensitive.isChecked())

        self.updateTable(lstRules)

    def updateTable(self, lstRules):
        # print("updateTable")
        # print("Total rules: " + str(lstRules))
        lstRules = list(set(lstRules))
        self.clearTable()
        self.tblResult.setRowCount(len(lstRules))
        for i in range(len(lstRules)):
            self.tblResult.setItem(
                i, self.COL_TITLE_INDEX, QTableWidgetItem(
                    lstRules[i].keyword.strip()))
            self.tblResult.setItem(
                i, self.COL_TYPE_INDEX, QTableWidgetItem(
                    lstRules[i].filterType.name.strip()))

    def searchResult(self, lstRules, keyword, caseSensitive):
        lstSearchResult = []
        for item in lstRules:
            if self.isSimilar(keyword, item.keyword, caseSensitive):
                lstSearchResult.append(item)

        return lstSearchResult

    def clearTable(self):
        self.tblResult.clear()
        self.tblResult.setRowCount(0)

    def isSimilar(self, keyword, target, caseSensitive):
        if not caseSensitive:
            return keyword.lower() in target.lower()
        else:
            return keyword in target
