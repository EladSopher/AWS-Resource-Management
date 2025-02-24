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

    Args:
    - access_type (str): "private" for a private bucket, "public" for a publicly accessible bucket.
    """

    bucket_name = get_next_bucket_name() # Generate a unique bucket name following the CLI convention

    # Check if we're running in Jenkins or a non-interactive environment
    skip_confirmation = os.getenv("SKIP_CONFIRMATION", "false").lower() == "true"

    # Ask for confirmation before creating a public bucket
    if access_type == "public" and not skip_confirmation:
        confirm = input(f"Bucket {bucket_name} will be public. Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Bucket creation canceled.")
            return

    # Pulumi program to create the S3 bucket
    def pulumi_program():
        """
        Defines the Pulumi resources for creating the S3 bucket.
        """

        # Create the S3 bucket with appropriate tags
        bucket = s3.BucketV2(
            bucket_name,
            bucket=bucket_name,
            tags={
                "Owner": "eladsopher",
                "Managed": "CLI Managed"
            },
            opts=ResourceOptions(retain_on_delete=True)  # Prevent Pulumi from deleting the bucket on destroy
        )

        ## Configure public access settings if required
        if access_type == "public":
            # Allow public access by modifying the bucket's public access settings
            public_access_block = s3.BucketPublicAccessBlock(
                f"{bucket_name}-public-access-block",
                bucket=bucket.id,
                block_public_acls=False,  # Allow public ACLs
                block_public_policy=False,  # Allow public policies
                ignore_public_acls=False,
                restrict_public_buckets=False,
                opts=ResourceOptions(depends_on=[bucket])  # Ensure bucket exists before applying settings
            )

            # Define an IAM policy to allow public read access to objects in the bucket
            public_read_policy = bucket.id.apply(lambda bucket_id: aws.iam.get_policy_document(
                statements=[{
                    "effect": "Allow",
                    "principals": [{"type": "AWS", "identifiers": ["*"]}],  # Allow access from any AWS principal (public)
                    "actions": ["s3:GetObject"], # Grant read access
                    "resources": [f"arn:aws:s3:::{bucket_id}/*"], # Apply to all objects in the bucket
                }]
            ))

            # Attach the public read policy to the bucket
            s3.BucketPolicy(
                f"{bucket_name}-policy",
                bucket=bucket.id,
                policy=public_read_policy.json,
                opts=ResourceOptions(depends_on=[bucket, public_access_block])  # Ensure dependencies are met
            )

        pulumi.export("bucket_name", bucket.id) # Export bucket name for reference

    # Create or select the Pulumi stack for managing the infrastructure
    stack_name = "dev"
    project_name = "AWS-Resource-Management"

    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=pulumi_program,
    )

    print("Running Pulumi to create the S3 Bucket...")
    try:
        up_res = stack.up(on_output=print) # Execute Pulumi to deploy resources
        print("Pulumi output:", up_res.summary)
        print(f"S3 Bucket '{bucket_name}' was created.") # Success message with the bucket name
    except Exception as e:
        print("Error creating bucket:", e) # Handle any errors during execution
