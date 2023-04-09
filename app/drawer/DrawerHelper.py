import os
from enum import Enum

DIAGEAM_FILE_EXTENSION = ".png"


def generate_puml_file_name(fileName):
    return fileName.replace("/", "-") + ".puml"


def generate_diagram_file_name(fileName):
    return fileName.replace("/", "-") + "" + DIAGEAM_FILE_EXTENSION


def generate_png(filepath):
    os.system("java -jar plantuml/plantuml.jar " + filepath)


def generate_svg(filepath):
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
    def generate_start_of_puml():
        lst_output = list()
        lst_output.append("@startuml")
        lst_output.append("scale max 2560 height")
        lst_output.append("scale max 2048 width")
        lst_output.append("")
        return lst_output

    @staticmethod
    def generate_end_of_puml():
        lst_output = list()
        lst_output.append("@enduml")
        return lst_output

    @staticmethod
    def define_note_style():
        lst_note = list()
        lst_note.append("skinparam " + DrawingStyle.NOTE.value + " {")
        lst_note.append("borderColor black")
        lst_note.append("backgroundColor #FFD28A")
        lst_note.append("}")
        lst_note.append("")
        return lst_note

    @staticmethod
    def defineDomainStyle():
        lst_domain = list()
        lst_domain.append("skinparam " + DrawingStyle.DOMAIN.value + " {")
        lst_domain.append("borderColor black")
        lst_domain.append("backgroundColor #A5FFD6")
        lst_domain.append("}")
        lst_domain.append("")
        return lst_domain

    @staticmethod
    def generate_note(title, position: DrawingPosition, items, firstLine=""):
        items = list(dict.fromkeys(items))
        lst_note = list()
        if title.strip() != "" and len(items) >= 1:
            lst_note.append(DrawingStyle.NOTE.value + " " +
                           position.value + " of [" + title + "]")
            lst_note.append("<b>" + firstLine + "</b>")
            for item in items:
                lst_note.append("  - " + item)
            lst_note.append("end " + DrawingStyle.NOTE.value)
            lst_note.append("")
        return lst_note

    @staticmethod
    def generate_legend(
            title,
            positionVertical: DrawingPosition,
            positionHorizontal: DrawingPosition,
            items,
            back_color: DrawingColor):
        items = list(dict.fromkeys(items))
        lst_note = list()
        if title.strip() != "" and len(items) >= 1:
            lst_note.append(
                DrawingStyle.LEGEND.value +
                " " +
                positionVertical.value +
                "   " +
                positionHorizontal.value)
            lst_note.append("<b>" + title + "</b>")
            for item in items:
                lst_note.append("  - " + item)
            lst_note.append("end" + DrawingStyle.LEGEND.value)
            lst_note.append("")
        return lst_note

    @staticmethod
    def generate_domain(title, description=None):
        lst_domain = list()
        if title.strip() != "":
            lst_domain.append(
                DrawingStyle.DOMAIN.value +
                " \"*" +
                title +
                "*\" {")
            lst_domain.append("[" + title + "]")
            lst_domain.append("}")
            lst_domain.append("")
        return lst_domain

    @staticmethod
    def generate_other_label(title, description=""):
        lst_domain = list()
        if title.strip() != "":
            lst_domain.append(
                DrawingStyle.DOMAIN.value +
                " \"" +
                description +
                "\" #FFA07A{")
            lst_domain.append("[" + title + "]")
            lst_domain.append("}")
            lst_domain.append("")
        return lst_domain


if __name__ == "__main__":
    print(DrawingStyle.NOTE)
    print(DrawingStyle.NOTE.value)
