
from PyQt5.QtWidgets import QStatusBar
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *


class StatusbarUi(QStatusBar):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        pass

    def initWidgets(self):
        pass

    def configSignals(self):
        pass

    def configLayout(self):
        pass

    def onDeleteSelectedFile(self):
        items = self.lstResults.selectedItems()
        for item in items:
            path = item.text()

    def onDeleteAllFile(self):
        self.analyzerLogic.clearOutput()

    def onResultAdded(self, filePath):
        item = QListWidgetItem(filePath)
        self.lstResults.addItem(item)

    def onAnalyzeFinished(self):
        self.lstResults.clear()
        for file in self.analyzerLogic.listOfDiagrams:
            self.lstResults.addItem(QListWidgetItem(file))

    def onSelectedResult(self):
        listItems = self.lstResults.selectedItems()
        if len(listItems) > 0:
            self.diagram = DiagramWindow(listItems[0].text())
            self.diagram.show()
