import sys, os
import argparse
from FileAnalyzer import *

class SeExplorer():
    def __init__(self) -> None:
        pass

    def initHelp(self):
        parser = argparse.ArgumentParser(description = "SELinuxExplorer helps to reveal the permission graphically.")
        parser.add_argument("path", help="Path of the Folder/File to analyze. ")
        parser.add_argument("--disable-drawing", help="Won't create any drawing(.png) file", action="store_true")
        #parser.add_argument("--draw-existing", help="Convert .puml analyzed files to drawing(.pmg)", action="store_true")

        args = parser.parse_args()
        return args

    def analyze(self):
        args = self.initHelp()
        print (args)
        if args.path == None or args.path == "" :
            print("run the command below to see the options:")
            print(">python SeExplorer.py -h")
            print("Example :")
            print(">python SeExplorer.py ../samples")
            return
        else:
            fileAnalyzer = FileAnalyzer()
            fileAnalyzer.analyze([args.path], None, args.disable_drawing)
        

if __name__ == "__main__" :
    seExplorer = SeExplorer()
    seExplorer.analyze()