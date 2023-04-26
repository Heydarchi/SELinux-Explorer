import sys
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import *
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger


class ContextsAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policy_file = None

    def analyze(self, file_path):
        try:
            if "file_contexts" in file_path:
                self.policy_file = PolicyFile(file_path, "", FileTypeEnum.FILE_CONTEXTS)
            elif "vndservice_contexts" in file_path:
                self.policy_file = PolicyFile(
                    file_path, "", FileTypeEnum.VNDSERVICE_CONTEXTS
                )
            elif "hwservice_contexts" in file_path:
                self.policy_file = PolicyFile(
                    file_path, "", FileTypeEnum.HWSERVICE_CONTEXTS
                )
            elif "service_contexts" in file_path:
                self.policy_file = PolicyFile(file_path, "", FileTypeEnum.SERVICE_CONTEXTS)
            elif "property_contexts" in file_path:
                self.policy_file = PolicyFile(file_path, "", FileTypeEnum.PROPERTY_CONTEXTS)
            else:
                return

            file_reader = FR.FileReader()
            temp_lines = file_reader.read_file_lines(file_path)
            for line in temp_lines:
                context = self.extract_definition(line)
                if context is not None:
                    self.policy_file.contexts.append(context)

            # print(self.policy_file)
            return self.policy_file
        except Exception as err:
            MyLogger.log_error(sys, err, file_path)
            return None

    def extract_definition(self, input_string):
        try:
            # print (input_string)
            input_string = clean_line(input_string)
            if input_string is None:
                return
            # print ("Cleaned: ",input_string)
            context = Context()
            items = input_string.replace(";", "").strip().split()
            context.path_name = items[0]
            if len(items) > 1:
                context.type_def = TypeDef()
                security_items = items[1].split(":")
                context.security_context = SecurityContext()
                # print(security_items)
                context.security_context.user = security_items[0]
                context.security_context.role = security_items[1]
                context.security_context.type = security_items[2]
                context.security_context.level = security_items[3]

                context.domain_name = context.security_context.type
                if len(security_items) > 4:
                    context.security_context.categories = security_items[4]
            # print(context)
            return context
        except Exception as err:
            MyLogger.log_error(sys, err, input_string)
            return None

    def analyze_port_contexts(self):
        pass

    def analyze_genfs_contexts(self):
        pass

    def analyze_keys_conf(self):
        pass


if __name__ == "__main__":
    print(sys.argv)
    analyzer = ContextsAnalyzer()
    analyzer.analyze(sys.argv[1])
