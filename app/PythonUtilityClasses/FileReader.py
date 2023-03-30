import os
import sys
import subprocess

class FileReader:
    def __init__(self) -> None:
        super().__init__()

    def readFile(self, filePath):
        return open(filePath).read()

    def readFileLines(self, filePath):
        return open(filePath).readlines()

    def removeComments(self, lines):
        filterdLines = list()
        for line in lines:
            if '#' in line:
                _str = line[0: line.index('#')].strip()
                if len(_str) :
                    filterdLines.append(  _str+ "\n")
            else:
                filterdLines.append(line)
        return filterdLines


if __name__ == "__main__" :
    print(sys.argv)
    fileReader = FileReader()
    print( fileReader.readFile( sys.argv[1]) )
