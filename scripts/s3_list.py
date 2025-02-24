import boto3
import botocore.exceptions


def list_buckets():
    """
    Lists all S3 buckets in the AWS account and filters those tagged as "CLI Managed".

    This function checks the tags of each bucket and identifies which ones are managed
    by the CLI based on the tag "Managed: CLI Managed". It then prints out the names
    of the CLI managed buckets.

    Args:
    - None

    Returns:
    - None
    """

    s3_client = boto3.client("s3") # Create an S3 client using boto3

    try:
        # Get all S3 buckets in the account
        response = s3_client.list_buckets()
        all_buckets = response.get("Buckets", []) # Retrieve the list of buckets

        cli_managed_buckets = [] # List to store CLI managed buckets

        # Iterate through each bucket
        for bucket in all_buckets:
            bucket_name = bucket["Name"] # Extract the bucket name

            try:
                # Get the tags for the current bucket
                tagging = s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag["Key"]: tag["Value"] for tag in tagging.get("TagSet", [])} # Create a dictionary of tags

                # Check if the "Managed" tag is set to "CLI Managed"
                if tags.get("Managed") == "CLI Managed":
                    cli_managed_buckets.append(bucket_name) # Add the bucket to the list of CLI managed buckets

            except botocore.exceptions.ClientError as e:
                # Handle error if bucket does not have tags or if there's another issue
                if e.response["Error"]["Code"] == "NoSuchTagSet":
                    continue # Skip the bucket if it has no tags
                else:
                    print(f"Error retrieving tags for bucket {bucket_name}: {e}") # Print error message if tags retrieval fails

        # If any CLI managed buckets were found, print them
        if cli_managed_buckets:
            print("CLI Managed Buckets:")
            for bucket in cli_managed_buckets:
                print(f" - {bucket}") # Print each CLI managed bucket name

        else:
            print("No CLI Managed buckets found.") # Print message if no CLI managed buckets were found

    except Exception as e:
        # Catch any other unexpected errors and print the error message
        print("Error listing buckets:", e)