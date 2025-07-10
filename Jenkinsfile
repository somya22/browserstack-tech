pipeline {
      agent any
      stages {
          stage('setup') {
            steps {
                browserstack(credentialsId: 'ab9025db-c1e4-44cb-b909-f9e375051dc8') {

            sh '''
            // python3 -m venv venv
            // source venv/bin/activate
            // pip install --upgrade pip
            browserstack-sdk tests/testcase.py
          '''
                }
            }
            # ...
          }
        }
      


  post {
    always {
      browserStackReportPublisher 'automate'
    }
  }
}