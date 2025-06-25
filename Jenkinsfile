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
        stage('Debug Config Files') {
            steps {
                sh '''
                    echo "=== Contents of config directory ==="
                    ls -la config/
                    
                    echo "\n=== Contents of config/config.py ==="
                    cat config/config.py || echo "File not found"
                    
                    echo "\n=== Contents of utils directory ==="
                    ls -la utils/
                    
                    echo "\n=== Contents of utils/driver_factory.py (first 20 lines) ==="
                    head -20 utils/driver_factory.py || echo "File not found"
                    
                    echo "\n=== Check config/__init__.py ==="
                    if [ -f "config/__init__.py" ]; then
                        echo "config/__init__.py exists"
                        cat config/__init__.py
                    else
                        echo "config/__init__.py NOT found - creating it"
                        touch config/__init__.py
                    fi
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
        
        stage('Test Python Import') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="${PWD}:${PYTHONPATH}"
                    
                    echo "=== Testing imports directly ==="
                    python -c "
try:
    import config
    print('✓ config module imported')
except Exception as e:
    print(f'✗ Failed to import config: {e}')
    
try:
    from config import config
    print('✓ config.config imported')
except Exception as e:
    print(f'✗ Failed to import config.config: {e}')
    
try:
    from config.config import Config
    print('✓ Config class imported')
except Exception as e:
    print(f'✗ Failed to import Config class: {e}')
    
try:
    import utils
    print('✓ utils module imported')
except Exception as e:
    print(f'✗ Failed to import utils: {e}')
"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="${PWD}:${PYTHONPATH}"
                    
                    # Try running tests
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
            echo 'Debug pipeline completed.'
        }
    }
}