import sys
from pathlib import Path
from AnalyzerUtility import *
import re
from AbstractAnalyzer import * 
from PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
class TeAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.TE_FILE) 
        fileReader = FR.FileReader()
        tempLines= fileReader.readFileLines(filePath)
        for line in tempLines :
            self.processLine(line)

        print(self.policyFile)

    def processLine(self, inputString):
        inputString = cleanLine(inputString)
        if inputString == None :
            return
        items = inputString.split()
        if len(items) > 0 :
            if items[0] == "type" :
                self.extractDefinition(items)
            elif items[0] in ["allow", "neverallow"] :
                self.extractRule(items)


    def extractDefinition(self,  items):
        types = items[1].replace(";","").strip().split(",") 
        typeDef = TypeDef()
        typeDef.name = types[0]
        typeDef.types.extend(types[1:])
        self.policyFile.typeDef.append( typeDef )

    def extractRule(self,  items):
        rule = Rule()
        for ruleEnum in RuleEnum:
            if ruleEnum.label == items[0].strip():
                rule.rule = ruleEnum
                rule.source = items[1]
                dstItems = items[2].split(":")
                rule.target = dstItems[0]
                rule.classType = dstItems[1]
                permissions = items[2].replace("{","").replace("}","").strip().split()
                rule.permissions.extend(permissions)
                self.policyFile.rules.append(rule)
                return

if __name__ == "__main__" :
    print(sys.argv)
    teAnalyzer = TeAnalyzer()
    teAnalyzer.analyze(sys.argv[1])

