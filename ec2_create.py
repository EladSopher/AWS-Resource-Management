import pulumi
import pulumi_aws as aws
import pulumi.automation as auto  # ✅ Import Automation API
from helpers import get_latest_ami

def pulumi_program(instance_type, os_type, count):
    """Define Pulumi infrastructure for creating EC2 instances."""
    arch = "x86_64" if instance_type == "t3.nano" else "arm64"
    ami_id = get_latest_ami(os_type, arch)

    instances = []
    for i in range(count):
        instance = aws.ec2.Instance(f"instance-{i+1}",
                                    instance_type=instance_type,
                                    ami=ami_id,
                                    tags={
                                        "Name": f"elad-sopher-MyInstance-{i+1}", #change per owner
                                        "Owner": "eladsopher" #change per owner
                                    })
        instances.append(instance)

    pulumi.export("instance_ids", [inst.id for inst in instances])

def create_instance(instance_type, os_type, count):
    """Run Pulumi Automation API to create EC2 instances."""
    project_name = "aws-ec2-management"
    stack_name = "dev"

    # ✅ Set up the Pulumi Stack using the Automation API
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: pulumi_program(instance_type, os_type, count),
    )

    print("Installing dependencies...")
    stack.workspace.install_plugin("aws", "v5")

    print("Setting AWS region...")
    stack.set_config("aws:region", auto.ConfigValue("us-east-1"))

    print("Running `pulumi up`...")
    stack.up(on_output=print)  # ✅ Executes `pulumi up`
