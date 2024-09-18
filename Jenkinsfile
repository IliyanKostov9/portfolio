pipeline {
        agent none
	env {
          SCANNER_HOME= tool 'sonar-scanner'
	}
        stages {
          stage('Git checkout') {
            steps {
              git branch: 'master', url: 'https://github.com/IliyanKostov9/portfolio.git'
            }
        }
          stage('Python version') {
            steps {
              sh 'python3 --version'
            }
          }
          stage("SonarQube analysis") {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=portfolio \
                    -Dsonar.projectKey=portfolio '''
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
