import pulumi_aws as aws


def get_latest_ami(os_type, arch):
    """
    Fetch the latest AMI ID for a given OS type and architecture.
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
            owners=["099720109477"],  # Canonical's AWS account ID
            filters=[
                {"name": "architecture", "values": [arch]},
                {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-*-server-*"]}
            ]
        )

    return ami.id
