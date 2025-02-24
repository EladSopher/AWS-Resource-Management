import boto3

def list_instances():
    """
    Lists all EC2 instances created via the CLI using specific tags.
    """
    ec2 = boto3.client("ec2")

    # Define the tag filters to only retrieve CLI-managed instances owned by "eladsopher"
    filters = [
        {"Name": "tag:Managed", "Values": ["CLI Managed"]},
        {"Name": "tag:Owner", "Values": ["eladsopher"]},
        {"Name": "instance-state-name", "Values": ["running", "stopped"]}, # Only include running/stopped instances
    ]

    try:
        response = ec2.describe_instances(Filters=filters)
        instances = []

        # Iterate through all instances returned by the AWS response
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                state = instance["State"]["Name"]
                public_ip = instance.get("PublicIpAddress", "N/A") # Handle instances without a public IP
                private_ip = instance.get("PrivateIpAddress", "N/A") # Handle instances without a private IP

                # Store instance details in a structured format
                instances.append({
                    "Instance ID": instance_id,
                    "Type": instance_type,
                    "State": state,
                    "Public IP": public_ip,
                    "Private IP": private_ip,
                })

        # Print the instance details if any are found
        if instances:
            print("\nList of Managed EC2 Instances:")
            for inst in instances:
                print(f"\nInstance ID: {inst['Instance ID']}")
                print(f"Type: {inst['Type']}")
                print(f"State: {inst['State']}")
                print(f"Public IP: {inst['Public IP']}")
                print(f"Private IP: {inst['Private IP']}")
                print("-" * 40) # Separator for better readability
        else:
            print("No managed instances found.")

    except Exception as e:
        print(f"Error retrieving instances: {e}") # Print error details if the API call fails
