
from PyQt5.QtWidgets import QStatusBar
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *


class StatusbarUi(QStatusBar):
    def __init__(self, mainWindow, analyzerLogic):
        super().__init__()
        self.main_window = mainWindow
        self.analyzer_logic = analyzerLogic

    def update_statusbar(self, message):
        self.showMessage(message)
