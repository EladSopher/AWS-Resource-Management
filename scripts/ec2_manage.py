import boto3
from scripts.helpers import is_cli_managed_instance

def start_instance(instance_id):
    """
    Starts a specific EC2 instance if it is CLI managed.

    :param instance_id: The ID of the instance to start.
    """
    if not is_cli_managed_instance(instance_id):
        print(f"Error: Instance {instance_id} is not CLI managed or does not exist.")
        return

    ec2 = boto3.client("ec2")
    response = ec2.start_instances(InstanceIds=[instance_id])

    for instance in response["StartingInstances"]:
        print(f"Starting instance: {instance['InstanceId']} (Previous state: {instance['PreviousState']['Name']})")

def stop_instance(instance_id):
    """
    Stops a specific EC2 instance if it is CLI managed.

    :param instance_id: The ID of the instance to stop.
    """
    if not is_cli_managed_instance(instance_id):
        print(f"Error: Instance {instance_id} is not CLI managed or does not exist.")
        return

    ec2 = boto3.client("ec2")
    response = ec2.stop_instances(InstanceIds=[instance_id])

    for instance in response["StoppingInstances"]:
        print(f"Stopping instance: {instance['InstanceId']} (Previous state: {instance['PreviousState']['Name']})")