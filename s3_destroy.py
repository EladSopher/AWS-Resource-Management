import boto3
from pulumi.automation import Stack, LocalWorkspace

def destroy_all_cli_buckets():
    """
    Deletes all S3 buckets created via the CLI and removes all objects inside before deletion.
    """
    s3 = boto3.client("s3")

    try:
        # List all buckets
        response = s3.list_buckets()
        buckets = response.get("Buckets", [])

        cli_managed_buckets = []

        # Identify CLI-managed buckets
        for bucket in buckets:
            bucket_name = bucket["Name"]
            try:
                bucket_tagging = s3.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag["Key"]: tag["Value"] for tag in bucket_tagging["TagSet"]}

                if tags.get("Managed") == "CLI Managed":
                    cli_managed_buckets.append(bucket_name)
            except s3.exceptions.ClientError as e:
                if e.response["Error"]["Code"] in ["NoSuchTagSet", "NoSuchBucket"]:
                    continue  # Skip non-CLI managed or deleted buckets

        if not cli_managed_buckets:
            print("No CLI-managed buckets found.")
            return

        # Empty and delete CLI-managed buckets
        for bucket_name in cli_managed_buckets:
            print(f"Deleting bucket: {bucket_name}")

            # Empty the bucket
            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket_name):
                if "Contents" in page:
                    objects = [{"Key": obj["Key"]} for obj in page["Contents"]]
                    s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})
                    print(f"Emptied {len(objects)} objects from {bucket_name}.")

            # Delete the bucket
            s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} deleted successfully.")

    except Exception as e:
        print(f"Error: {e}")

    # Delete Pulumi stack after deleting all CLI-managed buckets
    destroy_pulumi_stack()

def destroy_pulumi_stack():
    """
    Deletes the Pulumi stack for S3 resources.
    """
    stack_name = "dev"
    project_name = "aws-s3-management"

    try:
        workspace = LocalWorkspace(work_dir=".venv")
        stack = Stack.select(stack_name, workspace)
        stack.destroy(on_output=print)
        print(f"Pulumi stack '{stack_name}' destroyed successfully.")
    except Exception as e:
        print(f"Error deleting Pulumi stack: {e}")
