pipeline {
  agent any
        options {
          disableConcurrentBuilds()
        }
        stages {
          stage('Git checkout') {
          // agent { label 'lambda-java'}
            steps {
              git branch: env.BRANCH_NAME , url: 'https://codeberg.org/iliyan-kostov/portfolio.git'
            }
        }
          stage("Build") {
          // agent { label 'lambda-java'}
            // environment {
            //   scannerHome = tool 'SonarTool';
            // }
            steps {
              script {
                sh 'python3 --version'
              }
            }
          }
            }
      }
