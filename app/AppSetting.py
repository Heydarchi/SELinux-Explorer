from dataclasses import field
from typing import List
from PythonUtilityClasses.SystemUtility import *
from dataclass_wizard import JSONWizard
from PythonUtilityClasses.FileWriter import *

ICON_PATH = "./ui/icons/"
APP_VERSION = "0.2.11-beta"
APP_NAME = "SELinux Explorer"
APP_AUTHOR = "Mohammad Hossein Heydarchi"
AUTHOR_EMAIL = "m.h.heydarchi@gmail.com"
APP_COPYRIGHT = "2023"
APP_LICENSE = "MIT"
APP_WEBSITE = "https://github.com/Heydarchi/SELinux-Explorer"
APP_ICON_PATH = ""
OUT_DIR = "out/"


@dataclass
class AppSetting(JSONWizard):
    last_opened_path: str = ""
    list_of_added_paths: List[str] = field(default_factory=list)
    keep_the_result: bool = False
    selected_filter_type: bool = False
    filter_domain: bool = False
    filter_filename: bool = False
    filter_permission: bool = False


class SettingClass:
    def __init__(self) -> None:
        self.ref_dir = "ref"
        self.out_dir = "out"
        self.init_dirs()

    def init_dirs(self):
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        if not os.path.exists(self.ref_dir):
            os.makedirs(self.ref_dir)

    @staticmethod
    def save_list_as_json(file_name, lst_of_objects):
        lst_str = []
        for item in lst_of_objects:
            lst_str.append(item.to_json())
        FileWriter.write_list_to_file("ref/" + file_name + ".json", lst_str)


if __name__ == "__main__":
    app_setting = AppSetting()
    app_setting.last_opened_path = "123456"
    app_setting.filter_class_type = True
    print(app_setting.filter_class_type)
    print(app_setting.to_json())

    # appS = AppSetting()
    appS = AppSetting.from_json(app_setting.to_json())
    print(appS.last_opened_path)
    print(appS.filterClassType)
