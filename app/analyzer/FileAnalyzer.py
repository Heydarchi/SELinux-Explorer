from PythonUtilityClasses import SystemUtility as SU
from analyzer.TeAnalyzer import *
from analyzer.ContextsAnalyzer import *
from analyzer.SeAppAnalyzer import *
from drawer.RelationDrawer import *
from analyzer.AnalyzerEntities import *
class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.listOfPolicyFiles = list()
        self.listOfAnalyzerInfo = list()


    def clear(self):
        self.listOfPolicyFiles = list()
        self.listOfAnalyzerInfo = list()
        print("The previous analyze result is cleared!")
        

    def analyzeAndDraw(self, targetPaths, pattern, disableDrawing = False, drawExisting = False):
        listOfFiles = list()
        for path in targetPaths:
            listOfFiles.extend( self.gatherFileInfo(path, "*"))

        if listOfFiles == None or len(listOfFiles) == 0:
            print( "Nothing to analyze!")
            return

        #Setting up drawing
        relationDrawer = RelationDrawer()
        relationDrawer.start()
        relationDrawer.setDisableDrawing(disableDrawing)

        #print(listOfFiles)
        for filePath in listOfFiles:
            fileType = self.detectLang(filePath)
            if fileType != FileTypeEnum.UNDEFINED :
                print("Analyzing: " + filePath)#, fileType)
                policyFile = self.invokeAnalyzerClass(fileType, filePath)
                self.listOfPolicyFiles.append(policyFile)
                relationDrawer.enqueuePolicyFile(policyFile)
            else:
                print("Undefined file extension : " + filePath)
        
        #Wait till the drawing thread is done
        relationDrawer.letShutdownThread = True
        relationDrawer.join()

        return self.listOfPolicyFiles
    
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
                print(e)
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
    print("Input path/file: ", sys.argv[1])
    print("-----------------------------------------------------")
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyzeAndDraw(sys.argv[1], None)