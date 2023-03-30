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
    FILE_PATH = 5
@dataclass
class FilterRule(JSONWizard):
    filterType: FilterType = FilterType.DOMAIN
    keyword : str = ""
    exactWord: bool = False

    @staticmethod
    def getFilterTypeFromStr(keyword):
        for filterType in FilterType:
            if keyword == filterType.name:
                return filterType
class FilterResult:

    def filter(self, lstRules, policyFiles):
        self.filteredPolicyFile = PolicyFiles()
        self.filteredPolicyFile.fileName = "domain_filtered" 
        for filterRule in lstRules :
            #print("filterRule: ", filterRule)
            #print("FilterType.PERMISSION: ", FilterType.PERMISSION, filterRule.filterType)
            self.filteredPolicyFile.fileName =  self.filteredPolicyFile.fileName + ("_EW_" if filterRule.exactWord  else "_") + filterRule.keyword
            if FilterType(filterRule.filterType) == FilterType.DOMAIN:
                self.filterDomain(filterRule, policyFiles)
            elif FilterType(filterRule.filterType) == FilterType.FILE_NAME:
                self.filterFilename(filterRule, policyFiles)
            elif FilterType(filterRule.filterType) == FilterType.PERMISSION:
                self.filterPermission(filterRule, policyFiles)
            elif FilterType(filterRule.filterType) == FilterType.FILE_PATH:
                self.filterPathName(filterRule, policyFiles)

        self.removeDuplicatedItems()

        drawer = RelationDrawer()
        drawer.drawUml(self.filteredPolicyFile)

        drawerAdv = AdvancedDrawer()
        drawerAdv.drawUml(self.filteredPolicyFile)

        return generatePngFileName(self.filteredPolicyFile.fileName),  self.filteredPolicyFile


    def removeDuplicatedItems(self):
    #Remove duplicated items from typeDef, contexts, seApps, rules, functions of filteredPolicyFile
        #print(self.filteredPolicyFile.typeDef)
        self.filteredPolicyFile.typeDef = list({item.name: item for item in self.filteredPolicyFile.typeDef}.values())
        self.filteredPolicyFile.contexts = list({item.pathName: item for item in self.filteredPolicyFile.contexts}.values())
        self.filteredPolicyFile.seApps = list({item.name: item for item in self.filteredPolicyFile.seApps}.values())

        # Define a lambda function to extract a hashable representation of each Rule object
        get_hashable_rule = lambda r: (r.rule, r.source, r.target, r.classType, tuple(sorted(r.permissions)))
            # Remove duplicates based on all fields
        self.filteredPolicyFile.rules= list({get_hashable_rule(r): r for r in self.filteredPolicyFile.rules}.values())



    def filterDomain(self, filterRule, policyFiles):

            self.filteredPolicyFile.typeDef.extend(self.filterTypedef(filterRule, policyFiles))
            self.filteredPolicyFile.contexts.extend(self.filterContext(filterRule, policyFiles))
            self.filteredPolicyFile.seApps.extend(self.filterSeApp(filterRule, policyFiles))
            self.filteredPolicyFile.rules.extend(self.filterRule(filterRule, policyFiles))
            self.filteredPolicyFile.functions.extend(self.filterFunction(filterRule, policyFiles))
            self.filteredPolicyFile.attribute.extend(self.filterAttribute(filterRule, policyFiles))


    def filterFilename(self, filterRule, policyFiles):
            #print("----filterFilename")
            for policyFile in policyFiles:
                if self.checkSimilarity(filterRule, policyFile.fileName):
                    self.filteredPolicyFile.typeDef.extend(policyFile.typeDef)
                    self.filteredPolicyFile.contexts.extend(policyFile.contexts)
                    self.filteredPolicyFile.seApps.extend(policyFile.seApps)
                    self.filteredPolicyFile.rules.extend(policyFile.rules)
                    self.filteredPolicyFile.functions.extend(policyFile.functions)
                    self.filteredPolicyFile.attribute.extend(policyFile.attribute)



    def filterPermission(self, filterRule, policyFiles):
        '''Filter rules having permission for each policyFile in policyFiles and put them in filteredPolicyFile'''
        #print("----filterPermission: ", filterRule)
        for plicyFile in policyFiles:
            for rule in plicyFile.rules:
                if self.checkSimilarity(filterRule, rule.permissions):
                    #print(rule)
                    self.filteredPolicyFile.rules.append(rule)
                    self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.source, True), policyFiles))
                    self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.target, True), policyFiles))
                    self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.source, True), policyFiles))
                    self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.target, True), policyFiles))
                    self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.source, True), policyFiles))
                    self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.target, True), policyFiles))

    def filterPathName(self, filterRule, policyFiles):
        '''filter context having pathName or seApp havong name in policyFiles and add to self.filteredPolicyFile'''
        for policyFile in policyFiles:
            for context in policyFile.contexts:
                print("context.pathName: ", context.pathName, filterRule)
                if self.checkSimilarity(filterRule, context.pathName):
                    if context.securityContext.type.strip().endswith("_exec"):
                        domain = context.securityContext.type.strip().replace("_exec", "")
                    else:
                        domain = context.securityContext.type
                    print("context.securityContext.type: ", context.securityContext.type)
                    self.filteredPolicyFile.contexts.append(context)
                    self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))
                    self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))
                    self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))

            for seApp in policyFile.seApps:
                print("seApp.name: ", seApp.name, filterRule)
                if self.checkSimilarity(filterRule, seApp.name):
                    if seApp.domain.strip().endswith("_exec"):
                        domain = seApp.domain.strip().replace("_exec", "")
                    else:
                        domain = seApp.domain.strip()
                    print("domain: ", domain)
                    self.filteredPolicyFile.seApps.append(seApp)
                    self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))
                    self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))
                    self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, domain, True), policyFiles))


    def checkSimilarity(self, filterRule, stringToCheck):
        if filterRule.exactWord:
            return stringToCheck.strip() == filterRule.keyword.strip()
        else:
            return filterRule.keyword.strip() in stringToCheck.strip()

    def filterTypedef(self, filterRule, policyFiles):
        #print("---", filterRule)
        lstTyeDef = []
        for policyFile in policyFiles:
            for typeDef in policyFile.typeDef:
                if self.checkSimilarity(filterRule, typeDef.name):
                    lstTyeDef.append(typeDef)
        #print("---", lstTyeDef)
        return lstTyeDef

    def filterContext(self, filterRule, policyFiles):
        lstContext = []
        for policyFile in policyFiles:
            for context in policyFile.contexts:
                if self.checkSimilarity(filterRule, context.securityContext.type):
                    lstContext.append(context)
        return lstContext

    def filterSeApp(self, filterRule, policyFiles):
        lstSeApp = []
        for policyFile in policyFiles:
            for seApp in policyFile.seApps:
                if self.checkSimilarity(filterRule, seApp.domain):
                    lstSeApp.append(seApp)
        return lstSeApp

    def filterRule(self, filterRule, policyFiles):
        lstRule = []
        for policyFile in policyFiles:
            for rule in policyFile.rules:
                if self.checkSimilarity(filterRule, rule.source) or self.checkSimilarity(filterRule, rule.target):
                    lstRule.append(rule)
        return lstRule

    def filterFunction(self, filterRule, policyFiles):
        lstFunction = []
        for policyFile in policyFiles:
            for function in policyFile.functions:
                if self.checkSimilarity(filterRule, function.name):
                    lstFunction.append(function)
        return lstFunction

    def filterAttribute(self, filterRule, policyFiles):
        lstAttribute = []
        for policyFile in policyFiles:
            for attribute in policyFile.attribute:
                if self.checkSimilarity(filterRule, attribute.name):
                    lstAttribute.append(attribute)
        return lstAttribute
