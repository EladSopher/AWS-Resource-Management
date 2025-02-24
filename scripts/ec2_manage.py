import boto3
from scripts.helpers import is_cli_managed_instance

def start_instance(instance_id):
    """
    Starts a specific EC2 instance if it is CLI managed.

    :param instance_id: The ID of the instance to start.
    """

    # Verify that the instance is CLI-managed before starting it
    if not is_cli_managed_instance(instance_id):
        print(f"Error: Instance {instance_id} is not CLI managed or does not exist.")
        return

    ec2 = boto3.client("ec2")
    try:
        # Attempt to start the instance
        response = ec2.start_instances(InstanceIds=[instance_id])

        for instance in response["StartingInstances"]:
            print(f"Starting instance: {instance['InstanceId']} (Previous state: {instance['PreviousState']['Name']})")

    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}") # Handle any API errors


def stop_instance(instance_id):
    """
    Stops a specific EC2 instance if it is CLI managed.

    :param instance_id: The ID of the instance to stop.
    """

    # Verify that the instance is CLI-managed before stopping it
    if not is_cli_managed_instance(instance_id):
        print(f"Error: Instance {instance_id} is not CLI managed or does not exist.")
        return

    ec2 = boto3.client("ec2")
    try:
        # Attempt to stop the instance
        response = ec2.stop_instances(InstanceIds=[instance_id])

        for instance in response["StoppingInstances"]:
            print(f"Stopping instance: {instance['InstanceId']} (Previous state: {instance['PreviousState']['Name']})")

    except Exception as e:
        print(f"Error stopping instance {instance_id}: {e}")

