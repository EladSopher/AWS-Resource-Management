import pulumi
import pulumi_aws as aws
import pulumi.automation as auto
from pulumi import ResourceOptions
from scripts.helpers import get_latest_ami, get_cli_managed_instances  # Helper function to get AMI

def pulumi_program(instance_type, os_type, count, existing_instance_count, existing_instance_ids):
    """
    Pulumi program that provisions new EC2 instances while preserving existing ones.

    Args:
    - instance_type (str): The instance type (e.g., t3.nano or t4g.nano)
    - os_type (str): The OS for the instance (e.g., amazon-linux or ubuntu)
    - count (int): Number of new instances to create
    - existing_instance_count (int): Total CLI-managed instances count
    - existing_instance_ids (list): List of existing instance IDs
    """

    # Determine architecture based on instance type
    arch = "x86_64" if instance_type == "t3.nano" else "arm64"

    # Get the latest AMI based on the OS and architecture
    ami_id = get_latest_ami(os_type, arch)

    instances = []

    for i in range(count):
        # Ensure unique instance names by incrementing instance count
        instance_number = existing_instance_count + i + 1

        # Create EC2 instance with specified configurations
        instance = aws.ec2.Instance(f"instance-{instance_number}",
                                    instance_type=instance_type,
                                    ami=ami_id,
                                    subnet_id="subnet-0bc094de4c29eab3b",
                                    vpc_security_group_ids=["sg-02ec2894679b09083"],
                                    tags={
                                        "Name": f"elad-sopher-Instance-{instance_number}",
                                        "Owner": "eladsopher",
                                        "Managed": "CLI Managed"
                                    },
                                    opts=ResourceOptions(retain_on_delete=True)) # Prevent instance from being deleted on stack destroy
        instances.append(instance)

    # Export instance IDs (including existing ones) for tracking
    pulumi.export("instance_ids", existing_instance_ids + [inst.id for inst in instances])

def create_instance(instance_type, os_type, count):
    """
    Uses Pulumi Automation API to create EC2 instances with enforced rules:
    - Maximum 2 running CLI-Managed instances at a time.
    - Stopped instances do not count towards the limit.
    - If 1 instance is running, the user can only create 1 more.
    - If 2 instances are running, block creation.

    Args:
    - instance_type (str): EC2 instance type
    - os_type (str): OS for the instance
    - count (int): Number of instances to create (max 2 allowed)
    """

    # Fetch existing CLI-managed instances and count running ones
    existing_instance_ids, running_count = get_cli_managed_instances()

    # Enforce instance creation rules
    if running_count >= 2:
        print("Error: Cannot create new instances. There are already 2 running CLI-Managed instances.")
        return
    elif running_count == 1 and count > 1:
        print("Warning: You can only create 1 more instance since 1 is already running.")
        count = 1  # Limit count to 1 to prevent exceeding the max

    # Define Pulumi project and stack names
    project_name = "AWS-Resource-Management"
    stack_name = "dev"

    # Create or select the Pulumi stack
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: pulumi_program(instance_type, os_type, count, len(existing_instance_ids), existing_instance_ids),
    )

    print("Installing dependencies...")
    stack.workspace.install_plugin("aws", "v5") # Ensure AWS provider plugin is installed

    print("Setting AWS region...")
    stack.set_config("aws:region", auto.ConfigValue("us-east-1")) # Set deployment region

    print("Running `pulumi up`...")
    stack.up(on_output=print)  # Deploy instances via Pulumi

