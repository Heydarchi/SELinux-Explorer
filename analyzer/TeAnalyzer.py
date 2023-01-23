import sys
from pathlib import Path

import re
from AbstractAnalyzer import * 
from PolicyEntities import *
from PythonUtilityClasses import FileReader as FR
class TeAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        pass

    def analyze(self, filePath):
        fileReader = FR.FileReader()
        tempContent= fileReader.readFile(filePath)
        
    def extractRule(self, inputString):
        pass

if __name__ == "__main__" :
    print(sys.argv)
    policyEntities = PolicyEntities()
    policyEntities.analyze(sys.argv[1])

