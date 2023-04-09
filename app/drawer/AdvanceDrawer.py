from model.PolicyEntities import PolicyFile, TypeDef, Rule, RuleEnum
from model.PolicyEntities import SeAppContext, Context, DOMAIN_EXECUTABLE
from PythonUtilityClasses import FileWriter as FW
from drawer.DrawerHelper import generate_png, generate_puml_file_name
from drawer.DrawerHelper import DrawingTool, DrawingPosition, DrawingColor
from AppSetting import OUT_DIR
from typing import List
from drawer.AbstractDrawer import *

class AdvancedDrawer(AbstractDrawer):

    def draw_uml(self, policy_file):
        self.dict_of_participant = {}
        self.drawer_class = DrawerClass()

        plant_uml_list = []
        plant_uml_list.extend(DrawingTool.generate_start_of_puml())
        plant_uml_list.extend(self.generate_reference())

        self.dump_policy_file(policy_file)

        plant_uml_list.extend(DrawingTool.define_domain_style())
        plant_uml_list.extend(DrawingTool.define_note_style())
        plant_uml_list.extend(self.drawer_class.participants)
        plant_uml_list.extend(self.drawer_class.rules)

        plant_uml_list.extend(DrawingTool.generate_end_of_puml())

        # Remove redundance items
        # Temporary disabled since removes blindlt : plant_uml_list =
        # list(dict.fromkeys(plant_uml_list))

        # print(plant_uml_list)
        file_path = OUT_DIR + generate_puml_file_name(policy_file.file_name)
        self.write_to_file(file_path, plant_uml_list)
        print("drawing: ", file_path)

        generate_png(file_path)
        # print(policy_file)

    def dump_policy_file(self, policy_file: PolicyFile):

        policy_file = self.correlate_data(policy_file)

        return  super().dump_policy_file(policy_file)

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
                if policy_file.contexts[j].security_context.type.replace(
                        DOMAIN_EXECUTABLE, "") == policy_file.type_def[i].name:
                    policy_file.contexts[j].domain_name = policy_file.type_def[i].name
                    policy_file.contexts[j].type_def.types.extend(
                        policy_file.type_def[i].types)
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
                    type_def.name,
                    DrawingPosition.TOP,
                    lst_note,
                    "Types"))
        return type_def_list

    def draw_context(self, contexts: List[Context]):
        context_list = []
        for context in contexts:
            context_list.extend(
                DrawingTool.generate_other_label(
                    context.domain_name,
                    context.path_name))

            lst_note = []
            # lst_note.append("Path: " + context.path_name)
            lst_note.extend(context.type_def.types)
            context_list.extend(
                DrawingTool.generate_note(
                    context.domain_name,
                    DrawingPosition.TOP,
                    lst_note,
                    "Types"))
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
                    se_app_context.domain,
                    DrawingPosition.TOP,
                    lst_note,
                    "Types"))
        return se_app_list

    def draw_rule(self, rules: List[Rule]):
        rule_list = []
        for rule in rules:
            for permission in rule.permissions:
                if rule.rule == RuleEnum.NEVER_ALLOW:
                    rule_list.append(
                        "" +
                        self.insert_new_participant(
                            rule.source) +
                        " .....[#red]> \"" +
                        rule.target +
                        "\" : " +
                        "!! " +
                        permission +
                        " !!")
                else:
                    rule_list.append(
                        "" +
                        self.insert_new_participant(
                            rule.source) +
                        " -----[#green]> \"" +
                        rule.target +
                        "\" : " +
                        permission)

        return rule_list



    def generate_reference(self):
        lst_note = []
        lst_note.append("Sumbols")
        lst_note.append("Green Line: Allow")
        lst_note.append("Red Line: Never Allow")
        return DrawingTool.generate_legend(
            "Reference",
            DrawingPosition.TOP,
            DrawingPosition.LEFT,
            lst_note,
            DrawingColor.BLUE_LIGHT)

    def write_to_file(self, file_name, list_of_str):
        file_writer = FW.FileWriter
        file_writer.write_list_to_file(file_name, list_of_str)
