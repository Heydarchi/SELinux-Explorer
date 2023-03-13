
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout,  QWidget
from AnalyzerLogic import *
from ui.FileUi import *
from ui.AnalyzeUi import *
from ui.FilterUi import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SELinux-Explorer")
        self.initVariables()
        self.initMainLayout()
        self.configSignals()

    def initVariables(self):
        self.analyzerLogic = AnalyzerLogic()

    def initMainLayout(self):
        self.layoutPath = FileUi(self)
        self.layoutAnalyzer = AnalyzeUi(self, self.analyzerLogic)
        self.layoutFilter = FilterUi(self, self.analyzerLogic)
        self.mainLayout = QVBoxLayout()
        self.container = QWidget()

        #mainLayout
        self.mainLayout.addLayout(self.layoutPath)
        self.mainLayout.addLayout(self.layoutAnalyzer)
        self.mainLayout.addLayout(self.layoutFilter)

        self.container.setLayout(self.mainLayout)
        # Set the central widget of the Window.
        self.setCentralWidget(self.container)

        self.setWindowPosition()

    def configSignals(self):
        self.layoutAnalyzer.connectToGetSelectedPaths( self.layoutPath.getSelectedPaths)
        self.layoutAnalyzer.connectToGetAllPaths( self.layoutPath.getAllPaths)

    def setWindowPosition(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

