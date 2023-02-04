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
from AnalyzerEntites import *
class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.listOfPolicyFiles = list()
        self.listOfAnalyzerInfo = list()
        if not os.path.exists("out"):
            os.makedirs("out")

        

    def analyze(self, targetPath, pattern, disableDrawing = False, drawExisting = False):


        listOfFiles = self.gatherFileInfo(targetPath, "*")
        if listOfFiles == None or len(listOfFiles) == 0:
            print( "Nothing to analyze!")
            return

        relationDrawer = RelationDrawer()
        relationDrawer.start()
        relationDrawer.setDisableDrawing(disableDrawing)

        #print(listOfFiles)
        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("Analyzing: " + filePath)#, fileType)
                policyFile = self.invokeAnalyzerClass(fileType, filePath)
                relationDrawer.enqueuePolicyFile(policyFile)
            else:
                print("Undefined file extension : " + filePath)
        
        #Wait till the drawing thread is done
        relationDrawer.letShutdownThread = True
        relationDrawer.join()

    def gatherFileInfo(self, targetPath, pattern):
        
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, pattern)
        for file in listOfFiles :
            analyzerInfo = AnalyzerInfo()
            analyzerInfo.sourceFile = systemUtility.getFileInfo(file)
            self.listOfAnalyzerInfo.append(analyzerInfo)

        print(self.listOfAnalyzerInfo)
        return listOfFiles

    def detectLang(self, fileName):
        for fileType in FileTypeEnum:
            if fileType.label in os.path.basename(fileName):
                #print(os.path.basename(fileName))
                return fileType

        return FileTypeEnum.UNDEFINED
        
    def invokeAnalyzerClass(self, fileType, filePath):
        if fileType == FileTypeEnum.TE_FILE:
            return TeAnalyzer().analyze(filePath)
        elif fileType == FileTypeEnum.SEAPP_CONTEXTS:
            return SeAppAnalyzer().analyze(filePath)
        elif fileType in [FileTypeEnum.FILE_CONTEXTS, FileTypeEnum.SERVICE_CONTEXTS, FileTypeEnum.HWSERVICE_CONTEXTS, FileTypeEnum.VNDSERVICE_CONTEXTS, FileTypeEnum.PROPERTY_CONTEXTS]:
            return ContextsAnalyzer().analyze(filePath)
        else:
            return

if __name__ == "__main__" :
    #print(sys.argv)
    print("Input path/file: ", sys.argv[1])
    print("-----------------------------------------------------")
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze(sys.argv[1], None)