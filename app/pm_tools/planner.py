import requests
import os
import msal
from typing import Optional
from .adapter import PMToolAdapter

class PlannerAdapter(PMToolAdapter):
    """
    Microsoft Planner Adapter using Graph API.
    Handles task creation and file attachments via SharePoint.
    """
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, plan_id: str, bucket_id: str):
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = ["https://graph.microsoft.com/.default"]
        self.plan_id = plan_id
        self.bucket_id = bucket_id
        self.graph_url = "https://graph.microsoft.com/v1.0"
        
        # SharePoint Config
        self.sharepoint_drive_id = os.getenv("MS_SHAREPOINT_DRIVE_ID")
        
        self.app = msal.ConfidentialClientApplication(
            client_id, authority=self.authority, client_credential=client_secret
        )
        self._token = None

    def _get_token(self):
        """
        Acquires a token from Azure AD.
        """
        result = self.app.acquire_token_silent(self.scope, account=None)
        if not result:
            result = self.app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            self._token = result['access_token']
            return self._token
        else:
            raise Exception(f"Could not acquire token: {result.get('error_description')}")

    def create_ticket(self, title: str, description: str, pdf_path: Optional[str] = None) -> str:
        token = self._get_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        
        # 1. Create Task
        task_payload = {
            "planId": self.plan_id,
            "bucketId": self.bucket_id,
            "title": title
        }
        
        try:
            response = requests.post(f"{self.graph_url}/planner/tasks", json=task_payload, headers=headers)
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data['id']
            
            # 2. Update Task Details (Description)
            self._update_task_details(task_id, description, headers)
            
            # 3. Handle PDF Attachment
            if pdf_path and self.sharepoint_drive_id:
                sharepoint_url = self._upload_to_sharepoint(pdf_path, headers)
                if sharepoint_url:
                    self._add_attachment(task_id, sharepoint_url, os.path.basename(pdf_path), headers)

            return f"Planner Task ID: {task_id}"
            
        except Exception as e:
            print(f"❌ Planner Error: {e}")
            return f"Error: {str(e)}"

    def _update_task_details(self, task_id: str, description: str, headers: dict):
        details_url = f"{self.graph_url}/planner/tasks/{task_id}/details"
        response = requests.get(details_url, headers=headers)
        response.raise_for_status()
        etag = response.json().get('@odata.etag')
        
        update_headers = headers.copy()
        update_headers['If-Match'] = etag
        
        update_payload = {"description": description}
        requests.patch(details_url, json=update_payload, headers=update_headers)

    def _upload_to_sharepoint(self, file_path: str, headers: dict) -> Optional[str]:
        """
        Uploads a file to the configured SharePoint drive and returns its web URL.
        """
        filename = os.path.basename(file_path)
        upload_url = f"{self.graph_url}/drives/{self.sharepoint_drive_id}/root:/{filename}:/content"
        
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            upload_headers = headers.copy()
            upload_headers['Content-Type'] = 'application/pdf'
            
            response = requests.put(upload_url, data=file_content, headers=upload_headers)
            response.raise_for_status()
            
            web_url = response.json().get('webUrl')
            print(f"✅ PDF uploaded to SharePoint: {web_url}")
            return web_url
            
        except Exception as e:
            print(f"❌ SharePoint Upload Error: {e}")
            return None

    def _add_attachment(self, task_id: str, url: str, alias: str, headers: dict):
        """
        Adds a reference link attachment to a Planner task.
        """
        details_url = f"{self.graph_url}/planner/tasks/{task_id}/details"
        response = requests.get(details_url, headers=headers)
        response.raise_for_status()
        etag = response.json().get('@odata.etag')
        
        update_headers = headers.copy()
        update_headers['If-Match'] = etag
        
        attachment_payload = {
            "references": {
                f"{url}": {
                    "@odata.type": "microsoft.graph.plannerExternalReference",
                    "alias": alias,
                    "type": "Other",
                    "previewPriority": "!"
                }
            }
        }
        
        requests.patch(details_url, json=attachment_payload, headers=update_headers)
        print(f"✅ Link attached to Planner task {task_id}")
