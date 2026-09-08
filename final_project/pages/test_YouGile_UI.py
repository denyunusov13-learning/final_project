import pytest
from selenium import webdriver
from page_company import Main_Page


EXAMPLE_PROJECT = (By.XPATH, "//div[@data-itemid='18f57770-ccd3-4010-a7bc-224a0170ee1a']")
NEW_TASK = (By.XPATH, "//div[@data-testid='link-button-new'")
NEW_COLUMN = (By.CSS_SELECTOR, ".hint__cnt")
NEW_PROJECT = (By.XPATH, "//div[@data-testid='add-project-button'")

def test_create_project(self, driver):
