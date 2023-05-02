import sys

from PythonUtilityClasses import SystemUtility as SU
from analyzer.TeAnalyzer import *
from analyzer.ContextsAnalyzer import ContextsAnalyzer
from analyzer.SeAppAnalyzer import SeAppAnalyzer
from analyzer.AnalyzerEntities import *
from MyLogger import MyLogger


class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.list_of_policy_files = []
        self.list_of_analyzer_info = []

    def clear(self):
        self.list_of_policy_files = []
        self.list_of_analyzer_info = []
        print("The previous analyze result is cleared!")

    def analyze(self, target_paths):
        list_of_files = []
        for path in target_paths:
            list_of_files.extend(self.gather_file_info(path, "*"))

        if list_of_files is None or len(list_of_files) == 0:
            print("Nothing to analyze!")
            return

        for file_path in list_of_files:
            file_type = self.detect_lang(file_path)
            if file_type != FileTypeEnum.UNDEFINED:
                print("Analyzing: " + file_path)
                policy_file = self.invoke_analyzer_class(file_type, file_path)
                if policy_file is not None:
                    self.list_of_policy_files.append(policy_file)
            else:
                pass
                # print("Undefined file extension : " + file_path)

        return self.list_of_policy_files

    def gather_file_info(self, target_path, pattern):
        system_utility = SU.SystemUtility()
        list_of_files = system_utility.get_list_of_files(target_path, pattern)
        for file in list_of_files:
            try:
                analyzer_info = AnalyzerInfo()
                analyzer_info.source_file = system_utility.get_file_info(file)
                if analyzer_info.source_file is None:
                    continue
                self.list_of_analyzer_info.append(analyzer_info)
            except Exception as err:
                MyLogger.log_error(sys, err)
        # print(self.list_of_analyzer_info)
        return list_of_files

    def detect_lang(self, file_name):
        file_type = FileTypeEnum.UNDEFINED
        for file_type in FileTypeEnum:
            # if file_type.label in os.path.basename(file_name):
            if os.path.basename(file_name).strip().endswith(file_type.label):
                # print(os.path.basename(file_name))
                break
        if  os.path.basename(file_name).startswith(FileTypeEnum.TE_FILE_3.value[1]):
            print("TE_FILE_2", os.path.basename(file_name))
            file_type =  FileTypeEnum.TE_FILE_3

        return file_type

    def invoke_analyzer_class(self, file_type, file_path):
        if file_type in [ FileTypeEnum.TE_FILE, FileTypeEnum.TE_FILE_2, FileTypeEnum.TE_FILE_3]:
            return TeAnalyzer().analyze(file_path)
        elif file_type == FileTypeEnum.SEAPP_CONTEXTS:
            return SeAppAnalyzer().analyze(file_path)
        elif file_type in [
            FileTypeEnum.FILE_CONTEXTS,
            FileTypeEnum.SERVICE_CONTEXTS,
            FileTypeEnum.HWSERVICE_CONTEXTS,
            FileTypeEnum.VNDSERVICE_CONTEXTS,
            FileTypeEnum.PROPERTY_CONTEXTS,
        ]:
            return ContextsAnalyzer().analyze(file_path)
        else:
            return


if __name__ == "__main__":
    print(sys.argv)
    # print("Input path/file: ", sys.argv[1])
    # print("-----------------------------------------------------")
    # fileAnalyzer = FileAnalyzer()
    # fileAnalyzer.analyzeAndDraw(sys.argv[1], None)
