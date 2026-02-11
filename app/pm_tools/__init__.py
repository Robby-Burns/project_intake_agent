import os
from .adapter import PMToolAdapter
from .mock import MockAdapter
from .jira import JiraAdapter
from .monday import MondayAdapter

def get_pm_tool() -> PMToolAdapter:
    """
    Factory function to get the configured PM Tool Adapter.
    """
    tool_type = os.getenv("PM_TOOL", "mock").lower()
    print(f"🔧 Loading PM Tool: {tool_type}") # Debug Print
    
    if tool_type == "jira":
        return JiraAdapter(
            url=os.getenv("JIRA_URL"),
            email=os.getenv("JIRA_EMAIL"),
            api_token=os.getenv("JIRA_API_TOKEN"),
            project_key=os.getenv("JIRA_PROJECT_KEY")
        )
    elif tool_type == "monday":
        return MondayAdapter(
            api_key=os.getenv("MONDAY_API_KEY"),
            board_id=os.getenv("MONDAY_BOARD_ID")
        )
    else:
        return MockAdapter()
