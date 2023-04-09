import sys

from PythonUtilityClasses import SystemUtility as SU
from analyzer.TeAnalyzer import *
from analyzer.ContextsAnalyzer import *
from analyzer.SeAppAnalyzer import *
from drawer.RelationDrawer import *
from analyzer.AnalyzerEntities import *
from MyLogger import *


class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.listOfPolicyFiles = []
        self.listOfAnalyzerInfo = []

    def clear(self):
        self.listOfPolicyFiles = []
        self.listOfAnalyzerInfo = []
        print("The previous analyze result is cleared!")

    def analyze(self, targetPaths):
        list_of_files = []
        for path in targetPaths:
            list_of_files.extend(self.gatherFileInfo(path, "*"))

        if list_of_files is None or len(list_of_files) == 0:
            print("Nothing to analyze!")
            return

        for file_path in list_of_files:
            file_type = self.detectLang(file_path)
            if file_type != FileTypeEnum.UNDEFINED:
                print("Analyzing: " + file_path)
                policy_file = self.invokeAnalyzerClass(file_type, file_path)
                self.listOfPolicyFiles.append(policy_file)
            else:
                pass
                # print("Undefined file extension : " + file_path)

        return self.listOfPolicyFiles

    def gatherFileInfo(self, targetPath, pattern):

        system_utility = SU.SystemUtility()
        list_of_files = system_utility.get_list_of_files(targetPath, pattern)
        for file in list_of_files:
            try:
                analyzerInfo = AnalyzerInfo()
                analyzerInfo.sourceFile = system_utility.get_file_info(file)
                self.listOfAnalyzerInfo.append(analyzerInfo)
            except Exception as e:
                MyLogger.logError(sys, e)
        # print(self.listOfAnalyzerInfo)
        return list_of_files

    def detectLang(self, fileName):
        for fileType in FileTypeEnum:
            # if fileType.label in os.path.basename(file_name):
            if os.path.basename(fileName).strip().endswith(fileType.label):
                # print(os.path.basename(file_name))
                return fileType

        return FileTypeEnum.UNDEFINED

    def invokeAnalyzerClass(self, fileType, filePath):
        if fileType == FileTypeEnum.TE_FILE:
            return TeAnalyzer().analyze(filePath)
        elif fileType == FileTypeEnum.SEAPP_CONTEXTS:
            return SeAppAnalyzer().analyze(filePath)
        elif fileType in [FileTypeEnum.FILE_CONTEXTS,
                          FileTypeEnum.SERVICE_CONTEXTS,
                          FileTypeEnum.HWSERVICE_CONTEXTS,
                          FileTypeEnum.VNDSERVICE_CONTEXTS,
                          FileTypeEnum.PROPERTY_CONTEXTS]:
            return ContextsAnalyzer().analyze(filePath)
        else:
            return


if __name__ == "__main__":
    print(sys.argv)
    # print("Input path/file: ", sys.argv[1])
    # print("-----------------------------------------------------")
    # fileAnalyzer = FileAnalyzer()
    # fileAnalyzer.analyzeAndDraw(sys.argv[1], None)
