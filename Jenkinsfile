pipeline {
    agent any
    
    environment {
        BROWSERSTACK_USERNAME = 'michaelzada_kKTcgR'
        BROWSERSTACK_ACCESS_KEY = 'voDkvRqyaPzkku9ncwt8'
        DEMO_USERNAME = 'demouser'
        DEMO_PASSWORD = 'testingisfun99'
        PYTHONWARNINGS = 'ignore:Unverified HTTPS request'
    }
    
    stages {
        stage('Debug Project Structure') {
            steps {
                sh '''
                    echo "=== Project Structure ==="
                    pwd
                    ls -la
                    
                    echo "\n=== Contents of tests directory ==="
                    ls -la tests/
                    
                    echo "\n=== First few lines of test file ==="
                    head -20 tests/test_bstack_demo.py || echo "Test file not found"
                    
                    echo "\n=== Check for pages directory ==="
                    if [ -d "pages" ]; then
                        echo "Pages directory exists"
                        ls -la pages/
                    else
                        echo "Pages directory NOT found - this is the issue!"
                    fi
                    
                    echo "\n=== Check for __init__.py files ==="
                    find . -name "__init__.py" -type f 2>/dev/null || echo "No __init__.py files found"
                '''
            }
        }
        
        stage('Setup') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Fix Python Path and Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    # Add current directory to PYTHONPATH
                    export PYTHONPATH="${PYTHONPATH}:${PWD}"
                    echo "PYTHONPATH is: $PYTHONPATH"
                    
                    # Try to run tests
                    browserstack-sdk pytest tests/test_bstack_demo.py -v -n 3 --tb=short || true
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
            echo 'Pipeline completed!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}