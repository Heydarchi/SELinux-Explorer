
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QGridLayout
from PyQt5.QtWidgets import QListWidget, QGroupBox, QListWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from logic.AnalyzerLogic import *
from ui.UiUtility import *
import sys
from PythonUtilityClasses.SystemUtility import *


class DiagramWindow(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.filePath = filePath
        self.initVariables()
        self.initWidgets()
        self.configLayout()


    def initVariables(self):
        self.DEFAULT_WIDTH = 1200 * 2
        self.DEFAULT_HEIGHT = 1024 * 2

    def initWidgets(self):
        self.im = QPixmap(self.filePath)
        self.label = QLabel()
        self.grid = QGridLayout()

    def configLayout(self):
        self.grid.addWidget(self.label,1,1)
        self.setLayout(self.grid)

        self.setMaximumWidth(self.DEFAULT_WIDTH)
        self.setMaximumHeight(self.DEFAULT_HEIGHT)
        self.label.setPixmap(self.im)

        #self.setGeometry(50,50,320,200)
        self.setWindowTitle("Diagram")
        self.setWindowPosition()

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.label.setPixmap(self.im.scaled(self.label.width() ,self.label.height(), Qt.KeepAspectRatio))


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
        if not items: return
        for item in items:
            filePath = item.text()
            self.lstResults.takeItem(self.lstResults.row(item))
            self.analyzerLogic.removeFile(filePath)


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