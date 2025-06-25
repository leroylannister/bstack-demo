pipeline {
    agent any
    
    environment {
        // TEMPORARY: Replace these with your actual credentials
        // This is NOT recommended for production - use Jenkins credentials instead
        BROWSERSTACK_USERNAME = 'michaelzada_kKTcgR'
        BROWSERSTACK_ACCESS_KEY = 'voDkvRqyaPzkku9ncwt8'
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
                sh '''
                    . venv/bin/activate
                    
                    # Run tests in parallel across 3 browsers using browserstack-sdk
                    # The -n 3 flag runs 3 tests in parallel
                    browserstack-sdk pytest tests/test_bstack_demo.py -v -n 3 --tb=short
                '''
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
        always {
            echo 'Test execution completed.'
        }
        success {
            echo 'All tests passed successfully!'
            echo 'Check BrowserStack dashboard for detailed results and videos.'
        }
        failure {
            echo 'Some tests failed. Check BrowserStack dashboard for details.'
            echo 'Videos and logs are available in the BrowserStack Automate dashboard.'
        }
    }
}