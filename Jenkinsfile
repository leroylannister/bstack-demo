pipeline {
    agent any
    
    environment {
        BROWSERSTACK_USERNAME = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
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
                browserstack(credentialsId: 'browserstack-credentials') {
                    sh '''
                        . venv/bin/activate
                        pytest tests/test_bstack_demo.py -v -n 3 --tb=short
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv'
        }
        success {
            echo 'Tests completed successfully!'
        }
        failure {
            echo 'Tests failed. Check BrowserStack dashboard for details.'
        }
    }
}
