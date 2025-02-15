import argparse
from ec2_create import create_instance
from ec2_destroy import destroy_instance

def main():
    """Main function to handle CLI commands."""
    parser = argparse.ArgumentParser(description="AWS Resource Management CLI")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

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
    destroy_instance_parser.add_argument("instance_id",nargs="+", help="ID of the EC2 instance to destroy")

    # Parse CLI arguments
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == "create-instance":
        create_instance(args.type, args.os, args.count)
    elif args.command == "destroy-instance":
        destroy_instance(args.instance_id)

if __name__ == "__main__":
    main()
