from dataclasses import dataclass, field
import dataclasses
from enum import Enum
from typing import List
from PythonUtilityClasses.SystemUtility import *
import json
from dataclass_wizard import JSONWizard


@dataclass
class AppSetting(JSONWizard):
    lastOpenedPath: str = ""
    listOfAddedPaths : List[str] = field(default_factory=list)
    keepTheResult: bool = False
    filterClassType: bool = False
    filterDomain: bool = False
    filterFilename: bool = False
    filterPermission: bool = False


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