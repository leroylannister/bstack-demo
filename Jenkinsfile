pipeline {
    agent any
    
    environment {
        BROWSERSTACK_USERNAME = credentials('michaelzada_kKTcgR')
        BROWSERSTACK_ACCESS_KEY = credentials('voDkvRqyaPzkku9ncwt8')
        DEMO_USERNAME = 'demouser'
        DEMO_PASSWORD = 'testingisfun99'
    }
    
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run BrowserStack Tests') {
            steps {
                browserstack(credentialsId: 'd165da47-3c30-4ac2-9ab8-0bd037b78e0e') {
                    sh '''
                        . venv/bin/activate
                        pytest tests/test_bstack_demo.py -v -n 3 --tb=short
                    '''
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                sh 'rm -rf venv || true'
            }
        }
    }
    
    post {
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed. Check BrowserStack dashboard for details.'
        }
    }
}