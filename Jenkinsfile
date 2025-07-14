pipeline {
    agent any

    environment {
        BROWSERSTACK_BUILD_NAME = "jenkins-build-${BUILD_NUMBER}"
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                browserstack(credentialsId: 'ab9025db-c1e4-44cb-b909-f9e375051dc8') {
                    sh 'python3 -m unittest tests/test1_bstack.py'
                }
            }
        }
    }
}
