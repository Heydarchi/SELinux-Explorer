from model.PolicyEntities import  *
from drawer.RelationDrawer import *
from drawer.AdvanceDrawer import *
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from drawer.DrawerHelper import *

class FilterType(Enum):
    DOMAIN = 1
    FILE_NAME = 2
    TYPE_DEF = 3
    PERMISSION = 4
@dataclass
class FilterRule(JSONWizard):
    filterType: FilterType = FilterType.DOMAIN
    keyword : str = ""
    exactWord: bool = False

class FilterResult:

    def filter(self, lstRules, policyFiles):
        self.filteredPolicyFile = PolicyFiles()
        self.filteredPolicyFile.fileName = "domain_filtered" 
        for filterRule in lstRules :
            self.filteredPolicyFile.fileName =  self.filteredPolicyFile.fileName + ("_EW_" if filterRule.exactWord  else "_") + filterRule.keyword
            if filterRule.filterType == FilterType.DOMAIN:
                self.filterDomain(filterRule, policyFiles)
            elif filterRule.filterType == FilterType.FILE_NAME:
                self.filterFilename(filterRule, policyFiles)
            
        
        drawer = RelationDrawer()
        drawer.drawUml(self.filteredPolicyFile)

        drawerAdv = AdvancedDrawer()
        drawerAdv.drawUml(self.filteredPolicyFile)

        return generatePngFileName(self.filteredPolicyFile.fileName),  self.filteredPolicyFile


    def filterDomain(self, filterRule, policyFiles):
            for policyFile in policyFiles:
                for typeDef in policyFile.typeDef:
                    if self.checkSimilarity(filterRule, typeDef.name):
                        self.filteredPolicyFile.typeDef.append(typeDef)

                for context in policyFile.contexts:
                    if self.checkSimilarity(filterRule, context.securityContext.type):
                        self.filteredPolicyFile.contexts.append(context)     

                for seApp in policyFile.seApps:
                    if self.checkSimilarity(filterRule, seApp.domain):
                        self.filteredPolicyFile.seApps.append(seApp)                                   

                for rule in policyFile.rules:
                    if self.checkSimilarity(filterRule, rule.source) or self.checkSimilarity(filterRule, rule.target):
                        self.filteredPolicyFile.rules.append(rule)
            

    def filterFilename(self, filterRule, policyFiles):
            print("----filterFilename")
            for policyFile in policyFiles:
                for context in policyFile.contexts:
                    if context.pathName.strip() == filterRule.keyword.strip():
                        print(policyFile.fileName)
                        self.filteredPolicyFile.typeDef.extend(policyFile.typeDef)
                        self.filteredPolicyFile.contexts.extend(policyFile.contexts)
                        self.filteredPolicyFile.seApps.extend(policyFile.seApps)
                        self.filteredPolicyFile.rules.extend(policyFile.rules)
                        self.filteredPolicyFile.attribute.extend(policyFile.attribute)
                        self.filteredPolicyFile.functions.extend(policyFile.functions)
                        break
                for context in policyFile.contexts:
                    if context.pathName.strip() == filterRule.keyword.strip():
                        self.filteredPolicyFile.typeDef.extend(policyFile.typeDef)
                        self.filteredPolicyFile.contexts.extend(policyFile.contexts)
                        self.filteredPolicyFile.seApps.extend(policyFile.seApps)
                        self.filteredPolicyFile.rules.extend(policyFile.rules)
                        self.filteredPolicyFile.attribute.extend(policyFile.attribute)
                        self.filteredPolicyFile.functions.extend(policyFile.functions)
                        break



    def filterPermission(self, permission, policyFiles):
        pass

    def filterPathName(self, pathName, policyFiles):
        pass

    def filterTypedef(self, typeDef, policyFiles):
        pass

    def checkSimilarity(self, filterRule, stringToCheck):
        if filterRule.exactWord:
            return stringToCheck.strip() == filterRule.keyword.strip()
        else:
            return filterRule.keyword.strip() in stringToCheck.strip()