# 🏭 Agnostic PM Tool Factory
# Reference: workflow/08_AGNOSTIC_FACTORIES.md
from app.pm_tools.adapter import PMToolAdapter
import os

class PMToolFactory:
    """
    Factory to create a PM tool adapter based on environment variables.
    """
    
    _instance = None

    @staticmethod
    def get_adapter() -> PMToolAdapter:
        """
        Returns a singleton instance of the configured PM tool adapter.
        """
        if PMToolFactory._instance is None:
            tool_type = os.getenv("PM_TOOL_TYPE", "mock").lower()
            
            if tool_type == "jira":
                from app.pm_tools.jira import JiraAdapter
                PMToolFactory._instance = JiraAdapter()
            elif tool_type == "monday":
                from app.pm_tools.monday import MondayAdapter
                PMToolFactory._instance = MondayAdapter()
            elif tool_type == "planner":
                from app.pm_tools.planner import PlannerAdapter
                PMToolFactory._instance = PlannerAdapter()
            else:
                # Default to Mock for development/testing
                from app.pm_tools.mock import MockPMAdapter
                PMToolFactory._instance = MockPMAdapter()
                
        return PMToolFactory._instance
