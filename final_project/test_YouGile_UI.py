import pytest
from selenium import webdriver
from pages.page_company import YouGile_Main_Page
import time


def test_create_project(driver):
    main = YouGile_Main_Page(driver)
    name_project = "test_project_first"
    main.create_project(name_project)
    main.delete_project(name_project)


def test_create_column(driver):
    main = YouGile_Main_Page(driver)
    name_project = "test_project_first"
    name_column = "test_column"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    assert main.is_column_exist(name_column), f"Колонки '{name_column}' нет в проекте"
    main.delete_project(name_project)


def test_create_task(driver):
    main = YouGile_Main_Page(driver)
    name_project = "test_project_first"
    name_column = "test_column"
    name_task = "test_task"
    main.create_project(name_project)
    main.create_column(name_project, name_column)
    main.create_task(name_project, name_column, name_task)
    assert main.is_task_exist(name_task), f"Задача '{name_task}' не найдена в колонке"
    main.delete_project(name_project)
