from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FavoritesPage(BasePage):
    # Locators
    FAVORITE_PRODUCTS = (By.CSS_SELECTOR, ".shelf-item")
    GALAXY_S20_PLUS_FAVORITE = (By.XPATH, "//p[contains(text(), 'Galaxy S20+')]")
    
    def is_galaxy_s20_plus_in_favorites(self):
        return self.is_element_present(self.GALAXY_S20_PLUS_FAVORITE, timeout=10)
    
    def get_favorite_products_count(self):
        try:
            products = self.find_elements(self.FAVORITE_PRODUCTS)
            return len(products)
        except:
            return 0
