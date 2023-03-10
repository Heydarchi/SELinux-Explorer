import sys
from pathlib import Path
from AnalyzerUtility import *
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

        #print(self.policyFile)
        return self.policyFile

    def processLine(self, inputString):
        inputString = cleanLine(inputString)
        if inputString == None :
            return
        items = inputString.split()
        if len(items) > 0 :
            if items[0].strip() == "type" or items[0].strip() == "typeattribute" :
                self.extractDefinition(inputString)
            elif items[0] in ["allow", "neverallow"] :
                self.extractRule(inputString)
        #print(self.policyFile)

    def extractDefinition(self,  inputString):
        type = None
        if "typeattribute " in inputString :
            types = inputString.replace(";","").replace("typeattribute ","").strip().split(" ")
        else:
            types = inputString.replace(";","").replace("type ","").strip().split(",")

        typeDef = TypeDef()
        typeDef.name = types[0]
        typeDef.types.extend(types[1:])
        self.policyFile.typeDef.append( typeDef )
        #print (typeDef)

    def extractRule2(self,  inputString):
            #print("inputString:  ",inputString)
            items = inputString.replace(";","").replace(": ",":").replace("{","").replace("}","").strip().split()
            #print(items)
            #print(inputString.replace(";","").replace(": ",":").strip().split("}"))
            for ruleEnum in RuleEnum:
                if ruleEnum.label == items[0].strip():
                    countBrackets = inputString.count("}")
                    if ("}" in inputString ) and (countBrackets==2 or (inputString.replace(";","").strip().index("}") + 1 )< len(inputString.replace(";","").strip()) ):
                        #print(inputString.replace(";","").strip().index("}"))
                        #print((len(inputString.replace(";","").strip()) + 1 ))
                        sourcesString =inputString[inputString.index("{"): inputString.index("}")].replace("{","")
                        sources = sourcesString.replace("{","").replace("}","").strip().split() 
                        #print("sourcesString: ", sourcesString)
                        items = inputString.replace(sourcesString, "##").replace(";","").replace(": ",":").replace("{","").replace("}","").strip().split()
                        #print ("itemsss:  ", items)
                    else:
                        items = inputString.replace(";","").replace(": ",":").replace("{","").replace("}","").strip().split()
                        sources = [items[1]]

                    for source in sources:
                        rule = Rule()
                        rule.rule = ruleEnum                    
                        rule.source = source
                        dstItems = items[2].split(":")
                        rule.target = dstItems[0]
                        rule.classType = dstItems[1]
                        rule.permissions.extend(items[3:])
                        #print(items)
                        #print(rule)
                        self.policyFile.rules.append(rule)
                    return

    def extractRule(self,  inputString):
            items = inputString.replace(";","").replace(": ",":").strip().split()
            for ruleEnum in RuleEnum:
                if ruleEnum.label == items[0].strip():
                    
                    countBrackets = inputString.count("}")
                    lstBracketItems = list()
                    if countBrackets > 0 :
                        offset = 0
                        while '{' in inputString[offset:]:
                            print (inputString[offset:])
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
    #print(teAnalyzer.analyze(sys.argv[1]))
    
    print( teAnalyzer.extractRule2("allow dummy servicemanager:binder { call transfer };"))
    print( teAnalyzer.extractRule2("allow 1111111111111 22222:CCC 333333333"))
    print( teAnalyzer.extractRule2("allow {MM NN} {AA BB }:CCC { DD EE}"))
