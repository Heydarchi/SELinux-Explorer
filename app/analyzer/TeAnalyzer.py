import sys
from pathlib import Path
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import * 
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
class TeAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.TE_FILE) 
        fileReader = FR.FileReader()
        tempLines= fileReader.readFileLines(filePath)
        lastLine = ""
        for line in tempLines :
            if "#" not in line and ";" not in line:
                if "(" in line:
                    lastLine = ""
                    continue
                lastLine = lastLine.replace("\\n","") + " " + line
                continue
            else:
                lastLine = ""
            self.processLine(lastLine + " " + line)

        return self.policyFile

    def processLine(self, inputString):
        inputString = cleanLine(inputString)
        if inputString == None :
            return
        items = inputString.split()
        if len(items) > 0 :
            if items[0].strip() == "type" :
                self.extractDefinition(inputString)
            elif items[0].strip() == "typeattribute":
                self.extractAttribite(inputString)
            elif items[0] in ["allow", "neverallow"] :
                self.extractRule(inputString)

    def extractDefinition(self,  inputString):
        types = inputString.replace(";","").replace("type ","").strip().split(",")
        typeDef = TypeDef()
        typeDef.name = types[0].strip()
        typeDef.types.extend(types[1:])
        if DOMAIN_EXECUTABLE in typeDef.name:
            if not self.mergeExecDomain(typeDef):
                self.policyFile.typeDef.append( typeDef )
        else:
            self.policyFile.typeDef.append( typeDef )

    def mergeExecDomain(self, typeDefExec):
        title = typeDefExec.name.replace(DOMAIN_EXECUTABLE,"")
        for typeDef in self.policyFile.typeDef:
            if typeDef.name == title:
                typeDef.types.extend(typeDefExec.types)
                return True
        return False

    def extractAttribite(self,  inputString):
        types = inputString.replace(";","").replace("typeattribute ","").strip().split(" ")
        typeDef = TypeDef()
        typeDef.name = types[0]
        typeDef.types.extend(types[1:])
        self.policyFile.attribute.append( typeDef )


    def extractRule(self,  inputString):
            inputString = inputString.replace(' : ',':').replace(' :',':').replace(': ',':').strip()
            inputString = inputString.replace('{',' { ').replace('}',' } ').strip()
            #print("inputString; " + inputString)
            items = inputString.replace(";","").split()
            for ruleEnum in RuleEnum:
                if ruleEnum.label == items[0].strip():
                    
                    countBrackets = inputString.count("}")
                    lstBracketItems = list()
                    if countBrackets > 0 :
                        offset = 0
                        while '{' in inputString[offset:]:
                            #print (inputString[offset:])
                            start = inputString.find('{', offset)
                            end = inputString.find('}', start )
                            bracketString = inputString[start + 1: end]
                            inputString = inputString[:start] + "###" + inputString[end +1 :]
                            lstBracketItems.append(bracketString)
                            offset = start

                    items = inputString.replace(";","").replace(": ",":").strip().split()
                    sources = [items[1]] if "###" not in items[1] else lstBracketItems.pop(0).strip().split()
                    sec_context = items[2] if "###" not in items[2] else (lstBracketItems.pop(0) + ":" + items[2].split(":")[1])
                    permissions = [items[3]] if "###" not in items[3] != "###" else lstBracketItems.pop(0).strip().split()

                    for source in sources:
                        rule = Rule()
                        rule.rule = ruleEnum
                        rule.source = source
                        dstItems = sec_context.split(":")
                        targets = dstItems[0].split()
                        for target in targets:
                            rule.target = target
                            rule.classType = dstItems[1]
                            rule.permissions = permissions
                        self.policyFile.rules.append(rule)

                    return

if __name__ == "__main__" :
    print(sys.argv)
    teAnalyzer = TeAnalyzer()
    print(teAnalyzer.analyze(sys.argv[1]))