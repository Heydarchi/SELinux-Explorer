import os
import sys
import subprocess

class FileReader:
    def __init__(self) -> None:
        super().__init__()

    def readFile(self, filePath):
        return open(filePath, 'r').readlines()

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
    fileReader = FileReader()
    lines = fileReader.readFile( "../test/file_to_filter.txt")
    print (*lines)
    print("")
    print (*fileReader.removeComments(lines))