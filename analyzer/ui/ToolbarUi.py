
from PyQt5.QtWidgets import QAction, QToolBar, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from AnalyzerLogic import *
from PyQt5.QtCore import Qt
import sys
from PythonUtilityClasses.SystemUtility import *



class ToolbarUi(QToolBar):
    def __init__(self, mainWindow, analyzerLogic, appSetting):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic
        self.appSetting = appSetting
        self.initVariables()
        self.initWidgets()
        self.configSignals()
        self.configLayout()

    def initVariables(self):
        pass

    def initWidgets(self):
        iconPath = './ui/icons/'
        self.actAddFile = QAction(QIcon(iconPath + 'add-file.png'),"Add a file to the list", self.mainWindow)
        self.actAddPath = QAction(QIcon(iconPath + 'add-folder.png'),"Add a Path to the list", self.mainWindow)
        self.actRemoveOutput = QAction(QIcon(iconPath + 'remove.png'),"Remove Outputs", self.mainWindow)
        self.actClearAnalyze = QAction(QIcon(iconPath + 'reset.png'),"Clear Analyze", self.mainWindow)
        self.actWipeAll = QAction(QIcon(iconPath + 'broom.png'),"Wipe all(output, analyze, etc.)", self.mainWindow)
        self.actMakeReference = QAction(QIcon(iconPath + 'reference.png'),"Make reference from the analyzed data", self.mainWindow)
        self.actAnalyzeAll = QAction(QIcon(iconPath + 'data-integration.png'),"Analyze all the files/paths", self.mainWindow)


    def configSignals(self):
        self.addAction(self.actAddFile)
        self.addAction(self.actAddPath)
        self.addSeparator()
        self.addAction(self.actAnalyzeAll)
        self.addSeparator()
        self.addAction(self.actMakeReference)
        self.addSeparator()
        self.addAction(self.actRemoveOutput)
        self.addAction(self.actClearAnalyze)
        self.addAction(self.actWipeAll)

    def configLayout(self):
        self.actAddFile.triggered.connect(self.onAddFile)
        self.actAddPath.triggered.connect(self.onAddPath)

        self.setOrientation(Qt.Vertical)

    def onAddFile(self):
        dlg = QFileDialog(directory = self.appSetting.lastOpenedPath)
        if dlg.exec_():
            self.appSetting.lastOpenedPath = dlg.selectedFiles()[0]

    def onAddPath(self):
        self.appSetting.lastOpenedPath = QFileDialog(directory = self.appSetting.lastOpenedPath).getExistingDirectory(self.mainWindow, 'Hey! Select a Folder', options=QFileDialog.ShowDirsOnly)

    def addSelectedPathToList(self):
        item = QListWidgetItem(self.edtCurrentSelectedPath.text())
        print(self.edtCurrentSelectedPath.text())
        self.lstSelectedPath.addItem(item)


    def onAnalyzeSelectedPaths(self):
        paths = self.getSelectedPaths()
        self.analyzerLogic.analyzeAll(paths)
        showMessage("Analyzer", "The selected files are analyzed!")

    def onAnalyzeAll(self):
        paths = self.getAllPaths()
        self.analyzerLogic.analyzeAll(paths)
        showMessage("Analyzer", "All the files are analyzed!")

    def onClearAnalyze(self):
        self.analyzerLogic.clear()     

    def onClearOutput(self):
        self.analyzerLogic.clearOutput()
            
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
        listItems=self.lstResults.selectedItems()
        if len(listItems) > 0:
            self.diagram = DiagramWindow(listItems[0].text())
            self.diagram.show()

