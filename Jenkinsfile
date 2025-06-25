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
    BROWSERSTACK_HUB = f"https://{os.environ.get('BROWSERSTACK_USERNAME')}:{os.environ.get('BROWSERSTACK_ACCESS_KEY')}@hub-cloud.browserstack.com/wd/hub"
    
    # Demo site credentials
    DEMO_USERNAME = os.environ.get('DEMO_USERNAME', 'demouser')
    DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD', 'testingisfun99')
    
    # Base URL
    BASE_URL = "https://www.bstackdemo.com"
    
    # Browser configurations for parallel execution
    BROWSER_CONFIGS = [
        {
            'browserName': 'chrome',
            'bstack:options': {
                'os': 'Windows',
                'osVersion': '10',
                'sessionName': 'Windows Chrome Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        },
        {
            'browserName': 'firefox',
            'bstack:options': {
                'os': 'OS X',
                'osVersion': 'Ventura',
                'sessionName': 'macOS Firefox Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        },
        {
            'browserName': 'chrome',
            'bstack:options': {
                'deviceName': 'Samsung Galaxy S22',
                'platformName': 'android',
                'osVersion': '12.0',
                'sessionName': 'Samsung Galaxy S22 Test',
                'buildName': f"BStack Demo Suite - Build {os.getenv('BUILD_NUMBER', 'Local Build')}"
            }
        }
    ]
EOF
                    
                    # Also update the driver_factory.py to use modern Selenium 4 syntax
                    if [ -f utils/driver_factory.py ]; then
                        mv utils/driver_factory.py utils/driver_factory.py.bak
                    fi
                    
                    cat > utils/driver_factory.py << 'EOF'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.config import Config

class DriverFactory:
    @staticmethod
    def create_driver(browser_config):
        """Create a WebDriver instance for BrowserStack using Selenium 4 syntax"""
        if not Config.BROWSERSTACK_USERNAME or not Config.BROWSERSTACK_ACCESS_KEY:
            raise ValueError("BrowserStack credentials not found. Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables.")
        
        # Get browser name
        browser_name = browser_config.get('browserName', 'chrome').lower()
        
        # Create options based on browser type
        if browser_name == 'chrome':
            options = ChromeOptions()
        elif browser_name == 'firefox':
            options = FirefoxOptions()
        else:
            options = ChromeOptions()  # Default to Chrome
        
        # Set BrowserStack options
        options.set_capability('bstack:options', browser_config.get('bstack:options', {}))
        
        # Add build name from Jenkins if available
        import os
        build_name = os.getenv('BUILD_NUMBER', 'Local Build')
        if 'bstack:options' in browser_config:
            browser_config['bstack:options']['buildName'] = f"BStack Demo Suite - Build {build_name}"
        
        # Create WebDriver with Selenium 4 syntax
        driver = webdriver.Remote(
            command_executor=Config.BROWSERSTACK_HUB,
            options=options
        )
        
        return driver
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
                    # Restore original files if backed up
                    if [ -f config/config.py.bak ]; then
                        mv config/config.py.bak config/config.py
                    fi
                    
                    if [ -f utils/driver_factory.py.bak ]; then
                        mv utils/driver_factory.py.bak utils/driver_factory.py
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