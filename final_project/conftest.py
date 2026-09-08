import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get("https://ru.yougile.com/")

    email_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='example@mail.ru']")))
    email_field.clear()
    email_field.send_keys(os.getenv("YOUGILE_LOGIN"))

    password_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Введите пароль']")))
    password_field.clear()
    password_field.send_keys(os.getenv("YOUGILE_PASSWORD"))

    login_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[role='button']")))
    login_btn.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Моя компания')]")))

    yield driver
    driver.quit()
