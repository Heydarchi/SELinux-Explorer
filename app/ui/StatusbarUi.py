
from PyQt5.QtWidgets import QStatusBar
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *


class StatusbarUi(QStatusBar):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.mainWindow = mainWindow
        self.analyzerLogic = analyzerLogic

    def updateStatusbar(self, message):
        self.showMessage(message)
