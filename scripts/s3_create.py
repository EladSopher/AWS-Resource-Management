import os
import pulumi
import pulumi_aws as aws
from pulumi_aws import s3
from pulumi import ResourceOptions
import pulumi.automation as auto
from scripts.helpers import get_next_bucket_name

def create_bucket(access_type: str):
    """
    Creates an S3 bucket with either private or public access.

    :param access_type: "private" or "public"
    """
    bucket_name = get_next_bucket_name()

    # Check if we're running in Jenkins or a non-interactive environment
    skip_confirmation = os.getenv("SKIP_CONFIRMATION", "false").lower() == "true"

    # Ask for confirmation if public access is selected
    if access_type == "public" and not skip_confirmation:
        confirm = input(f"Bucket {bucket_name} will be public. Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Bucket creation canceled.")
            return

    # Pulumi program to create the bucket
    def pulumi_program():
        # Create the bucket
        bucket = s3.BucketV2(
            bucket_name,
            bucket=bucket_name,
            tags={
                "Owner": "eladsopher",
                "Managed": "CLI Managed"
            },
            opts=ResourceOptions(retain_on_delete=True)  # Prevent Pulumi from deleting old buckets
        )

        # If the bucket should be public, update its public access block settings
        if access_type == "public":
            public_access_block = s3.BucketPublicAccessBlock(
                f"{bucket_name}-public-access-block",
                bucket=bucket.id,
                block_public_acls=False,  # Allow public ACLs
                block_public_policy=False,  # Allow public policies
                ignore_public_acls=False,
                restrict_public_buckets=False,
                opts=ResourceOptions(depends_on=[bucket])  # Ensure bucket exists before applying
            )

            public_read_policy = bucket.id.apply(lambda bucket_id: aws.iam.get_policy_document(
                statements=[{
                    "effect": "Allow",
                    "principals": [{"type": "AWS", "identifiers": ["*"]}],  # Public access
                    "actions": ["s3:GetObject"],
                    "resources": [f"arn:aws:s3:::{bucket_id}/*"],
                }]
            ))

            s3.BucketPolicy(
                f"{bucket_name}-policy",
                bucket=bucket.id,
                policy=public_read_policy.json,
                opts=ResourceOptions(depends_on=[bucket, public_access_block])  # Ensure order
            )

        pulumi.export("bucket_name", bucket.id)

    # Create or select the Pulumi stack
    stack_name = "dev"
    project_name = "AWS-Resource-Management"

    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=pulumi_program,
    )

    print("Running Pulumi to create the S3 Bucket...")
    try:
        up_res = stack.up(on_output=print)
        print("Pulumi output:", up_res.summary)
        print(f"S3 Bucket '{bucket_name}' was created.")
    except Exception as e:
        print("Error creating bucket:", e)
