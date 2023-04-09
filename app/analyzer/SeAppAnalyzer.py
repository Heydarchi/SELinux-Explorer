import sys
from pathlib import Path
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import *
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger


class SeAppAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        self.policyFile = PolicyFiles(
            filePath, "", FileTypeEnum.SEAPP_CONTEXTS)
        file_reader = FR.FileReader()
        temp_lines = file_reader.read_file_lines(filePath)
        for line in temp_lines:
            self.processLine(line)

        # print(self.policy_file)
        return self.policyFile

    def processLine(self, input_string):
        input_string = clean_line(input_string)
        if input_string is None:
            return
        self.extractDefinition(input_string)

    def extractDefinition(self, input_string):
        try:
            se_app = SeAppContext()
            if "neverallow" in input_string:
                se_app.neverAllow = True
                input_string = input_string.replace("neverallow", "").strip()

            items = input_string.strip().split(" ")
            for item in items:
                split = item.split("=")
                # Input selectors
                if "user" in split[0]:
                    se_app.user = split[1]
                elif "isPrivApp" in split[0]:
                    se_app.isPrivApp = split[1]
                elif "isSystemServer" in split[0]:
                    se_app.isSystemServerer = split[1]
                elif "isEphemeralApp" in split[0]:
                    se_app.isEphemeralApp = split[1]
                elif "name" in split[0]:
                    se_app.name = split[1]
                elif "minTargetSdkVersion" in split[0]:
                    se_app.minTargetSdkVersion = split[1]
                elif "fromRunAs" in split[0]:
                    se_app.fromRunAs = split[1]
                elif "seinfo" in split[0]:
                    se_app.seinfo = split[1]
                # Outputs
                elif "domain" in split[0]:
                    se_app.domain = split[1]
                elif "type" in split[0]:
                    se_app.type = split[1]
                elif "levelFrom" in split[0]:
                    se_app.levelFrom = split[1]
                elif "level" in split[0]:
                    se_app.level = split[1]

            self.policyFile.seApps.append(se_app)

        except Exception as e:
            MyLogger.logError(sys, e, input_string)


if __name__ == "__main__":
    print(sys.argv)
    seAppAnalyzer = SeAppAnalyzer()
    seAppAnalyzer.analyze(sys.argv[1])
