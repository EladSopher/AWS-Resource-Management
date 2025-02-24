import pulumi_aws as aws
import boto3
import re

# ============================
# EC2 related functions
# ============================

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
        # Fetch the most recent Amazon Linux 2 AMI
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["amazon"], # Official Amazon AMI owner
            filters=[
                {"name": "architecture", "values": [arch]}, # Filter by architecture
                {"name": "name", "values": ["amzn2-ami-hvm-*"]} # Amazon Linux 2 pattern
            ]
        )
    else:  # Ubuntu AMI
        # Fetch the most recent Ubuntu AMI from the official Canonical account
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["099720109477"], # Canonical (Ubuntu) official AWS account ID
            filters=[
                {"name": "architecture", "values": [arch]}, # Filter by architecture
                {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-*-server-*"]} # Ubuntu AMI pattern
            ]
        )

    return ami.id # Return the AMI ID

def get_cli_managed_instances():
    """
    Fetches all CLI-managed EC2 instances (both running and stopped).

    Returns:
    - list: List of CLI-managed instance IDs.
    - int: Count of running CLI-managed instances.
    """
    ec2_client = boto3.client("ec2")

    # Filter instances that are tagged as 'CLI Managed'
    filters = [{"Name": "tag:Managed", "Values": ["CLI Managed"]}]
    response = ec2_client.describe_instances(Filters=filters)

    # Extract instances from the response
    instances = [
        instance for reservation in response["Reservations"] for instance in reservation["Instances"]
    ]

    # Count how many instances are currently running
    running_instances = [inst for inst in instances if inst["State"]["Name"] == "running"]

    return [inst["InstanceId"] for inst in instances], len(running_instances)

def is_cli_managed_instance(instance_id):
    """
    Checks if the given instance is managed by the CLI (has the 'CLI Managed' tag).

    Args:
    - instance_id (str): The ID of the EC2 instance to check.

    Returns:
    - bool: True if the instance is CLI-managed, False otherwise.
    """

    ec2 = boto3.client("ec2")

    try:
        # Get instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])

        # Check if the 'Managed' tag exists and is set to 'CLI Managed'
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                for tag in instance.get("Tags", []):  # Get instance tags safely
                    if tag["Key"] == "Managed" and tag["Value"] == "CLI Managed":
                        return True
    except Exception as e:
        print(f"Error checking instance {instance_id}: {e}")

    return False  # Default to False if the instance isn't found or not CLI-managed


# ============================
# S3 related functions
# ============================

def get_next_bucket_name():
    """
    Generates the next S3 bucket name in the format `elad-sopher-bucket-{i+1}`.

    Returns:
    - str: The next available bucket name.
    """
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    highest_index = 0
    pattern = re.compile(r"elad-sopher-bucket-(\d+)$")  # Regex pattern to extract index number

    # Iterate through existing buckets to find the highest index
    for bucket in response["Buckets"]:
        name = bucket["Name"]
        match = pattern.match(name)

        if match:
            try:
                index = int(match.group(1)) # Extract numerical index from bucket name
                highest_index = max(highest_index, index)
            except ValueError:
                continue # Skip if conversion fails (shouldn't happen with correct naming)

    return f"elad-sopher-bucket-{highest_index + 1}" # Generate the next bucket name

def is_cli_managed_bucket(bucket_name: str) -> bool:
    """
    Checks if the given S3 bucket has the "Managed: CLI Managed" tag.

    Args:
    - bucket_name (str): The name of the S3 bucket.

    Returns:
    - bool: True if the bucket is CLI-Managed, False otherwise.
    """
    s3_client = boto3.client("s3")

    try:
        # Get bucket tags
        response = s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}

        return tags.get("Managed") == "CLI Managed" # Check if 'Managed' tag is set correctly

    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchTagSet":
            print(f"Warning: Bucket {bucket_name} has no tags.") # Handle buckets with no tags
        else:
            print(f"Error checking bucket tags: {e}") # Handle other S3 client errors

    return False # Default to False if bucket isn't CLI-managed


# ============================
# Route 53 related functions
# ============================

def get_next_zone_name():
    """
    Determines the next available hosted zone name in the format `elad-sopher-zone-{i+1}.com`.

    Returns:
    - str: The next available hosted zone name.
    """
    client = boto3.client("route53")
    response = client.list_hosted_zones()

    # Extract all existing hosted zones that match the naming pattern
    existing_zones = [
        zone["Name"].rstrip(".") for zone in response["HostedZones"]
        if zone["Name"].startswith("elad-sopher-zone-") and zone["Name"].endswith(".com")
    ]

    # Increment index until a unique name is found
    index = 1
    while f"elad-sopher-zone-{index}.com" in existing_zones:
        index += 1

    return f"elad-sopher-zone-{index}.com" # Return the next available zone name