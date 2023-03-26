import os, sys
from PolicyEntities import  *
from PythonUtilityClasses import FileWriter as FW
from datetime import *
from queue import Queue
from threading import Thread
from time import sleep
from drawer.DrawerHelper import *

class AdvancedDrawer:

    def __init__(self) -> None:
        self.mapList = list()
        self.mapList.append( UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

        self.dataTypeToIgnore = []
        self.dictOfParticipant = dict()
        self.drawerClass = DrawerClass()

    def drawUml(self, policyFile):
        self.dictOfParticipant = dict()
        self.drawerClass = DrawerClass()

        plantUmlList = list()
        plantUmlList.append("@startuml")

        self.dumpPolicyFile(policyFile)

        plantUmlList.extend(DrawingTool.defineDomainStyle())
        plantUmlList.extend(DrawingTool.defineNoteStyle())
        plantUmlList.extend(self.drawerClass.participants)
        plantUmlList.extend(self.drawerClass.rules)
        plantUmlList.append("@enduml")

        #Remove redundance items
        #Temporary disabled since removes blindlt : plantUmlList = list(dict.fromkeys(plantUmlList))
        
        #print(plantUmlList)
        filePath = "out/Integrated-" + datetime.today().strftime("%d-%m-%y---%H-%M-%s")+"_relation_adv.puml"
        self.writeToFile(filePath, plantUmlList)
        print("drawing: ", filePath)

        generatePng(filePath)
        #print(policyFile)


    def dumpPolicyFile(self, policyFile: PolicyFiles):
        plantUmlList = list()

        policyFile = self.correlateData(policyFile)

        if policyFile!=None:
            self.drawerClass.participants.extend(self.drawSeApp(policyFile.seApps))
            self.drawerClass.participants.extend(self.drawTypeDef(policyFile.typeDef))
            self.drawerClass.participants.extend(self.drawContext(policyFile.contexts))
            self.drawerClass.rules.extend(self.drawRule(policyFile.rules))

        return plantUmlList

    def correlateData(self, policyFile: PolicyFiles):
        for seapp in policyFile.seApps:
              for typeDef in policyFile.typeDef:
                if seapp.domain == typeDef.name :
                    seapp.typeDef = typeDef
                    policyFile.typeDef.remove(typeDef)
                    break

              for attribute in policyFile.attribute:
                if seapp.domain == attribute.name :
                    seapp.attribute = attribute
                    policyFile.attribute.remove(attribute)
                    break

        for context in policyFile.contexts:
              for  i in reversed(range(len(policyFile.typeDef))):
                if context.securityContext.type.replace(DOMAIN_EXECUTABLE, "") == typeDef.name :
                    print(context.securityContext.type, policyFile.typeDef[i].name)
                    context.domainName = policyFile.typeDef[i].name
                    context.typeDef.types.extend(policyFile.typeDef[i].types)
                    policyFile.typeDef.remove_at(i)
                    #print(context, typeDef)
                    break
                
        return policyFile
    
    def drawTypeDef(self, typeDefs: List[TypeDef]):
        typeDefList = list()
        for typeDef in typeDefs:
                    #typeDefList.append("rectangle \""  + typeDef.name + "\" as " + self.insertNewParticipant(typeDef.name) )
                    typeDefList.extend(DrawingTool.generateDomain(typeDef.name))

                    lstNote=list()
                    lstNote.extend(typeDef.types)
                    typeDefList.extend(DrawingTool.generateNote(typeDef.name, DrawingPosition.TOP, lstNote))
        return typeDefList

    def drawContext(self, contexts: List[Context]):
        contextList = list()
        for context in contexts:
                    #contextList.append("rectangle \""  + context.securityContext.type  + "\" as " + self.insertNewParticipant(context.securityContext.type) )
                    contextList.extend(DrawingTool.generateOtherLabel(context.securityContext.type))

                    lstNote=list()
                    lstNote.append("Path: " + context.pathName)
                    lstNote.extend(context.typeDef.types)
                    contextList.extend(DrawingTool.generateNote(context.securityContext.type, DrawingPosition.TOP, lstNote))
        return contextList

    def drawSeApp(self, seAppContexts: List[SeAppContext]):
        seAppList = list()
        for seAppContext in seAppContexts:
                    #seAppList.append("rectangle \"" + seAppContext.user + '/'.join(seAppContext.typeDef.types) + '/'.join(seAppContext.attribute.attributes) + "/" + seAppContext.domain + "\" as " + self.insertNewParticipant(seAppContext.domain) )
                    seAppList.extend(DrawingTool.generateDomain(seAppContext.domain))

                    lstNote=list()
                    lstNote.append(seAppContext.user)
                    lstNote.extend(seAppContext.typeDef.types)
                    lstNote.extend(seAppContext.attribute.attributes)
                    seAppList.extend(DrawingTool.generateNote(seAppContext.domain, DrawingPosition.TOP, lstNote))
        return seAppList

    def drawRule(self, rules: List[Rule]):
        ruleList = list()
        for rule in rules:
                    if rule.source in self.dictOfParticipant:
                        src=self.dictOfParticipant[rule.source]
                    else:
                        src=rule.source

                    if rule.rule == RuleEnum.NEVER_ALLOW :
                        ruleList.append("" + self.insertNewParticipant(rule.source) + " -----[#red]> \"" + rule.target + "\" : " + rule.rule.label + " (" + ', '.join(rule.permissions) + ")")
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

    
    