import sys
from pathlib import Path
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import * 
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger

class TeAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policyFile = None

    def analyze(self, filePath):
        self.filePath = filePath
        self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.TE_FILE) 
        fileReader = FR.FileReader()
        tempLines= fileReader.readFileLines(filePath)
        lastLine = ""
        macroFound= False
        for line in tempLines :
            line = cleanLine(line)
            if line == None:
                continue

            if macroFound:
                if ")" in line:
                    macroFound = False
                    self.processLine(lastLine + " " + line)
                else:
                    lastLine = lastLine + " " + line
            else:
                if "define" in line:
                    macroFound = True
                    lastLine = line
                else:
                    self.processLine(line)

        return self.policyFile

    def processLine(self, inputString):
        inputString = cleanLine(inputString)
        if inputString == None :
            return
        items = inputString.split()
        #print("items: ", items)
        if len(items) > 0 :
            if items[0].strip() == "type" :
                typeDef = self.extractDefinition(inputString)
                if typeDef != None:
                    self.policyFile.typeDef.append(typeDef)
            elif items[0].strip() == "typeattribute":
                attribute = self.extractAttribite(inputString)
                if attribute != None:
                    self.policyFile.attribute.append(attribute)
            elif items[0] in ["allow", "neverallow"] :
                self.policyFile.rules.extend(self.extractRule(inputString))
            elif "define" in inputString  :
                macro = self.extractMacro(inputString)
                if macro != None:
                    self.policyFile.macros.append(macro)
            elif "(" in inputString and ")" in inputString:
                macroCall = self.extractMacroCall(inputString)
                if macroCall != None:
                    self.policyFile.macroCalls.append(macroCall)
            else:
                MyLogger.logError(sys, "Unknown line", inputString)
    def extractDefinition(self,  inputString):
        try:
            types = inputString.replace(";","").replace("type ","").strip().split(",")
            typeDef = TypeDef()
            typeDef.name = types[0].strip()
            typeDef.types.extend(types[1:])
            if DOMAIN_EXECUTABLE in typeDef.name:
                if not self.mergeExecDomain(typeDef):
                    return typeDef
            else:
                return typeDef

        except Exception as e:
            MyLogger.logError(sys, e, inputString)
            return None

    def mergeExecDomain(self, typeDefExec):
        try:
            title = typeDefExec.name.replace(DOMAIN_EXECUTABLE,"")
            for typeDef in self.policyFile.typeDef:
                if typeDef.name == title:
                    typeDef.types.extend(typeDefExec.types)
                    return True
            return False
        except Exception as e:
            MyLogger.logError(sys, e, typeDefExec)
            return False

    def extractAttribite(self,  inputString):
        try:
            attribute = Attribute()
            types = inputString.replace(";","").replace("typeattribute ","").strip().split(" ")
            attribute.name = types[0]
            attribute.types.extend(types[1:])
            return attribute

        except Exception as e:
            MyLogger.logError(sys, e, inputString)
            return None

    def extractRule(self,  inputString):
        lstRules = list()
        try:
            inputString = inputString.replace(' : ',':').replace(' :',':').replace(': ',':').strip()
            inputString = inputString.replace('{',' { ').replace('}',' } ').strip()
            inputString = inputString.replace(': {',':{ ').replace('} :','}:').strip()
            inputString = inputString.replace(':  {',':{ ').replace('}  :','}:').strip()


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
                        lstRules.append(rule)

                    return

        except Exception as e:
            MyLogger.logError(sys, e, inputString)
        finally:
            return lstRules


    def extractMacro(self, inputString):
        try:
            lstLines = inputString.splitlines()
            macro =  PolicyMacro()
            #It's supposed to have define in the first item
            firstLine= lstLines.pop(0).replace("define","").replace("\'","")
            firstLine= firstLine.replace("`","").replace("(","").replace(",","")
            macro.name = firstLine.strip()
            for line in lstLines:
                if ")" in line.strip() :
                    break
                macro.rulesString.append(line)
                macro.rules.extend(self.extractRule(line))
            #print("macro: ", macro)
            return macro
        except Exception as e:
            MyLogger.logError(sys, e, inputString)
            return None

    def extractMacroCall(self, inputString):
        try:
            #Convert string to PolicyMacroCall
            macroCall = PolicyMacroCall()
            macroCall.name = inputString.split("(")[0].strip()
            macroCall.parameters = inputString.split("(")[1].replace(")","").strip().split(",")
            return macroCall
        except Exception as e:
            MyLogger.logError(sys, e, inputString)
            return None

if __name__ == "__main__" :
    print(sys.argv)
    teAnalyzer = TeAnalyzer()
    print(teAnalyzer.analyze(sys.argv[1]))