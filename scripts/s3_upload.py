import boto3
import os
from scripts.helpers import is_cli_managed_bucket

def upload_files_to_bucket(bucket_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket, but only if the bucket was created via the CLI.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - file_path (str): Path to the file to be uploaded.

    Returns:
    - None
    """

    # Check if the file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Validate if the bucket is CLI-managed before uploading
    if not is_cli_managed_bucket(bucket_name):
        print(f"Error: Cannot upload. {bucket_name} is not a CLI-Managed bucket.")
        return

    # Initialize the S3 client
    s3_client = boto3.client("s3")

    try:
        # Upload the file to the specified S3 bucket
        s3_client.upload_file(file_path, bucket_name, os.path.basename(file_path))
        print(f"File '{file_path}' uploaded successfully to {bucket_name}.")

    except Exception as e:
        print(f"Error uploading file: {e}") # Handle upload errors
