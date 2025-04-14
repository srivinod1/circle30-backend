import os
import boto3
from botocore.exceptions import ClientError
import tempfile
import logging

logger = logging.getLogger(__name__)

class S3Storage:
    def __init__(self):
        try:
            logger.info("Initializing S3 client...")
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            region_name = os.getenv('AWS_REGION', 'us-east-1')
            
            logger.info(f"Using region: {region_name}")
            
            self.s3 = boto3.client('s3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
            self.bucket = 'circle30-ev-data'
            self.cache_dir = tempfile.gettempdir()
            logger.info(f"S3 client initialized successfully with bucket: {self.bucket}")
        except Exception as e:
            logger.error(f"Error initializing S3 client: {str(e)}")
            raise

    def get_file(self, key):
        """Get a file from S3, caching it locally if needed."""
        try:
            local_path = os.path.join(self.cache_dir, key)
            logger.info(f"Attempting to get file: {key}")
            
            # If file exists in cache and is less than 1 hour old, use it
            if os.path.exists(local_path):
                file_age = os.path.getmtime(local_path)
                if (os.path.getmtime(local_path) - file_age) < 3600:
                    logger.info(f"Using cached file: {local_path}")
                    return local_path

            # Download from S3
            logger.info(f"Downloading {key} from S3 to {local_path}")
            self.s3.download_file(self.bucket, key, local_path)
            logger.info(f"Successfully downloaded {key}")
            return local_path
        except ClientError as e:
            logger.error(f"Error downloading {key} from S3: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_file: {str(e)}")
            return None

# Global storage instance
storage = S3Storage() 