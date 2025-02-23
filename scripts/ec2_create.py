import pulumi
import pulumi_aws as aws
import pulumi.automation as auto
from pulumi import ResourceOptions
from scripts.helpers import get_latest_ami, get_cli_managed_instances  # Helper function to get AMI

def pulumi_program(instance_type, os_type, count, existing_instance_count, existing_instance_ids):
    """
    Pulumi program that provisions new EC2 instances while preserving existing ones.

    Args:
    - instance_type (str): The instance type (t3.nano or t4g.nano)
    - os_type (str): The OS for the instance (amazon-linux or ubuntu)
    - count (int): Number of instances to create
    - existing_instance_count (int): Total CLI-managed instances count
    - existing_instance_ids (list): List of existing instance IDs
    """
    arch = "x86_64" if instance_type == "t3.nano" else "arm64"
    ami_id = get_latest_ami(os_type, arch)

    instances = []

    for i in range(count):
        instance_number = existing_instance_count + i + 1  # Ensure unique instance names
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
                                    opts=ResourceOptions(retain_on_delete=True))
        instances.append(instance)

    pulumi.export("instance_ids", existing_instance_ids + [inst.id for inst in instances])

def create_instance(instance_type, os_type, count):
    """
    Uses Pulumi Automation API to create EC2 instances with rules:
    - Max 2 running CLI-Managed instances.
    - Stopped instances do not count against the limit.
    - If 1 instance is running, user can only create 1 more.
    - If 2 instances are running, block creation.

    Args:
    - instance_type (str): EC2 instance type
    - os_type (str): OS for the instance
    - count (int): Number of instances to create (max 2)
    """
    existing_instance_ids, running_count = get_cli_managed_instances()

    if running_count >= 2:
        print("Error: Cannot create new instances. There are already 2 running CLI-Managed instances.")
        return
    elif running_count == 1 and count > 1:
        print("Warning: You can only create 1 more instance since 1 is already running.")
        count = 1  # Adjust count so only 1 instance is created

    project_name = "AWS-Resource-Management"
    stack_name = "EC2Dev"

    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: pulumi_program(instance_type, os_type, count, len(existing_instance_ids), existing_instance_ids),
    )

    print("Installing dependencies...")
    stack.workspace.install_plugin("aws", "v5")

    print("Setting AWS region...")
    stack.set_config("aws:region", auto.ConfigValue("us-east-1"))

    print("Running `pulumi up`...")
    stack.up(on_output=print)  # Deploy instances

