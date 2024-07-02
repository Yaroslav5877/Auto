from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShopContainer:
    def __init__(self, browser):
        self.browser = browser

    def checkout(self):
        self.check = (By.ID, "checkout")
        self.browser.find_element(*self.check).click()

    def info(self):
        self.first_name = (By.ID, "first-name")
        self.browser.find_element(*self.first_name).send_keys("Yaroslav")
        self.last_name = (By.ID, "last-name")
        self.browser.find_element(*self.last_name).send_keys("Pon")
        self.postcode = (By.ID, "postal-code")
        self.browser.find_element(*self.postcode).send_keys("235126")
        self.continue_button = (By.ID, "continue")
        self.browser.find_element(*self.continue_button).click()

    def price(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".summary_total_label")))
        total_price_element = self.browser.find_element(By.CSS_SELECTOR, ".summary_total_label")
        total = total_price_element.text.strip().replace("Total: $", "")
        return total
