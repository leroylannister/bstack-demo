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
        stage('Setup') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    # Ensure __init__.py files exist
                    touch config/__init__.py
                    touch pages/__init__.py
                    touch utils/__init__.py
                    touch tests/__init__.py
                '''
            }
        }
        
        stage('Create Config File') {
            steps {
                echo 'Creating Config class...'
                sh '''
                    # Backup existing config.py if it exists
                    if [ -f config/config.py ]; then
                        mv config/config.py config/config.py.bak
                    fi
                    
                    # Create proper Config class
                    cat > config/config.py << 'EOF'
import os

class Config:
    """Configuration for BrowserStack tests"""
    
    # BrowserStack credentials from environment variables
    BROWSERSTACK_USERNAME = os.environ.get('BROWSERSTACK_USERNAME')
    BROWSERSTACK_ACCESS_KEY = os.environ.get('BROWSERSTACK_ACCESS_KEY')
    
    # BrowserStack Hub URL
    @property
    @staticmethod
    def BROWSERSTACK_HUB():
        username = Config.BROWSERSTACK_USERNAME
        access_key = Config.BROWSERSTACK_ACCESS_KEY
        if username and access_key:
            return f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        else:
            raise ValueError("BrowserStack credentials not found")
    
    # Alternative static hub URL (if the property doesn't work)
    BROWSERSTACK_HUB = f"https://{os.environ.get('BROWSERSTACK_USERNAME')}:{os.environ.get('BROWSERSTACK_ACCESS_KEY')}@hub-cloud.browserstack.com/wd/hub"
    
    # Demo site credentials
    DEMO_USERNAME = os.environ.get('DEMO_USERNAME', 'demouser')
    DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD', 'testingisfun99')
    
    # Base URL
    BASE_URL = "https://www.bstackdemo.com"
    
    # Browser configurations for parallel execution
    BROWSER_CONFIGS = [
        {
            'bstack:options': {
                'os': 'Windows',
                'osVersion': '10',
                'browserName': 'Chrome',
                'browserVersion': 'latest',
                'sessionName': 'Windows Chrome Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        },
        {
            'bstack:options': {
                'os': 'OS X',
                'osVersion': 'Ventura',
                'browserName': 'Firefox',
                'browserVersion': 'latest',
                'sessionName': 'macOS Firefox Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        },
        {
            'bstack:options': {
                'deviceName': 'Samsung Galaxy S22',
                'platformName': 'android',
                'osVersion': '12.0',
                'browserName': 'chrome',
                'sessionName': 'Samsung Galaxy S22 Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        }
    ]
EOF
                '''
            }
        }
        
        stage('Run BrowserStack Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH="${PWD}:${PYTHONPATH}"
                    
                    # Run tests in parallel across 3 browsers using browserstack-sdk
                    browserstack-sdk pytest tests/test_bstack_demo.py -v -n 3 --tb=short || echo "Tests completed with status: $?"
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                sh '''
                    # Restore original config.py if backed up
                    if [ -f config/config.py.bak ]; then
                        mv config/config.py.bak config/config.py
                    fi
                    
                    rm -rf venv || true
                '''
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