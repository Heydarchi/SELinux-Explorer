import os, sys
from PolicyEntities import  *
from RelationDrawer import *
class FilterResult:


    def filterDomain(self, domain, policyFiles, exactWord = False):
        filteredPolicyFile = PolicyFiles()
        filteredPolicyFile.fileName = "domain_filtered_" + ("ExactWord_" if exactWord  else "") + domain
        for policyFile in policyFiles:
            for typeDef in policyFile.typeDef:
                if self.checkSimilarity(exactWord, domain, typeDef.name):
                    filteredPolicyFile.typeDef.append(typeDef)

            for context in policyFile.contexts:
                if self.checkSimilarity(exactWord, domain, context.securityContext.type):
                    filteredPolicyFile.contexts.append(context)     

            for seApp in policyFile.seApps:
                if self.checkSimilarity(exactWord, domain, seApp.domain):
                    filteredPolicyFile.seApps.append(seApp)                                   

            for rule in policyFile.rules:
                if self.checkSimilarity(exactWord, domain, rule.source) or self.checkSimilarity(exactWord, domain, rule.target):
                    filteredPolicyFile.rules.append(rule)
            
        
        drawer = RelationDrawer()
        drawer.drawUml(filteredPolicyFile)
        return drawer.generatePngFileName(filteredPolicyFile.fileName)                                 


    def filterFilename(self, fileName, policyFiles, exactWord = False):
        pass

    def filterPermission(self, permission, policyFiles, exactWord = False):
        pass

    def filterPathName(self, pathName, policyFiles, exactWord = False):
        pass

    def filterTypedef(self, typeDef, policyFiles, exactWord = False):
        pass

    def checkSimilarity(self, exactWord, word, stringToCheck):
        if exactWord:
            return stringToCheck.strip() == word.strip()
        else:
            return word.strip() in stringToCheck.strip()