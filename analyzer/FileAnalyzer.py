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
        self.relationDrawer = RelationDrawer()

    def analyze(self, targetPath, pattern, disableDrawing = False, drawExisting = False):
        self.relationDrawer.start()
        self.relationDrawer.setDisableDrawing(disableDrawing)

        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, "*")
        #print(listOfFiles)
        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("Analyzing: " + filePath)#, fileType)
                policyFile = self.invokeAnalyzerClass(fileType, filePath)
                self.relationDrawer.enqueuePolicyFile(policyFile)
            else:
                print("Undefined file extension : " + filePath)
        
        #Wait till the drawing thread is done
        self.relationDrawer.letShutdownThread = True
        self.relationDrawer.join()
    

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