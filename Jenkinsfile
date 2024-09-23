pipeline {
  agent any
  options {
    disableConcurrentBuilds()
     timeout(time: 10, unit: 'MINUTES')
  }
  environment {
    PATH ="/usr/bin/python3:$PATH"
  }
  stages {
    stage('Git checkout') {
    agent { label 'lambda-cloud'}
     timeout(time: 5, unit: 'MINUTES')
      steps {
        git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
      }
  }
    stage("Lint") {
      agent { label 'lambda-cloud'}
     timeout(time: 3, unit: 'MINUTES')
      steps {
        sh 'python3 --version'
        }
    }
  }
}
