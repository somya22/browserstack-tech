pipeline {
  agent any
  environment {
    PATH = "/Users/somyamaheshwari/Library/Python/3.9/bin:$PATH"
  }
  stages {
    stage('Run BrowserStack SDK Test') {
      steps {
        browserstack(credentialsId: 'ab9025db-c1e4-44cb-b909-f9e375051dc8') {
          sh 'browserstack-sdk tests/testcase.py'
        }
      }
    }
  }
  post {
    always {
      browserStackReportPublisher 'automate'
    }
  }
}
