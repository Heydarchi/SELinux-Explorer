import os
import sys
import subprocess
from dataclasses import dataclass, field


@dataclass
class FileInfo:
    name: str = ""
    size: int = 0
    lastModifies: str = ""
    created: str = ""
    md5: str = ""


class SystemUtility:
    def __init__(self) -> None:
        super().__init__()


    def getListOfFiles(self, path, pattern):
        result = subprocess.Popen(['find',  path , '-name',pattern ], stdout=subprocess.PIPE).communicate()[0]
        result = str(result, encoding='utf-8').split('\n')
        result = [item for item in result if item]
        return result


    def getFileInfo(self, path):
        fileInfo = FileInfo()
        fileInfo.name = path
        fileInfo.size = os.path.getsize(path)
        fileInfo.lastModifies = os.path.getmtime(path)
        fileInfo.created = os.path.getctime(path)
        return fileInfo
    
    def deleteFiles(self, path):
        os.remove(path)

if __name__ == "__main__" :
    sysUtil = SystemUtility()
    print (sysUtil.getListOfFiles( "./test","*_contexts"))
    print (sysUtil.getListOfFiles( "./test","*.te"))
