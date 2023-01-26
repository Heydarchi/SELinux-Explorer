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

    def analyzeFileContexts(self):
        pass


    def analyzeServiceContexts(self):
        pass


    def analyzePortContexts(self):
        pass
    

    def analyzeGenfsContexts(self):
        pass


    def analyzeServiceContexts(self):
        pass


    def analyzeHwserviceContexts(self):
        pass


    def analyzeVndserviceContexts(self):
        pass


    def analyzePropertyContexts(self):
        pass


    def analyzeKeysConf(self):
        pass


if __name__ == "__main__" :
    analyzer = ContextsAnalyzer()   
    print (sysUtil.getListOfFiles( "./test","*_contexts"))
    print (sysUtil.getListOfFiles( "./test","*.te"))