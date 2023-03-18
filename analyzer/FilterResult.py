import os, sys
from PolicyEntities import  *
from RelationDrawer import *
class FilterResult:


    def filterDomain(self, domain, policyFiles):
        filteredPolicyFile = PolicyFiles()
        filteredPolicyFile.fileName = "domain_filtered_" + domain
        for policyFile in policyFiles:
            for typeDef in policyFile.typeDef:
                if domain in typeDef.name:
                    filteredPolicyFile.typeDef.append(typeDef)

            for context in policyFile.contexts:
                if domain == context.securityContext.type:
                    filteredPolicyFile.contexts.append(context)     

            for seApp in policyFile.seApps:
                if domain in seApp.domain:
                    filteredPolicyFile.seApps.append(seApp)                                   

            for rule in policyFile.rules:
                if domain in rule.source or domain in rule.target:
                    filteredPolicyFile.rules.append(rule)
            
        
        drawer = RelationDrawer()
        drawer.drawUml(filteredPolicyFile)
        return drawer.generatePngFileName(filteredPolicyFile.fileName)                                 


    def filterFilename(self, fileName, policyFiles):
        pass

    def filterPermission(self, permission, policyFiles):
        pass

    def filterPathName(self, pathName, policyFiles):
        pass

    def filterTypedef(self, typeDef, policyFiles):
        pass