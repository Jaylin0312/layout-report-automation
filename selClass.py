from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import logging
import os


class SelCore:
    def __init__(self, driver: webdriver, logger: logging.Logger) -> None:
        self.layout_on = False
        self.driver = driver
        self.logger = logger

    def click(self, args: str = ""):
        action_chains = ActionChains(self.driver)
        action_chains.click(args).perform()

    def getitem(self, args: str = ""):
        select_type = args.split(" ", 1)[0].strip()
        element = args.split(" ", 1)[1].strip()
        locator = getattr(By, select_type.upper())
        # Try to wait until element is vsible
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((locator, element))
            )
        except:
            raise Exception(f"Time out waiting for element {element}")
        return self.driver.find_element(locator, element)

    def login(self, args="username password"):
        username = args.split()[0].strip()
        password = args.split()[1].strip()
        self.logger.debug(
            f"Attempting to login user: {username} with password {password}"
        )
        # Get username textarea
        username_elem = self.getitem("id username")
        username_elem.clear()
        username_elem.send_keys(username)
        # Get password textarea
        password_elem = self.getitem("id password")
        password_elem.clear()
        password_elem.send_keys(password)
        # Click on log in button
        login_button = self.getitem("id login")
        self.click(login_button)
        self.logger.debug(
            f"Successfully logged in as: {username} with password {password}"
        )

    def logout(self):
        account_elem = self.getitem("XPATH (//div[@class='portal_menubar_menu'])[2]")
        self.click(account_elem)
        logout_button = self.getitem(
            "XPATH //td[@class='menu_item_text' and contains(text(), 'Logout')]"
        )
        self.click(logout_button)
        confirm_button = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'OK')]"
        )
        self.click(confirm_button)

    def check_pop(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), 'Continue')]")
                )
            )
            popup = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Continue')]"
            )
            self.click(popup)
        except:
            self.logger.debug(f"No pop up detected. Proceed to log out")
            pass

    def screenshot(self, args: str = ""):
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, args)
        self.driver.save_screenshot(screenshot_path)

    def import_layout(self, f: str = "", counter: int = 0):
        # Locate the textarea
        textarea = self.getitem("XPATH //textarea")
        self.logger.debug(f"Importing layout from {f} file...")
        # Read the layout from layout file
        layout = f.read()
        if len(layout) <= 0:
            raise Exception("Layout file is empty")
        # Input layout into textarea
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", textarea, layout
        )
        # Click on import button
        import_button = self.getitem("XPATH //button[contains(text(), 'Import')]")
        self.click(import_button)
        # Click OK
        confirm_button = self.getitem("XPATH //button[contains(text(), 'OK')]")
        self.click(confirm_button)
        time.sleep(3)
        self.screenshot(f"layout{counter}.png")
