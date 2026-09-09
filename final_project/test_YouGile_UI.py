import pytest
from selenium import webdriver
from pages.page_company import YouGile_Main_Page
import time


def test_create_column(driver):
    main = YouGile_Main_Page(driver)
    name_column = "test_column"
    main.click_firs_project()
    main.create_column(name_column)
    assert main.is_colums_exist(name_column)
