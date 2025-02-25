import pulumi
import pulumi_aws as aws
from pulumi.automation import create_or_select_stack
from scripts.helpers import get_next_zone_name

def pulumi_program():
    """
    Pulumi program to create a Route 53 hosted zone.

    This function:
    - Retrieves the next available hosted zone name using `get_next_zone_name()`.
    - Creates a Route 53 hosted zone with the "CLI Managed" tag.
    - Exports the zone name for later reference.
    """

    zone_name = get_next_zone_name() # Generate the next unique hosted zone name

    # Create a new Route 53 hosted zone
    hosted_zone = aws.route53.Zone(
        "CLIManagedZone",
        name=zone_name,
        tags={"Managed": "CLI Managed", "Owner": "eladsopher"}, # Tags for tracking CLI-managed resources
    )

    pulumi.export("zone_name", hosted_zone.name) # Export the zone name for Pulumi output

def create_hosted_zone():
    """
    Manages the Pulumi stack and creates a Route 53 hosted zone.

    This function:
    - Selects or creates the Pulumi stack.
    - Runs `pulumi up` to deploy the hosted zone.
    - Displays the output of the operation.
    """

    project_name = "AWS-Resource-Management" # Define the Pulumi project name
    stack_name = "dev53" # Define the stack name

    # Select or create the Pulumi stack for managing Route 53
    stack = create_or_select_stack(stack_name=stack_name, project_name=project_name, program=pulumi_program)

    print("Running Pulumi to create the Hosted Zone...")
    try:
        # Execute Pulumi deployment
        up_res = stack.up(on_output=print)

        # Print deployment summary and the created hosted zone name
        print("Pulumi output:", up_res.summary)
        print(f"Hosted Zone '{up_res.outputs['zone_name'].value}' was created.")
    except Exception as e:
        print("Error creating hosted zone:", e) # Handle errors during deployment