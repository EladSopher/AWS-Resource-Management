import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import customtkinter

# Function to show a "Running..." pop-up
def show_running_popup():
    running_popup = tk.Toplevel(root)
    running_popup.title("Running...")
    running_popup.geometry("200x100")
    running_popup.resizable(False, False)
    tk.Label(running_popup, text="Processing...", font=("Arial", 12)).pack(expand=True)
    root.update()  # Update UI
    return running_popup


# Function to run CLI commands in a separate thread
def run_cli_command(command):
    running_popup = show_running_popup()

    def execute():
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            messagebox.showinfo("Output", result.stdout)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            running_popup.destroy()  # Close popup when done

    threading.Thread(target=execute).start()  # Run in a separate thread

# Initialize Tkinter window
root = customtkinter.CTk()
root.title("AWS CLI Management Tool")
root.geometry("750x800")
root.configure(bg="#1e1e2e")

# Section Styles
frame_bg = "#282a36"
button_bg = "#44475a"
text_fg = "#f8f8f2"

# EC2 instance creation function
def create_instance():
    instance_type = instance_type_var.get()
    os_type = os_var.get()
    count = instance_count_var.get()

    if count not in ["1", "2"]:  # Ensure valid count
        messagebox.showerror("Error", "Instance count must be 1 or 2.")
        return

    run_cli_command(["python", "cli.py", "create-instances", instance_type, os_type, "--count", count])


# Start/Stop EC2 Instance
def start_instance():
    instance_id = instance_entry.get()
    run_cli_command(["python", "cli.py", "manage-instances", "start", instance_id])


def stop_instance():
    instance_id = instance_entry.get()
    run_cli_command(["python", "cli.py", "manage-instances", "stop", instance_id])


def list_instances():
    run_cli_command(["python", "cli.py", "list-instances"])


# S3 Bucket Functions
def create_bucket():
    access_type = bucket_access_var.get()
    run_cli_command(["python", "cli.py", "create-bucket", access_type])


def list_buckets():
    run_cli_command(["python", "cli.py", "list-buckets"])


def upload_file_to_bucket():
    bucket_name = bucket_name_entry.get()
    file_path = file_path_entry.get()
    run_cli_command(["python", "cli.py", "upload-file-to-bucket", bucket_name, file_path])


# Route 53 Functions
def create_hosted_zone():
    run_cli_command(["python", "cli.py", "create-hosted-zone"])


def manage_dns_record():
    zone_name = dns_zone_entry.get()
    record_name = dns_record_name_entry.get()
    record_type = dns_record_type_var.get()
    record_value = dns_record_value_entry.get()
    action = dns_record_action_var.get()

    run_cli_command(["python", "cli.py", "manage-record", zone_name, record_name, record_type, record_value, action])


# Destroy All Resources
def destroy_resources():
    run_cli_command(["python", "cli.py", "destroy-resources"])


# Create a scrollable frame inside the root window
main_frame = customtkinter.CTkScrollableFrame(root)
main_frame.pack(padx=20, pady=40, fill="both", expand=True)

# EC2 Management Frame
ec2_frame = customtkinter.CTkFrame(main_frame)
ec2_frame.pack(pady=10, fill="x")

tk.Label(ec2_frame, text="EC2 Management", font=("Arial", 16, "bold"), fg=text_fg, bg=frame_bg).pack()

# EC2 Instance Creation
create_instance_frame = customtkinter.CTkFrame(main_frame)
create_instance_frame.pack(pady=10, fill="x")

