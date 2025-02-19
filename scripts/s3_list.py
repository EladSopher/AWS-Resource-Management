import boto3
import botocore.exceptions


def list_buckets():
    s3_client = boto3.client("s3")

    try:
        # Get all S3 buckets
        response = s3_client.list_buckets()
        all_buckets = response.get("Buckets", [])

        cli_managed_buckets = []

        for bucket in all_buckets:
            bucket_name = bucket["Name"]

            try:

                # Get bucket tags
                tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag["Key"]: tag["Value"] for tag in tagging.get("TagSet", [])}

                # Check if "Managed: CLI Managed" exists in tags
                if tags.get("Managed") == "CLI Managed":
                    cli_managed_buckets.append(bucket_name)

            except botocore.exceptions.ClientError as e:
                # Handle case where bucket has no tags
                if e.response["Error"]["Code"] == "NoSuchTagSet":
                    continue # Skip the bucket
                else:
                    print(f"Error retrieving tags for bucket {bucket_name}: {e}")

        if cli_managed_buckets:
            print("CLI Managed Buckets:")
            for bucket in cli_managed_buckets:
                print(f" - {bucket}")

        else:
            print("No CLI Managed buckets found.")

    except Exception as e:
        print("Error listing buckets:", e)