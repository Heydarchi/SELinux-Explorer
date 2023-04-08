from model.PolicyEntities import  *
from drawer.RelationDrawer import *
from drawer.AdvanceDrawer import *
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from drawer.DrawerHelper import *

class FilterType(Enum):
    DOMAIN = 1
    CLASS_TYPE = 2
    PERMISSION = 3
    FILE_PATH = 4
    #ATTRIBUTE = 5
@dataclass
class FilterRule(JSONWizard):
    filterType: FilterType = FilterType.DOMAIN
    keyword : str = ""
    exactWord: bool = False

    def __eq__(self, other):
        return isinstance(other, FilterRule) and \
               self.filterType == other.filterType and \
               self.keyword == other.keyword and \
               self.exactWord == other.exactWord

    def __hash__(self):
        return hash((self.filterType, self.keyword, self.exactWord))

    @staticmethod
    def getFilterTypeFromStr(keyword):
        for filterType in FilterType:
            if keyword == filterType.name:
                return filterType

class FilterResult:

    def filter(self, lstRules, policyFile):

        self.filteredPolicyFile = PolicyFiles()
        self.filteredPolicyFile.fileName = "domain_filtered"

        for filterRule in lstRules :
            self.filteredPolicyFile.fileName =  self.filteredPolicyFile.fileName + ("_ew_" if filterRule.exactWord  else "_") + filterRule.keyword

            if FilterType(filterRule.filterType) == FilterType.DOMAIN:
                self.filterDomain(filterRule, policyFile)
            elif FilterType(filterRule.filterType) == FilterType.PERMISSION:
                self.filterPermission(filterRule, policyFile)
            elif FilterType(filterRule.filterType) == FilterType.FILE_PATH:
                self.filterPathName(filterRule, policyFile)
            elif FilterType(filterRule.filterType) == FilterType.CLASS_TYPE:
                self.filterClassType(filterRule, policyFile)

        self.removeDuplicatedItems()

        drawer = RelationDrawer()
        drawer.drawUml(self.filteredPolicyFile)

        drawerAdv = AdvancedDrawer()
        drawerAdv.drawUml(self.filteredPolicyFile)

        return generateDiagramFileName(self.filteredPolicyFile.fileName),  self.filteredPolicyFile


    def removeDuplicatedItems(self):
    #Remove duplicated items from typeDef, contexts, seApps, rules, macros of filteredPolicyFile
        #print(self.filteredPolicyFile.typeDef)
        self.filteredPolicyFile.typeDef = list({item.name: item for item in self.filteredPolicyFile.typeDef}.values())
        self.filteredPolicyFile.contexts = list({item.pathName: item for item in self.filteredPolicyFile.contexts}.values())
        self.filteredPolicyFile.seApps = list({item.name: item for item in self.filteredPolicyFile.seApps}.values())

        # Define a lambda function to extract a hashable representation of each Rule object
        get_hashable_rule = lambda r: (r.rule, r.source, r.target, r.classType, tuple(sorted(r.permissions)))
            # Remove duplicates based on all fields
        self.filteredPolicyFile.rules= list({get_hashable_rule(r): r for r in self.filteredPolicyFile.rules}.values())



    def filterDomain(self, filterRule, policyFile):

        self.filteredPolicyFile.typeDef.extend(self.filterTypedef(filterRule, policyFile))
        self.filteredPolicyFile.contexts.extend(self.filterContext(filterRule, policyFile))
        self.filteredPolicyFile.seApps.extend(self.filterSeApp(filterRule, policyFile))
        self.filteredPolicyFile.rules.extend(self.filterRule(filterRule, policyFile))
        self.filteredPolicyFile.macros.extend(self.filterFunction(filterRule, policyFile))
        self.filteredPolicyFile.attribute.extend(self.filterAttribute(filterRule, policyFile))


    def filterFilename(self, filterRule, policyFile):
        #print("----filterFilename")
        if self.checkSimilarity(filterRule, policyFile.fileName):
            self.filteredPolicyFile.typeDef.extend(policyFile.typeDef)
            self.filteredPolicyFile.contexts.extend(policyFile.contexts)
            self.filteredPolicyFile.seApps.extend(policyFile.seApps)
            self.filteredPolicyFile.rules.extend(policyFile.rules)
            self.filteredPolicyFile.macros.extend(policyFile.macros)
            self.filteredPolicyFile.attribute.extend(policyFile.attribute)



    def filterPermission(self, filterRule, policyFile):
        '''Filter rules having permission in the policyFile and put them in filteredPolicyFile'''
        #print("----filterPermission: ", filterRule)
        for rule in policyFile.rules:
            if filterRule.keyword in rule.permissions:
                #print(rule)
                tempRule = rule
                tempRule.permissions = [filterRule.keyword]
                self.filteredPolicyFile.rules.append(tempRule)
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))

    def filterPathName(self, filterRule, policyFile):
        '''filter context having pathName or seApp havong name in policyFile and add to self.filteredPolicyFile'''
        for context in policyFile.contexts:
            print("context.pathName: ", context.pathName, filterRule)
            if self.checkSimilarity(filterRule, context.pathName):
                if context.securityContext.type.strip().endswith("_exec"):
                    domain = context.securityContext.type.strip().replace("_exec", "")
                else:
                    domain = context.securityContext.type
                print("context.securityContext.type: ", context.securityContext.type)
                self.filteredPolicyFile.contexts.append(context)
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, domain, True), policyFile))

        for seApp in policyFile.seApps:
            print("seApp.name: ", seApp.name, filterRule)
            if self.checkSimilarity(filterRule, seApp.name):
                if seApp.domain.strip().endswith("_exec"):
                    domain = seApp.domain.strip().replace("_exec", "")
                else:
                    domain = seApp.domain.strip()
                print("domain: ", domain)
                self.filteredPolicyFile.seApps.append(seApp)
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, domain, True), policyFile))

    def filterClassType(self, filterRule, policyFile):
        '''find domain and rule with the same class type and then filter based on the found domain'''
        for typeDef in policyFile.typeDef:
            for type in typeDef.types:
                if self.checkSimilarity(filterRule, type):
                    self.filteredPolicyFile.typeDef.append(typeDef)
                    self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, typeDef.name, True), policyFile))
                    self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, typeDef.name, True), policyFile))
                    self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, typeDef.name, True), policyFile))

        for rule in policyFile.rules:
            if self.checkSimilarity(filterRule, rule.classType):
                self.filteredPolicyFile.rules.append(rule)
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.typeDef.extend(self.filterTypedef(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))

        for seapp in policyFile.seApps:
            for type in seapp.typeDef.types:
                if self.checkSimilarity(filterRule, type):
                    self.filteredPolicyFile.typeDef.append(seapp.typeDef)
                    self.filteredPolicyFile.rules.extend(self.filterRule(FilterRule(FilterType.DOMAIN, seapp.typeDef.name, True), policyFile))
                    self.filteredPolicyFile.contexts.extend(self.filterContext(FilterRule(FilterType.DOMAIN, seapp.typeDef.name, True), policyFile))
                    self.filteredPolicyFile.seApps.extend(self.filterSeApp(FilterRule(FilterType.DOMAIN, seapp.typeDef.name, True), policyFile))


    def checkSimilarity(self, filterRule, stringToCheck):
        if filterRule.exactWord:
            return stringToCheck.strip() == filterRule.keyword.strip()
        else:
            return filterRule.keyword.strip() in stringToCheck.strip()

    def filterTypedef(self, filterRule, policyFile):
        lstTyeDef = []
        for typeDef in policyFile.typeDef:
            if self.checkSimilarity(filterRule, typeDef.name):
                lstTyeDef.append(typeDef)
        return lstTyeDef

    def filterContext(self, filterRule, policyFile):
        lstContext = []
        for context in policyFile.contexts:
            if self.checkSimilarity(filterRule, context.securityContext.type):
                lstContext.append(context)
        return lstContext

    def filterSeApp(self, filterRule, policyFile):
        lstSeApp = []
        for seApp in policyFile.seApps:
            if self.checkSimilarity(filterRule, seApp.domain):
                lstSeApp.append(seApp)
        return lstSeApp

    def filterRule(self, filterRule, policyFile):
        lstRule = []
        for rule in policyFile.rules:
            if self.checkSimilarity(filterRule, rule.source) or self.checkSimilarity(filterRule, rule.target):
                lstRule.append(rule)
        return lstRule

    def filterFunction(self, filterRule, policyFile):
        lstFunction = []
        for function in policyFile.macros:
            if self.checkSimilarity(filterRule, function.name):
                lstFunction.append(function)
        return lstFunction

    def filterAttribute(self, filterRule, policyFile):
        lstAttribute = []
        for attribute in policyFile.attribute:
            if self.checkSimilarity(filterRule, attribute.name):
                lstAttribute.append(attribute)
        return lstAttribute
