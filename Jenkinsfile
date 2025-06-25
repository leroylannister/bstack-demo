pipeline {
    agent any
    
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
                withCredentials([
                    string(credentialsId: 'browserstack-username', variable: 'BROWSERSTACK_USERNAME'),
                    string(credentialsId: 'browserstack-access-key', variable: 'BROWSERSTACK_ACCESS_KEY')
                ]) {
                    sh '''
                        . venv/bin/activate
                        export DEMO_USERNAME='demouser'
                        export DEMO_PASSWORD='testingisfun99'
                        
                        # Run tests in parallel across 3 browsers using browserstack-sdk
                        # The -n 3 flag runs 3 tests in parallel
                        browserstack-sdk pytest tests/test_bstack_demo.py -v -n 3 --tb=short
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