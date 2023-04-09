from model.PolicyEntities import *
from PythonUtilityClasses import FileWriter as FW
from drawer.DrawerHelper import *
from AppSetting import *
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

        plant_uml_list.extend(DrawingTool.defineDomainStyle())
        plant_uml_list.extend(DrawingTool.define_note_style())
        plant_uml_list.extend(self.drawer_class.participants)
        plant_uml_list.extend(self.drawer_class.rules)

        plant_uml_list.extend(DrawingTool.generate_end_of_puml())

        # Remove redundance items
        # Temporary disabled since removes blindlt : plant_uml_list =
        # list(dict.fromkeys(plant_uml_list))

        # print(plant_uml_list)
        file_path = OUT_DIR + generate_puml_file_name(policy_file.fileName)
        self.write_to_file(file_path, plant_uml_list)
        print("drawing: ", file_path)

        generate_png(file_path)
        # print(policy_file)

    def dump_policy_file(self, policy_file: PolicyFiles):

        policy_file = self.correlate_data(policy_file)

        return  super().dump_policy_file(policy_file)

    def correlate_data(self, policy_file: PolicyFiles):
        for se_app in policy_file.seApps:
            for i in reversed(range(len(policy_file.typeDef))):
                if se_app.domain == policy_file.typeDef[i].name:
                    se_app.typeDef.types.extend(policy_file.typeDef[i].types)
                    del policy_file.typeDef[i]
                    break

        for se_app in policy_file.seApps:
            for i in reversed(range(len(policy_file.attribute))):
                if se_app.domain == policy_file.attribute[i].name:
                    se_app.attribute = policy_file.attribute[i]
                    del policy_file.attribute[i]
                    break

        for j in range(len(policy_file.contexts)):
            for i in reversed(range(len(policy_file.typeDef))):
                if policy_file.contexts[j].securityContext.type.replace(
                        DOMAIN_EXECUTABLE, "") == policy_file.typeDef[i].name:
                    policy_file.contexts[j].domainName = policy_file.typeDef[i].name
                    policy_file.contexts[j].typeDef.types.extend(
                        policy_file.typeDef[i].types)
                    del policy_file.typeDef[i]
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
                    context.domainName,
                    context.pathName))

            lst_note = []
            # lst_note.append("Path: " + context.pathName)
            lst_note.extend(context.typeDef.types)
            context_list.extend(
                DrawingTool.generate_note(
                    context.domainName,
                    DrawingPosition.TOP,
                    lst_note,
                    "Types"))
        return context_list

    def draw_se_app(self, se_app_contexts: List[SeAppContext]):
        se_app_list = []
        for seAppContext in se_app_contexts:
            se_app_list.extend(DrawingTool.generate_domain(seAppContext.domain))

            lst_note = []
            lst_note.append(seAppContext.user)
            lst_note.extend(seAppContext.typeDef.types)
            lst_note.extend(seAppContext.attribute.attributes)
            se_app_list.extend(
                DrawingTool.generate_note(
                    seAppContext.domain,
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


