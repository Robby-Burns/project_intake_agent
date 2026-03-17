# 💾 Storage Adapter Interface - Defines the contract for file storage.
# This follows the Agnostic Factory pattern, allowing for swappable storage backends.
# Reference: agent.md - The System Kernel for AI behavior and rules.

from abc import ABC, abstractmethod

class StorageAdapter(ABC):
    """
    Abstract Base Class for Storage Adapters (e.g., Local, S3, Azure Blob).
    """
    
    @abstractmethod
    def save(self, file_name: str, file_data: bytes) -> str:
        """
        Saves file data to the storage backend.
        
        Args:
            file_name: The name of the file (e.g., "my_report.pdf").
            file_data: The raw binary data of the file.
            
        Returns:
            str: The path or URL where the file was saved.
        """
        pass
