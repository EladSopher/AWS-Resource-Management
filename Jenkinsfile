pipeline {
    agent any

    parameters {
        choice(name: 'COMMAND', choices: [
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

        choice(name: 'ACTION', choices: ['start', 'stop', 'CREATE', 'UPDATE', 'DELETE'], description: 'Action for managing instances or DNS records')

        choice(name: 'TYPE', choices: ['t3.nano', 't4g.nano'], description: 'Instance Type (for create-instances)')
        choice(name: 'OS', choices: ['ubuntu', 'amazon-linux'], description: 'OS Type (for create-instances)')
        choice(name: 'COUNT', choices: ['1', '2'], description: 'Number of instances to create')
        string(name: 'INSTANCE_ID', defaultValue: '', description: 'Instance ID (for manage-instances)')
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
        AWS_PROFILE = 'default'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Execute Command') {
            steps {
                script {
                    def command = params.COMMAND

                    if (command == "create-instances") {
                        sh "python3 cli.py create-instances --type ${params.TYPE} --os ${params.OS} --count ${params.COUNT}"
                    } else if (command == "manage-instances") {
                        sh "python3 cli.py manage-instances --action ${params.ACTION} --instance-id ${params.INSTANCE_ID}"
                    } else if (command == "list-instances") {
                        sh "python3 cli.py list-instances"
                    } else if (command == "create-bucket") {
                        sh "python3 cli.py create-bucket --access private"
                    } else if (command == "upload-file-to-bucket") {
                        sh "python3 cli.py upload-file-to-bucket --bucket-name ${params.BUCKET_NAME} --file-path ${params.FILE_PATH}"
                    } else if (command == "list-buckets") {
                        sh "python3 cli.py list-buckets"
                    } else if (command == "create-hosted-zone") {
                        sh "python3 cli.py create-hosted-zone"
                    } else if (command == "manage-record") {
                        sh "python3 cli.py manage-record --zone-name ${params.ZONE_NAME} --record-name ${params.RECORD_NAME} --record-type ${params.RECORD_TYPE} --record-value ${params.RECORD_VALUE} --action ${params.ACTION}"
                    } else if (command == "destroy-resources") {
                        sh "python3 cli.py destroy-resources"
                    }
                }
            }
        }
    }
}
