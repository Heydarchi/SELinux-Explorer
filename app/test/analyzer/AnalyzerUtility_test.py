import unittest
from analyzer.AnalyzerUtility import *

# This class is going to test the AnalyzerUtility class


class TestAnalyzerUtility(unittest.TestCase):
    def test_clean_line(self):
        # Test the clean_line function
        self.assertEqual(
            clean_line("allow domain1 domain2:file { read write }"),
            "allow domain1 domain2:file { read write }",
        )
        self.assertEqual(
            clean_line(" allow domain1 domain2:file { read write }; "),
            "allow domain1 domain2:file { read write };",
        )
        self.assertEqual(
            clean_line(" allow domain1 domain2:file { read write }; #comment "),
            "allow domain1 domain2:file { read write };",
        )
        self.assertEqual(
            clean_line("allow domain1 domain2:file { read write };"),
            "allow domain1 domain2:file { read write };",
        )
