pipeline {
    agent any

    parameters {
	choice(name: 'COMMAND', choices: ['create-instances', 'manage-instances', 'list-instances', 'create-bucket', 'upload-file-to-bucket', 'list-buckets', 'create-hosted-zone', 'manage-record', 'destroy-resources'], description: 'Select the CLI command to run')

	choice(name: 'INSTANCE_TYPE', choices: ['t3.nano', 't4g.nano'], description: 'Select the Instance type')
        choice(name: 'INSTANCE_OS', choices: ['ubuntu', 'amazon-linux'], description: 'Select the OS')
        string(name: 'INSTANCE_COUNT', defaultValue: '1', description: 'Number of instances to create (only for create-instances)')
        
        string(name: 'INSTANCE_ID', defaultValue: '', description: 'Instance ID (only for manage-instances)')
        choice(name: 'INSTANCE_ACTION', choices: ['start', 'stop'], description: 'Action to perform on instance (only for manage-instances)')

        choice(name: 'BUCKET_ACCESS', choices: ['private', 'public'], description: 'Access type for S3 bucket (only for create-bucket)')
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'S3 bucket name (only for upload-file-to-bucket)')
        string(name: 'FILE_PATH', defaultValue: '', description: 'File path to upload (only for upload-file-to-bucket)')

        string(name: 'ZONE_NAME', defaultValue: '', description: 'DNS Zone Name (only for manage-record)')
        string(name: 'RECORD_NAME', defaultValue: '', description: 'DNS Record Name (only for manage-record)')
        choice(name: 'RECORD_TYPE', choices: ['A', 'CNAME', 'MX', 'TXT'], description: 'DNS Record Type (only for manage-record)')
        string(name: 'RECORD_VALUE', defaultValue: '', description: 'DNS Record Value (only for manage-record)')
        choice(name: 'RECORD_ACTION', choices: ['create', 'update', 'delete'], description: 'DNS Record Action (only for manage-record)')
    }

    environment {
        AWS_REGION = 'us-east-1'
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_PROFILE = 'default'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/EladSopher/AWS-Resource-Management.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install --upgrade pip' // Ensure pip is up to date
                bat 'pip install -r requirements.txt' // Install dependencies globally
            }
        }

        stage('Execute CLI Command') {
            steps {
                script {
                    def command = ""

                    switch (params.COMMAND) {
                        case 'create-instances':
                            command = "python cli.py create-instances --type ${params.INSTANCE_TYPE} --os ${params.INSTANCE_OS} --count ${params.INSTANCE_COUNT}"
                            break
                        case 'manage-instances':
                            command = "python cli.py manage-instances --action ${params.INSTANCE_ACTION} --instance-id ${params.INSTANCE_ID}"
                            break
                        case 'list-instances':
                            command = "python cli.py list-instances"
                            break
                        case 'create-bucket':
                            command = "python cli.py create-bucket --access ${params.BUCKET_ACCESS}"
                            break
                        case 'upload-file-to-bucket':
                            command = "python cli.py upload-file-to-bucket --bucket-name ${params.BUCKET_NAME} --file-path ${params.FILE_PATH}"
                            break
                        case 'list-buckets':
                            command = "python cli.py list-buckets"
                            break
                        case 'create-hosted-zone':
                            command = "python cli.py create-hosted-zone"
                            break
                        case 'manage-record':
                            command = "python cli.py manage-record --zone-name ${params.ZONE_NAME} --record-name ${params.RECORD_NAME} --record-type ${params.RECORD_TYPE} --record-value ${params.RECORD_VALUE} --action ${params.RECORD_ACTION}"
                            break
                        case 'destroy-resources':
                            command = "python cli.py destroy-resources"
                            break
                        default:
                            error "Invalid command selected!"
                }
            }
        }
    }
}

    post {
        always {
            script {
                echo 'Pipeline execution completed!'
            }
        }
    }
}
