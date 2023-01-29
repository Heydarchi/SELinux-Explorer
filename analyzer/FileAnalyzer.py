import re
import sys
import os
from AbstractAnalyzer import * 
from PolicyEntities import *
from PythonUtilityClasses import SystemUtility as SU
from TeAnalyzer import *
from ContextsAnalyzer import *
from SeAppAnalyzer import *
from RelationDrawer import *
class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.listOfPolicyFiles = list()
        if not os.path.exists("out"):
            os.makedirs("out")

    def analyze(self, targetPath, pattern):
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, "*")
        print(listOfFiles)
        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("- Analyzing: " + filePath, fileType)
                self.listOfPolicyFiles.append(self.invokeAnalyzerClass(fileType, filePath))
                self.drawUmls(self.listOfPolicyFiles)
            else:
                print("- Undefined file extension : " + filePath)
    
    def drawUmls(self, listOfPolicyFiles):
        for policyFile in listOfPolicyFiles:
            relationDrawer = RelationDrawer()
            relationDrawer.drawUml(policyFile)
    

    def detectLang(self, fileName):
        for fileType in FileTypeEnum:
            if fileType.label in fileName:
                return fileType

        return FileTypeEnum.UNDEFINED
        
    def invokeAnalyzerClass(self, fileType, filePath):
        if fileType == FileTypeEnum.TE_FILE:
            return TeAnalyzer().analyze(filePath)
        elif fileType == FileTypeEnum.SEAPP_CONTEXTS:
            return SeAppAnalyzer().analyze(filePath)
        elif fileType in [FileTypeEnum.FILE_CONTEXTS, FileTypeEnum.SERVICE_CONTEXTS, FileTypeEnum.HWSERVICE_CONTEXTS, FileTypeEnum.VNDSERVICE_CONTEXTS]:
            return ContextsAnalyzer().analyze(filePath)

if __name__ == "__main__" :
    print(sys.argv)
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze(sys.argv[1], None)