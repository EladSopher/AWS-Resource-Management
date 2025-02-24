import pulumi
import pulumi_aws as aws
from pulumi.automation import create_or_select_stack
from scripts.helpers import get_next_zone_name

def pulumi_program():
    """
    Pulumi program to create a Route 53 hosted zone.
    """
    zone_name = get_next_zone_name()

    hosted_zone = aws.route53.Zone(
        "CLIManagedZone",
        name=zone_name,
        tags={"Managed": "CLI Managed", "Owner": "eladsopher"},
    )

    pulumi.export("zone_name", hosted_zone.name)

def create_hosted_zone():
    """
    Manages the Pulumi stack and creates a hosted zone.
    """
    project_name = "AWS-Resource-Management"
    stack_name = "dev"

    stack = create_or_select_stack(stack_name=stack_name, project_name=project_name, program=pulumi_program)

    print("Running Pulumi to create the Hosted Zone...")
    try:
        up_res = stack.up(on_output=print)
        print("Pulumi output:", up_res.summary)
        print(f"Hosted Zone '{up_res.outputs['zone_name'].value}' was created.")
    except Exception as e:
        print("Error creating hosted zone:", e)