import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # BrowserStack credentials - should be set as environment variables
    BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME')
    BROWSERSTACK_ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')
    
    # Test data
    DEMO_USERNAME = os.getenv('DEMO_USERNAME', 'demouser')
    DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'testingisfun99')
    
    # URLs
    BASE_URL = "https://www.bstackdemo.com"
    BROWSERSTACK_HUB = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    
    # Browser configurations for parallel execution
    BROWSER_CONFIGS = [
        {
            'browserName': 'Chrome',
            'browserVersion': 'latest',
            'bstack:options': {
                'os': 'Windows',
                'osVersion': '10',
                'sessionName': 'BStack Demo - Windows Chrome',
                'seleniumVersion': '4.15.0',
                'maskCommands': 'setValues, getValues, setCookies, getCookies'
            }
        },
        {
            'browserName': 'Firefox',
            'browserVersion': 'latest',
            'bstack:options': {
                'os': 'OS X',
                'osVersion': 'Ventura',
                'sessionName': 'BStack Demo - macOS Firefox',
                'seleniumVersion': '4.15.0',
                'maskCommands': 'setValues, getValues, setCookies, getCookies'
            }
        },
        {
            'browserName': 'chrome',
            'bstack:options': {
                'deviceName': 'Samsung Galaxy S22',
                'osVersion': '12.0',
                'sessionName': 'BStack Demo - Galaxy S22',
                'realMobile': 'true',
                'maskCommands': 'setValues, getValues, setCookies, getCookies'
            }
        }
    ]
