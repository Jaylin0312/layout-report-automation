from selClass import SelCore
from selenium import webdriver
import generateLayout
import time
import os
import logging


def count_file():
    dir_path = r"dir of your layouts folder"
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


def main():
    # Generate layout files
    generateLayout.main()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    # Count number of files in layouts dir
    counter = count_file()

    # Start a chrome driver
    driver = webdriver.Chrome()
    driver.get("AMI URL goes here")
    sel_core = SelCore(driver, logger)
    sel_core.logger.debug(f"Starting test case {i}")

    # For loop to start and close the process for each json test file
    for i in range(counter):
        try:
            # Log in
            sel_core.screenshot("loginScreen.png")
            sel_core.login("your username your password")

            # Click on import button and open up import textarea
            file_elem = sel_core.getitem(
                "XPATH (//div[@class='portal_menubar_menu'])[1]"
            )
            sel_core.click(file_elem)
            import_elem = sel_core.getitem(
                "XPATH //td[@class='menu_item_text' and contains(text(), 'Import')]"
            )
            sel_core.click(import_elem)

            # Import layout
            layout_path = f"layouts/layout{i}.json"
            if not os.path.exists(layout_path):
                raise Exception("Layout file does not exist, please check")
            with open(layout_path, "r") as f:
                sel_core.import_layout(f, i)

            # Log out
            sel_core.check_pop()
            sel_core.logout()
            sel_core.logger.debug(f"Gracefully shutting down test case {i}")

        finally:
            driver.delete_all_cookies()
            time.sleep(3)


if __name__ == "__main__":
    main()
