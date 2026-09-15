import os
import pytest
import requests
from faker import Faker
import allure

fake = Faker()

BASE_URL = "https://yougile.com/api-v2"
YOUGILE_TOKEN = os.getenv("YOUGILE_TOKEN", "")


@allure.epic("YouGile API v2")
@allure.feature("Проекты")
@allure.severity(allure.severity_level.BLOCKER)
def test_create_project(session, created_project):
    """Тест-кейс 1: Успешное создание проекта"""
    assert "id" in created_project
    assert created_project["id"]

    resp = session.get(f"{BASE_URL}/projects/{created_project['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created_project["id"]


@allure.epic("YouGile API v2")
@allure.feature("Колонки")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_column(session, created_column):
    """Тест-кейс 2: Успешное создание колонки"""
    assert "id" in created_column
    assert created_column["id"]

    resp = session.get(f"{BASE_URL}/columns/{created_column['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == created_column["title"]


@allure.epic("YouGile API v2")
@allure.feature("Колонки")
@allure.severity(allure.severity_level.NORMAL)
def test_update_column_title_and_color(session, created_column):
    """Тест-кейс 3: Изменение названия и цвета колонки (цвет = 5)"""
    new_title = f"{fake.city()} Column {fake.random_int(1, 50)}"
    payload = {"title": new_title, "color": 5}

    resp = session.put(f"{BASE_URL}/columns/{created_column['id']}", json=payload)
    assert resp.status_code == 200
    assert resp.json()["id"] == created_column["id"]

    get_resp = session.get(f"{BASE_URL}/columns/{created_column['id']}")
    assert get_resp.status_code == 200
    updated = get_resp.json()
    assert updated["title"] == new_title
    assert updated["color"] == 5


@allure.epic("YouGile API v2")
@allure.feature("Задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task(session, created_column):
    """Тест-кейс 4: Успешное создание задачи"""
    payload = {
        "title": f"Task {fake.catch_phrase()} [{fake.isbn10()}]",
        "columnId": created_column["id"],
    }
    resp = session.post(f"{BASE_URL}/tasks", json=payload)
    assert resp.status_code == 201
    task = resp.json()
    assert "id" in task
    assert task["id"]

    get_resp = session.get(f"{BASE_URL}/tasks/{task['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == payload["title"]


@allure.epic("YouGile API v2")
@allure.feature("Колонки")
@allure.severity(allure.severity_level.MINOR)
def test_update_column_nonexistent_id(session):
    """Тест-кейс 5: Изменение колонки с несуществующим ID (id = 123)"""
    payload = {"title": f"Ghost Column {fake.name()}", "color": 1}
    resp = session.put(f"{BASE_URL}/columns/123", json=payload)
    assert resp.status_code in (400, 404)


@allure.epic("YouGile API v2")
@allure.feature("Проекты")
@allure.severity(allure.severity_level.NORMAL)
def test_create_project_empty_title(session):
    """Тест-кейс 6: Создание проекта с пустым title"""
    resp = session.post(f"{BASE_URL}/projects", json={"title": ""})
    assert resp.status_code in (400, 422)
