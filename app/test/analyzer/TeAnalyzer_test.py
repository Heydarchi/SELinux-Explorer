# This class is going to test the TeAnalyzer class
import unittest
from analyzer.TeAnalyzer import TeAnalyzer
from model.PolicyEntities import *


class TestTeAnalyzer(unittest.TestCase):
    def test_extract_macro_call(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "call_macro(1, 2, 3)"
        # Act
        macro_call = te_analyzer.extract_macro_call(input_string)
        # Assert
        self.assertEqual(macro_call.name, "call_macro")
        self.assertEqual(macro_call.parameters, ["1", "2", "3"])

    def test_extract_macro_no_param(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = """define(`call_macro',`
        allow source1 target1:class1 permission1;
        allow source2 target2:class2 permission2;
        ')
        """
        # Act
        macro = te_analyzer.extract_macro(input_string)
        # Assert
        self.assertEqual(macro.name, "call_macro")
        self.assertEqual(len(macro.rules), 2)
        self.assertEqual(macro.rules[0].source, "source1")
        self.assertEqual(macro.rules[0].target, "target1")
        self.assertEqual(macro.rules[0].class_type, "class1")
        self.assertEqual(macro.rules[0].permissions, ["permission1"])
        self.assertEqual(macro.rules[1].source, "source2")
        self.assertEqual(macro.rules[1].target, "target2")
        self.assertEqual(macro.rules[1].class_type, "class2")
        self.assertEqual(macro.rules[1].permissions, ["permission2"])

    def test_extract_macro_with_param(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = """define(`call_macro',`
        allow $1 $2:$3 $4;
        allow $5 {$6 $7}:$8 $9;
        ')
        """
        # Act
        macro = te_analyzer.extract_macro(input_string)
        # Assert
        self.assertEqual(macro.name, "call_macro")
        self.assertEqual(len(macro.rules), 3)
        self.assertEqual(macro.rules[0].source, "$1")
        self.assertEqual(macro.rules[0].target, "$2")
        self.assertEqual(macro.rules[0].class_type, "$3")
        self.assertEqual(macro.rules[0].permissions, ["$4"])
        self.assertEqual(macro.rules[1].source, "$5")
        self.assertEqual(macro.rules[1].target, "$6")
        self.assertEqual(macro.rules[1].class_type, "$8")
        self.assertEqual(macro.rules[1].permissions, ["$9"])
        self.assertEqual(macro.rules[2].source, "$5")
        self.assertEqual(macro.rules[2].target, "$7")
        self.assertEqual(macro.rules[2].class_type, "$8")
        self.assertEqual(macro.rules[2].permissions, ["$9"])

    def test_extract_macrocall_with_param(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "call_macro(source1, target1, class1, source2, target2, class2)"
        # Act
        macro_call = te_analyzer.extract_macro_call(input_string)
        # Assert
        self.assertEqual(macro_call.name, "call_macro")
        self.assertEqual(
            macro_call.parameters,
            ["source1", "target1", "class1", "source2", "target2", "class2"],
        )

    def test_extract_macrocall_no_param(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "call_macro()"
        # Act
        macro_call = te_analyzer.extract_macro_call(input_string)
        # Assert
        self.assertEqual(macro_call.name, "call_macro")
        self.assertEqual(macro_call.parameters, [""])

    def test_extract_rule(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "allow source1 target1:class1 permission1;"
        # Act
        rules = te_analyzer.extract_rule(input_string)
        # Assert
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].source, "source1")
        self.assertEqual(rules[0].target, "target1")
        self.assertEqual(rules[0].class_type, "class1")
        self.assertEqual(rules[0].permissions, ["permission1"])

    def test_extract_rule_multiple_source(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "allow {source1 source2} target1:class1 permission1;"
        # Act
        rules = te_analyzer.extract_rule(input_string)
        # Assert
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0].source, "source1")
        self.assertEqual(rules[0].target, "target1")
        self.assertEqual(rules[0].class_type, "class1")
        self.assertEqual(rules[0].permissions, ["permission1"])
        self.assertEqual(rules[1].source, "source2")
        self.assertEqual(rules[1].target, "target1")
        self.assertEqual(rules[1].class_type, "class1")
        self.assertEqual(rules[1].permissions, ["permission1"])

    def test_extract_rule_multiple_target(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "allow source1 {target1 target2}:class1 permission1;"
        # Act
        rules = te_analyzer.extract_rule(input_string)
        # Assert
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0].source, "source1")
        self.assertEqual(rules[0].target, "target1")
        self.assertEqual(rules[0].class_type, "class1")
        self.assertEqual(rules[0].permissions, ["permission1"])
        self.assertEqual(rules[1].source, "source1")
        self.assertEqual(rules[1].target, "target2")
        self.assertEqual(rules[1].class_type, "class1")
        self.assertEqual(rules[1].permissions, ["permission1"])

    def test_extract_rule_multiple_permission(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "allow source1 target1:class1 {permission1 permission2};"
        # Act
        rules = te_analyzer.extract_rule(input_string)
        # Assert
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].source, "source1")
        self.assertEqual(rules[0].target, "target1")
        self.assertEqual(rules[0].class_type, "class1")
        self.assertEqual(rules[0].permissions, ["permission1", "permission2"])

    def test_extract_rule_multiple_source_target_permission(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "allow {source1 source2} {target1 target2}:class1 {permission1 permission2};"
        # Act
        rules = te_analyzer.extract_rule(input_string)
        # Assert
        self.assertEqual(len(rules), 4)
        self.assertEqual(rules[0].source, "source1")
        self.assertEqual(rules[0].target, "target1")
        self.assertEqual(rules[0].class_type, "class1")
        self.assertEqual(rules[0].permissions, ["permission1", "permission2"])
        self.assertEqual(rules[1].source, "source1")
        self.assertEqual(rules[1].target, "target2")
        self.assertEqual(rules[1].class_type, "class1")
        self.assertEqual(rules[1].permissions, ["permission1", "permission2"])
        self.assertEqual(rules[2].source, "source2")
        self.assertEqual(rules[2].target, "target1")
        self.assertEqual(rules[2].class_type, "class1")
        self.assertEqual(rules[2].permissions, ["permission1", "permission2"])
        self.assertEqual(rules[3].source, "source2")
        self.assertEqual(rules[3].target, "target2")
        self.assertEqual(rules[3].class_type, "class1")
        self.assertEqual(rules[3].permissions, ["permission1", "permission2"])

    """def test_extract_rule_multiple_class_and_macrocall(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = ["  # debugfs",
                          "neverallow {",
                            "coredomain",
                            "no_debugfs_restriction(`",
                              "-dumpstate",
                              "-init",
                              "-system_server",
                            "')",
                          "} debugfs:file no_rw_file_perms;"]
        # Act
        line = te_analyzer.extract_items_to_process(input_string)
        print(line)
        rules = te_analyzer.extract_rule(line)
        # Assert
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0].source, "coredomain")
        self.assertEqual(rules[0].target, "debugfs")
        self.assertEqual(rules[0].class_type, "file")
        self.assertEqual(rules[0].permissions, ["no_rw_file_perms"])
        self.assertEqual(rules[1].source, "no_debugfs_restriction(`-dumpstate -init -system_server')")
        self.assertEqual(rules[1].target, "debugfs")
        self.assertEqual(rules[1].class_type, "file")
        self.assertEqual(rules[1].permissions, ["no_rw_file_perms"])
    """

    def test_extract_attribute(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "typeattribute type_id attr1, attr2;"
        # Act
        attribute = te_analyzer.extract_attribute(input_string)
        # Assert
        self.assertEqual(len(attribute.attributes), 2)
        self.assertEqual(attribute.name, "type_id")
        self.assertEqual(attribute.attributes[0], "attr1")
        self.assertEqual(attribute.attributes[1], "attr2")

    def test_extract_definition(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "type type_id, type1, type2, type3;"
        # Act
        definition = te_analyzer.extract_definition(input_string)
        # Assert
        self.assertEqual(len(definition.types), 3)
        self.assertEqual(definition.name, "type_id")
        self.assertEqual(definition.types[0], "type1")
        self.assertEqual(definition.types[1], "type2")
        self.assertEqual(definition.types[2], "type3")

    def test_extract_items_to_process(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        file_lines = [
            "allow { ",
            "source1 ",
            "source2}",
            " target1:class1 permission1;",
            "allow source3 target3:class3 permission3;",
            "type type_id, type1, type2, type3;",
            "typeattribute type_id attr1, attr2;",
            "allow ",
            " source4 ",
            "target4:class4 permission4;",
            "define(`call_macro`,`",
            "allow $1 $2:$3 $4;",
            "allow $5 {$6 $7}:$8 $9;",
            " `)",
        ]
        # Act
        items_to_process = te_analyzer.extract_items_to_process(file_lines)
        # Assert
        self.assertEqual(len(items_to_process), 6)
        self.assertEqual(
            items_to_process[0], "allow { source1 source2} target1:class1 permission1;"
        )
        self.assertEqual(
            items_to_process[1], "allow source3 target3:class3 permission3;"
        )
        self.assertEqual(items_to_process[2], "type type_id, type1, type2, type3;")
        self.assertEqual(items_to_process[3], "typeattribute type_id attr1, attr2;")
        self.assertEqual(
            items_to_process[4], "allow source4 target4:class4 permission4;"
        )
        self.assertEqual(
            items_to_process[5],
            "define(`call_macro`,`\n allow $1 $2:$3 $4;\n allow $5 {$6 $7}:$8 $9;\n `)",
        )

    def test_extract_items_to_process_miltiple_macro_define(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        file_lines = [
            "#The dumpstate HAL reads debugFs files, which become part of the bug report",
            "#But there are some restrictions according to system/sepolicy/private/domain.te line 529",
            "#This is only needed in userdebug",
            "userdebug_or_eng(`dontaudit dumpstate debugfs_wakeup_sources:file read;",
            "')",
        ]
        # Act
        items_to_process = te_analyzer.extract_items_to_process(file_lines)
        # Assert
        self.assertEqual(len(items_to_process), 1)
        self.assertEqual(
            items_to_process[0].replace("\n", ""),
            "userdebug_or_eng(`dontaudit dumpstate debugfs_wakeup_sources:file read; ')",
        )

    def test_extact_items_to_process_miltiple_class_and_macrocall(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        file_lines = [
            "full_treble_only(`",
            "  # Vendor apps are permitted to use only stable public services. If they were to use arbitrary",
            "  # services which can change any time framework/core is updated, breakage is likely.",
            "  #",
            "  # Note, this same logic applies to untrusted apps, but neverallows for these are separate.",
            "  neverallow {",
            "    appdomain",
            "    -coredomain",
            "  } {",
            "    service_manager_type",
            "",
            "    -app_api_service",
            "    -vendor_service # must be @VintfStability to be used by an app",
            "    -ephemeral_app_api_service",
            "",
            "    -apc_service",
            "    -audioserver_service # TODO(b/36783122) remove exemptions below once app_api_service is fixed",
            "    -cameraserver_service",
            "    -drmserver_service",
            "    -credstore_service",
            "    -keystore_maintenance_service",
            "    -keystore_service",
            "    -legacykeystore_service",
            "    -mediadrmserver_service",
            "    -mediaextractor_service",
            "    -mediametrics_service",
            "    -mediaserver_service",
            "    -nfc_service",
            "    -radio_service",
            "    -virtual_touchpad_service",
            "    -vr_hwc_service",
            "    -vr_manager_service",
            "    userdebug_or_eng(`-hal_face_service')",
            "  }:service_manager find;",
            "')",
        ]
        # Act
        items_to_process = te_analyzer.extract_items_to_process(file_lines)
        # Assert
        self.assertEqual(len(items_to_process), 1)
        self.assertEqual(
            items_to_process[0].replace("\n", ""),
            "full_treble_only(` neverallow { appdomain -coredomain }"
            + " { service_manager_type -app_api_service -vendor_service -ephemeral_app_api_service"
            + " -apc_service -audioserver_service -cameraserver_service -drmserver_service -credstore_service"
            + " -keystore_maintenance_service -keystore_service -legacykeystore_service -mediadrmserver_service"
            + " -mediaextractor_service -mediametrics_service -mediaserver_service -nfc_service -radio_service"
            + " -virtual_touchpad_service -vr_hwc_service -vr_manager_service userdebug_or_eng(`-hal_face_service')"
            + " }:service_manager find; ')",
        )

    def test_extract_permissive(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "permissive domain;"
        # Act
        permissive = te_analyzer.extract_permissive(input_string)
        # Assert
        self.assertEqual(permissive.name, "domain")

    def test_extract_type_alias(self):
        # Arrange
        te_analyzer = TeAnalyzer()
        input_string = "typealias type_id alias alias;"
        # Act
        type_alias = te_analyzer.extract_type_alias(input_string)
        # Assert
        self.assertEqual(type_alias.name, "type_id")
        self.assertEqual(type_alias.alias, "alias")

    """def test_extract_definition_with_alis(self):
        
        Need to be implemented !!!
    """

    """def test_merge_exec_domain(self):
    
        Need to be implemented !!!
    """


if __name__ == "__main__":
    unittest.main()
