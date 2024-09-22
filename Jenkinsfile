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
          agent { label 'lambda-java'}
            environment {
              scannerHome = tool 'SonarTool';
            }
            steps {
                withSonarQubeEnv(installationName: 'SonarCloud', credentialsId: '8049a509-1e79-4369-8240-2f413248d607') {
                  sh "${scannerHome}/bin/sonar-scanner"
                  }
            }
          }
            }
      }
