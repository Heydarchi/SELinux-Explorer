from model.PolicyEntities import PolicyFile, TypeDef, Rule, RuleEnum
from model.PolicyEntities import SeAppContext, Context, DOMAIN_EXECUTABLE
from model.PolicyEntities import Attribute
from PythonUtilityClasses import FileWriter as FW
from drawer.DrawerHelper import generate_png, generate_puml_file_name
from drawer.DrawerHelper import (
    DrawingTool,
    DrawingPosition,
    DrawingColor,
    DrawingPackage,
)
from AppSetting import OUT_DIR
from typing import List
from drawer.AbstractDrawer import *


class AdvancedDrawer(AbstractDrawer):
    def draw_uml(self, policy_file):
        self.dict_of_participant = {}
        self.drawer_class = DrawerClass()

        height = DrawingTool.default_height
        width = DrawingTool.default_width
        if (
            len(policy_file.se_apps)
            + len(policy_file.contexts)
            + len(policy_file.rules)
            > 20
        ):
            height = DrawingTool.default_height * 2
            width = DrawingTool.default_width * 2

        plant_uml_list = []
        plant_uml_list.extend(DrawingTool.generate_start_of_puml(height, width))
        plant_uml_list.extend(self.generate_reference())

        lst_packe_infos = self.dump_policy_file(policy_file)
        plant_uml_list.extend(lst_packe_infos)

        plant_uml_list.extend(DrawingTool.define_domain_style())
        plant_uml_list.extend(DrawingTool.define_note_style())
        plant_uml_list.extend(self.drawer_class.participants)

        self.drawer_class.rules.extend(self.draw_rule(policy_file.rules))
        plant_uml_list.extend(self.drawer_class.rules)

        plant_uml_list.extend(DrawingTool.generate_end_of_puml())

        # Remove redundant items
        # Temporary disabled  : plant_uml_list =
        # list(dict.fromkeys(plant_uml_list))

        # print(plant_uml_list)
        file_path = OUT_DIR + generate_puml_file_name(policy_file.file_name)
        self.write_to_file(file_path, plant_uml_list)
        print("drawing: ", file_path)

        generate_png(file_path)
        # print(policy_file)

    def dump_policy_file(self, policy_file: PolicyFile):
        policy_file = self.correlate_data(policy_file)

        lst_drawing_package = []
        lst_drawing_package = self.convert_seapps_to_drawingpackage(
            policy_file.se_apps, lst_drawing_package
        )
        lst_drawing_package = self.convert_contexts_to_drawingpackage(
            policy_file.contexts, lst_drawing_package
        )
        lst_drawing_package = self.convert_types_to_drawingpackage(
            policy_file.type_def, lst_drawing_package
        )
        lst_drawing_package = self.convert_attributes_to_drawingpackage(
            policy_file.attribute, lst_drawing_package
        )

        return self.draw_drawingpackages(lst_drawing_package)

    def correlate_data(self, policy_file: PolicyFile):
        for se_app in policy_file.se_apps:
            for i in reversed(range(len(policy_file.type_def))):
                if se_app.domain == policy_file.type_def[i].name:
                    se_app.type_def.types.extend(policy_file.type_def[i].types)
                    del policy_file.type_def[i]
                    break

        for se_app in policy_file.se_apps:
            for i in reversed(range(len(policy_file.attribute))):
                if se_app.domain == policy_file.attribute[i].name:
                    se_app.attribute = policy_file.attribute[i]
                    del policy_file.attribute[i]
                    break

        for j in range(len(policy_file.contexts)):
            for i in reversed(range(len(policy_file.type_def))):
                if (
                    policy_file.contexts[j].security_context.type.replace(
                        DOMAIN_EXECUTABLE, ""
                    )
                    == policy_file.type_def[i].name
                ):
                    policy_file.contexts[j].domain_name = policy_file.type_def[i].name
                    policy_file.contexts[j].type_def.types.extend(
                        policy_file.type_def[i].types
                    )
                    del policy_file.type_def[i]
                    break
        return policy_file

    def draw_type_def(self, type_defs: List[TypeDef]):
        type_def_list = []
        for type_def in type_defs:
            type_def_list.extend(DrawingTool.generate_domain(type_def.name))

            lst_note = []
            lst_note.extend(type_def.types)
            type_def_list.extend(
                DrawingTool.generate_note(
                    type_def.name, DrawingPosition.TOP, lst_note, "Types"
                )
            )
        return type_def_list

    def draw_context(self, contexts: List[Context]):
        context_list = []
        for context in contexts:
            context_list.extend(
                DrawingTool.generate_other_label(context.domain_name, context.path_name)
            )

            lst_note = []
            # lst_note.append("Path: " + context.path_name)
            lst_note.extend(context.type_def.types)
            context_list.extend(
                DrawingTool.generate_note(
                    context.domain_name, DrawingPosition.TOP, lst_note, "Types"
                )
            )
        return context_list

    def draw_se_app(self, se_apps: List[SeAppContext]):
        se_app_list = []
        for se_app_context in se_apps:
            se_app_list.extend(DrawingTool.generate_domain(se_app_context.domain))

            lst_note = []
            lst_note.append(se_app_context.user)
            lst_note.extend(se_app_context.type_def.types)
            lst_note.extend(se_app_context.attribute.attributes)
            se_app_list.extend(
                DrawingTool.generate_note(
                    se_app_context.domain, DrawingPosition.TOP, lst_note, "Types"
                )
            )
        return se_app_list

    def draw_rule(self, rules: List[Rule]):
        rule_list = []
        for rule in rules:
            for permission in rule.permissions:
                if rule.rule == RuleEnum.NEVER_ALLOW:
                    rule_list.append(
                        ""
                        + self.correct_name(rule.source)
                        + ' .....[#red]> "'
                        + rule.target
                        + '" : '
                        + "!! "
                        + permission
                        + " !!"
                    )
                else:
                    rule_list.append(
                        ""
                        + self.correct_name(rule.source)
                        + ' -----[#green]> "'
                        + rule.target
                        + '" : '
                        + permission
                    )

        return rule_list

    def generate_reference(self):
        lst_note = []
        lst_note.append("Symbols")
        lst_note.append("Green Line: Allow")
        lst_note.append("Red Line: Never Allow")
        return DrawingTool.generate_legend(
            "Reference",
            DrawingPosition.TOP,
            DrawingPosition.LEFT,
            lst_note,
            DrawingColor.BLUE_LIGHT,
        )

    def convert_seapps_to_drawingpackage(
        self, se_apps: List[SeAppContext], lst_drawing_package
    ):
        for se_app_context in se_apps:
            if se_app_context is None:
                continue
            found = False
            if len(lst_drawing_package) > 0:
                for drawing_package in lst_drawing_package:
                    if drawing_package is None:
                        continue
                    if drawing_package.domain == se_app_context.domain:
                        drawing_package = self.add_seapp_info_to_drawingpackage(
                            se_app_context, drawing_package
                        )
                        found = True
                        break
            if not found:
                drawing_package = DrawingPackage()
                drawing_package.domain = se_app_context.domain
                drawing_package = self.add_seapp_info_to_drawingpackage(
                    se_app_context, drawing_package
                )
                lst_drawing_package.append(drawing_package)

        return lst_drawing_package

    def add_seapp_info_to_drawingpackage(self, se_apps, drawing_package):
        drawing_package.users.append(se_apps.user)
        drawing_package.names.append(se_apps.name)
        drawing_package.type_defs.extend(se_apps.type_def.types)
        drawing_package.attributes.extend(se_apps.attribute.attributes)

    def convert_contexts_to_drawingpackage(
        self, contexts: List[Context], lst_drawing_package
    ):
        for context in contexts:
            if context is None:
                continue
            found = False
            for drawing_package in lst_drawing_package:
                if drawing_package is None:
                    continue
                if drawing_package.domain == context.domain_name:
                    drawing_package = self.add_context_info_to_drawingpackage(
                        context, drawing_package
                    )
                    found = True
                    break
            if not found:
                drawing_package = DrawingPackage()
                drawing_package.domain = context.domain_name
                drawing_package = self.add_context_info_to_drawingpackage(
                    context, drawing_package
                )
                lst_drawing_package.append(drawing_package)

        return lst_drawing_package

    def add_context_info_to_drawingpackage(self, context, drawing_package):
        drawing_package.names.append(context.path_name)
        drawing_package.type_defs.extend(context.type_def.types)
        return drawing_package

    def convert_types_to_drawingpackage(
        self, type_defs: List[TypeDef], lst_drawing_package
    ):
        for type_def in type_defs:
            if type_def is None:
                continue
            found = False
            for drawing_package in lst_drawing_package:
                if drawing_package is None:
                    continue
                if type_def is not None and drawing_package.domain == type_def.name:
                    drawing_package = self.add_type_info_to_drawingpackage(
                        type_def, drawing_package
                    )
                    found = True
                    break
            if not found:
                drawing_package = DrawingPackage()
                drawing_package.domain = type_def.name
                drawing_package = self.add_type_info_to_drawingpackage(
                    type_def, drawing_package
                )
                lst_drawing_package.append(drawing_package)

        return lst_drawing_package

    def add_type_info_to_drawingpackage(self, type_def, drawing_package):
        drawing_package.type_defs.extend(type_def.types)
        drawing_package.aliases.extend(type_def.alises)
        return drawing_package

    def convert_attributes_to_drawingpackage(
        self, attributes: List[Attribute], lst_drawing_package
    ):
        for attribute in attributes:
            if attribute is None:
                continue
            found = False
            for drawing_package in lst_drawing_package:
                if drawing_package is None:
                    continue
                if attribute is not None and drawing_package.domain == attribute.name:
                    drawing_package = self.add_attribute_info_to_drawingpackage(
                        attribute, drawing_package
                    )
                    found = True
                    break
            if not found:
                drawing_package = DrawingPackage()
                drawing_package.domain = attribute.name
                drawing_package = self.add_attribute_info_to_drawingpackage(
                    attribute, drawing_package
                )
                lst_drawing_package.append(drawing_package)

        return lst_drawing_package

    def add_attribute_info_to_drawingpackage(self, attribute, drawing_package):
        drawing_package.attributes.extend(attribute.attributes)
        return drawing_package

    def draw_drawingpackages(self, lst_drawing_package):
        drawing_package_list = []
        for drawing_package in lst_drawing_package:
            if drawing_package is None:
                continue
            drawing_package_list.extend(
                DrawingTool.generate_domain(drawing_package.domain)
            )

            lst_process = []
            lst_process.extend(drawing_package.names)
            drawing_package_list.extend(
                DrawingTool.generate_note(
                    drawing_package.domain,
                    DrawingPosition.TOP,
                    lst_process,
                    "Processes",
                )
            )

            lst_type = []
            lst_type.extend(drawing_package.type_defs)
            drawing_package_list.extend(
                DrawingTool.generate_note(
                    drawing_package.domain, DrawingPosition.TOP, lst_type, "Types"
                )
            )

            lst_attribute = []
            lst_attribute.extend(drawing_package.attributes)
            drawing_package_list.extend(
                DrawingTool.generate_note(
                    drawing_package.domain,
                    DrawingPosition.TOP,
                    lst_attribute,
                    "Attributes",
                )
            )

            lst_user = []
            lst_user.extend(drawing_package.users)
            drawing_package_list.extend(
                DrawingTool.generate_note(
                    drawing_package.domain, DrawingPosition.TOP, lst_user, "Users"
                )
            )

        print(drawing_package_list)
        return drawing_package_list

    def write_to_file(self, file_name, list_of_str):
        file_writer = FW.FileWriter
        file_writer.write_list_to_file(file_name, list_of_str)
