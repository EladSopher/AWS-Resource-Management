import boto3
import pulumi_aws as aws
import os


def is_cli_managed_bucket(bucket_name: str) -> bool:
    """
    Checks if the given S3 bucket has the "Managed: CLI Managed" tag.

    :param bucket_name: Name of the S3 bucket.
    :return: True if the bucket is CLI-Managed, False otherwise.
    """
    s3_client = boto3.client("s3")

    try:
        # Get bucket tags
        response = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}
        return tags.get("Managed") == "CLI Managed"

    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchTagSet":
            print(f"Warning: Bucket {bucket_name} has no tags.")
        else:
            print(f"Error checking bucket tags: {e}")

    return False


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
