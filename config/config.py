import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="Browser to run tests on"
    )
    parser.addoption(
        "--platform",
        action="store",
        default="windows",
        help="Platform to run tests on"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Create WebDriver instance for BrowserStack"""
    
    # Get credentials from environment variables
    username = os.environ.get('BROWSERSTACK_USERNAME')
    access_key = os.environ.get('BROWSERSTACK_ACCESS_KEY')
    
    if not username or not access_key:
        raise ValueError("BrowserStack credentials not found in environment variables")
    
    # BrowserStack hub URL
    hub_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
    
    # Get browser and platform from command line or use defaults
    browser = request.config.getoption("--browser")
    platform = request.config.getoption("--platform")
    
    # Define capabilities based on browser/platform
    # These will be overridden by browserstack.yml when using browserstack-sdk
    desired_caps = {
        'browserName': browser,
        'browserstack:options': {
            'os': 'Windows' if platform == 'windows' else 'OS X',
            'osVersion': '10' if platform == 'windows' else 'Ventura',
            'sessionName': request.node.name,
            'buildName': 'BStack Demo Test Suite',
            'projectName': 'BrowserStack Demo Tests'
        }
    }
    
    # Create WebDriver instance
    driver = webdriver.Remote(
        command_executor=hub_url,
        desired_capabilities=desired_caps
    )
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    # Provide the driver to the test
    yield driver
    
    # Quit the driver after test
    driver.quit()

@pytest.fixture(scope="session")
def demo_credentials():
    """Provide demo credentials as fixture"""
    return {
        'username': os.environ.get('DEMO_USERNAME', 'demouser'),
        'password': os.environ.get('DEMO_PASSWORD', 'testingisfun99')
    }