import os
import boto3
from botocore.exceptions import ClientError
import tempfile

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket = 'circle30-ev-data'  # Hardcoded bucket name
        self.cache_dir = tempfile.gettempdir()

    def get_file(self, key):
        """Get a file from S3, caching it locally if needed."""
        local_path = os.path.join(self.cache_dir, key)
        
        # If file exists in cache and is less than 1 hour old, use it
        if os.path.exists(local_path):
            file_age = os.path.getmtime(local_path)
            if (os.path.getmtime(local_path) - file_age) < 3600:
                return local_path

        # Download from S3
        try:
            self.s3.download_file(self.bucket, key, local_path)
            return local_path
        except ClientError as e:
            print(f"Error downloading {key} from S3: {e}")
            return None

# Global storage instance
storage = S3Storage() 