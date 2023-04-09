from dataclasses import dataclass, field
from PythonUtilityClasses.SystemUtility import *


@dataclass
class AnalyzerInfo:
    source_file: FileInfo = FileInfo()
    puml_file: FileInfo = FileInfo()
    png_file: FileInfo = FileInfo()
