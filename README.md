# 🚀 CLI Resource Management Tool

A Python-based CLI tool for managing AWS resources (EC2, S3, and Route 53) with DevOps compliance.  
This tool can be used **interactively** or **via Jenkins UI**.

---

## 📌 Table of Contents

- [Installation](#installation)
- [Usage (Interactive Mode)](#usage-interactive-mode)
- [Usage (Jenkins UI)](#usage-jenkins-ui)
- [Pipeline Setup in Jenkins](#pipeline-setup-in-jenkins)
- [Available Commands](#available-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Installation

### **Prerequisites**
- Python 3.8+ installed
- AWS CLI installed and configured (`aws configure`)
- Pulumi installed (`pip install pulumi`)
- Jenkins installed (for UI integration)

### **Installation Steps**

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/cli-resource-management.git
   cd cli-resource-management
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python cli.py --help
   ```

---

## 🖥️ Usage (Interactive Mode)

Run the CLI tool directly from the command line.

### **Example Commands**

- **Create EC2 instances:**
  ```bash
  python cli.py create-instances --os "Ubuntu" --type "t2.micro" --count 2
  ```

- **Start an EC2 instance:**
  ```bash
  python cli.py manage-instances --action start --instance-id i-1234567890abcdef
  ```

- **Upload a file to an S3 bucket:**
  ```bash
  python cli.py upload-file-to-bucket --bucket-name MyBucket-1 --file-path ./myfile.txt
  ```

For a full list of commands, see [Available Commands](#available-commands).

---

## 🌐 Usage (Jenkins UI)

This CLI tool is integrated with Jenkins for automation.

### **Running the Pipeline in Jenkins**

1. Open **Jenkins Dashboard** → Select **CLI-Resource-Management** Pipeline.
2. Click **"Build with Parameters"**.
3. Choose a command from the **COMMAND** dropdown.
4. Fill in the required fields based on the selected command.
5. Click **"Build"** to execute the pipeline.

#### **Example: Create an EC2 Instance**
- **COMMAND**: `create-instances`
- **OS**: `Ubuntu`
- **TYPE**: `t2.micro`
- **COUNT**: `1`
- Click **"Build"**.

---

## ⚙️ Pipeline Setup in Jenkins

To set up this pipeline on another Jenkins instance:

1. **Ensure Jenkins is installed** and AWS credentials are configured (`aws configure`).
2. **Create a new pipeline** in Jenkins:
   - Go to **Jenkins Dashboard** → **New Item** → **Pipeline**.
   - Name it **CLI-Resource-Management**.
   - Select **Pipeline** and click **OK**.
3. **Configure the pipeline**:
   - Under **Pipeline** section, select **Pipeline script from SCM**.
   - Choose **Git** and enter your repository URL.
   - Set the **Script Path** to `Jenkinsfile`.
   - Click **Save**.
4. **Define parameters** in Jenkins (if not auto-detected):
   - Add parameters **COMMAND, ACTION, INSTANCE_ID, OS, TYPE, COUNT, BUCKET_NAME, etc.**
5. **Run the pipeline** by clicking **Build with Parameters**.

---

## 📜 Available Commands

| Command                 | Description                             | Required Parameters                     |
|-------------------------|-----------------------------------------|-----------------------------------------|
| `create-instances`      | Create new EC2 instances               | `OS`, `TYPE`, `COUNT`                  |
| `manage-instances`      | Start or stop EC2 instances            | `ACTION`, `INSTANCE_ID`                 |
| `list-instances`        | List all EC2 instances                 | None                                    |
| `create-bucket`         | Create a new S3 bucket                 | None                                    |
| `upload-file-to-bucket` | Upload a file to an S3 bucket          | `BUCKET_NAME`, `FILE_PATH`              |
| `list-buckets`         | List all S3 buckets                     | None                                    |
| `create-hosted-zone`    | Create a new Route 53 hosted zone      | None                                    |
| `manage-record`         | Create, update, or delete DNS records  | `ACTION`, `ZONE_NAME`, `RECORD_NAME`, `RECORD_TYPE`, `RECORD_VALUE` |
| `destroy-resources`     | Delete AWS resources                   | None                                    |

---

## 🛠️ Troubleshooting

### **1. AWS Permissions Issues**
If you see **Access Denied**, ensure that the IAM user has the necessary permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:*",
    "s3:*",
    "route53:*"
  ],
  "Resource": "*"
}
```

Attach this policy to the IAM user running the CLI tool.

### **2. Jenkins Pipeline Fails**
- Check the **console output** for error messages.
- Ensure AWS credentials are configured in the Jenkins environment.
- Verify the repository URL and branch in Jenkins pipeline settings.

### **3. CLI Command Not Found**
- Ensure the repository is cloned and dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```
- Run the command with:
  ```bash
  python cli.py --help
  ```

---

## 🤝 Contributing

If you’d like to contribute, feel free to fork this repo, create a new branch, and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.
