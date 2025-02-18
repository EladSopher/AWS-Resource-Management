import boto3
import os
from helpers import is_cli_managed_bucket

def upload_files_to_bucket(bucket_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket, but only if the bucket was created via the CLI.

    :param bucket_name: Name of the S3 bucket.
    :param file_path: Path to the file to be uploaded.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Validate if the bucket is CLI-managed
    if not is_cli_managed_bucket(bucket_name):
        print(f"Error: Cannot upload. {bucket_name} is not a CLI-Managed bucket.")
        return

    # Upload file using boto3
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
        print(f"File '{file_path}' uploaded successfully to {bucket_name}.")

    except Exception as e:
        print(f"Error uploading file: {e}")
