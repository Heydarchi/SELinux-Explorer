import os
from enum import Enum

DIAGEAM_FILE_EXTENSION = ".png"

def generatePumlFileName(fileName):
    return fileName.replace("/","-")+"_relation.puml"

def generateDiagramFileName(fileName):
    return fileName.replace("/","-")+"_relation" + DIAGEAM_FILE_EXTENSION

def generatePng( filepath):
    os.system("java -jar plantuml/plantuml.jar " + filepath)

def generateSvg( filepath):
    os.system("java -jar plantuml/plantuml.jar -tsvg " + filepath)

class DrawingPosition(Enum):
    RIGHT = "tight"
    LEFT = "left"
    TOP = "top"
    BOTTOM = "bottom"

class DrawingStyle(Enum):
    NOTE = "note"
    DOMAIN = "package"
    LEGEND = "legend"

class DrawingColor(Enum):
    BLUE = "#blue"
    BLUE_LIGHT = "#lightblue"
    GREEN = "#green"
    GREEN_LIGHT = "#lightgreen"
    RED = "#red"
    RED_LIGHT = "#lightred"
    YELLOW = "#yellow"
    ORANGE = "#orange"

class DrawingTool:

    @staticmethod
    def generateStartOfPuml():
        lstOutput = list()
        lstOutput.append("@startuml")
        lstOutput.append("scale max 2560 height")
        lstOutput.append("scale max 2048 width")
        lstOutput.append("")
        return lstOutput

    @staticmethod
    def generateEndOfPuml():
        lstOutput = list()
        lstOutput.append("@enduml")
        return lstOutput
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
        items = list(dict.fromkeys(items))
        lstNote = list()
        if title.strip() != "" and len(items) >= 1 :
            lstNote.append(DrawingStyle.NOTE.value + " " + position.value +  " of " + title)
            lstNote.append("<b>" + firstLine + "</b>")
            for item in items:
                lstNote.append("  - " + item)
            lstNote.append("end " + DrawingStyle.NOTE.value)
            lstNote.append("")
        return lstNote

    @staticmethod
    def generateLegend(title, positionVertical: DrawingPosition, positionHorizontal: DrawingPosition, items, back_color: DrawingColor):
        items = list(dict.fromkeys(items))
        lstNote = list()
        if title.strip() != "" and len(items) >= 1 :
            lstNote.append(DrawingStyle.LEGEND.value + " " + positionVertical.value +  "   " + positionHorizontal.value )
            lstNote.append("<b>" + title + "</b>")
            for item in items:
                lstNote.append("  - " + item)
            lstNote.append("end" + DrawingStyle.LEGEND.value)
            lstNote.append("")
        return lstNote
    
    @staticmethod
    def generateDomain(title, description = None):
        lstDomain = list()
        if title.strip() != "" :
            lstDomain.append(DrawingStyle.DOMAIN.value + " \"*" +  title + "*\" {")
            lstDomain.append("[" +  title + "]" )
            lstDomain.append("}")
            lstDomain.append("")
        return lstDomain    
    
    @staticmethod
    def generateOtherLabel(title, description = ""):       
        lstDomain = list()
        if title.strip() != "" :
            lstDomain.append(DrawingStyle.DOMAIN.value + " \"" +  description + "\" #FFA07A{")
            lstDomain.append("[" +  title + "]" )
            lstDomain.append("}")
            lstDomain.append("")
        return lstDomain        

if __name__ == "__main__" :
        print(DrawingStyle.NOTE)
        print(DrawingStyle.NOTE.value)
