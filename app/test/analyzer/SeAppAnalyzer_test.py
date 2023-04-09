# This class is going to test the SeAppAnalyzer class
import unittest
from analyzer.SeAppAnalyzer import SeAppAnalyzer

class TestSeAppAnalyzer(unittest.TestCase):
    def test_extract_definition(self):
        # Test the extractDefinition function
        se_app_analyzer = SeAppAnalyzer()
        se_app = se_app_analyzer.extract_definition(
            "user=app0 name=app1 domain=app2 type=app3 level_from=app4 "
            "level=app5 seinfo=app6 is_priv_app=True is_system_server=False "
            "is_ephemeral_app=True from_run_as=app7 min_target_sdk_version=21")
        self.assertEqual(se_app.user, "app0")
        self.assertEqual(se_app.name, "app1")
        self.assertEqual(se_app.domain, "app2")
        self.assertEqual(se_app.type, "app3")
        self.assertEqual(se_app.level_from, "app4")
        self.assertEqual(se_app.level, "app5")
        self.assertEqual(se_app.seinfo, "app6")
        self.assertEqual(se_app.is_priv_app, 'True')
        self.assertEqual(
            se_app.is_system_server, False)
        self.assertEqual(
            se_app.is_ephemeral_app, 'True')
        self.assertEqual(se_app.from_run_as, "app7")
        self.assertEqual(
            se_app.min_target_sdk_version, '21')
