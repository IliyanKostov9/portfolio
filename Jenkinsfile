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
            environment {
              scannerHome = tool 'SonarCloud';
            }
            steps {
              script {
                withSonarQubeEnv('SonarCloud') {
                  sh "${scannerHome}/bin/sonar-scanner -h"
                  sh "${scannerHome}/bin/sonar-scanner"
                    // sh """
                    //   ${scannerHome}/bin/sonar-scanner \
                    //   -Dsonar.qualitygate.wait=false \
                    //   -Dsonar.projectKey=IliyanKostov9_portfolio \
                    //   -Dsonar.organization=iliyankostov9 \
                    //   -Dsonar.branch.name=${env.BRANCH_NAME} \
                    //   -Dorg.jenkinsci.plugins.durabletask.BourneShellScript.LAUNCH_DIAGNOSTICS=true
                    //   """
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
