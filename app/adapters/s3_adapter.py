# 💾 S3 Storage Adapter - Saves files to AWS S3.
# This is a placeholder for production S3 storage.
# Reference: agent.md - The System Kernel for AI behavior and rules.

import os
from app.interfaces.storage_adapter import StorageAdapter

class S3StorageAdapter(StorageAdapter):
    """
    Saves files to an AWS S3 bucket.
    Requires `boto3` to be installed and AWS credentials to be configured.
    """
    
    def __init__(self):
        # These would be loaded from environment variables
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        # boto3 will automatically look for AWS_ACCESS_KEY_ID, etc.
        
        # Lazy import boto3
        try:
            import boto3
            self.s3_client = boto3.client("s3")
        except ImportError:
            raise ImportError("boto3 is required for the S3 adapter. Please run 'pip install boto3'.")

    def save(self, file_name: str, file_data: bytes) -> str:
        """
        Uploads the file data to the S3 bucket.
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET_NAME environment variable is not set.")
            
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_data,
                ContentType='application/pdf'
            )
            # Return the S3 URL
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        except Exception as e:
            print(f"❌ S3 upload error: {e}")
            raise
