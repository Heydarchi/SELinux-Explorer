from model.PolicyEntities import *
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
    # ATTRIBUTE = 5


@dataclass
class FilterRule(JSONWizard):
    filterType: FilterType = FilterType.DOMAIN
    keyword: str = ""
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

    def filter(self, lst_rules, policy_file):

        self.filteredPolicyFile = PolicyFiles()
        self.filteredPolicyFile.fileName = "domain_filtered"

        for filter_rule in lst_rules:
            self.filteredPolicyFile.fileName = self.filteredPolicyFile.fileName + \
                ("_ew_" if filter_rule.exactWord else "_") + filter_rule.keyword

            if FilterType(filter_rule.filterType) == FilterType.DOMAIN:
                self.filter_domain(filter_rule, policy_file)
            elif FilterType(filter_rule.filterType) == FilterType.PERMISSION:
                self.filter_permission(filter_rule, policy_file)
            elif FilterType(filter_rule.filterType) == FilterType.FILE_PATH:
                self.filter_pathname(filter_rule, policy_file)
            elif FilterType(filter_rule.filterType) == FilterType.CLASS_TYPE:
                self.filter_classyype(filter_rule, policy_file)

        self.remove_duplicated_Items()

        drawer = RelationDrawer()
        drawer.drawUml(self.filteredPolicyFile)

        drawer_adv = AdvancedDrawer()
        drawer_adv.drawUml(self.filteredPolicyFile)

        return generate_diagram_file_name(
            self.filteredPolicyFile.fileName), self.filteredPolicyFile

    def remove_duplicated_Items(self):
        # Remove duplicated items from typeDef, contexts, seApps, rules, macros of filteredPolicyFile
        # print(self.filteredPolicyFile.typeDef)
        self.filteredPolicyFile.typeDef = list(
            {item.name: item for item in self.filteredPolicyFile.typeDef}.values())
        self.filteredPolicyFile.contexts = list(
            {item.pathName: item for item in self.filteredPolicyFile.contexts}.values())
        self.filteredPolicyFile.seApps = list(
            {item.name: item for item in self.filteredPolicyFile.seApps}.values())

        # Define a lambda function to extract a hashable representation of each
        # Rule object
        def get_hashable_rule(r): return (
            r.rule,
            r.source,
            r.target,
            r.classType,
            tuple(
                sorted(
                    r.permissions)))
        # Remove duplicates based on all fields
        self.filteredPolicyFile.rules = list(
            {get_hashable_rule(r): r for r in self.filteredPolicyFile.rules}.values())

    def filter_domain(self, filterRule, policyFile):

        self.filteredPolicyFile.typeDef.extend(
            self.filter_typedef(filterRule, policyFile))
        self.filteredPolicyFile.contexts.extend(
            self.filter_context(filterRule, policyFile))
        self.filteredPolicyFile.seApps.extend(
            self.filter_se_app(filterRule, policyFile))
        self.filteredPolicyFile.rules.extend(
            self.filter_rule(filterRule, policyFile))
        self.filteredPolicyFile.macros.extend(
            self.filter_function(filterRule, policyFile))
        self.filteredPolicyFile.attribute.extend(
            self.filter_attribute(filterRule, policyFile))

    def filter_filename(self, filterRule, policyFile):
        # print("----filterFilename")
        if self.check_similarity(filterRule, policyFile.fileName):
            self.filteredPolicyFile.typeDef.extend(policyFile.typeDef)
            self.filteredPolicyFile.contexts.extend(policyFile.contexts)
            self.filteredPolicyFile.seApps.extend(policyFile.seApps)
            self.filteredPolicyFile.rules.extend(policyFile.rules)
            self.filteredPolicyFile.macros.extend(policyFile.macros)
            self.filteredPolicyFile.attribute.extend(policyFile.attribute)

    def filter_permission(self, filterRule, policyFile):
        '''Filter rules having permission in the policyFile and put them in filteredPolicyFile'''
        # print("----filterPermission: ", filterRule)
        for rule in policyFile.rules:
            if filterRule.keyword in rule.permissions:
                # print(rule)
                tempRule = rule
                tempRule.permissions = [filterRule.keyword]
                self.filteredPolicyFile.rules.append(tempRule)
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.source,
                            True),
                        policyFile))
                self.filteredPolicyFile.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.target,
                            True),
                        policyFile))

    def filter_pathname(self, filterRule, policyFile):
        '''filter context having pathName or se_app havong name in policyFile and add to self.filteredPolicyFile'''
        for context in policyFile.contexts:
            print("context.pathName: ", context.pathName, filterRule)
            if self.check_similarity(filterRule, context.pathName):
                if context.securityContext.type.strip().endswith("_exec"):
                    domain = context.securityContext.type.strip().replace("_exec", "")
                else:
                    domain = context.securityContext.type
                print(
                    "context.securityContext.type: ",
                    context.securityContext.type)
                self.filteredPolicyFile.contexts.append(context)
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.seApps.extend(self.filter_se_app(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.rules.extend(self.filter_rule(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))

        for se_app in policyFile.seApps:
            print("se_app.name: ", se_app.name, filterRule)
            if self.check_similarity(filterRule, se_app.name):
                if se_app.domain.strip().endswith("_exec"):
                    domain = se_app.domain.strip().replace("_exec", "")
                else:
                    domain = se_app.domain.strip()
                print("domain: ", domain)
                self.filteredPolicyFile.seApps.append(se_app)
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))
                self.filteredPolicyFile.rules.extend(self.filter_rule(
                    FilterRule(FilterType.DOMAIN, domain, True), policyFile))

    def filter_classyype(self, filterRule, policyFile):
        '''find domain and rule with the same class type and then filter based on the found domain'''
        for type_def in policyFile.typeDef:
            for type in type_def.types:
                if self.check_similarity(filterRule, type):
                    self.filteredPolicyFile.typeDef.append(type_def)
                    self.filteredPolicyFile.rules.extend(
                        self.filter_rule(
                            FilterRule(
                                FilterType.DOMAIN,
                                type_def.name,
                                True),
                            policyFile))
                    self.filteredPolicyFile.contexts.extend(self.filter_context(
                        FilterRule(FilterType.DOMAIN, type_def.name, True), policyFile))
                    self.filteredPolicyFile.seApps.extend(
                        self.filter_se_app(
                            FilterRule(
                                FilterType.DOMAIN,
                                type_def.name,
                                True),
                            policyFile))

        for rule in policyFile.rules:
            if self.check_similarity(filterRule, rule.classType):
                self.filteredPolicyFile.rules.append(rule)
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policyFile))
                self.filteredPolicyFile.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policyFile))
                self.filteredPolicyFile.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.source,
                            True),
                        policyFile))
                self.filteredPolicyFile.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.target,
                            True),
                        policyFile))

        for se_app in policyFile.seApps:
            for type in se_app.typeDef.types:
                if self.check_similarity(filterRule, type):
                    self.filteredPolicyFile.typeDef.append(se_app.typeDef)
                    self.filteredPolicyFile.rules.extend(
                        self.filter_rule(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policyFile))
                    self.filteredPolicyFile.contexts.extend(
                        self.filter_context(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policyFile))
                    self.filteredPolicyFile.seApps.extend(
                        self.filter_se_app(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policyFile))

    def check_similarity(self, filterRule, stringToCheck):
        if filterRule.exactWord:
            return stringToCheck.strip() == filterRule.keyword.strip()
        else:
            return filterRule.keyword.strip() in stringToCheck.strip()

    def filter_typedef(self, filterRule, policyFile):
        lst_tye_def = []
        for type_def in policyFile.typeDef:
            if self.check_similarity(filterRule, type_def.name):
                lst_tye_def.append(type_def)
        return lst_tye_def

    def filter_context(self, filterRule, policyFile):
        lst_context = []
        for context in policyFile.contexts:
            if self.check_similarity(filterRule, context.securityContext.type):
                lst_context.append(context)
        return lst_context

    def filter_se_app(self, filterRule, policyFile):
        lst_se_app = []
        for se_app in policyFile.seApps:
            if self.check_similarity(filterRule, se_app.domain):
                lst_se_app.append(se_app)
        return lst_se_app

    def filter_rule(self, filterRule, policyFile):
        lst_rule = []
        for rule in policyFile.rules:
            if self.check_similarity(
                    filterRule,
                    rule.source) or self.check_similarity(
                    filterRule,
                    rule.target):
                lst_rule.append(rule)
        return lst_rule

    def filter_function(self, filterRule, policyFile):
        lst_function = []
        for function in policyFile.macros:
            if self.check_similarity(filterRule, function.name):
                lst_function.append(function)
        return lst_function

    def filter_attribute(self, filterRule, policyFile):
        lst_attribute = []
        for attribute in policyFile.attribute:
            if self.check_similarity(filterRule, attribute.name):
                lst_attribute.append(attribute)
        return lst_attribute
