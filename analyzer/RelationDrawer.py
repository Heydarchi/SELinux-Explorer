import os, sys
from PolicyEntities import  *
from PythonUtilityClasses import FileWriter as FW
from datetime import *
from queue import Queue
from threading import Thread
from time import sleep


class RelationDrawer(Thread):

    def __init__(self) -> None:
        Thread.__init__(self)
        self.mapList = list()
        self.mapList.append( UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

        self.dataTypeToIgnore = []
        self.dictOfParticipant = dict()
        self.drawerClass = DrawerClass()

        self.letShutdownThread = False
        self.queuePolicyFiles = Queue()
        self.listOfPolicyFiles = list()

    def run(self):
        while self.letShutdownThread == False or not self.queuePolicyFiles.empty():
            if self.queuePolicyFiles.empty():
                sleep(0.05)
            else:
                self.drawUml(self.queuePolicyFiles.get())

        if len(self.listOfPolicyFiles) > 0:
            self.drawListOfUml(self.listOfPolicyFiles)

    def enqueuePolicyFile(self, policyFile):
        self.queuePolicyFiles.put(policyFile)
        self.listOfPolicyFiles.append(policyFile)

    def drawUml(self, policyFile: PolicyFiles):
        self.dictOfParticipant = dict()
        self.drawerClass = DrawerClass()

        plantUmlList = list()
        plantUmlList.append("@startuml")

        self.dumpPolicyFile(policyFile)
        plantUmlList.extend(self.drawerClass.participants)
        plantUmlList.extend(self.drawerClass.rules)

        plantUmlList.append("@enduml")

        #Remove redundance items
        plantUmlList = list(dict.fromkeys(plantUmlList))
        #print(plantUmlList)
        filePath = "out/" + policyFile.fileName.replace("/","-")+"_relation.puml"
        self.writeToFile(filePath, plantUmlList)
        print("drawing: ", filePath)
        self.generatePng(filePath)
        #print(policyFile)

    def drawListOfUml(self, policyFiles: List[PolicyFiles]):
        self.dictOfParticipant = dict()
        self.drawerClass = DrawerClass()

        plantUmlList = list()
        plantUmlList.append("@startuml")

        for policyFile in policyFiles:
            self.dumpPolicyFile(policyFile)

        plantUmlList.extend(self.drawerClass.participants)
        plantUmlList.extend(self.drawerClass.rules)
        plantUmlList.append("@enduml")

        #Remove redundance items
        plantUmlList = list(dict.fromkeys(plantUmlList))
        #print(plantUmlList)
        filePath = "out/Integrated-" + datetime.today().strftime("%d-%m-%y---%H-%M-%s")+"_relation.puml"
        self.writeToFile(filePath, plantUmlList)
        print("drawing: ", filePath)
        self.generatePng(filePath)
        #print(policyFile)

    def dumpPolicyFile(self, policyFile: PolicyFiles):
        plantUmlList = list()

        if policyFile!=None:
            self.drawerClass.participants.extend(self.drawSeApp(policyFile.seApps))
            self.drawerClass.participants.extend(self.drawTypeDef(policyFile.typeDef))
            self.drawerClass.participants.extend(self.drawContext(policyFile.contexts))
            self.drawerClass.rules.extend(self.drawRule(policyFile.rules))

        return plantUmlList


    def drawTypeDef(self, typeDefs: List[TypeDef]):
        typeDefList = list()
        for typeDef in typeDefs:
                    #typeDef.append("\"" + typeDef.name + "\" -----> \"" + typeDef.types + "\"" )
                    typeDefList.append("participant " +  self.insertNewParticipant(typeDef.name)  + " [\n=" + typeDef.name + "\n ----- \n\"\"" + ', '.join(typeDef.types) + "\"\"\n]" )
        return typeDefList

    def drawContext(self, contexts: List[Context]):
        contextList = list()
        for context in contexts:
                    #contextList.append("\"" + context.pathName + "\" -----> \"" + context.securityContext.type + "\"" )
                    contextList.append("participant " +  self.insertNewParticipant(context.securityContext.type)   + " [\n=" + context.securityContext.type  + "\n ----- \n\"\"" + context.pathName + "\"\"\n]" )
        return contextList

    def drawSeApp(self, seAppContexts: List[SeAppContext]):
        seAppList = list()
        for seAppContext in seAppContexts:
                    #seAppList.append("\"" + seAppContext.user + "\" -----> \"" + seAppContext.domain + "\"" )
                    seAppList.append("participant " +  self.insertNewParticipant(seAppContext.domain)  + " [\n=" + seAppContext.domain + "\n ----- \n\"\"" + seAppContext.user + "\"\"\n]" )
        return seAppList

    def drawRule(self, rules: List[Rule]):
        ruleList = list()
        for rule in rules:
                    if rule.source in self.dictOfParticipant:
                        src=self.dictOfParticipant[rule.source]
                    else:
                        src=rule.source

                    if rule.rule == RuleEnum.NEVER_ALLOW :
                        ruleList.append("" + self.insertNewParticipant(rule.source) + " -----[#red]>x \"" + rule.target + "\" : " + rule.rule.label + " (" + ', '.join(rule.permissions) + ")")
                    else:
                        ruleList.append("" + self.insertNewParticipant(rule.source) + " -----[#green]> \"" + rule.target + "\" : " + rule.rule.label + " (" + ', '.join(rule.permissions) + ")")

        return ruleList

    def insertNewParticipant(self, name) :
        if  any(x in name for x in ["-","/",":"]) :
            if name not in self.dictOfParticipant:
                self.dictOfParticipant[name]=name.replace("-","__").replace("/","_1_").replace(":","_2_")
                #print ( "==========", name, self.dictOfParticipant[name])
                self.drawerClass.participants.append("participant " +  self.insertNewParticipant(self.dictOfParticipant[name])  + " [\n=" + name + "\n ]" )
            return self.dictOfParticipant[name]
        else:
            return name

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