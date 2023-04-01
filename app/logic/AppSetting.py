from dataclasses import dataclass, field
from typing import List
from PythonUtilityClasses.SystemUtility import *
from dataclass_wizard import JSONWizard
from PythonUtilityClasses.FileWriter import *

@dataclass
class AppSetting(JSONWizard):
    lastOpenedPath: str = ""
    listOfAddedPaths : List[str] = field(default_factory=list)
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
    def saveListAsJson(fileName, lstOfObjects):
        lstStr = list()
        for item in lstOfObjects:
            lstStr.append(item.to_json())
        FileWriter().writeListToFile("ref/"+fileName+".json", lstStr)

        


if __name__ == "__main__" :
    appSetting = AppSetting()
    appSetting.lastOpenedPath = "123456"
    appSetting.filterClassType = True
    print(appSetting.filterClassType)
    print( appSetting.to_json())

    #appS = AppSetting()
    appS = AppSetting.from_json(appSetting.to_json())
    print(appS.lastOpenedPath)
    print(appS.filterClassType)