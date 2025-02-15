import pulumi_aws as aws


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
