from inspect import stack
import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2
from pulumi.automation import Stack, LocalWorkspace

def destroy_instance():#instance_ids):
    # """
    # Destroys one or more EC2 instances by their IDs.
    # """
    # project_name = "aws-ec2-management"
    # stack_name = "dev"
    #
    # # Load the Pulumi stack
    # stack = Stack.select(stack_name, LocalWorkspace(work_dir=".venv"))
    #
    # for instance_id in instance_ids:
    #     print(f"Destroying instance: {instance_id}")
    #
    #     try:
    #         ec2_instance = aws.ec2.Instance.get(instance_id, instance_id)
    #         ec2_instance.InstanceState("terminate_state",
    #                                    instance_id=instance_id,
    #                                    state="terminated")
    #         print(f"Successfully deleted instance {instance_id}")
    #     except Exception as e:
    #         print(f"Error deleting instance {instance_id}: {e}")
    #
    # print("Pulumi update to reflect deletions...")
    # stack.up(on_output=print)
    # def pulumi_program():
    #     instance = ec2.get_instance(instance_id=instance_ids)
    #     pulumi.ResourceOptions(delete_before_replace=True)
    #     return [instance]

    stack_name = "dev"
    project_name = "aws-ec2-management"

    workspace = LocalWorkspace(work_dir=".venv")
    try:
        stack = Stack.create_or_select(stack_name, project_name, workspace)
    except Exception:
        stack = Stack.select(stack_name, workspace)

    stack.destroy(on_output=print)  # Run `pulumi destroy` to remove the instance