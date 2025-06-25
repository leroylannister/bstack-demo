from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config.config import Config

class DriverFactory:
    @staticmethod
    def create_driver(browser_config):
        """Create a WebDriver instance for BrowserStack"""
        if not Config.BROWSERSTACK_USERNAME or not Config.BROWSERSTACK_ACCESS_KEY:
            raise ValueError("BrowserStack credentials not found. Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables.")
        
        # Create capabilities
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities.update(browser_config)
        
        # Add build name from Jenkins if available
        import os
        build_name = os.getenv('BUILD_NUMBER', 'Local Build')
        capabilities['bstack:options']['buildName'] = f"BStack Demo Suite - Build {build_name}"
        
        # Create remote driver
        driver = webdriver.Remote(
            command_executor=Config.BROWSERSTACK_HUB,
            desired_capabilities=capabilities
        )
        
        driver.maximize_window()
        return driver
