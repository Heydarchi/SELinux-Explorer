<<<<<<< HEAD
import os
import sys

# Ensure the 'app' directory (parent of this file) is on sys.path so imports like
# 'from analyzer.TeAnalyzer import TeAnalyzer' resolve during pytest runs from repo root.
=======
import sys
import os

# Ensure `app` package (project's app folder) is on sys.path so tests can import modules like `analyzer.*`.
>>>>>>> 45972e0 (- Enhance clean_line method)
TEST_DIR = os.path.dirname(__file__)
APP_DIR = os.path.dirname(TEST_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
