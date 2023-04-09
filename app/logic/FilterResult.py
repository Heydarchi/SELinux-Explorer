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
        for filter_type in FilterType:
            if keyword == filter_type.name:
                return filter_type


class FilterResult:

    def filter(self, lst_rules, policy_file):

        self.filtered_policy_file = PolicyFile()
        self.filtered_policy_file.fileName = "domain_filtered"

        for filter_rule in lst_rules:
            self.filtered_policy_file.fileName = self.filtered_policy_file.fileName + \
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
        drawer.draw_uml(self.filtered_policy_file)

        drawer_adv = AdvancedDrawer()
        drawer_adv.draw_uml(self.filtered_policy_file)

        return generate_diagram_file_name(
            self.filtered_policy_file.fileName), self.filtered_policy_file

    def remove_duplicated_Items(self):
        # Remove duplicated items from typeDef, contexts, seApps, rules, macros of filtered_policy_file
        # print(self.filtered_policy_file.typeDef)
        self.filtered_policy_file.typeDef = list(
            {item.name: item for item in self.filtered_policy_file.typeDef}.values())
        self.filtered_policy_file.contexts = list(
            {item.pathName: item for item in self.filtered_policy_file.contexts}.values())
        self.filtered_policy_file.seApps = list(
            {item.name: item for item in self.filtered_policy_file.seApps}.values())

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
        self.filtered_policy_file.rules = list(
            {get_hashable_rule(r): r for r in self.filtered_policy_file.rules}.values())

    def filter_domain(self, filter_rule, policy_file):

        self.filtered_policy_file.typeDef.extend(
            self.filter_typedef(filter_rule, policy_file))
        self.filtered_policy_file.contexts.extend(
            self.filter_context(filter_rule, policy_file))
        self.filtered_policy_file.seApps.extend(
            self.filter_se_app(filter_rule, policy_file))
        self.filtered_policy_file.rules.extend(
            self.filter_rule(filter_rule, policy_file))
        self.filtered_policy_file.macros.extend(
            self.filter_function(filter_rule, policy_file))
        self.filtered_policy_file.attribute.extend(
            self.filter_attribute(filter_rule, policy_file))

    def filter_filename(self, filter_rule, policy_file):
        # print("----filter_filename")
        if self.check_similarity(filter_rule, policy_file.fileName):
            self.filtered_policy_file.typeDef.extend(policy_file.typeDef)
            self.filtered_policy_file.contexts.extend(policy_file.contexts)
            self.filtered_policy_file.seApps.extend(policy_file.seApps)
            self.filtered_policy_file.rules.extend(policy_file.rules)
            self.filtered_policy_file.macros.extend(policy_file.macros)
            self.filtered_policy_file.attribute.extend(policy_file.attribute)

    def filter_permission(self, filter_rule, policy_file):
        '''Filter rules having permission in the policy_file and put them in filtered_policy_file'''
        # print("----filter_permission: ", filter_rule)
        for rule in policy_file.rules:
            if filter_rule.keyword in rule.permissions:
                # print(rule)
                tempRule = rule
                tempRule.permissions = [filter_rule.keyword]
                self.filtered_policy_file.rules.append(tempRule)
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policy_file))
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policy_file))
                self.filtered_policy_file.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policy_file))
                self.filtered_policy_file.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policy_file))
                self.filtered_policy_file.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.source,
                            True),
                        policy_file))
                self.filtered_policy_file.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.target,
                            True),
                        policy_file))

    def filter_pathname(self, filter_rule, policy_file):
        '''filter context having pathName or se_app havong name
        in policy_file and add to self.filtered_policy_file'''
        for context in policy_file.contexts:
            print("context.pathName: ", context.pathName, filter_rule)
            if self.check_similarity(filter_rule, context.pathName):
                if context.securityContext.type.strip().endswith("_exec"):
                    domain = context.securityContext.type.strip().replace("_exec", "")
                else:
                    domain = context.securityContext.type
                print(
                    "context.securityContext.type: ",
                    context.securityContext.type)
                self.filtered_policy_file.contexts.append(context)
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))
                self.filtered_policy_file.seApps.extend(self.filter_se_app(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))
                self.filtered_policy_file.rules.extend(self.filter_rule(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))

        for se_app in policy_file.seApps:
            print("se_app.name: ", se_app.name, filter_rule)
            if self.check_similarity(filter_rule, se_app.name):
                if se_app.domain.strip().endswith("_exec"):
                    domain = se_app.domain.strip().replace("_exec", "")
                else:
                    domain = se_app.domain.strip()
                print("domain: ", domain)
                self.filtered_policy_file.seApps.append(se_app)
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))
                self.filtered_policy_file.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))
                self.filtered_policy_file.rules.extend(self.filter_rule(
                    FilterRule(FilterType.DOMAIN, domain, True), policy_file))

    def filter_classyype(self, filter_rule, policy_file):
        '''find domain and rule with the same class type
        and then filter based on the found domain'''
        for type_def in policy_file.typeDef:
            for type in type_def.types:
                if self.check_similarity(filter_rule, type):
                    self.filtered_policy_file.typeDef.append(type_def)
                    self.filtered_policy_file.rules.extend(
                        self.filter_rule(
                            FilterRule(
                                FilterType.DOMAIN,
                                type_def.name,
                                True),
                            policy_file))
                    self.filtered_policy_file.contexts.extend(self.filter_context(
                        FilterRule(FilterType.DOMAIN, type_def.name, True), policy_file))
                    self.filtered_policy_file.seApps.extend(
                        self.filter_se_app(
                            FilterRule(
                                FilterType.DOMAIN,
                                type_def.name,
                                True),
                            policy_file))

        for rule in policy_file.rules:
            if self.check_similarity(filter_rule, rule.classType):
                self.filtered_policy_file.rules.append(rule)
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policy_file))
                self.filtered_policy_file.typeDef.extend(self.filter_typedef(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policy_file))
                self.filtered_policy_file.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.source, True), policy_file))
                self.filtered_policy_file.contexts.extend(self.filter_context(
                    FilterRule(FilterType.DOMAIN, rule.target, True), policy_file))
                self.filtered_policy_file.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.source,
                            True),
                        policy_file))
                self.filtered_policy_file.seApps.extend(
                    self.filter_se_app(
                        FilterRule(
                            FilterType.DOMAIN,
                            rule.target,
                            True),
                        policy_file))

        for se_app in policy_file.seApps:
            for type in se_app.typeDef.types:
                if self.check_similarity(filter_rule, type):
                    self.filtered_policy_file.typeDef.append(se_app.typeDef)
                    self.filtered_policy_file.rules.extend(
                        self.filter_rule(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policy_file))
                    self.filtered_policy_file.contexts.extend(
                        self.filter_context(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policy_file))
                    self.filtered_policy_file.seApps.extend(
                        self.filter_se_app(
                            FilterRule(
                                FilterType.DOMAIN,
                                se_app.typeDef.name,
                                True),
                            policy_file))

    def check_similarity(self, filter_rule, string_to_check):
        if filter_rule.exactWord:
            return string_to_check.strip() == filter_rule.keyword.strip()
        else:
            return filter_rule.keyword.strip() in string_to_check.strip()

    def filter_typedef(self, filter_rule, policy_file):
        lst_tye_def = []
        for type_def in policy_file.typeDef:
            if self.check_similarity(filter_rule, type_def.name):
                lst_tye_def.append(type_def)
        return lst_tye_def

    def filter_context(self, filter_rule, policy_file):
        lst_context = []
        for context in policy_file.contexts:
            if self.check_similarity(filter_rule, context.securityContext.type):
                lst_context.append(context)
        return lst_context

    def filter_se_app(self, filter_rule, policy_file):
        lst_se_app = []
        for se_app in policy_file.seApps:
            if self.check_similarity(filter_rule, se_app.domain):
                lst_se_app.append(se_app)
        return lst_se_app

    def filter_rule(self, filter_rule, policy_file):
        lst_rule = []
        for rule in policy_file.rules:
            if self.check_similarity(
                    filter_rule,
                    rule.source) or self.check_similarity(
                    filter_rule,
                    rule.target):
                lst_rule.append(rule)
        return lst_rule

    def filter_function(self, filter_rule, policy_file):
        lst_function = []
        for function in policy_file.macros:
            if self.check_similarity(filter_rule, function.name):
                lst_function.append(function)
        return lst_function

    def filter_attribute(self, filter_rule, policy_file):
        lst_attribute = []
        for attribute in policy_file.attribute:
            if self.check_similarity(filter_rule, attribute.name):
                lst_attribute.append(attribute)
        return lst_attribute
