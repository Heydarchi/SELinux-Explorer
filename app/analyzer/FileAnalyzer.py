from PythonUtilityClasses import SystemUtility as SU
from analyzer.TeAnalyzer import *
from analyzer.ContextsAnalyzer import *
from analyzer.SeAppAnalyzer import *
from drawer.RelationDrawer import *
from analyzer.AnalyzerEntities import *
from MyLogger import *

class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.listOfPolicyFiles = list()
        self.listOfAnalyzerInfo = list()


    def clear(self):
        self.listOfPolicyFiles = list()
        self.listOfAnalyzerInfo = list()
        print("The previous analyze result is cleared!")

    def analyze(self, targetPaths):
        listOfFiles = list()
        for path in targetPaths:
            listOfFiles.extend( self.gatherFileInfo(path, "*"))

        if listOfFiles == None or len(listOfFiles) == 0:
            print( "Nothing to analyze!")
            return

        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("Analyzing: " + filePath)
                policyFile = self.invokeAnalyzerClass(fileType, filePath)
                self.listOfPolicyFiles.append(policyFile)
            else:
                pass
                #print("Undefined file extension : " + filePath)

        return self.listOfPolicyFiles    

    def gatherFileInfo(self, targetPath, pattern):
        
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, pattern)
        for file in listOfFiles :
            try:
                analyzerInfo = AnalyzerInfo()
                analyzerInfo.sourceFile = systemUtility.getFileInfo(file)
                self.listOfAnalyzerInfo.append(analyzerInfo)
            except Exception as e:
                MyLogger.logError(sys, e)
        #print(self.listOfAnalyzerInfo)
        return listOfFiles

    def detectLang(self, fileName):
        for fileType in FileTypeEnum:
            #if fileType.label in os.path.basename(fileName):
            if os.path.basename(fileName).strip().endswith(fileType.label):
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
    # print("Input path/file: ", sys.argv[1])
    # print("-----------------------------------------------------")
    # fileAnalyzer = FileAnalyzer()
    # fileAnalyzer.analyzeAndDraw(sys.argv[1], None)