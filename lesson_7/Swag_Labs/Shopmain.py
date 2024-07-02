from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lesson_7.constants import Shop_URL

class ShopmainPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get(Shop_URL)

    def reristration_field(self):
        self._name = (By.ID, "user-name")
        self._pass = (By.ID, "password")
        self._log_button = (By.ID, "login-button")
        self.browser.find_element(*self._name).send_keys("standard_user")
        self.browser.find_element(*self._pass).send_keys("secret_sauce")
        self.browser.find_element(*self._log_button).click()

    def buy_issue(self):
        self.Sauce_Labs_Backpack = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.Sauce_Labs_Bolt_TShirt = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
        self.Sauce_Labs_Onesie = (By.ID, "add-to-cart-sauce-labs-onesie")

        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(self.Sauce_Labs_Backpack))
        self.browser.find_element(*self.Sauce_Labs_Backpack).click()

        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(self.Sauce_Labs_Bolt_TShirt))
        self.browser.find_element(*self.Sauce_Labs_Bolt_TShirt).click()

        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(self.Sauce_Labs_Onesie))
        self.browser.find_element(*self.Sauce_Labs_Onesie).click()

    def click_issue(self):
        self.browser.find_element(By.ID, "shopping_cart_container").click()

    def into_container(self):
        self.Container = (By.ID, "shopping_cart_container")
        self.browser.find_element(*self.Container).click()
