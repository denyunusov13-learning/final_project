import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import requests
from faker import Faker

load_dotenv()
fake = Faker()

YOUGILE_TOKEN = os.getenv("YOUGILE_TOKEN", "")
BASE_URL = "https://yougile.com/api-v2"


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    driver.maximize_window()

    driver.get("https://ru.yougile.com/team/")

    email_field = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='example@mail.ru']")
        )
    )
    email_field.clear()
    email_field.send_keys(os.getenv("YOUGILE_EMAIL"))

    password_field = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Введите пароль']")
        )
    )
    password_field.clear()
    password_field.send_keys(os.getenv("YOUGILE_PASS"))

    login_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[role='button']"))
    )
    login_btn.click()

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Моя компания')]")
        )
    )

    yield driver
    driver.quit()


@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {YOUGILE_TOKEN}",
        "Content-Type": "application/json",
    })
    return s


@pytest.fixture
def created_project(session):
    payload = {"title": f"Project {fake.word().capitalize()} {fake.random_int(100, 999)}"}
    resp = session.post(f"{BASE_URL}/projects", json=payload)
    assert resp.status_code == 201, f"Не удалось создать проект: {resp.text}"
    project = resp.json()
    yield project


@pytest.fixture
def created_board(session, created_project):
    title_board = f"Board {fake.word()} {fake.color_name()}"
    payload = {
        "title": title_board,
        "projectId": created_project["id"],
    }
    resp = session.post(f"{BASE_URL}/boards", json=payload)
    assert resp.status_code == 201, f"Не удалось создать доску: {resp.text}"
    board = resp.json()
    board["title"] = title_board
    yield board


@pytest.fixture
def created_column(session, created_board):
    title_column = f"{fake.job().replace(' ', '')} To Do"
    payload = {
        "title": title_column,
        "boardId": created_board["id"]
    }
    resp = session.post(f"{BASE_URL}/columns", json=payload)
    assert resp.status_code == 201, f"Не удалось создать колонку: {resp.text}"
    column = resp.json()
    column["title"] = title_column
    yield column
