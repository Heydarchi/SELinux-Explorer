import os, sys
from PolicyEntities import  *
from PythonUtilityClasses import FileWriter as FW

class RelationDrawer:

    def __init__(self) -> None:
        self.mapList = list()
        self.mapList.append( UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

        self.dataTypeToIgnore = []


    def drawUml(self, policyFile: PolicyFiles):
        plantUmlList = list()
        plantUmlList.append("@startuml")

        '''
        if policyFile.isInterface:
            plantUmlList.append("interface " + policyFile.name)
        else:
            plantUmlList.append("class " + policyFile.name)
        '''
        plantUmlList.extend(self.dumpPolicyFile(policyFile))

        plantUmlList.append("@enduml")

        #Remove redundance items
        plantUmlList = list(dict.fromkeys(plantUmlList))
        print(plantUmlList)
        filePath = "out/" + policyFile.fileName.replace("/","-")+"_relation.puml"
        self.writeToFile(filePath, plantUmlList)
        self.generatePng(filePath)
        #print(policyFile)

    def dumpPolicyFile(self, policyFile: PolicyFiles):
        plantUmlList = list()

        plantUmlList.extend(self.drawTypeDef(policyFile.typeDef))
        plantUmlList.extend(self.drawContext(policyFile.contexts))
        plantUmlList.extend(self.drawRule(policyFile.rules))

        return plantUmlList


    def drawTypeDef(self, typeDefs: List[TypeDef]):
        typeDefList = list()
        for typeDef in typeDefList:
                    typeDef.append("\"" + typeDef.name + "\" .....> \"" + typeDef.types + "\"" )
        return typeDefList

    def drawContext(self, contexts: List[Context]):
        contextList = list()
        for context in contexts:
                    contextList.append("\"" + context.pathName + "\" .....> \"" + context.fileType + "\"" )
        return contextList

    def drawRule(self, rules: List[Rule]):
        ruleList = list()
        for rule in rules:
                    if rule.rule == RuleEnum.NEVER_ALLOW :
                        ruleList.append("\"" + rule.source + "\" -----[#red]>x \"" + rule.target + "\" : " + rule.rule.label )
                    else:
                        ruleList.append("\"" + rule.source + "\" -----[#green]> \"" + rule.target + "\" : " + rule.rule.label )

        return ruleList

    def generatePng(self, filepath):
        os.system("java -jar plantuml/plantuml.jar " + filepath)

    def writeToFile(self, fileName, listOfStr):
        fw = FW.FileWriter()
        fw.writeListToFile(fileName, listOfStr)

if __name__ == "__main__" :
    '''print(sys.argv)
    policyFile = ClassNode()
    policyFile.name = "TestClass"
    policyFile.relations.append( Inheritance("Class1", InheritanceEnum.DEPENDED) )
    policyFile.relations.append( Inheritance("Class2", InheritanceEnum.EXTENDED) )
    policyFile.relations.append( Inheritance("Class3", InheritanceEnum.IMPLEMENTED) )
    relationDrawer = RelationDrawer()
    relationDrawer.drawUml(policyFile)
    '''