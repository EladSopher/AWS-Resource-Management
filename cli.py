import argparse
from scripts.ec2_create import create_instance
from scripts.ec2_list import list_instances
from scripts.ec2_manage import start_instance, stop_instance
from scripts.s3_create import create_bucket
from scripts.s3_upload import upload_files_to_bucket
from scripts.s3_list import list_buckets
from scripts.route53_create import create_hosted_zone
from scripts.route53_manage import manage_dns_record
from scripts.destroy_resources import destroy_resources

def main():
    """
    AWS Resource Management CLI

    This script provides a command-line interface to manage various AWS resources,
    including EC2 instances, S3 buckets, and Route 53 hosted zones. Each command
    is implemented as a subcommand, and the script uses argparse for argument parsing.

    The CLI supports the following commands:
    - EC2: Create, list, and manage (start/stop) EC2 instances.
    - S3: Create S3 buckets, upload files to buckets, and list buckets.
    - Route 53: Create hosted zones and manage DNS records.
    - Destroy: Destroy all CLI-managed AWS resources (EC2, S3, and Route 53).

    Args:
    - None

    Returns:
    - None
    """

    parser = argparse.ArgumentParser(description="AWS Resource Management CLI")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # EC2 Related Commands
    # Subcommand for creating EC2 instances
    create_instance_parser = subparsers.add_parser("create-instances", help="Create an EC2 instance")
    create_instance_parser.add_argument("type", choices=["t3.nano", "t4g.nano"], help="EC2 instance type")
    create_instance_parser.add_argument("os", choices=["amazon-linux", "ubuntu"], help="OS for the AMI")
    create_instance_parser.add_argument("--count", type=int, default=1,
                                        help="Number of instances to create (max 2)")

    # Subcommand for managing instances (start/stop)
    manage_instance_parser = subparsers.add_parser("manage-instances",
                                                   help="Manage a CLI-Managed EC2 instance (start/stop)")
    manage_instance_subparsers = manage_instance_parser.add_subparsers(dest="action", required=True)
    start_instance_parser = manage_instance_subparsers.add_parser("start",
                                                                  help="Start a ClI managed EC2 instance")
    start_instance_parser.add_argument("instance_id", help="ID of the instance to start")
    stop_instance_parser = manage_instance_subparsers.add_parser("stop", help="Stop a CLI managed EC2 instance")
    stop_instance_parser.add_argument("instance_id", help="ID of the instance to stop")

    # Subcommand for listing instances
    subparsers.add_parser("list-instances", help="List EC2 instances created via the CLI")



    # S3 Bucket Related Commands
    # Subcommand for creating S3 Bucket
    create_bucket_parser = subparsers.add_parser("create-bucket", help="Create a S3 Bucket")
    create_bucket_parser.add_argument("access", choices=["private", "public"], help="Bucket access type")

    # Subcommand for uploading file to S3 Bucket
    upload_file_parser = subparsers.add_parser("upload-file-to-bucket", help="Upload a file to a S3 Bucket")
    upload_file_parser.add_argument("bucket_name", help="Name of the S3 Bucket")
    upload_file_parser.add_argument("file_path", help="Path to the file to upload")

    # Subcommand for listing S3 Buckets
    subparsers.add_parser("list-buckets", help="List all CLI-Managed S3 Buckets")



    # Route 53 Related Commands
    # Subcommand for creating a Route 53 hosted zone
    subparsers.add_parser("create-hosted-zone", help="Create a Route 53 hosted zone")

    # Subcommand for managing DNS records in a hosted zone
    manage_record_parser = subparsers.add_parser("manage-record",
                                                 help="Manage DNS records in a CLI-managed hosted zone")
    manage_record_parser.add_argument("zone_name", help="Hosted zone name (must be CLI-managed)")
    manage_record_parser.add_argument("record_name", help="DNS record name")
    manage_record_parser.add_argument("record_type", choices=["A", "CNAME", "TXT", "MX"],
                                      help="DNS record type")
    manage_record_parser.add_argument("record_value", help="DNS record value")
    manage_record_parser.add_argument("action", choices=["CREATE", "UPDATE", "DELETE"],
                                      help="Action to perform")



    # Subcommand for destroying all resources
    subparsers.add_parser("destroy-resources", help="Destroy all CLI-managed AWS resources (EC2, S3 & Route53)")

    # Parse CLI arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == "create-instances":
        create_instance(args.type, args.os, args.count) # Create EC2 instance(s)
    elif args.command == "manage-instances":
        if args.action == "start":
            start_instance(args.instance_id) # Start the specified EC2 instance
        elif args.action == "stop":
            stop_instance(args.instance_id) # Stop the specified EC2 instance
    elif args.command == "list-instances":
        list_instances() # List EC2 instances
    elif args.command == "create-bucket":
        create_bucket(args.access) # Create an S3 bucket with specified access type
    elif args.command == "upload-file-to-bucket":
        upload_files_to_bucket(args.bucket_name, args.file_path) # Upload file to S3 bucket
    elif args.command == "list-buckets":
        list_buckets() # List CLI-managed S3 buckets
    elif args.command == "create-hosted-zone":
        create_hosted_zone() # Create a Route 53 hosted zone
    elif args.command == "manage-record":
        manage_dns_record(args.zone_name, args.record_name, args.record_type, args.record_value, args.action) # Manage DNS record
    elif args.command == "destroy-resources":
        destroy_resources() # Destroy all CLI-managed resources


if __name__ == "__main__":
    main()
