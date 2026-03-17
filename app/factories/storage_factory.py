# 🏭 Agnostic Storage Factory - Creates storage adapters.
# This factory implements the "Agnostic Factory" pattern, allowing the system
# to switch between local and cloud storage via configuration.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import os
from app.interfaces.storage_adapter import StorageAdapter
from app.config import config # <-- Use the global config object

class StorageFactory:
    """
    Factory to create a storage adapter based on environment variables.
    """
    
    _instance = None

    @staticmethod
    def get_adapter() -> StorageAdapter:
        """
        Returns a singleton instance of the configured storage adapter.
        """
        if StorageFactory._instance is None:
            storage_type = os.getenv("STORAGE_TYPE", "local").lower()
            
            if storage_type == "s3":
                from app.adapters.s3_adapter import S3StorageAdapter
                StorageFactory._instance = S3StorageAdapter()
            elif storage_type == "azure":
                from app.adapters.azure_blob_adapter import AzureBlobStorageAdapter
                StorageFactory._instance = AzureBlobStorageAdapter()
            else: # Default to local
                from app.adapters.local_storage_adapter import LocalStorageAdapter
                StorageFactory._instance = LocalStorageAdapter()
                
        return StorageFactory._instance
