import pytest
from selenium import webdriver
from pages.page_company import YouGile_Main_Page
from faker import Faker
import allure


fake = Faker()


@allure.epic("YouGile UI")
@allure.feature("Проекты")
@allure.severity(allure.severity_level.BLOCKER)
def test_create_project(driver):
    """Тест-кейс 1: Успешное создание нового проекта"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    main.create_project(name_project)
    assert main.is_project_exist(name_project), f"Проект '{name_project}' не найден"
    main.delete_project(name_project)


@allure.epic("YouGile UI")
@allure.feature("Колонки")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_column(driver):
    """Тест-кейс 2: Успешное создание колонки в проекте"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    name_column = f"Column {fake.word().capitalize()}"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    assert main.is_column_exist(name_column), f"Колонка '{name_column}' не найдена"
    main.delete_project(name_project)


@allure.epic("YouGile UI")
@allure.feature("Задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task(driver):
    """Тест-кейс 3: Успешное создание задачи в колонке"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    name_column = f"Column {fake.word().capitalize()}"
    name_task = f"Task {fake.word().capitalize()}"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    main.create_task(name_project, name_column, name_task)
    assert main.is_task_exist(name_task), f"Задача '{name_task}' не найдена"
    main.delete_project(name_project)


@allure.epic("YouGile UI")
@allure.feature("Проекты")
@allure.severity(allure.severity_level.NORMAL)
def test_rename_project(driver):
    """Тест-кейс 4: Успешное изменение имени проекта"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    new_name = f"Project {fake.word().capitalize()}"
    main.create_project(name_project)
    main.rename_project(name_project, new_name)
    assert main.is_project_exist(new_name), f"Проект '{new_name}' не найден после переименования"
    main.delete_project(new_name)


@allure.epic("YouGile UI")
@allure.feature("Колонки")
@allure.severity(allure.severity_level.NORMAL)
def test_update_column(driver):
    """Тест-кейс 5: Успешное изменение колонки (название и цвет)"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    name_column = f"Column {fake.word().capitalize()}"
    new_column_name = f"Column {fake.word().capitalize()}"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    main.update_column(name_project, name_column, new_column_name, 5)
    assert main.is_column_exist(new_column_name), f"Колонка '{new_column_name}' не найдена после изменения"
    main.delete_project(name_project)


@allure.epic("YouGile UI")
@allure.feature("Задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_task(driver):
    """Тест-кейс 6: Успешное удаление задачи"""
    main = YouGile_Main_Page(driver)
    name_project = f"Project {fake.word().capitalize()}"
    name_column = f"Column {fake.word().capitalize()}"
    name_task = f"Task {fake.word().capitalize()}"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    main.create_task(name_project, name_column, name_task)
    assert main.is_task_exist(name_task), f"Задача '{name_task}' не найдена перед удалением"
    main.delete_task(name_task)
    assert not main.is_task_exist(name_task), f"Задача '{name_task}' всё ещё существует"
    main.delete_project(name_project)
