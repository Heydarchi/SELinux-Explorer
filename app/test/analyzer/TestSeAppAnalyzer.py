# This class is going to test the SeAppAnalyzer class

class TestSeAppAnalyzer(unittest.TestCase):
    def test_extractDefinition(self):
        # Test the extractDefinition function
        seAppAnalyzer = SeAppAnalyzer()
        seAppAnalyzer.extract_definition(
            "user=app0 name=app1 domain=app2 type=app3 levelFrom=app4 "
            "level=app5 seinfo=app6 isPrivApp=True isSystemServer=False "
            "isEphemeralApp=True fromRunAs=app7 minTargetSdkVersion=21")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].user, "app0")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].name, "app1")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].domain, "app2")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].type, "app3")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].levelFrom, "app4")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].level, "app5")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].seinfo, "app6")
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].isPrivApp, True)
        self.assertEqual(
            seAppAnalyzer.policyFile.seApps[0].isSystemServer, False)
        self.assertEqual(
            seAppAnalyzer.policyFile.seApps[0].isEphemeralApp, True)
        self.assertEqual(seAppAnalyzer.policyFile.seApps[0].fromRunAs, "app7")
        self.assertEqual(
            seAppAnalyzer.policyFile.seApps[0].minTargetSdkVersion, 21)
