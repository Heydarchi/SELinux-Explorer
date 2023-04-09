import sys
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import *
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger


class TeAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policy_file = None

    def analyze(self, file_path):
        self.file_path = file_path
        self.policy_file = PolicyFile(file_path, "", FileTypeEnum.TE_FILE)
        file_reader = FR.FileReader()
        temp_lines = file_reader.read_file_lines(file_path)
        last_line = ""
        macro_found = False
        for line in temp_lines:
            line = clean_line(line)
            if line is None:
                continue

            if macro_found:
                if ")" in line:
                    macro_found = False
                    self.process_line(last_line + " " + line)
                else:
                    last_line = last_line + " " + line
            else:
                if "define" in line:
                    macro_found = True
                    last_line = line
                else:
                    self.process_line(line)

        return self.policy_file

    def process_line(self, input_string):
        input_string = clean_line(input_string)
        if input_string is None:
            return
        items = input_string.split()
        # print("items: ", items)
        if len(items) > 0:
            if items[0].strip() == "type":
                type_def = self.extract_definition(input_string)
                if type_def is not None:
                    self.policy_file.type_def.append(type_def)
            elif items[0].strip() == "typeattribute":
                attribute = self.extract_attribite(input_string)
                if attribute is not None:
                    self.policy_file.attribute.append(attribute)
            elif items[0] in ["allow", "neverallow"]:
                self.policy_file.rules.extend(self.extract_rule(input_string))
            elif "define" in input_string:
                macro = self.extract_macro(input_string)
                if macro is not None:
                    self.policy_file.macros.append(macro)
            elif "(" in input_string and ")" in input_string:
                macro_call = self.extract_macro_call(input_string)
                if macro_call is not None:
                    self.policy_file.macro_calls.append(macro_call)
            else:
                MyLogger.log_error(sys, "Unknown line", input_string)

    def extract_definition(self, input_string):
        try:
            types = input_string.replace(
                ";", "").replace(
                "type ", "").strip().split(",")
            type_def = TypeDef()
            type_def.name = types[0].strip()
            type_def.types.extend(types[1:])
            if DOMAIN_EXECUTABLE in type_def.name:
                if not self.merge_exec_domain(type_def):
                    return type_def
            else:
                return type_def

        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
            return None

    def merge_exec_domain(self, type_def_exec):
        try:
            title = type_def_exec.name.replace(DOMAIN_EXECUTABLE, "")
            for type_def in self.policy_file.type_def:
                if type_def.name == title:
                    type_def.types.extend(type_def_exec.types)
                    return True
            return False
        except Exception as err:
            MyLogger.log_error(sys, err, type_def_exec)
            return False

    def extract_attribite(self, input_string):
        try:
            attribute = Attribute()
            types = input_string.replace(";", "").replace(
                "typeattribute ", "").strip().split(" ")
            attribute.name = types[0]
            attribute.types.extend(types[1:])
            return attribute

        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
            return None

    def extract_rule(self, input_string):
        lst_rules = []
        try:
            input_string = input_string.replace(
                ' : ',
                ':').replace(
                ' :',
                ':').replace(
                ': ',
                ':').strip()
            input_string = input_string.replace(
                '{', ' { ').replace('}', ' } ').strip()
            input_string = input_string.replace(
                ': {', ':{ ').replace('} :', '}:').strip()
            input_string = input_string.replace(
                ':  {', ':{ ').replace('}  :', '}:').strip()

            # print("inputString; " + inputString)
            items = input_string.replace(";", "").split()
            for rule_enum in RuleEnum:
                if rule_enum.label == items[0].strip():

                    count_brackets = input_string.count("}")
                    lst_bracket_items = []
                    if count_brackets > 0:
                        offset = 0
                        while '{' in input_string[offset:]:
                            # print (inputString[offset:])
                            start = input_string.find('{', offset)
                            end = input_string.find('}', start)
                            bracket_string = input_string[start + 1: end]
                            input_string = input_string[:start] + \
                                "###" + input_string[end + 1:]
                            lst_bracket_items.append(bracket_string)
                            offset = start

                    items = input_string.replace(
                        ";", "").replace(
                        ": ", ":").strip().split()
                    sources = [items[1]] if "###" not in items[1] else lst_bracket_items.pop(
                        0).strip().split()
                    sec_context = items[2] if "###" not in items[2] else (
                            lst_bracket_items.pop(0) + ":" + items[2].split(":")[1])
                    permissions = [items[3]] if "###" not in items[3] != "###" else lst_bracket_items.pop(
                        0).strip().split()

                    for source in sources:
                        rule = Rule()
                        rule.rule = rule_enum
                        rule.source = source
                        dst_items = sec_context.split(":")
                        targets = dst_items[0].split()
                        for target in targets:
                            rule.target = target
                            rule.class_type = dst_items[1]
                            rule.permissions = permissions
                        lst_rules.append(rule)

                    return

        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
        finally:
            return lst_rules

    def extract_macro(self, input_string):
        try:
            lst_lines = input_string.splitlines()
            macro = PolicyMacro()
            # It's supposed to have define in the first item
            first_line = lst_lines.pop(0).replace("define", "").replace("\'", "")
            first_line = first_line.replace(
                "`",
                "").replace(
                "(",
                "").replace(
                ",",
                "")
            macro.name = first_line.strip()
            for line in lst_lines:
                if ")" in line.strip():
                    break
                macro.rules_string.append(line)
                macro.rules.extend(self.extract_rule(line))
            # print("macro: ", macro)
            return macro
        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
            return None

    def extract_macro_call(self, input_string):
        try:
            # Convert string to PolicyMacroCall
            macro_call = PolicyMacroCall()
            macro_call.name = input_string.split("(")[0].strip()
            macro_call.parameters = input_string.split(
                "(")[1].replace(")", "").strip().split(",")
            return macro_call
        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
            return None


if __name__ == "__main__":
    print(sys.argv)
    te_analyzer = TeAnalyzer()
    print(te_analyzer.analyze(sys.argv[1]))
