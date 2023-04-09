from model.PolicyEntities import *
from drawer.DrawerHelper import *
from AppSetting import *
from typing import List
from model.PolicyEntities import *


class AbstractDrawer:
    def __init__(self) -> None:
        self.map_list = []
        self.map_list.append(UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.map_list.append(UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.map_list.append(UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

        self.data_type_to_ignore = []
        self.dict_of_participant = {}
        self.drawer_class = DrawerClass()

    def insert_new_participant(self, name):
        if any(x in name for x in ["-", "/", ":"]):
            if name not in self.dict_of_participant:
                self.dict_of_participant[name] = name.replace(
                    "-",
                    "__").replace(
                    "/",
                    "_1_").replace(
                    ":",
                    "_2_")
                # print ( "==========", name, self.dictOfParticipant[name])
                self.drawer_class.participants.append(
                    "participant " +
                    self.insert_new_participant(
                        self.dict_of_participant[name]) +
                    " [\n=" +
                    name +
                    "\n ]")
            return self.dict_of_participant[name]
        return name

    def draw_se_app(self, se_apps):
        pass

    def draw_type_def(self, type_defs):
        pass

    def draw_context(self, contexts):
        pass

    def dump_policy_file(self, policy_file):
        plant_uml_list = []

        if policy_file is not None:
            self.drawer_class.participants.extend(
                self.draw_se_app(policy_file.seApps))
            self.drawer_class.participants.extend(
                self.draw_type_def(policy_file.typeDef))
            self.drawer_class.participants.extend(
                self.draw_context(policy_file.contexts))
            self.drawer_class.rules.extend(self.draw_rule(policy_file.rules))

        return plant_uml_list