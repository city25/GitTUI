"""Fixtures package that re-exports test helper implementations.

This package provides an easy import path for integration tests that need
sample CLI implementations. It re-uses the existing `tests.src` helper
implementation to avoid duplicating code during migration.
"""
try:
    from tests.src import *  # re-export existing test helpers (keeps compatibility)
except Exception:
    # If tests.src is not present or import fails, leave package empty.
    pass
