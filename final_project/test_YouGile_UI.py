import pytest
from selenium import webdriver
from pages.page_company import YouGile_Main_Page
import time


def test_create_column(self, driver):
    main = YouGile_Main_Page(driver)

    time.sleep(5)
