from dataclasses import dataclass, field
from typing import List
from PythonUtilityClasses.SystemUtility import *
from dataclass_wizard import JSONWizard
from PythonUtilityClasses.FileWriter import *

ICON_PATH = './ui/icons/'
APP_VERSION = '0.2.2-beta'
APP_NAME = 'SELinux Explorer'
APP_AUTHOR = 'Mohammad Hossein Heydarchi'
AUTHOR_EMAIL = 'm.h.heydarchi@gmail.com'
APP_COPYRIGHT = '2023'
APP_LICENSE = 'MIT'
APP_WEBSITE = 'https://github.com/Heydarchi/SELinux-Explorer'
APP_ICON_PATH = ''
OUT_DIR = 'out/'


@dataclass
class AppSetting(JSONWizard):
    lastOpenedPath: str = ""
    listOfAddedPaths: List[str] = field(default_factory=list)
    keepTheResult: bool = False
    selectedFilterType: bool = False
    filterDomain: bool = False
    filterFilename: bool = False
    filterPermission: bool = False


class SettingClass:
    def __init__(self) -> None:
        self.refDir = "ref"
        self.outDir = "out"
        self.initDirs()

    def initDirs(self):
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

        if not os.path.exists(self.refDir):
            os.makedirs(self.refDir)

    @staticmethod
    def saveListAsJson(file_name, lst_of_objects):
        lst_str = list()
        for item in lst_of_objects:
            lst_str.append(item.to_json())
        FileWriter.writeListToFile("ref/" + file_name + ".json", lst_str)


if __name__ == "__main__":
    appSetting = AppSetting()
    appSetting.lastOpenedPath = "123456"
    appSetting.filterClassType = True
    print(appSetting.filterClassType)
    print(appSetting.to_json())

    # appS = AppSetting()
    appS = AppSetting.from_json(appSetting.to_json())
    print(appS.lastOpenedPath)
    print(appS.filterClassType)
