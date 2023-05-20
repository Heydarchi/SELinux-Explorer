"""This class is going to test the ContextsAnalyzer class"""
import unittest
from analyzer.ContextsAnalyzer import ContextsAnalyzer
from model.PolicyEntities import *


class TestContextsAnalyzer(unittest.TestCase):
    def test_extract_definition(self):
        # Test the extractDefinition function
        contexts_analyzer = ContextsAnalyzer()
        contexts_analyzer.policy_file = PolicyFile("test.te", "", FileTypeEnum.FILE_CONTEXTS)
        context = contexts_analyzer.extract_definition(
            "/system/bin/app_process32 system_app:system_app:s0:c512:c768"
        )
        self.assertEqual(context.path_name, "/system/bin/app_process32")
        self.assertEqual(context.security_context.user, "system_app")
        self.assertEqual(context.security_context.role, "system_app")
        self.assertEqual(context.security_context.type, "s0")
        self.assertEqual(context.security_context.level, "c512")
        self.assertEqual(context.security_context.categories, "c768")
