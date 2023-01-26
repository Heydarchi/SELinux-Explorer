import sys
from pathlib import Path
from AnalyzerUtility import *
import re
from AbstractAnalyzer import * 
from PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
class SeAppAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.SEAPP_CONTEXTS) 
        fileReader = FR.FileReader()
        tempLines= fileReader.readFileLines(filePath)
        for line in tempLines :
            self.processLine(line)

        print(self.policyFile)

    def processLine(self, inputString):
        inputString = cleanLine(inputString)
        if inputString == None :
            return
        self.extractDefinition(inputString)


    def extractDefinition(self,  inputString):
        seApp = SeAppContext()
        if "neverallow" in inputString:
            seApp.neverAllow = True
            inputString = inputString.replace("neverallow","").strip()

        items = inputString.strip().split(" ")
        for item in items:
            splitted = item.split("=")
            ####   Input selectors
            if "user" in splitted[0]:
                seApp.user= splitted[1]
            elif "isPrivApp" in splitted[0]:
                seApp.isPrivApp= splitted[1]
            elif "isSystemServer" in splitted[0]:
                seApp.isSystemServerer= splitted[1]
            elif "isEphemeralApp" in splitted[0]:
                seApp.isEphemeralApp= splitted[1]
            elif "name" in splitted[0]:
                seApp.name= splitted[1]
            elif "minTargetSdkVersion" in splitted[0]:
                seApp.minTargetSdkVersion= splitted[1]
            elif "fromRunAs" in splitted[0]:
                seApp.fromRunAs= splitted[1]
            elif "seinfo" in splitted[0]:
                seApp.seinfo= splitted[1]
            ####   Outputs
            elif "domain" in splitted[0]:
                seApp.domain= splitted[1]
            elif "type" in splitted[0]:
                seApp.type= splitted[1]
            elif "levelFrom" in splitted[0]:
                seApp.levelFrom= splitted[1]
            elif "level" in splitted[0]:
                seApp.level= splitted[1]

        self.policyFile.seApps.append(seApp)


if __name__ == "__main__" :
    print(sys.argv)
    seAppAnalyzer = SeAppAnalyzer()
    seAppAnalyzer.analyze(sys.argv[1])

