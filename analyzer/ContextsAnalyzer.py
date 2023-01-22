from FileAnalyzer import *
import re

class ContextsAnalyzer(FileAnalyzer):

    def __init__(self) -> None:
        self.regxDict = {
            "file_contexts","*_contexts", 
            "seapp_contexts","*_contexts", 
       }


    def analyze(self, filePath):
        pass

    def readFile(self, filePath):
        return open(filePath, 'r').readlines()

    def selectRegx(self, filePath):
        pass

    def AnalyzeSeappContexts(self):
        pass
    

    def AnalyzeFileContexts(self):
        pass


    def AnalyzeServiceContexts(self):
        pass


    def AnalyzePortContexts(self):
        pass
    

    def AnalyzeGenfsContexts(self):
        pass


    def AnalyzeServiceContexts(self):
        pass


    def AnalyzeHwserviceContexts(self):
        pass


    def AnalyzeVndserviceContexts(self):
        pass


    def AnalyzePropertyContexts(self):
        pass


    def AnalyzeKeysConf(self):
        pass


if __name__ == "__main__" :
    analyzer = ContextsAnalyzer()   
    print (sysUtil.getListOfFiles( "./test","*_contexts"))
    print (sysUtil.getListOfFiles( "./test","*.te"))