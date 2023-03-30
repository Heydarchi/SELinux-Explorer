
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QGridLayout
from PyQt5.QtWidgets import QListWidget, QGroupBox, QListWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDesktopWidget
from logic.AnalyzerLogic import *
from ui.UiUtility import *
import sys
from PythonUtilityClasses.SystemUtility import *


class DiagramWindow(QWidget):
    def __init__(self, filePath):
        super().__init__()

        print(filePath)
        self.im = QPixmap(filePath)
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,1,1)
        self.setLayout(self.grid)

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Diagram")
        self.setWindowPosition()

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ResultUi(QVBoxLayout):
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


    def initWidgets(self):
        iconPath = './ui/icons/'

        self.lstResults = QListWidget()
        self.layoutButton = QHBoxLayout()
        self.grpLayout = QVBoxLayout()
        self.grpResult = QGroupBox("Results")

        self.btnDeleteSelected =UiUtility.createButton("Delete the selected file", QIcon(iconPath + "delete.png"), 24, 24)

    def configSignals(self):
        self.btnDeleteSelected.clicked.connect(self.onDeleteSelectedFile)
        self.lstResults.itemClicked.connect(self.onSelectedResult) 

        self.analyzerLogic.setUiUpdateSignal(self.onAnalyzeFinished)

    def configLayout(self):
        self.layoutButton.addWidget(self.btnDeleteSelected)

        self.grpLayout.addWidget(self.lstResults)
        self.grpLayout.addLayout(self.layoutButton)
        self.grpResult.setLayout(self.grpLayout)

        self.addWidget(self.grpResult)

    def onDeleteSelectedFile(self):
        items = self.lstResults.selectedItems()
        for item in items:
            path = item.text()

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

    def onDispose(self):
        if self.diagram != None :
            self.diagram.close()