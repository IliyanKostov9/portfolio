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
              jdk 'jdk21'
            }
            environment {
              scannerHome = tool 'SonarTool';
              // JAVA_HOME = "/tmp/tools/hudson.model.JDK/jdk17/jdk-17.0.1"
              // PATH = "${JAVA_HOME}/bin:${env.PATH}"
              SONAR_USER_HOME = "/tmp/sonar-cache"
            }
            steps {
              script {
                withSonarQubeEnv(installationName: 'SonarCloud') {
                  sh 'mkdir -p /tmp/sonar-cache'

                  sh 'echo "JAVA_HOME: $JAVA_HOME"'
                  sh 'echo "PATH: $PATH"'
                  sh 'java --version'

                  sh '''
                  export JAVA_HOME="/tmp/tools/hudson.model.JDK/jdk21/jdk-21"
                  export PATH="$JAVA_HOME/bin:$PATH"
                  /tmp/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarTool/bin/sonar-scanner -X
                  '''

                  // sh "${scannerHome}/bin/sonar-scanner -X"
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
