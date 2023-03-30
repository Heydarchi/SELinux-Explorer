import os
import sys
import subprocess

class FileWriter:
    def __init__(self) -> None:
        super().__init__()

    def writeFile(self, filePath, str):
        return open(filePath, "w+").write(str)

    def writeFileAppend(self, filePath, str):
        return open(filePath, "a+").write(str)

    def writeListToFile(self, filePath, listOfStr):
        return open(filePath, "w+").write("\n".join(listOfStr))


if __name__ == "__main__" :
    print(sys.argv)
    fileWriter = FileWriter()
    print( fileWriter.writeFile( sys.argv[1], "Yohoooooooooooo") )
    listOfStr = list()
    listOfStr.append("Haha")
    listOfStr.append("Hehe")
    listOfStr.append("Hoho")
    print( fileWriter.writeListToFile( sys.argv[1]+"_1",listOfStr) )
