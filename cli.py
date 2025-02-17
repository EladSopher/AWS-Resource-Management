import argparse
from ec2_create import create_instance
from ec2_destroy import destroy_instance
from ec2_list import list_instances
from ec2_manage import start_instance, stop_instance
from s3_create import create_bucket
from s3_upload import upload_files_to_bucket
from s3_list import list_buckets
from s3_destroy import destroy_all_cli_buckets

def main():
    """Main function to handle CLI commands."""
    parser = argparse.ArgumentParser(description="AWS Resource Management CLI")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # EC2 Related Commands
    # Subcommand for creating EC2 instances
    create_instance_parser = subparsers.add_parser("create-instances", help="Create an EC2 instance")
    create_instance_parser.add_argument("--type", choices=["t3.nano", "t4g.nano"], required=True,
                                        help="EC2 instance type")
    create_instance_parser.add_argument("--os", choices=["amazon-linux", "ubuntu"], required=True,
                                        help="OS for the AMI")
    create_instance_parser.add_argument("--count", type=int, default=1,
                                        help="Number of instances to create (max 2)")

    # Subcommand for terminating EC2 instances
    # destroy_instance_parser = subparsers.add_parser("destroy-instance", help="Destroy an EC2 instance")
    subparsers.add_parser("destroy-instances", help="Destroy an EC2 instance")
    # destroy_instance_parser.add_argument("instance_id",nargs="+", help="ID of the EC2 instance to destroy")

    # Subcommand for managing instances
    manage_instance_parser = subparsers.add_parser("manage-instances",
                                                   help="Manage a CLI-Managed EC2 instance (start/stop)")
    manage_instance_subparsers = manage_instance_parser.add_subparsers(dest="action", required=True)
    start_instance_parser = manage_instance_subparsers.add_parser("start", help="Start a ClI managed EC2 instance")
    start_instance_parser.add_argument("instance_id", help="ID of the instance to start")
    stop_instance_parser = manage_instance_subparsers.add_parser("stop", help="Stop a CLI managed EC2 instance")
    stop_instance_parser.add_argument("instance_id", help="ID of the instance to stop")

    # Subcommand for listing instances
    # list_parser = subparsers.add_parser("list-instances", help="List EC2 instances created via the CLI")
    subparsers.add_parser("list-instances", help="List EC2 instances created via the CLI")



    # S3 Bucket Related Commands
    # Create Bucket Command
    create_bucket_parser = subparsers.add_parser("create-bucket", help="Create a S3 Bucket")
    create_bucket_parser.add_argument("--access", choices=["private", "public"], required=True,
                                      help="Bucket access type")

    # Upload File Command
    upload_file_parser = subparsers.add_parser("upload-file-to-bucket", help="Upload a file to a S3 Bucket")
    upload_file_parser.add_argument("bucket_name", help="Name of the S3 Bucket")
    upload_file_parser.add_argument("file_path", help="Path to the file to upload")

    # List Buckets Command
    subparsers.add_parser("list-buckets", help="List all CLI-Managed S3 Buckets")

    # Destroy all CLI-Managed S3 Buckets Command
    subparsers.add_parser("destroy-buckets", help="Delete all CLI-Managed S3 Buckets and destroy Pulumi stack")

    # Parse CLI arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == "create-instances":
        create_instance(args.type, args.os, args.count)
    elif args.command == "destroy-instances":
        destroy_instance()
    elif args.command == "manage-instances":
        if args.action == "start":
            start_instance(args.instance_id)
        elif args.action == "stop":
            stop_instance(args.instance_id)
    elif args.command == "list-instances":
        list_instances()
    elif args.command == "create-bucket":
        create_bucket(args.access)
    elif args.command == "upload-file-to-bucket":
        upload_files_to_bucket(args.bucket_name, args.file_path)
    elif args.command == "list-buckets":
        list_buckets()
    elif args.command == "destroy-buckets":
        destroy_all_cli_buckets()


if __name__ == "__main__":
    main()
