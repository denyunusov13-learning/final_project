import os

import pytest
import requests
from faker import Faker

fake = Faker()

BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
API_KEY = os.getenv("YOUGILE_API_KEY", "")


# ─────────────────────────────────────────────
#  Фикстуры
# ─────────────────────────────────────────────

@pytest.fixture
def session():
    """Авторизованная сессия с общими заголовками."""
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })
    return s


@pytest.fixture
def created_project(session):
    """Создаёт проект, отдаёт его данные, затем удаляет."""
    project_title = f"Project {fake.word().capitalize()} {fake.random_int(100, 999)}"
    payload = {"title": project_title}

    resp = session.post(f"{BASE_URL}/projects", json=payload)
    assert resp.status_code == 201, f"Не удалось создать проект: {resp.text}"
    project = resp.json()
    yield project
    # teardown — удаляем проект
    session.put(f"{BASE_URL}/projects/{project['id']}", json={"deleted": True})


@pytest.fixture
def created_board(session, created_project):
    """Создаёт доску внутри проекта, отдаёт её данные."""
    board_title = f"Board {fake.company_prefix()} {fake.color_name()}"
    payload = {"title": board_title}

    resp = session.post(f"{BASE_URL}/boards", json=payload)
    assert resp.status_code == 201, f"Не удалось создать доску: {resp.text}"
    board = resp.json()
    yield board
    # teardown — удаляем доску
    session.put(f"{BASE_URL}/boards/{board['id']}", json={"deleted": True})


@pytest.fixture
def created_column(session, created_board):
    """Создаёт колонку внутри доски, отдаёт её данные."""
    column_title = f"{fake.job().replace(' ', '')} To Do"
    payload = {
        "title": column_title,
        "color": 2,
        "boardId": created_board["id"],
    }
    resp = session.post(f"{BASE_URL}/columns", json=payload)
    assert resp.status_code == 201, f"Не удалось создать колонку: {resp.text}"
    column = resp.json()
    yield column
    # teardown — удаляем колонку
    session.put(f"{BASE_URL}/columns/{column['id']}", json={"deleted": True})


# ─────────────────────────────────────────────
#  Тест-кейсы
# ─────────────────────────────────────────────

class TestCreateProject:
    """Тест-кейс 1: Успешное создание проекта через API"""

    def test_create_project_success(self, session, created_project):
        assert "id" in created_project
        assert created_project["id"]
        # Доп. проверка: GET на созданный проект
        resp = session.get(f"{BASE_URL}/projects/{created_project['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created_project["id"]


class TestCreateColumn:
    """Тест-кейс 2: Успешное создание колонки через API"""

    def test_create_column_success(self, session, created_column):
        assert "id" in created_column
        assert created_column["id"]
        # Проверяем, что колонка доступна по GET
        resp = session.get(f"{BASE_URL}/columns/{created_column['id']}")
        assert resp.status_code == 200
        assert resp.json()["title"] == created_column["title"]


class TestUpdateColumn:
    """Тест-кейс 3: Успешное изменение названия и цвета колонки (цвет = 5)"""

    def test_update_column_title_and_color(self, session, created_column):
        new_title = f"{fake.city()} Column {fake.random_int(1, 50)}"
        payload = {
            "title": new_title,
            "color": 5,
        }
        resp = session.put(f"{BASE_URL}/columns/{created_column['id']}", json=payload)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["title"] == new_title
        assert updated["color"] == 5


class TestCreateTask:
    """Тест-кейс 4: Успешное создание задачи через API"""

    def test_create_task_success(self, session, created_column):
        task_title = f"Task {fake.catch_phrase()} [{fake.isbn10()}]"
        payload = {
            "title": task_title,
            "columnId": created_column["id"],
        }
        resp = session.post(f"{BASE_URL}/tasks", json=payload)
        assert resp.status_code == 201
        task = resp.json()
        assert "id" in task
        assert task["id"]

        # Проверка: задача доступна по GET
        get_resp = session.get(f"{BASE_URL}/tasks/{task['id']}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == payload["title"]


class TestUpdateColumnNotFound:
    """Тест-кейс 5: Изменение колонки с несуществующим ID (id = 123)"""

    def test_update_column_nonexistent_id(self, session):
        payload = {
            "title": f"Ghost Column {fake.name()}",
            "color": 1,
        }
        resp = session.put(f"{BASE_URL}/columns/123", json=payload)
        # YouGile возвращает 400 / 404 для несуществующего ресурса
        assert resp.status_code in (400, 404)
        body = resp.json()
        assert "error" in body or "message" in body or resp.text


class TestCreateProjectEmptyTitle:
    """Тест-кейс 6: Создание проекта с пустым полем title"""

    def test_create_project_empty_title(self, session):
        payload = {"title": ""}
        resp = session.post(f"{BASE_URL}/projects", json=payload)
        # Ожидаем ошибку валидации
        assert resp.status_code in (400, 422)
        body = resp.json()
        assert "error" in body or "message" in body or resp.text






import os

import pytest
import requests
from faker import Faker
import allure

fake = Faker()

BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
API_KEY = os.getenv("YOUGILE_API_KEY", "")


# ─────────────────────────────────────────────
#  Фикстуры
# ─────────────────────────────────────────────

@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {API_KEY}",
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
    session.put(f"{BASE_URL}/projects/{project['id']}", json={"deleted": True})


@pytest.fixture
def created_board(session, created_project):
    payload = {"title": f"Board {fake.company_prefix()} {fake.color_name()}"}
    resp = session.post(f"{BASE_URL}/boards", json=payload)
    assert resp.status_code == 201, f"Не удалось создать доску: {resp.text}"
    board = resp.json()
    yield board
    session.put(f"{BASE_URL}/boards/{board['id']}", json={"deleted": True})


@pytest.fixture
def created_column(session, created_board):
    payload = {
        "title": f"{fake.job().replace(' ', '')} To Do",
        "color": 2,
        "boardId": created_board["id"],
    }
    resp = session.post(f"{BASE_URL}/columns", json=payload)
    assert resp.status_code == 201, f"Не удалось создать колонку: {resp.text}"
    column = resp.json()
    yield column
    session.put(f"{BASE_URL}/columns/{column['id']}", json={"deleted": True})


# ─────────────────────────────────────────────
#  Тест-кейсы
# ─────────────────────────────────────────────

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
    updated = resp.json()
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