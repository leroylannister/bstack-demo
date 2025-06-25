from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config.config import Config

class DriverFactory:
    @staticmethod
    def create_driver(browser_config):
        """Create a WebDriver instance for BrowserStack"""
        if not Config.BROWSERSTACK_USERNAME or not Config.BROWSERSTACK_ACCESS_KEY:
            raise ValueError("BrowserStack credentials not found. Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables.")
        
        import os
        build_name = os.getenv('BUILD_NUMBER', 'Local Build')
        
        # Prepare BrowserStack options
        bstack_options = browser_config.get('bstack:options', {})
        bstack_options['buildName'] = f"BStack Demo Suite - Build {build_name}"
        
        # Remove bstack:options from browser_config to avoid duplication
        browser_config = {k: v for k, v in browser_config.items() if k != 'bstack:options'}
        
        options = ChromeOptions()
        for key, value in browser_config.items():
            options.set_capability(key, value)
        options.set_capability('bstack:options', bstack_options)
        
        driver = webdriver.Remote(
            command_executor=Config.BROWSERSTACK_HUB,
            options=options
        )
        
        driver.maximize_window()
        return driver
