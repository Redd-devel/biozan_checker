pipeline {
    agent any
    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }
    parameters {
        booleanParam defaultValue: false, description: 'Show products', name: 'isProducts'
    }

    stages {
        stage('Preparing') {
            steps {
                sh '''python3 -m venv envir
                      . ${WORKSPACE}/envir/bin/activate > /dev/null
                      pip install -r requirements.txt'''
            }
        }
        stage('Pull') { 
            steps {
                withCredentials([usernamePassword(credentialsId: 'biozan_cred', usernameVariable: 'USERLOGIN', passwordVariable: 'USERPASS'),
                                 string(credentialsId: 'biozan_csrf', variable: 'CSRF')]) {
                    sh '''
                    . ${WORKSPACE}/envir/bin/activate > /dev/null
                    python biozan_checker.py
                    '''
                }
            }
        }
    }
    post {
        cleanup {
            cleanWs(
                cleanWhenNotBuilt:false,
                cleanWhenAborted:true,
                cleanWhenFailure:true,
                cleanWhenSuccess:true,
                cleanWhenUnstable:true,
                deleteDirs:true)

        }
    }
}

