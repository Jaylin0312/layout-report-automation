from selClass import SelCore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import generateExcel
import generateLayout
import time
import os
import logging


def main():
    fields = generateLayout.main()
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    # For loop to start and close the process for each json test file
    for elem in fields:
        try:
            # Create Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--start-fullscreen")

            # Create a driver instance with the Chrome options
            driver = webdriver.Chrome(options=chrome_options)
            # Start a chrome driver
            driver = webdriver.Chrome()
            driver.get("http://localhost:33332/portal/portal.jsp")
            sel_core = SelCore(driver, logger)
            sel_core.logger.debug(f"Starting test case for {elem}")

            # Log in
            sel_core.screenshot("loginScreen.png")
            sel_core.login("demo demo123")

            # Click on import button and open up import textarea
            file_elem = sel_core.getitem(
                "XPATH (//div[@class='portal_menubar_menu'])[1]"
            )
            sel_core.click(file_elem)
            import_elem = sel_core.getitem(
                "XPATH //td[@class='menu_item_text' and contains(text(), 'Import')]"
            )
            sel_core.click(import_elem)

            layout_path = f"layouts/layout_{elem}.json"
            if not os.path.exists(layout_path):
                raise Exception("Layout file does not exist, please check")
            with open(layout_path, "r") as f:
                sel_core.import_layout(f, elem)
                generateExcel.main(elem, f"screenshot_{elem}.png")

            sel_core.check_pop()
            sel_core.logout()
            sel_core.logger.debug(f"Gracefully shutting down test case for {elem}")

        finally:
            driver.delete_all_cookies()
            time.sleep(5)


if __name__ == "__main__":
    main()
