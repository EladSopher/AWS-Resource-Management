# AWS Resource Management CLI Tool

This CLI tool allows users to manage AWS resources (EC2, S3, Route 53) using Pulumi and boto3.  
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
Ensure you have **Pulumi** and **AWS CLI** installed.

- **Pulumi:**  
  ```bash
  winget install pulumi # For Windows
  curl -fsSL https://get.pulumi.com | sh # For Ububtu/Linux
  brew install pulumi/tap/pulumi # For macOS
  ```

- **AWS CLI:**  
  ```bash
  https://awscli.amazonaws.com/AWSCLIV2.msi # For Windows
  sudo apt install awscli  # For Ubuntu/Linux
  brew install awscli       # For macOS
  ```

- **Set Up AWS Credentials:**  
  ```bash
  aws configure
  ```

---

## 🖥️ Using the CLI

Run commands using:  
```bash
python cli.py COMMAND [OPTIONS]
```

### Example Commands

- **Create an EC2 instance:**
  ```bash
  python cli.py create-instances --type t2.micro --os ubuntu --count 1
  ```

- **Start an EC2 instance:**
  ```bash
  python cli.py manage-instances --action start --instance-id i-0abcd1234efgh5678
  ```

- **Create an S3 bucket:**
  ```bash
  python cli.py create-bucket
  ```

- **Upload a file to an S3 bucket:**
  ```bash
  python cli.py upload-file-to-bucket --bucket-name MyBucket-1 --file-path ./file.txt
  ```

---

## 🖥️ Using Jenkins UI

### 🔹 **Step 1: Import the Jenkins Job**  

#### Method 1: Using `config.xml` (Recommended)

1. Locate the `config.xml` file inside the Jenkins job directory:  
   ```
   JENKINS_HOME/jobs/YOUR_JOB_NAME/config.xml
   ```
2. Copy this file and share it with the user who wants to use the Jenkins pipeline.
3. On the target Jenkins instance:
   - Create a new folder inside:
     ```
     JENKINS_HOME/jobs/New_Job_Name/
     ```
   - Place the `config.xml` inside this folder.
   - Restart Jenkins:
     ```bash
     systemctl restart jenkins
     ```

#### Method 2: Using Jenkins CLI

If the user has Jenkins CLI access, they can run:  
```bash
java -jar jenkins-cli.jar -s http://your-jenkins-url create-job NEW_JOB_NAME < config.xml
```

### 🔹 **Step 2: Run the Job via Jenkins UI**

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

