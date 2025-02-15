import pulumi
import pulumi_aws as aws
import pulumi.automation as auto  # Import Pulumi Automation API
from helpers import get_latest_ami # Helper function to get AMI

def pulumi_program(instance_type, os_type, count):
    """
    Pulumi program that provisions EC2 instances.

    Args:
    - instance_type (str): The instance type (t3.nano or t4g.nano)
    - os_type (str): The OS for the instance (amazon-linux or ubuntu)
    - count (int): Number of instances to create (max 2)
    """
    # Determine the architecture based on instance type
    arch = "x86_64" if instance_type == "t3.nano" else "arm64"

    # Get the latest AMI for the selected OS and architecture
    ami_id = get_latest_ami(os_type, arch)

    instances = [] # Store created instances
    for i in range(count):
        # Create an EC2 instance with predefined tags
        instance = aws.ec2.Instance(f"instance-{i+1}",
                                    instance_type=instance_type,
                                    ami=ami_id,
                                    tags={
                                        "Name": f"elad-sopher-MyInstance-{i+1}", #change per owner
                                        "Owner": "eladsopher" #change per owner
                                    })
        instances.append(instance)

    # Export instance IDs for tracking
    pulumi.export("instance_ids", [inst.id for inst in instances])

def create_instance(instance_type, os_type, count):
    """
    Uses Pulumi Automation API to create EC2 instances.

    Args:
    - instance_type (str): EC2 instance type
    - os_type (str): OS for the instance
    - count (int): Number of instances
    """
    project_name = "aws-ec2-management"
    stack_name = "dev"

    # Create or select a Pulumi stack
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: pulumi_program(instance_type, os_type, count),
    )

    print("Installing dependencies...")
    stack.workspace.install_plugin("aws", "v5") # Ensure AWS provider is installed

    print("Setting AWS region...")
    stack.set_config("aws:region", auto.ConfigValue("us-east-1")) # Set AWS region

    print("Running `pulumi up`...")
    stack.up(on_output=print)  # Run `pulumi up` to deploy EC2 instance(s)
