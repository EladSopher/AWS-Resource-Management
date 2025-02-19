import pulumi_aws as aws
import boto3
import re

# EC2 related functions
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

def get_cli_managed_instances():
    """
    Fetches all CLI-managed EC2 instances (both running and stopped).

    Returns:
    - list: List of CLI-managed instance IDs.
    - int: Count of running CLI-managed instances.
    """
    ec2_client = boto3.client("ec2")

    filters = [{"Name": "tag:Managed", "Values": ["CLI Managed"]}]
    response = ec2_client.describe_instances(Filters=filters)

    instances = [
        instance for reservation in response["Reservations"] for instance in reservation["Instances"]
    ]

    running_instances = [inst for inst in instances if inst["State"]["Name"] == "running"]
    return [inst["InstanceId"] for inst in instances], len(running_instances)

def is_cli_managed_instance(instance_id):
    """
    Checks if the given instance is managed by the CLI (has the 'CLI Managed' tag).

    :param instance_id: The ID of the EC2 instance to check.
    :return: True if the instance is CLI managed, False otherwise.
    """
    ec2 = boto3.client("ec2")

    response = ec2.describe_instances(InstanceIds=[instance_id])

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Managed" and tag["Value"] == "CLI Managed":
                    return True

    return False
# EC2 related functions


# S3 related functions
def get_next_bucket_name():
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    highest_index = 0
    pattern = re.compile(r"elad-sopher-bucket-(\d+)$")  # Regex to extract the number

    for bucket in response["Buckets"]:
        name = bucket["Name"]
        match = pattern.match(name)

        if match:
            try:
                index = int(match.group(1))
                highest_index = max(highest_index, index)
            except ValueError:
                continue

    return f"elad-sopher-bucket-{highest_index + 1}"

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
# S3 related functions


# Route53 related functions
def get_next_zone_name():
    """
    Determines the next available hosted zone name in the format `myzone-{i+1}.com`.
    """
    client = boto3.client("route53")
    response = client.list_hosted_zones()

    existing_zones = [
        zone["Name"].rstrip(".") for zone in response["HostedZones"]
        if zone["Name"].startswith("elad-sopher-zone-") and zone["Name"].endswith(".com")
    ]

    index = 1
    while f"elad-sopher-zone-{index}.com" in existing_zones:
        index += 1

    return f"elad-sopher-zone-{index}.com"
# Route53 related functions