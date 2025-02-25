import boto3
from pulumi.automation import Stack, LocalWorkspace

def destroy_resources():
    """
    Destroys all CLI-managed AWS resources (EC2 instances, S3 buckets, and Route 53 hosted zones).
    """

    def delete_retained_instances():
        """Finds and deletes CLI-managed EC2 instances retained due to `retain_on_delete=True`."""
        ec2_client = boto3.client("ec2")

        # Filter for instances tagged as "CLI Managed"
        filters = [{"Name": "tag:Managed", "Values": ["CLI Managed"]}]
        response = ec2_client.describe_instances(Filters=filters)

        # Extract instance IDs
        instance_ids = [
            instance["InstanceId"]
            for reservation in response["Reservations"]
            for instance in reservation["Instances"]
        ]

        # Terminate instances if any are found
        if instance_ids:
            print(f"Manually deleting retained instances: {instance_ids}")
            ec2_client.terminate_instances(InstanceIds=instance_ids)
            print("Retained instances successfully deleted.")
        else:
            print("No retained instances found.")

    def destroy_pulumi_stack(stack_name, project_name):
        """Destroys a specific Pulumi stack."""
        try:
            # Initialize Pulumi workspace
            workspace = LocalWorkspace(work_dir="../.venv")
            stack = Stack.select(stack_name, workspace)

            # Run Pulumi destroy command
            stack.destroy(on_output=print)
            print(f"Pulumi stack '{stack_name}' destroyed successfully.")
        except Exception as e:
            print(f"Error deleting Pulumi stack '{stack_name}': {e}")

    # Destroy EC2 stack and delete retained instances
    destroy_pulumi_stack("devec2", "AWS-Resource-Management")
    delete_retained_instances()

    # Destroy S3 stack and delete CLI-managed buckets
    def destroy_all_cli_buckets():
        """Deletes all CLI-managed S3 buckets."""
        s3 = boto3.client("s3")

        try:
            # List all S3 buckets
            response = s3.list_buckets()
            buckets = response.get("Buckets", [])

            cli_managed_buckets = []

            for bucket in buckets:
                bucket_name = bucket["Name"]
                try:
                    # Check bucket tags to determine if it's CLI-managed
                    bucket_tagging = s3.get_bucket_tagging(Bucket=bucket_name)
                    tags = {tag["Key"]: tag["Value"] for tag in bucket_tagging["TagSet"]}

                    if tags.get("Managed") == "CLI Managed":
                        cli_managed_buckets.append(bucket_name)
                except s3.exceptions.ClientError as e:
                    # Handle buckets without tags or already deleted buckets
                    if e.response["Error"]["Code"] in ["NoSuchTagSet", "NoSuchBucket"]:
                        continue  # Skip non-CLI managed or deleted buckets

            if not cli_managed_buckets:
                print("No CLI-managed buckets found.")
                return

            for bucket_name in cli_managed_buckets:
                print(f"Deleting bucket: {bucket_name}")

                # Empty the bucket before deletion
                paginator = s3.get_paginator("list_objects_v2")
                for page in paginator.paginate(Bucket=bucket_name):
                    if "Contents" in page:
                        objects = [{"Key": obj["Key"]} for obj in page["Contents"]]
                        s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})
                        print(f"Emptied {len(objects)} objects from {bucket_name}.")

                # Delete the empty bucket
                s3.delete_bucket(Bucket=bucket_name)
                print(f"Bucket {bucket_name} deleted successfully.")

        except Exception as e:
            print(f"Error: {e}")

    # Destroy all CLI-managed S3 buckets
    destroy_all_cli_buckets()
    destroy_pulumi_stack("devs3", "AWS-Resource-Management")

    def destroy_route53_resources():
        """Deletes all CLI-managed Route 53 hosted zones."""
        client = boto3.client("route53")

        try:
            # List all hosted zones
            response = client.list_hosted_zones()
            cli_managed_zones = []

            for zone in response["HostedZones"]:
                zone_id = zone["Id"].split("/")[-1]

                # Fetch tags for each hosted zone
                tag_response = client.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
                tags = {tag["Key"]: tag["Value"] for tag in tag_response["ResourceTagSet"]["Tags"]}

                if tags.get("Managed") == "CLI Managed":
                    cli_managed_zones.append((zone_id, zone["Name"]))

            if not cli_managed_zones:
                print("No CLI-managed hosted zones found.")
                return

            for zone_id, zone_name in cli_managed_zones:
                print(f"Deleting hosted zone: {zone_name}")

                # List and delete all DNS records except NS and SOA (required by AWS)
                record_sets = client.list_resource_record_sets(HostedZoneId=zone_id)
                for record in record_sets["ResourceRecordSets"]:
                    if record["Type"] not in ["NS", "SOA"]:
                        client.change_resource_record_sets(
                            HostedZoneId=zone_id,
                            ChangeBatch={
                                "Changes": [
                                    {"Action": "DELETE", "ResourceRecordSet": record}
                                ]
                            },
                        )
                        print(f"Deleted record: {record['Name']} ({record['Type']})")

                # Delete the hosted zone
                client.delete_hosted_zone(Id=zone_id)
                print(f"Hosted zone '{zone_name}' deleted successfully.")

        except Exception as e:
            print(f"Error deleting Route 53 hosted zones: {e}")

    # Destroy all CLI-managed Route 53 hosted zones
    destroy_route53_resources()
    destroy_pulumi_stack("dev53", "AWS-Resource-Management")