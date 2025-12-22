import sys
import os

# Ensure `app` package (project's app folder) is on sys.path so tests can import modules like `analyzer.*`.
TEST_DIR = os.path.dirname(__file__)
APP_DIR = os.path.dirname(TEST_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
