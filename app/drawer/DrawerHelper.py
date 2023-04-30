import os
from enum import Enum
from dataclasses import dataclass, field
from typing import List

DIAGRAM_FILE_EXTENSION = ".png"


def generate_puml_file_name(file_name):
    return file_name.replace("/", "-") + ".puml"


def generate_diagram_file_name(file_name):
    return file_name.replace("/", "-") + "" + DIAGRAM_FILE_EXTENSION


def generate_png(filepath):
    os.system("java -jar plantuml/plantuml.jar " + filepath)


def generate_svg(filepath):
    os.system("java -jar plantuml/plantuml.jar -tsvg " + filepath)


@dataclass
class DrawingPackage:
    domain: str = ""
    names: List[str] = field(default_factory=list)
    type_defs: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    users: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)


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
    default_height = 1500
    default_width = 2500

    @staticmethod
    def generate_start_of_puml(height=default_height, width=default_width):
        lst_output = []
        lst_output.append("@startuml")
        lst_output.append("scale max %s height" % height)
        lst_output.append("scale max %s width" % width)
        lst_output.append("")
        return lst_output

    @staticmethod
    def generate_end_of_puml():
        lst_output = []
        lst_output.append("@enduml")
        return lst_output

    @staticmethod
    def define_note_style():
        lst_note = []
        lst_note.append("skinparam " + DrawingStyle.NOTE.value + " {")
        lst_note.append("borderColor black")
        lst_note.append("backgroundColor #FFD28A")
        lst_note.append("}")
        lst_note.append("")
        return lst_note

    @staticmethod
    def define_domain_style():
        lst_domain = []
        lst_domain.append("skinparam " + DrawingStyle.DOMAIN.value + " {")
        lst_domain.append("borderColor black")
        lst_domain.append("backgroundColor #A5FFD6")
        lst_domain.append("}")
        lst_domain.append("")
        return lst_domain

    @staticmethod
    def generate_note(title, position: DrawingPosition, items, first_line=""):
        items = list(dict.fromkeys(items))
        lst_note = []
        if title.strip() != "" and len(items) >= 1:
            lst_note.append(
                DrawingStyle.NOTE.value + " " + position.value + " of [" + title + "]"
            )
            lst_note.append("<b>" + first_line + "</b>")
            for item in items:
                lst_note.append("  - " + item)
            lst_note.append("end " + DrawingStyle.NOTE.value)
            lst_note.append("")
        return lst_note

    @staticmethod
    def generate_legend(
        title,
        position_vertical: DrawingPosition,
        position_horizontal: DrawingPosition,
        items,
        back_color: DrawingColor,
    ):
        items = list(dict.fromkeys(items))
        lst_note = []
        if title.strip() != "" and len(items) >= 1:
            lst_note.append(
                DrawingStyle.LEGEND.value
                + " "
                + position_vertical.value
                + "   "
                + position_horizontal.value
            )
            lst_note.append("<b>" + title + "</b>")
            for item in items:
                lst_note.append("  - " + item)
            lst_note.append("end" + DrawingStyle.LEGEND.value)
            lst_note.append("")
        return lst_note

    @staticmethod
    def generate_domain(title, description=None):
        lst_domain = []
        if title.strip() != "":
            lst_domain.append(DrawingStyle.DOMAIN.value + ' "*' + title + '*" {')
            lst_domain.append("[" + title + "]")
            lst_domain.append("}")
            lst_domain.append("")
        return lst_domain

    @staticmethod
    def generate_other_label(title, description=""):
        lst_domain = []
        if title.strip() != "":
            lst_domain.append(
                DrawingStyle.DOMAIN.value + ' "' + description + '" #FFA07A{'
            )
            lst_domain.append("[" + title + "]")
            lst_domain.append("}")
            lst_domain.append("")
        return lst_domain


if __name__ == "__main__":
    print(DrawingStyle.NOTE)
    print(DrawingStyle.NOTE.value)
