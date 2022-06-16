pipeline {
  agent any
  stages {
    stage('Run unit tests') {
      steps {
        sh '''#!/bin/bash
          sudo apt update
          sudo apt install python3 python3-pip python3-venv -y
          python3 -m venv venv
          source venv/bin/activate
          pip3 install -r requirements.txt
          python3 -m pytest --cov=application --cov-report xml
        '''
      }
    }
    stage('Copy files') {
      steps {
        sh '''#!/bin/bash
          scp -r application jenkins@app-server:/home/jenkins/
          scp app.py jenkins@app-server:/home/jenkins
          scp create.py jenkins@app-server:/home/jenkins
          scp requirements.txt jenkins@app-server:/home/jenkins
        '''
      }
    }
    stage('Deploy app') {
      steps {
        sh '''#!/bin/bash
          ssh jenkins@app-server < deploy.sh
        '''
      }
    }
  }
}