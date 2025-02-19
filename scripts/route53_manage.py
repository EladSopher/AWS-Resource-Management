import boto3

def get_cli_managed_zone(zone_name):
    """
    Checks if the given hosted zone is managed by the CLI (has the "CLI Managed" tag) and returns its ID.
    """
    client = boto3.client("route53")
    response = client.list_hosted_zones()

    for zone in response["HostedZones"]:
        if zone["Name"].rstrip(".") == zone_name:
            zone_id = zone["Id"].split("/")[-1]

            # Get the tags for the zone
            tag_response = client.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
            tags = {tag["Key"]: tag["Value"] for tag in tag_response["ResourceTagSet"]["Tags"]}

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
    """
    client = boto3.client("route53")
    zone_id = get_cli_managed_zone(zone_name)

    if not zone_id:
        raise ValueError("Cannot modify records in a non-CLI-managed zone.")

    try:
        if action in ["CREATE", "UPDATE"]:
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    "Changes": [
                        {
                            "Action": "UPSERT",  # Works for both CREATE and UPDATE
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
            print(f"DNS Record '{record_name}' {action.lower()}d successfully.")
            print("Change Info:", response["ChangeInfo"])

        elif action == "DELETE":
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
        print(f"Error managing DNS record: {e}")
