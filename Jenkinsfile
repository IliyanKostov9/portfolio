pipeline {
  agent any
  options {
    disableConcurrentBuilds()
  }
  environment {
    python3 = tool 'Python'
  }
  stages {
    stage('Git checkout') {
    agent { label 'lambda-cloud'}
      steps {
        git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
      }
  }
    stage("Lint") {
      agent { label 'lambda-cloud'}
      steps {
        sh '${python3} --version'
        }
    }
  }
}
