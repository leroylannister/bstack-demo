import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.favorites_page import FavoritesPage
from utils.driver_factory import DriverFactory
from config.config import Config

class TestBStackDemo:
    
    @pytest.fixture(params=Config.BROWSER_CONFIGS, ids=['Windows-Chrome', 'macOS-Firefox', 'Galaxy-S22'])
    def driver(self, request):
        """Fixture to create driver instances for parallel execution"""
        browser_config = request.param
        driver = DriverFactory.create_driver(browser_config)
        driver.get(Config.BASE_URL)
        yield driver
        
        # Mark test status on BrowserStack
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Test failed"}}')
        else:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
        
        driver.quit()
    
    def test_bstack_demo_workflow(self, driver):
        """
        Complete test workflow:
        1. Login with demo credentials
        2. Filter products to show Samsung devices
        3. Favorite Galaxy S20+
        4. Verify Galaxy S20+ appears in favorites
        """
        # Initialize page objects
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        favorites_page = FavoritesPage(driver)
        
        # Step 1: Login
        login_page.login(Config.DEMO_USERNAME, Config.DEMO_PASSWORD)
        assert login_page.is_logged_in(), "Login failed - user not logged in"
        
        # Step 2: Apply Samsung filter
        products_page.apply_samsung_filter()
        
        # Step 3: Favorite Galaxy S20+
        products_page.favorite_galaxy_s20_plus()
        
        # Step 4: Navigate to favorites and verify
        products_page.go_to_favorites()
        assert favorites_page.is_galaxy_s20_plus_in_favorites(), "Galaxy S20+ not found in favorites"
        
        # Additional verification
        favorites_count = favorites_page.get_favorite_products_count()
        assert favorites_count > 0, "No favorite products found"

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Hook to capture test results for BrowserStack status"""
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_" + rep.when, rep)