tk.Label(create_instance_frame, text="Create EC2 Instance", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()
tk.Label(create_instance_frame, text="Instance Type:", fg=text_fg, bg=frame_bg).pack()

instance_type_var = tk.StringVar(value="-")
tk.OptionMenu(create_instance_frame, instance_type_var, "t3.nano", "t4g.nano").pack()

tk.Label(create_instance_frame, text="Instance OS:", fg=text_fg, bg=frame_bg).pack()
os_var = tk.StringVar(value="-")
tk.OptionMenu(create_instance_frame, os_var, "ubuntu", "amazon-linux").pack()

tk.Label(create_instance_frame, text="Amount (1 or 2):", fg=text_fg, bg=frame_bg).pack()
instance_count_var = tk.StringVar(value="-")
tk.OptionMenu(create_instance_frame, instance_count_var, "1", "2").pack()

tk.Button(create_instance_frame, text="Create Instance", command=create_instance, bg=button_bg, fg=text_fg).pack(pady=5)

# EC2 instance start/stop
manage_instance_frame = customtkinter.CTkFrame(main_frame)
manage_instance_frame.pack(pady=10, fill="x")

tk.Label(manage_instance_frame, text="Manage EC2 Instance", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Label(manage_instance_frame, text="Instance ID:", fg=text_fg, bg=frame_bg).pack()
instance_entry = tk.Entry(manage_instance_frame)
instance_entry.pack()

tk.Button(manage_instance_frame, text="Start Instance", command=start_instance, bg=button_bg, fg=text_fg).pack(pady=2)
tk.Button(manage_instance_frame, text="Stop Instance", command=stop_instance, bg=button_bg, fg=text_fg).pack(pady=2)

# EC2 instance list
list_instance_frame = customtkinter.CTkFrame(main_frame)
list_instance_frame.pack(pady=10, fill="x")

tk.Label(list_instance_frame, text="List EC2 Instances", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Button(list_instance_frame, text="List Instances", command=list_instances, bg=button_bg, fg=text_fg).pack(pady=2)

# S3 Management Frame
s3_frame = customtkinter.CTkFrame(main_frame)
s3_frame.pack(pady=10, fill="x")

tk.Label(s3_frame, text="S3 Management", font=("Arial", 16, "bold"), fg=text_fg, bg=frame_bg).pack()

# S3 bucket create
create_bucket_frame = customtkinter.CTkFrame(main_frame)
create_bucket_frame.pack(pady=10, fill="x")

tk.Label(create_bucket_frame, text="Create S3 Bucket", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

bucket_access_var = tk.StringVar(value="-")
tk.Label(create_bucket_frame, text="S3 Bucket Access:", fg=text_fg, bg=frame_bg).pack()
tk.OptionMenu(create_bucket_frame, bucket_access_var, "private", "public").pack()

tk.Button(create_bucket_frame, text="Create Bucket", command=create_bucket, bg=button_bg, fg=text_fg).pack(pady=2)

# Upload file to S3 bucket
file_upload_frame = customtkinter.CTkFrame(main_frame)
file_upload_frame.pack(pady=10, fill="x")

tk.Label(file_upload_frame, text="Upload File to S3 Bucket", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Label(file_upload_frame, text="Bucket Name:", fg=text_fg, bg=frame_bg).pack()
bucket_name_entry = tk.Entry(file_upload_frame)
bucket_name_entry.pack()

tk.Label(file_upload_frame, text="File Path:", fg=text_fg, bg=frame_bg).pack()
file_path_entry = tk.Entry(file_upload_frame)
file_path_entry.pack()

tk.Button(file_upload_frame, text="Upload File", command=upload_file_to_bucket, bg=button_bg, fg=text_fg).pack(pady=2)

# List S3 buckets
list_bucket_frame = customtkinter.CTkFrame(main_frame)
list_bucket_frame.pack(pady=10, fill="x")

tk.Label(list_bucket_frame, text="List S3 Buckets", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Button(list_bucket_frame, text="List Buckets", command=list_buckets, bg=button_bg, fg=text_fg).pack(pady=2)

# Route 53 Management Frame
route53_frame = customtkinter.CTkFrame(main_frame)
route53_frame.pack(pady=10, fill="x")

tk.Label(route53_frame, text="Route 53 Management", font=("Arial", 16, "bold"), fg=text_fg, bg=frame_bg).pack()

# Hosted Zone Creation
create_zone_frame = customtkinter.CTkFrame(main_frame)
create_zone_frame.pack(pady=10, fill="x")

tk.Label(create_zone_frame, text="Create Hosted Zone", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Button(create_zone_frame, text="Create Hosted Zone", command=create_hosted_zone, bg=button_bg, fg=text_fg).pack(pady=2)

# DNS record management
dns_record_frame = customtkinter.CTkFrame(main_frame)
dns_record_frame.pack(pady=10, fill="x")

tk.Label(dns_record_frame, text="Manage Zone Record", font=("Arial", 12, "bold"), fg=text_fg, bg=frame_bg).pack()

tk.Label(dns_record_frame, text="Hosted Zone Name:", fg=text_fg, bg=frame_bg).pack()
dns_zone_entry = tk.Entry(dns_record_frame)
dns_zone_entry.pack()

tk.Label(dns_record_frame, text="Record Name:", fg=text_fg, bg=frame_bg).pack()
dns_record_name_entry = tk.Entry(dns_record_frame)
dns_record_name_entry.pack()

dns_record_type_var = tk.StringVar(value="-")
tk.Label(dns_record_frame, text="Record Type:", fg=text_fg, bg=frame_bg).pack()
tk.OptionMenu(dns_record_frame, dns_record_type_var, "A", "CNAME", "TXT", "MX").pack()

tk.Label(dns_record_frame, text="Record Value:", fg=text_fg, bg=frame_bg).pack()
dns_record_value_entry = tk.Entry(dns_record_frame)
dns_record_value_entry.pack()

dns_record_action_var = tk.StringVar(value="-")
tk.Label(dns_record_frame, text="Action:", fg=text_fg, bg=frame_bg).pack()
tk.OptionMenu(dns_record_frame, dns_record_action_var, "CREATE", "UPDATE", "DELETE").pack()

tk.Button(dns_record_frame, text="Manage DNS Record", command=manage_dns_record, bg=button_bg, fg=text_fg).pack(pady=2)

# Destroy Resources Section
destroy_frame = customtkinter.CTkFrame(main_frame)
destroy_frame.pack(pady=10, fill="x")

tk.Button(destroy_frame, text="Destroy All Resources", command=destroy_resources, bg="red", fg="white").pack()

# Run the UI
root.mainloop()
