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

        // Dynamic fields (defined using Active Choices Plugin)
        dynamicReference(name: 'ACTION', referencedParameter: 'COMMAND', script: '''
            if (COMMAND == 'manage-instances' || COMMAND == 'manage-record') {
                return ['start', 'stop', 'CREATE', 'UPDATE', 'DELETE']
            }
            return []
        ''')

        dynamicReference(name: 'INSTANCE_ID', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'manage-instances') ? ['Enter Instance ID'] : []
        ''')

        dynamicReference(name: 'TYPE', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'create-instances') ? ['t2.micro', 't3.medium', 'm5.large'] : []
        ''')

        dynamicReference(name: 'OS', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'create-instances') ? ['Windows', 'Linux'] : []
        ''')

        dynamicReference(name: 'COUNT', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'create-instances') ? ['1', '2', '3', '4', '5'] : []
        ''')

        dynamicReference(name: 'BUCKET_NAME', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'upload-file-to-bucket') ? ['Enter Bucket Name'] : []
        ''')

        dynamicReference(name: 'FILE_PATH', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'upload-file-to-bucket') ? ['Enter File Path'] : []
        ''')

        dynamicReference(name: 'ZONE_NAME', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'manage-record') ? ['Enter Zone Name'] : []
        ''')

        dynamicReference(name: 'RECORD_NAME', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'manage-record') ? ['Enter Record Name'] : []
        ''')

        dynamicReference(name: 'RECORD_TYPE', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'manage-record') ? ['A', 'CNAME', 'TXT', 'MX'] : []
        ''')

        dynamicReference(name: 'RECORD_VALUE', referencedParameter: 'COMMAND', script: '''
            return (COMMAND == 'manage-record') ? ['Enter Record Value'] : []
        ''')
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
                    def command = "python cli.py --command ${params.COMMAND} " +
                        (params.INSTANCE_ID ? "--instance-id ${params.INSTANCE_ID} " : "") +
                        (params.TYPE ? "--type ${params.TYPE} " : "") +
                        (params.OS ? "--os ${params.OS} " : "") +
                        (params.COUNT ? "--count ${params.COUNT} " : "") +
                        (params.BUCKET_NAME ? "--bucket-name ${params.BUCKET_NAME} " : "") +
                        (params.FILE_PATH ? "--file-path ${params.FILE_PATH} " : "") +
                        (params.ZONE_NAME ? "--zone-name ${params.ZONE_NAME} " : "") +
                        (params.RECORD_NAME ? "--record-name ${params.RECORD_NAME} " : "") +
                        (params.RECORD_TYPE ? "--record-type ${params.RECORD_TYPE} " : "") +
                        (params.RECORD_VALUE ? "--record-value ${params.RECORD_VALUE} " : "")

                    bat command.trim()
                }
            }
        }
    }
}
