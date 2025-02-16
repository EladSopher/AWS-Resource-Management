import pulumi_aws as aws
import boto3
import re


def get_latest_ami(os_type, arch):
    """
    Retrieves the latest AMI ID for the given OS and architecture.

    Args:
    - os_type (str): OS type ('amazon-linux' or 'ubuntu')
    - architecture (str): CPU architecture ('x86_64' or 'arm64')

    Returns:
    - str: AMI ID of the latest image
    """
    if os_type == "amazon-linux":
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["amazon"],
            filters=[
                {"name": "architecture", "values": [arch]},
                {"name": "name", "values": ["amzn2-ami-hvm-*"]}
            ]
        )
    else:  # Ubuntu AMI
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["099720109477"], # Canonical (Ubuntu) official account ID
            filters=[
                {"name": "architecture", "values": [arch]},
                {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-*-server-*"]}
            ]
        )

    return ami.id

def get_next_bucket_name():
    # """
    # Determines the next available S3 bucket name in the format 'eladsopherBucket-{i+1}'.
    #
    # :return: The next available bucket name.
    # """
    # s3_client = boto3.client("s3")
    #
    # try:
    #     response = s3_client.list_buckets()
    #     existing_buckets = response.get("Buckets", [])
    # except Exception as e:
    #     print(f"Error fetching bucket list: {e}")
    #     return "elad-sopher-bucket-1"
    #
    # print("Existing Buckets:", [b["Name"] for b in response["Buckets"]])  # Debugging output
    #
    # highest_index = 0
    #
    # for bucket in existing_buckets:
    #     bucket_name = bucket["Name"]
    #     try:
    #         # Get the bucket tags
    #         tag_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
    #         tags = {tag["Key"]: tag["Value"] for tag in tag_response["TagSet"]}
    #
    #         # Check if the bucket list has the correct tags
    #         if tags.get("Owner") == "eladsopher" and tags.get("Managed") == "CLI Managed":
    #             if bucket_name.startswith("elad-sopher-bucket-"):
    #                 try:
    #                     index = int(bucket_name.split("-")[1])
    #                     highest_index = max(highest_index, index)
    #                 except ValueError:
    #                     continue
    #     except s3_client.exceptions.ClientError as e:
    #         # Ignore buckets that don't have tags
    #         if "NoSuchTagSet" in str(e):
    #             continue
    #         else:
    #             print(f"Error fetching tags for {bucket_name}: {e}")
    #
    # print("Highest Index Found:", highest_index)  # Debugging output
    # return f"elad-sopher-bucket-{highest_index + 1}"
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    # print("Existing Buckets:", [b["Name"] for b in response["Buckets"]])  # Debugging output

    highest_index = 0
    pattern = re.compile(r"elad-sopher-bucket-(\d+)$")  # Regex to extract the number

    for bucket in response["Buckets"]:
        name = bucket["Name"]
        match = pattern.match(name)

        if match:
            try:
                index = int(match.group(1))
                # print(f"Extracted index from '{name}': {index}")  # Debugging output
                highest_index = max(highest_index, index)
            except ValueError:
                # print(f"Skipping invalid bucket name: {name}")  # Debugging output
                continue

    # print("Highest Index Found:", highest_index)  # Debugging output
    return f"elad-sopher-bucket-{highest_index + 1}"