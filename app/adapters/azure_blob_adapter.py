# 💾 Azure Blob Storage Adapter - Saves files to Azure.
# This is a placeholder for production Azure storage.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import os
from app.interfaces.storage_adapter import StorageAdapter

class AzureBlobStorageAdapter(StorageAdapter):
    """
    Saves files to an Azure Blob Storage container.
    Requires `azure-storage-blob` to be installed and credentials configured.
    """
    
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        try:
            from azure.storage.blob import BlobServiceClient
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        except ImportError:
            raise ImportError("azure-storage-blob is required for the Azure adapter. Please run 'pip install azure-storage-blob'.")

    def save(self, file_name: str, file_data: bytes) -> str:
        """
        Uploads the file data to the Azure Blob container.
        """
        if not self.connection_string or not self.container_name:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING and AZURE_STORAGE_CONTAINER_NAME must be set.")
            
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)
            blob_client.upload_blob(file_data, overwrite=True, content_settings={'content_type': 'application/pdf'})
            return blob_client.url
        except Exception as e:
            print(f"❌ Azure Blob upload error: {e}")
            raise
