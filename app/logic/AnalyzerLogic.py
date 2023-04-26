from analyzer.FileAnalyzer import *
from drawer.RelationDrawer import *
from drawer.DrawerHelper import *
from AppSetting import *
from model.PolicyEntities import *
from logic.FilterResult import *


class AnalyzerLogic:
    def __init__(self):
        super().__init__()
        self._init_variables()
        self.init_analyzer()

    def _init_variables(self):
        self.keep_result = False
        self.list_of_diagrams = []
        self.ref_policy_file = PolicyFile()
        self.drawer = RelationDrawer()

    def init_analyzer(self):
        self.analyzer = FileAnalyzer()

    def analyze_all(self, paths):
        if self.keep_result:
            policy_files.extend(self.analyzer.analyze(paths))
        else:
            policy_files = self.analyzer.analyze(paths)

        self.ref_policy_file = self.make_ref_policy_file(policy_files)
        self.on_analyze_finished(None)
        self.update_analyzer_data_result(self.ref_policy_file)

    def make_ref_policy_file(self, policy_files):
        if policy_files is None or len(policy_files) == 0:
            return None

        ref_policy_file = PolicyFile()
        for policy_file in policy_files:
            ref_policy_file.type_def.extend(policy_file.type_def)
            ref_policy_file.attribute.extend(policy_file.attribute)
            ref_policy_file.contexts.extend(policy_file.contexts)
            ref_policy_file.se_apps.extend(policy_file.se_apps)
            ref_policy_file.rules.extend(policy_file.rules)
            ref_policy_file.macros.extend(policy_file.macros)
            ref_policy_file.macro_calls.extend(policy_file.macro_calls)

        ref_policy_file.rules.extend(
            self.convert_macrocall_to_rule(
                ref_policy_file.macro_calls, ref_policy_file.macros
            )
        )

        return ref_policy_file

    def convert_macrocall_to_rule(self, macro_calls, macros):
        lst_rules = []

        for macro_call in macro_calls:
            # print("macroCall.name: ", macro_call.name)
            for macro in macros:
                # print("macro.name: ", macro.name)
                if macro.name == macro_call.name:
                    rules = macro.rules
                    for rule in rules:
                        """Need to replace $number in source, target or
                        class_type with parameter from macro call with
                         the same number"""
                        for i in range(0, len(macro_call.parameters)):
                            rule.source = rule.source.replace(
                                "$" + str(i + 1), macro_call.parameters[i]
                            )
                            rule.target = rule.target.replace(
                                "$" + str(i + 1), macro_call.parameters[i]
                            )
                            rule.class_type = rule.class_type.replace(
                                "$" + str(i), macro_call.parameters[i]
                            )
                        # print("rule: ", rule)
                        lst_rules.append(rule)

        return lst_rules

    def clear_output(self):
        files = SystemUtility().get_list_of_files(os.getcwd() + "/" + OUT_DIR, "*")
        for file in files:
            if os.path.isfile(file):
                SystemUtility().delete_files(file)
        self.on_analyze_finished(None)
        self.update_analyzer_data_result(None)

    def clear_file_from_analyzer(self, file_path):
        self.analyzer.clear()
        SystemUtility().delete_files(generate_diagram_file_name(file_path))
        SystemUtility().delete_files(generate_puml_file_name(file_path))
        self.on_analyze_finished(None)

    def remove_file(self, file_path):
        SystemUtility().delete_files(
            os.path.splitext(file_path)[0] + DIAGEAM_FILE_EXTENSION
        )
        SystemUtility().delete_files(os.path.splitext(file_path)[0] + ".puml")

    def clear(self):
        self.ref_policy_file = PolicyFile()

    def get_image_path(self, file_path):
        return generate_diagram_file_name(file_path)

    def set_keep_result(self, state):
        self.keep_result = state
        print("self.keep_result:", self.keep_result)

    def set_ui_update_signal(self, update_result):
        self.update_result = update_result

    def set_ui_update_analyzer_data_signal(self, update_result):
        self.update_analyzer_data_result = update_result

    def on_analyze_finished(self, filtered_policy_file):
        self.list_of_diagrams = SystemUtility().get_list_of_files(
            os.getcwd() + "/" + OUT_DIR, "*" + DIAGEAM_FILE_EXTENSION
        )
        self.update_result()

    """This function collects all the information of a filter rule and returns it as a list of string"""

    def get_info_of_item(self, filter_rule):
        if self.ref_policy_file is None:
            return None

        lst_info = []
        filter_result = FilterResult()
        # print("filter_rule: ", filter_rule)
        if filter_rule.filter_type == FilterType.DOMAIN:
            lst_info.extend(
                filter_result.filter_se_app(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_context(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_context(
                    FilterRule(
                        filter_rule.filter_type,
                        filter_rule.keyword + DOMAIN_EXECUTABLE,
                        filter_rule.exact_word,
                    ),
                    self.ref_policy_file,
                )
            )
            return lst_info
        elif filter_rule.filter_type == FilterType.CLASS_TYPE:
            lst_info.extend(
                filter_result.filter_context(filter_rule, self.ref_policy_file)
            )
            lst_info.extend(
                filter_result.filter_se_app(filter_rule, self.ref_policy_file)
            )
            return lst_info
        else:
            return None
