pipeline {
  agent: any
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
            steps {
              script {
                def scannerHome = tool 'SonarCloud';
                withSonarQubeEnv('SonarCloud') {
                    sh """
                      ${scannerHome}/bin/sonar-scanner -X \
                      -Dsonar.qualitygate.wait=true \
                      -Dsonar.projectKey=IliyanKostov9_portfolio \
                      -Dsonar.organization=iliyankostov9 \
                      -Dsonar.branch.name=${env.BRANCH_NAME}
                      """
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
