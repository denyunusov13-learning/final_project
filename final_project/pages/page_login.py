from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Main_Shop_Page:

    EXAMPLE_PROJECT = (By.XPATH, "//div[@data-itemid='18f57770-ccd3-4010-a7bc-224a0170ee1a']")
    NEW_TASK = (By.XPATH, "//div[@data-testid='link-button-new'")
    NEW_COLUMN = (By.CSS_SELECTOR, ".hint__cnt")
    NEW_PROJECT = (By.XPATH, "//div[@data-testid='add-project-button'")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)