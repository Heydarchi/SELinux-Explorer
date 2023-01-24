import re
import sys
import os
from AbstractAnalyzer import * 
from PolicyEntities import *
from PythonUtilityClasses import SystemUtility as SU

class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        if not os.path.exists("../out"):
            os.makedirs("../out")

    def analyze(self, targetPath, pattern):
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, "*")
        print(listOfFiles)
        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("- Analyzing: " + filePath, fileType)
                #listOfClasses = classAnalyzer.analyze(filePath, language)
                #self.drawUmls(listOfClasses)
            else:
                print("- Undefined file extension : " + filePath)
    """     def drawUmls(self, listOfClassNodes):
        for classInfo in listOfClassNodes:
            umlDrawer = ClassUmlDrawer()
            umlDrawer.drawUml(classInfo)
    """

    def detectLang(self, fileName):
        for fileType in FileTypeEnum:
            if fileType.label in fileName:
                return fileType

        return FileTypeEnum.UNDEFINED
        
        

if __name__ == "__main__" :
    print(sys.argv)
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze(sys.argv[1], None)