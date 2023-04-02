import sys
from pathlib import Path
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import * 
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR

class ContextsAnalyzer(AbstractAnalyzer):

    def __init__(self) -> None:
        self.policyFile = None


    def analyze(self, filePath):
        if "file_contexts" in filePath:
            self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.FILE_CONTEXTS)
        elif "vndservice_contexts" in filePath:
            self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.VNDSERVICE_CONTEXTS)
        elif "hwservice_contexts" in filePath:
            self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.HWSERVICE_CONTEXTS)
        elif "service_contexts" in filePath:
            self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.SERVICE_CONTEXTS)
        elif "property_contexts" in filePath:
            self.policyFile = PolicyFiles(filePath, "" , FileTypeEnum.PROPERTY_CONTEXTS)
        else:
            return

        fileReader = FR.FileReader()
        tempLines= fileReader.readFileLines(filePath)
        for line in tempLines :
            self.extractDefinition(line)

        #print(self.policyFile)
        return self.policyFile

    def extractDefinition(self,  inputString):
        try:
            #print (inputString)
            inputString = cleanLine(inputString)
            if inputString == None :
                return
            #print ("Cleaned: ",inputString)
            context = Context()
            items = inputString.replace(";","").strip().split()
            context.pathName = items[0]
            if len(items) > 1 :
                context.typeDef = TypeDef()
                securityItems = items[1].split(":")
                context.securityContext= SecurityContext()
                #print(securityItems)
                context.securityContext.user = securityItems[0]
                context.securityContext.role = securityItems[1]
                context.securityContext.type = securityItems[2]
                context.securityContext.level = securityItems[3]
                if len(securityItems) > 4 :
                    context.securityContext.categories = securityItems[4]
            #print(context)
            self.policyFile.contexts.append(context)
        except Exception as e:
            print("Error in extractDefinition: ", inputString)
            print(e)

    def analyzePortContexts(self):
        pass
    

    def analyzeGenfsContexts(self):
        pass

    def analyzeKeysConf(self):
        pass


if __name__ == "__main__" :
    print(sys.argv)
    analyzer = ContextsAnalyzer()   
    analyzer.analyze(sys.argv[1])