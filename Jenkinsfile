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
            tools {
              jdk 'jdk17'
            }
            environment {
              scannerHome = tool 'SonarTool';
              // JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
              // PATH = "${JAVA_HOME}/bin:${env.PATH}"
            }
            steps {
              script {
                withSonarQubeEnv(installationName: 'SonarCloud') {
                  sh 'echo "JAVA_HOME: $JAVA_HOME"'
                  sh 'echo "PATH: $PATH"'
                  sh 'java -version'
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
