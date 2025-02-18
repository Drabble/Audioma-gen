from pathlib import Path

import boto3
import os
from dotenv import load_dotenv

DATA_DIR_GENERATED = Path.cwd() / "generated"
bucket_name = "books"

# Load environment variables from .env file located five folders up
load_dotenv()

# S3 configuration
s3_client = boto3.client('s3',
                         endpoint_url=os.getenv('S3_API_URL'),
                         aws_access_key_id=os.getenv('S3_API_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('S3_API_ACCESS_KEY_SECRET'))

def upload_file_to_s3(file_name, bucket_name, key=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if key is None:
        key = os.path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket_name, key)
        print(f"File {file_name} uploaded to {bucket_name}/{key}")
        return True
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {str(e)}")
        return False

def try_upload_to_s3(filename: str, key: str):
    while True:
        mp3_uploaded = upload_file_to_s3(DATA_DIR_GENERATED / filename, bucket_name, key)
        if not mp3_uploaded:
            print(f"S3 file upload failed.")
            print(f"Press any button to try again")
            input()  # Waits for the user to press Enter or any other key
        else:
            return