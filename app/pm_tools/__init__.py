# app/pm_tools/__init__.py
# This file intentionally only exposes the factory to enforce lazy loading
# and prevent ModuleNotFoundErrors for uninstalled optional dependencies.

from .adapter import PMToolAdapter
from ..factories.pm_tool_factory import PMToolFactory

def get_pm_tool() -> PMToolAdapter:
    """
    Public method to get the configured PM tool adapter.
    This is the single entry point for the rest of the application.
    """
    return PMToolFactory.get_adapter()
