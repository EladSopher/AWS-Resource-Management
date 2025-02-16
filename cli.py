import argparse
from ec2_create import create_instance
from ec2_destroy import destroy_instance
from ec2_list import list_instances
from s3_create import create_bucket
from s3_upload import upload_files_to_bucket
from s3_list import list_buckets

def main():
    """Main function to handle CLI commands."""
    parser = argparse.ArgumentParser(description="AWS Resource Management CLI")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # EC2 Related Commands
    # Subcommand for creating EC2 instances
    create_instance_parser = subparsers.add_parser("create-instance", help="Create an EC2 instance")
    create_instance_parser.add_argument("--type", choices=["t3.nano", "t4g.nano"], required=True,
                                        help="EC2 instance type")
    create_instance_parser.add_argument("--os", choices=["amazon-linux", "ubuntu"], required=True,
                                        help="OS for the AMI")
    create_instance_parser.add_argument("--count", type=int, default=1,
                                        help="Number of instances to create (max 2)")

    #Subcommand for terminating EC2 instances
    destroy_instance_parser = subparsers.add_parser("destroy-instance", help="Destroy an EC2 instance")
    # destroy_instance_parser.add_argument("instance_id",nargs="+", help="ID of the EC2 instance to destroy")

    # List instances command
    list_parser = subparsers.add_parser("list-instances", help="List EC2 instances created via the CLI")


    # S3 Bucket Related Commands
    # Create Bucket Command
    create_bucket_parser = subparsers.add_parser("create-bucket", help="Create a S3 Bucket")
    create_bucket_parser.add_argument("--access", choices=["private", "public"], required=True,
                                      help="Bucket access type")

    # Upload File Command
    upload_file_parser = subparsers.add_parser("upload-file", help="Upload a file to a S3 Bucket")
    upload_file_parser.add_argument("bucket_name", help="Name of the S3 Bucket")
    upload_file_parser.add_argument("file_path", help="Path to the file to upload")

    # List Buckets Command
    subparsers.add_parser("list-buckets", help="List all CLI-Managed S3 Buckets")

    # Parse CLI arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == "create-instance":
        create_instance(args.type, args.os, args.count)
    elif args.command == "destroy-instance":
        destroy_instance()#args.instance_id)
    elif args.command == "list-instances":
        list_instances()
    elif args.command == "create-bucket":
        create_bucket(args.access)
    elif args.command == "upload-file":
        upload_files_to_bucket(args.bucket_name, args.file_path)
    elif args.command == "list-buckets":
        list_buckets()

if __name__ == "__main__":
    main()
