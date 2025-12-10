"""pytest fixtures and test import path setup for the project.

Adds the project `src/` directory to `sys.path` so tests can import `cli.*` modules.
"""
import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


@pytest.fixture
def dummy_tmpdir(tmp_path):
    """Simple fixture that returns a temporary path for tests."""
    return tmp_path
