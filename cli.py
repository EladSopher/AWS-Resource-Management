import argparse
from ec2_create import create_instance

def main():
    parser = argparse.ArgumentParser(description="AWS Resource Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: create-instance
    create_instance_parser = subparsers.add_parser("create-instance", help="Create an EC2 instance")
    create_instance_parser.add_argument("--type", choices=["t3.nano", "t4g.nano"], required=True, help="EC2 instance type")
    create_instance_parser.add_argument("--os", choices=["amazon-linux", "ubuntu"], required=True, help="OS for the AMI")
    create_instance_parser.add_argument("--count", type=int, default=1, help="Number of instances to create (max 2)")

    args = parser.parse_args()

    if args.command == "create-instance":
        create_instance(args.type, args.os, args.count)

if __name__ == "__main__":
    main()
