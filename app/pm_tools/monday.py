import requests
import os
import json
from typing import Optional
from .adapter import PMToolAdapter

class MondayAdapter(PMToolAdapter):
    """
    Monday.com Adapter using GraphQL API.
    """
    
    def __init__(self, api_key: str, board_id: str):
        self.api_url = "https://api.monday.com/v2"
        self.file_url = "https://api.monday.com/v2/file"
        self.headers = {"Authorization": api_key}
        self.board_id = int(board_id) if board_id else 0
        self.files_column_id = os.getenv("MONDAY_FILES_COLUMN_ID", "file")
        
    def create_ticket(self, title: str, description: str, pdf_path: Optional[str] = None) -> str:
        print(f"🚀 Creating Monday Item: {title}", flush=True)
        
        # 1. Create Item
        query = """
        mutation ($board_id: ID!, $item_name: String!, $column_values: JSON!) {
            create_item (board_id: $board_id, item_name: $item_name, column_values: $column_values) {
                id
            }
        }
        """
        
        vars = {
            "board_id": self.board_id,
            "item_name": title,
            "column_values": json.dumps({}) 
        }
        
        try:
            response = requests.post(self.api_url, json={'query': query, 'variables': vars}, headers=self.headers)
            response_json = response.json()
            
            if 'errors' in response_json:
                raise Exception(response_json['errors'])
                
            item_id = response_json['data']['create_item']['id']
            print(f"✅ Item Created: {item_id}", flush=True)
            
            # 2. Add Description as an Update (Comment)
            self._add_update(item_id, description)
            
            # 3. Attach PDF
            if pdf_path and os.path.exists(pdf_path):
                print(f"📎 Attaching PDF: {pdf_path}", flush=True)
                self._attach_file(item_id, pdf_path)
            else:
                print(f"⚠️ PDF path not found: {pdf_path}", flush=True)
                
            return f"https://monday.com/boards/{self.board_id}/pulses/{item_id}"
            
        except Exception as e:
            print(f"❌ Monday Error: {e}", flush=True)
            return f"Error: {str(e)}"

    def _add_update(self, item_id: str, text: str):
        query = """
        mutation ($item_id: ID!, $body: String!) {
            create_update (item_id: $item_id, body: $body) {
                id
            }
        }
        """
        vars = {"item_id": item_id, "body": text}
        requests.post(self.api_url, json={'query': query, 'variables': vars}, headers=self.headers)

    def _attach_file(self, item_id: str, file_path: str):
        """
        Uploads a file using the strict Monday.com multipart specification.
        """
        query = """
        mutation ($file: File!) {
            add_file_to_column (
                file: $file,
                item_id: %s,
                column_id: "%s"
            ) {
                id
            }
        }
        """ % (item_id, self.files_column_id)
        
        try:
            with open(file_path, 'rb') as f:
                files = {
                    'query': (None, query),
                    'variables': (None, json.dumps({"file": None})),
                    'map': (None, json.dumps({"file": ["variables.file"]})),
                    'file': (os.path.basename(file_path), f, 'application/pdf')
                }
                
                headers = {'Authorization': self.headers['Authorization']}
                
                print(f"📤 Sending upload request to {self.file_url}...", flush=True)
                response = requests.post(self.file_url, files=files, headers=headers)
                
                try:
                    response_json = response.json()
                except:
                    print(f"❌ Non-JSON response: {response.text}", flush=True)
                    return

                if 'errors' in response_json:
                    print(f"⚠️ Direct upload failed: {response_json['errors']}", flush=True)
                else:
                    print(f"✅ PDF successfully uploaded to Monday item {item_id}", flush=True)
                    
        except Exception as e:
            print(f"❌ Upload exception: {e}", flush=True)
