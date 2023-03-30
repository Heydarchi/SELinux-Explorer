from utility.SystemUtility import *

class FileEnumeration:
    def __init__(self, path) -> None:
        self.path = path
        self.sysUtil = SystemUtility()
        self.listContexts = list()
        self.listTeFiles = list()
        self.enumeratePolicyFiles(self.path)
        

    def enumeratePolicyFiles(self, path):
        self.listContexts = self.sysUtil.getListOfFiles( "./test","*_contexts")
        self.listTeFiles = self.sysUtil.getListOfFiles( "./test","*.te")


if __name__ == "__main__" :
    flEnum = FileEnumeration('.')
    print ('-- List of *_contexts files:')
    print (flEnum.listContexts)
    print ('-- List of *.te files:')
    print (flEnum.listTeFiles)