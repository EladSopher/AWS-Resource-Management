pipeline {
    agent any

    parameters {
        choice(name: 'COMMAND', choices: [
            '--none--',
            'create-instances',
            'manage-instances',
            'list-instances',
            'create-bucket',
            'upload-file-to-bucket',
            'list-buckets',
            'create-hosted-zone',
            'manage-record',
            'destroy-resources'
        ], description: 'Choose a command to execute')

        choice(name: 'ACTION', choices: ['--none--', 'start', 'stop', 'CREATE', 'UPDATE', 'DELETE'], description: 'Action for managing instances or DNS records')

        choice(name: 'TYPE', choices: ['--none--', 't3.nano', 't4g.nano'], description: 'Instance Type (for create-instances)')
        choice(name: 'OS', choices: ['--none--', 'ubuntu', 'amazon-linux'], description: 'OS Type (for create-instances)')
        choice(name: 'COUNT', choices: ['1', '2'], description: 'Number of instances to create')
        string(name: 'INSTANCE_ID', defaultValue: '', description: 'Instance ID (for manage-instances)')
        choice(name: 'BUCKET_ACCESS', choices: ['--none--', 'private', 'public'], description: 'Bucket access (for create-bucket)')
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'Bucket name (for upload-file-to-bucket)')
        string(name: 'FILE_PATH', defaultValue: '', description: 'Path to file (for upload-file-to-bucket)')
        string(name: 'ZONE_NAME', defaultValue: '', description: 'DNS Zone Name (for manage-record)')
        string(name: 'RECORD_NAME', defaultValue: '', description: 'Record Name (for manage-record)')
        string(name: 'RECORD_TYPE', defaultValue: '', description: 'Record Type (for manage-record)')
        string(name: 'RECORD_VALUE', defaultValue: '', description: 'Record Value (for manage-record)')
    }

   environment {
        AWS_REGION = 'us-east-1'
        AWS_DEFAULT_REGION = 'us-east-1'
        // AWS_PROFILE = 'default'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Execute Command') {
            steps {
                withAWS(credentials: 'AWS creds')
                {
                    script {
                        def command = params.COMMAND
    
                        if (command == "create-instances") {
                            bat "python cli.py create-instances --type ${params.TYPE} --os ${params.OS} --count ${params.COUNT}"
                        } else if (command == "manage-instances") {
                            bat "python cli.py manage-instances --action ${params.ACTION} --instance-id ${params.INSTANCE_ID}"
                        } else if (command == "list-instances") {
                            bat "python cli.py list-instances"
                        } else if (command == "create-bucket") {
                            bat "python cli.py create-bucket --access ${params.BUCKET_ACCESS}"
                        } else if (command == "upload-file-to-bucket") {
                            bat "python cli.py upload-file-to-bucket ${params.BUCKET_NAME} ${params.FILE_PATH}"
                        } else if (command == "list-buckets") {
                            bat "python cli.py list-buckets"
                        } else if (command == "create-hosted-zone") {
                            bat "python cli.py create-hosted-zone"
                        } else if (command == "manage-record") {
                            bat "python cli.py manage-record ${params.ZONE_NAME} ${params.RECORD_NAME} ${params.RECORD_TYPE} ${params.RECORD_VALUE} ${params.ACTION}"
                        } else if (command == "destroy-resources") {
                            bat "python cli.py destroy-resources"
                        }
                    }
                }
            }
        }
    }
}
