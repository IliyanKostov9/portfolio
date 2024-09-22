pipeline {
  agent any
        options {
          disableConcurrentBuilds()
        }
        stages {
          stage('Git checkout') {
          agent { label 'lambda-java'}
          steps {
              git branch: env.BRANCH_NAME , url: 'https://codeberg.org/iliyan-kostov/portfolio.git'
            }
        }
          stage("Sonar Analysis") {
          agent { label 'lambda-java'}
            // tools {
            //   jdk 'jdk11'
            // }
            environment {
              scannerHome = tool 'SonarTool';
              JAVA_HOME = "/tmp/tools/hudson.model.JDK/jdk11/jdk-11"
              PATH = "${JAVA_HOME}/bin:${env.PATH}"
              SONAR_USER_HOME = "/tmp/sonar-cache"
            }
            steps {
              script {
                withSonarQubeEnv(installationName: 'SonarCloud') {
                  sh 'mkdir /tmp/sonar-cache'
                  sh "${scannerHome}/bin/sonar-scanner -X"
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
