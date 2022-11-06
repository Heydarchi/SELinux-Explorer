import os
import sys
import subprocess

class SystemUtility:
    def __init__(self) -> None:
        super().__init__()


    def getListOfFiles(self, path, pattern):
        result = subprocess.Popen(['find',  path , '-name',pattern ], stdout=subprocess.PIPE).communicate()[0]
        result = str(result, encoding='utf-8').split('\n')
        result = [item for item in result if item]
        return result


if __name__ == "__main__" :
    sysUtil = SystemUtility()
    print (sysUtil.getListOfFiles( "./test","*_contexts"))
    print (sysUtil.getListOfFiles( "./test","*.te"))