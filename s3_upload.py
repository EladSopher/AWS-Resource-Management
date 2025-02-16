import pulumi_aws as aws

def upload_files_to_bucket(bucket_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket, but only if the bucket was created via the CLI.

    :param bucket_name: Name of the S3 bucket.
    :param file_path: Path to the file to be uploaded.
    """
    # Fetch the bucket details
    bucket = aws.s3.get_bucket(name=bucket_name)

    # Check if the bucket has the correct tag
    if bucket.tags.get("Managed") != "CLI Managed":
        print(f"Error: Cannot upload. {bucket_name} is not a CLI-Managed bucket.")
        return

    # Upload the file
    s3_object = aws.s3.BucketObject(
        file_path.split("/")[-1],
        bucket=bucket_name,
        source=file_path,
    )

    print(f"File uploaded successfully to {bucket_name}")