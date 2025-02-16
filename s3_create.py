import pulumi
import pulumi_aws as aws
from pulumi_aws import s3
from pulumi import ResourceOptions
from pulumi.automation import create_or_select_stack
from helpers import get_next_bucket_name

def create_bucket(access_type: str):
    """
    Creates an S3 bucket with either private or public access.

    :param access_type: "private" or "public"
    """
    bucket_name = get_next_bucket_name()

    # Ask for confirmation if public access is selected
    if access_type == "public":
        confirm = input(f"Bucket {bucket_name} will be public. Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Bucket creation canceled.")
            return

    # Define ACL based on access type
    acl = "public-read" if access_type == "public" else "private"

    # Pulumi program to create the bucket
    def pulumi_program():
        # Create a new bucket with a unique URN by using its name
        bucket = s3.BucketV2(
            bucket_name,
            bucket=bucket_name,
            acl=acl,
            tags={
                "Owner": "eladsopher",
                "Managed": "CLI Managed"
            },
            opts = ResourceOptions(retain_on_delete=True)  # Prevent Pulumi from deleting old buckets
        )
        pulumi.export("bucket_name", bucket.id)

    # Create or select the Pulumi stack
    stack = create_or_select_stack(stack_name="dev", project_name="aws-s3-management", program=pulumi_program)

    print("Running Pulumi to create the S3 Bucket...")
    try:
        up_res = stack.up(on_output=print)
        print("Pulumi output:", up_res.summary)
        print(f"S3 Bucket '{bucket_name}' was created.")
    except Exception as e:
        print("Error creating bucket:", e)