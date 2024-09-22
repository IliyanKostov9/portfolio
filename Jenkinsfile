pipeline {
  agent any
      // environment {
      //   JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
      //   PATH = "${JAVA_HOME}/bin:${env.PATH}"
      // }
        tools {
          jdk 'JDK9'
        }
        options {
          disableConcurrentBuilds()
        }
        stages {
          stage('List env') {
          agent { label 'lambda-java'}
          steps {
            sh 'echo "JAVA_HOME: $JAVA_HOME"'
            sh 'echo "PATH: $PATH"'
             sh 'java -version'
            }
          }
          stage('Git checkout') {
          agent { label 'lambda-java'}
          steps {
              git branch: env.BRANCH_NAME , url: 'https://codeberg.org/iliyan-kostov/portfolio.git'
            }
        }
          stage("Sonar Analysis") {
          agent { label 'lambda-java'}
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
