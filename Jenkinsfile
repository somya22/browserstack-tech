pipeline {
    agent any

    environment {
        BROWSERSTACK_BUILD_NAME = "jenkins-build-${BUILD_NUMBER}"
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                browserstack(credentialsId: 'browserstack-credentials') {
                    sh '''
                        browserstack-sdk tests/test_bstack.py
                    '''
                }
            }
        }
    }
}
