# 🏭 Agnostic PM Tool Factory - Creates PM tool adapters.
# This factory implements the "Agnostic Factory" pattern, a core tenet of the framework,
# allowing the system to be decoupled from a specific PM tool (e.g., Jira, Monday).
# Reference: agent.md - The System Kernel for AI behavior and rules.
# Reference: workflow/08_AGNOSTIC_FACTORIES.md

from app.pm_tools.adapter import PMToolAdapter
import os

class PMToolFactory:
    """
    Factory to create a PM tool adapter based on environment variables.
    This factory is responsible for reading all necessary secrets and config
    from the environment and passing them to the adapter's constructor.
    It also validates that all required environment variables are set.
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
                config = {
                    "url": os.getenv("JIRA_URL"),
                    "email": os.getenv("JIRA_EMAIL"),
                    "api_token": os.getenv("JIRA_API_TOKEN"),
                    "project_key": os.getenv("JIRA_PROJECT_KEY")
                }
                if not all(config.values()):
                    raise ValueError("JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_PROJECT_KEY must be set for Jira integration.")
                PMToolFactory._instance = JiraAdapter(**config)

            elif tool_type == "monday":
                from app.pm_tools.monday import MondayAdapter
                config = {
                    "api_key": os.getenv("MONDAY_API_KEY"),
                    "board_id": os.getenv("MONDAY_BOARD_ID"),
                    "files_column_id": os.getenv("MONDAY_FILES_COLUMN_ID")
                }
                if not all(config.values()):
                    raise ValueError("MONDAY_API_KEY, MONDAY_BOARD_ID, and MONDAY_FILES_COLUMN_ID must be set for Monday.com integration.")
                PMToolFactory._instance = MondayAdapter(**config)

            elif tool_type == "planner":
                from app.pm_tools.planner import PlannerAdapter
                config = {
                    "tenant_id": os.getenv("MS_TENANT_ID"),
                    "client_id": os.getenv("MS_CLIENT_ID"),
                    "client_secret": os.getenv("MS_CLIENT_SECRET"),
                    "plan_id": os.getenv("MS_PLANNER_PLAN_ID"),
                    "bucket_id": os.getenv("MS_PLANNER_BUCKET_ID"),
                    "sharepoint_drive_id": os.getenv("MS_SHAREPOINT_DRIVE_ID")
                }
                if not all(config.values()):
                    raise ValueError("All MS_* environment variables must be set for Planner integration.")
                PMToolFactory._instance = PlannerAdapter(**config)
            
            else: # Default to Mock
                from app.pm_tools.mock import MockPMAdapter
                PMToolFactory._instance = MockPMAdapter()
                
        return PMToolFactory._instance
