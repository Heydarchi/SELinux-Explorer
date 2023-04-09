import sys
from pathlib import Path
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import *
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger


class ContextsAnalyzer(AbstractAnalyzer):

    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        if "file_contexts" in filePath:
            self.policyFile = PolicyFiles(
                filePath, "", FileTypeEnum.FILE_CONTEXTS)
        elif "vndservice_contexts" in filePath:
            self.policyFile = PolicyFiles(
                filePath, "", FileTypeEnum.VNDSERVICE_CONTEXTS)
        elif "hwservice_contexts" in filePath:
            self.policyFile = PolicyFiles(
                filePath, "", FileTypeEnum.HWSERVICE_CONTEXTS)
        elif "service_contexts" in filePath:
            self.policyFile = PolicyFiles(
                filePath, "", FileTypeEnum.SERVICE_CONTEXTS)
        elif "property_contexts" in filePath:
            self.policyFile = PolicyFiles(
                filePath, "", FileTypeEnum.PROPERTY_CONTEXTS)
        else:
            return

        file_reader = FR.FileReader()
        temp_lines = file_reader.readFileLines(filePath)
        for line in temp_lines:
            self.extract_definition(line)

        # print(self.policyFile)
        return self.policyFile

    def extract_definition(self, input_string):
        try:
            # print (input_string)
            input_string = clean_line(input_string)
            if input_string is None:
                return
            # print ("Cleaned: ",input_string)
            context = Context()
            items = input_string.replace(";", "").strip().split()
            context.pathName = items[0]
            if len(items) > 1:
                context.typeDef = TypeDef()
                security_items = items[1].split(":")
                context.securityContext = SecurityContext()
                # print(security_items)
                context.securityContext.user = security_items[0]
                context.securityContext.role = security_items[1]
                context.securityContext.type = security_items[2]
                context.securityContext.level = security_items[3]
                if len(security_items) > 4:
                    context.securityContext.categories = security_items[4]
            # print(context)
            self.policyFile.contexts.append(context)
        except Exception as e:
            MyLogger.logError(sys, e, input_string)

    def analyzePortContexts(self):
        pass

    def analyzeGenfsContexts(self):
        pass

    def analyzeKeysConf(self):
        pass


if __name__ == "__main__":
    print(sys.argv)
    analyzer = ContextsAnalyzer()
    analyzer.analyze(sys.argv[1])
