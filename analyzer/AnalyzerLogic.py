from FileAnalyzer import  * 
from RelationDrawer import *


class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self.initVariables()
        self.initAnalyzer()


    def initVariables(self):
        self.keepResult = False

    def initAnalyzer(self):
        self.analyzer = FileAnalyzer()

    def analyzeAll(self, paths):
        if not self.keepResult :
            self.analyzer.clear()

        self.analyzer.analyze(paths, None)

    def onAnalyzeSelectedPaths(self, paths):
        if not self.keepResult :
            self.analyzer.clear()

        self.analyzer.analyze(paths, None)

    def clearAnalyze(self):
        self.analyzer.clear()     

    def setKeepResult(self, state):
        self.keepResult = state
        print("self.keepResult:", self.keepResult)
