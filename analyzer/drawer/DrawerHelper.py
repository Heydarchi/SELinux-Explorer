import os, sys
from enum import Enum


def generatePumlFileName(fileName):
    return fileName.replace("/","-")+"_relation.puml"

def generatePngFileName(fileName):
    return fileName.replace("/","-")+"_relation.png"

def generatePng( filepath):
    os.system("java -jar plantuml/plantuml.jar " + filepath)


class DrawingPosition(Enum):
    RIGHT = "tight"
    LEFT = "left"
    TOP = "top"
    BOTTOM = "bottom"

class DrawingStyle(Enum):
    NOTE = "note"
    DOMAIN = "package"

class DrawingTool:
    @staticmethod
    def defineNoteStyle():
        lstNote = list()
        lstNote.append("skinparam " + DrawingStyle.NOTE.value +  " {")
        lstNote.append("borderColor black")
        lstNote.append("backgroundColor #FFD28A")
        lstNote.append("}")
        lstNote.append("")
        return lstNote
    
    @staticmethod
    def defineDomainStyle():
        lstDomain = list()
        lstDomain.append("skinparam " + DrawingStyle.DOMAIN.value +  " {")
        lstDomain.append("borderColor black")
        lstDomain.append("backgroundColor #A5FFD6")
        lstDomain.append("}")
        lstDomain.append("")
        return lstDomain
    
        
    @staticmethod
    def generateNote(title, position: DrawingPosition, items, firstLine = ""):
        lstNote = list()
        lstNote.append(DrawingStyle.NOTE.value + " " + position.value +  " of " + title)
        lstNote.append("<b>" + firstLine + "</b>")
        for item in items:
            lstNote.append("  - " + item)
        lstNote.append("end " + DrawingStyle.NOTE.value)
        lstNote.append("")
        return lstNote
    
    @staticmethod
    def generateDomain(title, description = None):
        lstDomain = list()
        lstDomain.append(DrawingStyle.DOMAIN.value + " \"*" +  title + "*\" {")
        lstDomain.append("[" +  title + "]" )
        lstDomain.append("}")
        lstDomain.append("")
        return lstDomain    
    
    @staticmethod
    def generateOtherLabel(title, description = ""):
        lstDomain = list()
        lstDomain.append(DrawingStyle.DOMAIN.value + " \"" +  description + "\" #FFA07A{")
        lstDomain.append("[" +  title + "]" )
        lstDomain.append("}")
        lstDomain.append("")
        return lstDomain        

if __name__ == "__main__" :
        print(DrawingStyle.NOTE)
        print(DrawingStyle.NOTE.value)
