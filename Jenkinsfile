pipeline {
  agent any
        options {
          disableConcurrentBuilds()
        }
        stages {
          stage('Git checkout') {
          agent { label 'lambda-java'}
            steps {
              git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
            }
        }
          stage("SonarQube analysis") {
          agent { label 'lambda-java'}
            environment {
              scannerHome = tool 'SonarTool';
            }
            steps {
              script {
                sh "echo '${scannerHome}"
                withSonarQubeEnv(installationName: 'SonarCloud', credentialsId: '8049a509-1e79-4369-8240-2f413248d607') {
                  sh "${scannerHome}/bin/sonar-scanner -v"
                  }
              }
            }
          }
          stage("Quality Gate") {
            agent { label 'lambda-java'}
            steps {
              timeout(time: 1, unit: 'HOURS') {
               waitForQualityGate abortPipeline: true, credentialsId: 'Sonar-token'
              }
            }
          }
        }
      }
