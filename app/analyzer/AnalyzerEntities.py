from dataclasses import dataclass, field
from enum import Enum
from typing import List
from PythonUtilityClasses.SystemUtility import *


@dataclass
class AnalyzerInfo:
    sourceFile: FileInfo = FileInfo()
    pumlFile: FileInfo = FileInfo()
    pngFile: FileInfo = FileInfo()
