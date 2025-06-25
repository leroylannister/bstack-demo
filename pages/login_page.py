from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    SIGN_IN_BUTTON = (By.ID, "signin")
    USERNAME_INPUT = (By.CSS_SELECTOR, "#username input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password input")
    LOGIN_BUTTON = (By.ID, "login-btn")
    LOGOUT_BUTTON = (By.ID, "logout")
    
    def click_sign_in(self):
        self.click_element(self.SIGN_IN_BUTTON)
    
    def enter_credentials(self, username, password):
        self.send_keys_to_element(self.USERNAME_INPUT, username)
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        self.click_sign_in()
        self.enter_credentials(username, password)
        self.click_login()
    
    def is_logged_in(self):
        return self.is_element_present(self.LOGOUT_BUTTON)
