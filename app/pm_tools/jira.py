import requests
import os
from typing import Optional
from .adapter import PMToolAdapter

class JiraAdapter(PMToolAdapter):
    """
    Jira Adapter using REST API.
    """
    
    def __init__(self, url: str, email: str, api_token: str, project_key: str):
        self.url = url.rstrip('/')
        self.auth = (email, api_token)
        self.project_key = project_key
        
    def create_ticket(self, title: str, description: str, pdf_path: Optional[str] = None) -> str:
        # 1. Create Issue
        issue_url = f"{self.url}/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": "Task"}
            }
        }
        
        try:
            response = requests.post(issue_url, json=payload, auth=self.auth)
            response.raise_for_status()
            issue_key = response.json()['key']
            
            # 2. Attach PDF (if provided)
            if pdf_path and os.path.exists(pdf_path):
                self._attach_file(issue_key, pdf_path)
                
            return f"{self.url}/browse/{issue_key}"
            
        except Exception as e:
            print(f"❌ Jira Error: {e}")
            return f"Error: {str(e)}"

    def _attach_file(self, issue_key: str, file_path: str):
        url = f"{self.url}/rest/api/3/issue/{issue_key}/attachments"
        headers = {"X-Atlassian-Token": "no-check"}
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            requests.post(url, headers=headers, files=files, auth=self.auth)
