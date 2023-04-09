import sys
from analyzer.AnalyzerUtility import *
from analyzer.AbstractAnalyzer import *
from model.PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
from MyLogger import MyLogger


class SeAppAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.policy_file = None

    def analyze(self, filePath):
        self.policy_file = PolicyFile(
            filePath, "", FileTypeEnum.SEAPP_CONTEXTS)
        file_reader = FR.FileReader()
        temp_lines = file_reader.read_file_lines(filePath)
        for line in temp_lines:
            self.process_line(line)

        # print(self.policy_file)
        return self.policy_file

    def process_line(self, input_string):
        input_string = clean_line(input_string)
        if input_string is None:
            return
        self.extract_definition(input_string)

    def extract_definition(self, input_string):
        try:
            se_app = SeAppContext()
            if "neverallow" in input_string:
                se_app.never_allow = True
                input_string = input_string.replace("neverallow", "").strip()

            items = input_string.strip().split(" ")
            for item in items:
                split = item.split("=")
                # Input selectors
                if "user" in split[0]:
                    se_app.user = split[1]
                elif "is_priv_app" in split[0]:
                    se_app.is_priv_app = split[1]
                elif "is_system_server" in split[0]:
                    se_app.is_system_serverer = split[1]
                elif "is_ephemeral_app" in split[0]:
                    se_app.is_ephemeral_app = split[1]
                elif "name" in split[0]:
                    se_app.name = split[1]
                elif "min_target_sdk_version" in split[0]:
                    se_app.min_target_sdk_version = split[1]
                elif "from_run_as" in split[0]:
                    se_app.from_run_as = split[1]
                elif "seinfo" in split[0]:
                    se_app.seinfo = split[1]
                # Outputs
                elif "domain" in split[0]:
                    se_app.domain = split[1]
                elif "type" in split[0]:
                    se_app.type = split[1]
                elif "level_from" in split[0]:
                    se_app.level_from = split[1]
                elif "level" in split[0]:
                    se_app.level = split[1]

            self.policy_file.se_apps.append(se_app)

        except Exception as err:
            MyLogger.log_error(sys, err, input_string)


if __name__ == "__main__":
    print(sys.argv)
    seAppAnalyzer = SeAppAnalyzer()
    seAppAnalyzer.analyze(sys.argv[1])
