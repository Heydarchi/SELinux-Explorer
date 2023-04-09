
from PyQt5.QtWidgets import QStatusBar
from logic.AnalyzerLogic import *
from PythonUtilityClasses.SystemUtility import *


class StatusbarUi(QStatusBar):
    def __init__(self, main_window, analyzer_logic):
        super().__init__()
        self.main_window = main_window
        self.analyzer_logic = analyzer_logic

    def update_statusbar(self, message):
        self.showMessage(message)
