# AWS Resource Management CLI Tool

This CLI tool allows users to manage AWS resources (EC2, S3, Route 53) using Pulumi and Boto3.  
Users can interact with it in two ways:  
- **Directly via the command line**
- **Through a Jenkins UI**

## 🚀 Features

- **EC2 Instance Management:** Create, list, start, and stop instances.
- **S3 Bucket Management:** Create, list, and upload files to buckets.
- **Route 53 DNS Management:** Create hosted zones and manage DNS records.
- **Jenkins UI Integration:** Execute CLI commands using a graphical interface.

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/EladSopher/AWS-Resource-Management.git
cd AWS-Resource-Management
```

### 2️⃣ Install Dependencies  
Ensure you have **Python** installed.

You can install the requirements by running the command:
  ```bash
  pip install -r requirements.txt
  ```

Or you can install them one by one:

- **Pulumi:**  
  ```bash
  winget install pulumi # For Windows
  curl -fsSL https://get.pulumi.com | sh # For Ububtu/Linux
  brew install pulumi/tap/pulumi # For macOS
  ```

  ```bash
  pulumi login
  ```

- **Boto3:**
  ```bash
  pip install boto3
  ```

- **AWS CLI:**  
  ```bash
  https://awscli.amazonaws.com/AWSCLIV2.msi # For Windows
  sudo apt install awscli  # For Ubuntu/Linux
  brew install awscli       # For macOS
  ```
  
- **Jenkins:**
  ```bash
  https://www.jenkins.io/download/#downloading-jenkins # For Windows

  # For Ubuntu
  sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
  echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
  sudo apt-get update
  sudo apt-get install jenkins
  sudo apt update
  sudo apt install fontconfig openjdk-17-jre
  
  brew install jenkins-lts # For macOS 

### 3️⃣ Set Up AWS Credentials
```bash
  aws configure
  AWS Access Key ID [None]: YOUR ACCESS KEY
  AWS Secret Access Key [None]: YOUR SECRET ACCESS KEY
  Default region name [None]: YOUR REGION
  Default output format [None]:
  ```

---

## 🖥️ Using the CLI

Run commands using:  
```bash
python cli.py COMMAND [OPTIONS]
python cli.py COMMAND -h
```

### Example Commands

- **Create an EC2 instance:**
  ```bash
  python cli.py create-instances [TYPE] [OS] --count
  python cli.py create-instances t3.nano ubuntu
  python cli.py create-instances t4g.nano amazon-linux --count 2
  ```

- **Manage an EC2 instance:**
  ```bash
  python cli.py manage-instances [ACTION] [INSTANCE_ID]
  python cli.py manage-instances start i-0abcd1234efgh5678
  python cli.py manage-instances stop i-0abcd1234efgh5678
  ```

- **List all EC2 instances:**
  ```bash
  python cli.py list-instances
  ```

- **Create an S3 bucket:**
  ```bash
  python cli.py create-bucket [ACCESS]
  python cli.py create-bucket private
  python cli.py create-bucket public
  ```

- **Upload a file to an S3 bucket:**
  ```bash
  python cli.py upload-file-to-bucket [BUCKET_NAME] [FILE_PATH]
  python cli.py upload-file-to-bucket MyBucket-1 ./file.txt
  ```

- **List all S3 buckets:**
  ```bash
  python cli.py upload-file-to-bucket [BUCKET_NAME] [FILE_PATH]
  python cli.py upload-file-to-bucket MyBucket-1 ./file.txt
  ```

- **Create a hosted zone:**
  ```bash
  python cli.py create-hosted-zone
  ```

- **Manage a hosted zone record:**
  ```bash
  python cli.py manage-record [ZONE_NAME] [RECORD_NAME] [RECORD_TYPE] [RECORD_VALUE] [ACTION]
  python cli.py manage-record zone-1.com test.zone-1.com A 192.168.1.1 CREATE
  python cli.py manage-record zone-1.com test.zone-1.com A 192.168.1.2 UPDATE
  python cli.py manage-record zone-1.com test.zone-1.com A 192.168.1.1 DELETE
  ```

- **Destroy all resources:**
  ```bash
  python cli.py destroy-resources
  ```

---

## 🖥️ Using Jenkins UI

### 🔹 **Step 1: Import the Jenkins Job**  

1. Copy the `config.xml` file from the Jenkins directory inside the repo.

2. Navigate to Jenkins location on your PC:
   - Create a new folder inside:
     ```
     JENKINS_HOME/jobs/New_Job_Name/
     ```
   - Place the `config.xml` inside this folder.
   - Restart Jenkins:
     ```bash
     .\jenkins.exe restart # For Windows
     systemctl restart jenkins # For ubuntu/linux
     brew services restart jenkins-lts # For macOS
     ```

### 🔹 **Step 2: Install all required plugins**

1.  Navigate to **Jenkins Dashboard > Manage Jenkins > Plugins**.
2.  Install 'AWS steps', 'AWS Credentials', 'GitHub', 'Git plugin', 'Pipeline'.
3.  Restart Jenkins.

### 🔹 **Step 3: Set up AWS Credentials**

1. Navigate to **Jenkins Dashboard > Manage Jenkins > Credentials**.
2. Click on **global** and then **Add Credentials**.
3. Under the 'ID' field, insert 'AWS creds' and add your access key and secret key.

### 🔹 **Step 4: Run the Job via Jenkins UI**

1. Navigate to **Jenkins Dashboard > Your Job**.
2. Click on **Build with Parameters**.
3. Choose a command (`create-instances`, `manage-instances`, etc.).
4. Fill in the required fields (only relevant fields are enabled based on the selection).
5. Click **Build** to execute the command.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Feel free to fork this repository and contribute improvements! Submit a PR when you're ready.

---

## 🆘 Need Help?

Open an issue on GitHub, or reach out via our **Discord Server**.

