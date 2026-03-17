# 💾 Local Storage Adapter - Saves files to the local disk.
# This is the default adapter for local development.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import os
from app.interfaces.storage_adapter import StorageAdapter

class LocalStorageAdapter(StorageAdapter):
    """
    Saves files to a local 'reports' directory.
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, file_name: str, file_data: bytes) -> str:
        """
        Saves the file data to the local filesystem.
        """
        file_path = os.path.join(self.output_dir, file_name)
        try:
            with open(file_path, "wb") as f:
                f.write(file_data)
            print(f"✅ File saved locally: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ Local storage error: {e}")
            raise
