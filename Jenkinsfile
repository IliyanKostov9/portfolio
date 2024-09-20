pipeline {
  agent any
        options {
          disableConcurrentBuilds()
        }
        stages {
    stage('Check Network Access') {
      steps {
        sh 'ping sonarcloud.io -c 4'
      }
    }
          stage('Git checkout') {
          agent { label 'lambda-java'}
            steps {
              git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
            }
        }
          stage("SonarQube analysis") {
            environment {
              scannerHome = tool 'SonarTool';
            }
            steps {
              script {
                withSonarQubeEnv(installationName: 'SonarCloud', credentialsId: '8049a509-1e79-4369-8240-2f413248d607') {
                  sh "${scannerHome}/bin/sonar-scanner"
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
