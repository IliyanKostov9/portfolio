pipeline {
  agent any
  options {
    disableConcurrentBuilds()
     timeout(time: 10, unit: 'MINUTES')
  }
  environment {
    PATH ="/usr/bin/python3:$PATH"
  }
  stages {
    stage('Git checkout') {
      agent { label 'lambda-cloud'}
      options {
       timeout(time: 5, unit: 'MINUTES')
      }
      steps {
        git branch: env.BRANCH_NAME , url: 'https://github.com/IliyanKostov9/portfolio.git'
      }
    }
    stage("Security Analyze") {
      agent { label 'master'}
      options {
       timeout(time: 10, unit: 'MINUTES')
      }
      steps {
        sh '''
        python3 --version
        echo "Activating virtual env..."
        python3 -m venv .venv
        chmod -R u+x .venv/bin/activate
        . .venv/bin/activate
        echo "Now installing pyre deps..."
        pip install --upgrade setuptools
        pip install wheel pyre-check fb-sapp
        echo "Now performing analysis..."
        pyre --output=json | python3 -m json.tool
        pyre --noninteractive analyze --no-verify --output-format json
        '''
      }
    }
  }
}
