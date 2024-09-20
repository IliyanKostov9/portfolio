pipeline {
  agent { label 'lambda-java'}
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
                def scannerHome = tool 'SonarCloud';
                withSonarQubeEnv('SonarCloud') {
                    sh """
                      ${scannerHome}/bin/sonar-scanner \
                      -Dsonar.projectKey=IliyanKostov9_portfolio \
                      -Dsonar.organization=iliyankostov9 \
                      -Dsonar.branch.name=${env.BRANCH_NAME} \
                      -Dorg.jenkinsci.plugins.durabletask.BourneShellScript.LAUNCH_DIAGNOSTICS=true
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
