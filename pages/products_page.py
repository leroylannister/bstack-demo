from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ProductsPage(BasePage):
    # Locators
    VENDOR_FILTER = (By.XPATH, "//span[text()='Vendors']")
    SAMSUNG_FILTER = (By.XPATH, "//span[text()='Samsung']")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".shelf-item")
    GALAXY_S20_PLUS = (By.XPATH, "//p[contains(text(), 'Galaxy S20+')]")
    FAVORITE_BUTTON = (By.CSS_SELECTOR, "[id*='fav']")
    FAVORITES_LINK = (By.CSS_SELECTOR, ".favourites")
    
    def apply_samsung_filter(self):
        self.click_element(self.VENDOR_FILTER)
        self.wait.until(EC.element_to_be_clickable(self.SAMSUNG_FILTER))
        self.click_element(self.SAMSUNG_FILTER)
        # Wait for products to load after filtering
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARDS))
    
    def favorite_galaxy_s20_plus(self):
        # Find the Galaxy S20+ product card
        galaxy_s20_card = self.find_element(self.GALAXY_S20_PLUS)
        # Find the favorite button within that card's parent container
        product_container = galaxy_s20_card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'shelf-item')]")
        favorite_btn = product_container.find_element(By.CSS_SELECTOR, "[id*='fav']")
        
        # Scroll to element if needed
        self.driver.execute_script("arguments[0].scrollIntoView(true);", favorite_btn)
        self.wait.until(EC.element_to_be_clickable(favorite_btn))
        favorite_btn.click()
    
    def go_to_favorites(self):
        self.click_element(self.FAVORITES_LINK)
