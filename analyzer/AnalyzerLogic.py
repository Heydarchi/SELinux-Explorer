from FileAnalyzer import  * 
from RelationDrawer import *


class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self.initVariables()
        self.initAnalyzer()


    def initVariables(self):
        self.keepResult = False
        self.listOfPolicyFiles = list()
        self.listOfDiagrams = list()
        self.drawer = RelationDrawer()

    def initAnalyzer(self):
        self.analyzer = FileAnalyzer()

    def analyzeAll(self, paths):
        if self.keepResult :
            self.listOfPolicyFiles.extend(self.analyzer.analyze(paths))
        else:
            self.listOfPolicyFiles =  self.analyzer.analyze(paths)

        self.onAnalyzeFinished()

    def onAnalyzeSelectedPaths(self, paths):
        if self.keepResult :
            self.listOfPolicyFiles.extend(self.analyzer.analyze(paths))
        else:
            self.listOfPolicyFiles = self.analyzer.analyze(paths)

        self.onAnalyzeFinished()

    def clearOutput(self):
        files = SystemUtility().getListOfFiles(os.getcwd() + "/out/","*")
        for file in files :
            if os.path.isfile(file):
                SystemUtility().deleteFiles(file)
        self.onAnalyzeFinished()

    def clearFileFromAnalyzer(self, filePath):
        self.analyzer.clear()     
        SystemUtility().deleteFiles(self.drawer.generatePngFileName(filePath))    
        SystemUtility().deleteFiles(self.drawer.generatePumlFileName(filePath)) 
        self.onAnalyzeFinished()

    def getImagePath(self, filePath):
        return self.drawer.generatePngFileName(filePath)
    
    def setKeepResult(self, state):
        self.keepResult = state
        print("self.keepResult:", self.keepResult)


    def setUiUpdateSignal(self, updateResult):
        self.updateResult = updateResult

    def onAnalyzeFinished(self):
        self.listOfDiagrams = SystemUtility().getListOfFiles(os.getcwd() + "/out/","*.png")
        self.updateResult()
        