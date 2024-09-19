pipeline {
        agent any
        options {
          disableConcurrentBuilds()
        }
        stages {
          stage('Git checkout') {
            steps {
              git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
            }
        }
          stage("SonarQube analysis") {
            steps {
              script {
                def scannerHome = tool 'SonarQubeScanner';
                withSonarQubeEnv('SonarQubeScanner') {
                    sh """
                      ${scannerHome}/bin/sonar-scanner \
                      -Dsonar.qualitygate.wait=true \
                      -Dsonar.projectKey=portfolio \
                      -Dsonar.branch.name=${env.BRANCH_NAME}
                      """
                }
                  }
            }
          }
          stage("Quality Gate") {
            steps {
              timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true, credentialsId: 'Sonar-token'
              }
            }
          }
        }
      }
