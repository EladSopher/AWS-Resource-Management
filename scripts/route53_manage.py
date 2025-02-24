import boto3

def get_cli_managed_zone(zone_name):
    """
    Checks if the given hosted zone is managed by the CLI (has the "CLI Managed" tag) and returns its ID.

    Args:
    - zone_name (str): The name of the hosted zone to check.

    Returns:
    - str: The hosted zone ID if it is CLI-managed.
    - None: If the zone is not found or not CLI-managed.
    """

    client = boto3.client("route53")
    response = client.list_hosted_zones()

    # Iterate through all hosted zones to find the matching name
    for zone in response["HostedZones"]:
        if zone["Name"].rstrip(".") == zone_name: # Strip trailing dot from Route 53 zone names
            zone_id = zone["Id"].split("/")[-1] # Extract the actual zone ID

            # Fetch tags for the hosted zone
            tag_response = client.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
            tags = {tag["Key"]: tag["Value"] for tag in tag_response["ResourceTagSet"]["Tags"]}

            # Check if the zone has the "Managed: CLI Managed" tag
            if tags.get("Managed") == "CLI Managed":
                return zone_id
            else:
                print(f"Zone '{zone_name}' is not managed by the CLI.")
                return None

    print(f"Zone '{zone_name}' not found.")
    return None

def manage_dns_record(zone_name, record_name, record_type, record_value, action):
    """
    Manages DNS records in a CLI-managed hosted zone using Boto3.
    Supports CREATE, UPDATE, and DELETE actions.

    Args:
    - zone_name (str): The name of the hosted zone where the record is managed.
    - record_name (str): The DNS record name (e.g., "subdomain.example.com").
    - record_type (str): The DNS record type (e.g., "A", "CNAME").
    - record_value (str): The value for the DNS record (e.g., an IP address or domain).
    - action (str): The action to perform ("CREATE", "UPDATE", or "DELETE").

    Returns:
    - None
    """

    client = boto3.client("route53")
    zone_id = get_cli_managed_zone(zone_name) # Get the hosted zone ID if it is CLI-managed

    if not zone_id:
        raise ValueError("Cannot modify records in a non-CLI-managed zone.") # Prevent modifications in unmanaged zones

    try:
        if action in ["CREATE", "UPDATE"]:
            # Use UPSERT to handle both CREATE and UPDATE actions
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": record_name,
                                "Type": record_type,
                                "TTL": 300, # Time-to-live for DNS propagation
                                "ResourceRecords": [{"Value": record_value}],
                            },
                        }
                    ]
                },
            )
            print(f"DNS Record '{record_name}' {action.lower()}d successfully.")
            print("Change Info:", response["ChangeInfo"])

        elif action == "DELETE":
            # Delete the specified DNS record
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    "Changes": [
                        {
                            "Action": "DELETE",
                            "ResourceRecordSet": {
                                "Name": record_name,
                                "Type": record_type,
                                "TTL": 300,
                                "ResourceRecords": [{"Value": record_value}],
                            },
                        }
                    ]
                },
            )
            print(f"DNS Record '{record_name}' deleted successfully.")
            print("Change Info:", response["ChangeInfo"])

    except Exception as e:
        print(f"Error managing DNS record: {e}") # Handle errors gracefully
