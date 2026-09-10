from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.keys import Keys

class YouGile_Main_Page:
    """Page Object главной страницы YouGile /team/."""

    URL = "https://ru.yougile.com/team/"

    # локаторы взаимодействия с проектами
    CREATE_NEW_PROJECT = (By.XPATH, "//div[@data-testid='add-project-button']")
    CREATE_PR_WITH_TASKS = (By.XPATH, "//div[@data-testid='menu-item-add-default-project']")
    PROJECT_NAME_FIELD = (By.XPATH, "//input[@placeholder='Введите название проекта…']")
    ADD_BUTTON = (By.XPATH, "//div[@role='button' and contains(., 'Добавить проект с задачами')]")
    PROJECT_SETTINGS_BTN = (By.XPATH, "//div[@data-testid='project-card-menu-button']")
    SETTINGS_DELETE_PROJECT = (By.XPATH, "//div[@data-testid='menu-item-remove']")
    CONFIRM_DELETE_PROJECT = (By.XPATH, "//div[@role='button' and contains(., 'Удалить')]")

    # локаторы взаимодействия с колонками
    NEW_COLUMN = (By.XPATH, "//div[@role='button' and contains(., 'Создать колонку')]")
    COLUMN_NAME_FIELD = (By.XPATH, "//textarea[@placeholder='Введите имя колонки…']")
    COLUMN_ICON_BTN = None
    DELETE_COLUMN_BTN = (By.XPATH, "//div[@data-testid='menu-item-delete']")
    CONFIRM_DELETE_COLUMN = (By.XPATH, "//div[@role='button' and contains(., 'Удалить')]")

    # локаторы взаимодействия с задачами
    NEW_TASK = (By.XPATH, "//div[@data-testid='link-button-new']")
    TASK_NAME_FIELD = (By.XPATH, "//div[@data-testid='board-task-input-name']")

    # прочие локаторы
    MY_COMPANY_BTN = (By.XPATH, "//div[@data-testid='my-company-item']")
    FIRST_TEST_PROJECT = (By.XPATH, "//div[@data-testid='project-item'][2]")
    EXAMPLE_PROJECT = (By.XPATH, "//div[@data-itemid='18f57770-ccd3-4010-a7bc-224a0170ee1a']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _click(self, locator: tuple) -> None:
        """Вспомогательный метод, кликающий по элементу
            с соответствющим локатором"""
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

    def _input(self, locator: tuple, text: str) -> None:
        """Вспомогательный метод, передающий в поле
            необходимый текст"""
        with allure.step(f"Ввод текста '{text}' в поле: {locator}"):
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)

    def create_project(self, name: str) -> None:
        """Метод создания проекта"""
        with allure.step(f"Создать проект '{name}'"):
            self._click(self.CREATE_NEW_PROJECT)
            self._click(self.CREATE_PR_WITH_TASKS)
            self._input(self.PROJECT_NAME_FIELD, name)
            self._click(self.ADD_BUTTON)

    def get_project_locator(self, name: str) -> tuple:
        return (By.XPATH, f"//div[@data-testid='project-item' and .//*[text()='{name}']]")

    def delete_project(self, name: str) -> None:
        """Метод удаления проекта.
            Передавай локатор конкретного проекта, который надо удалить"""
        with allure.step("Удалить проект"):
            project_locator = self.get_project_locator(name)
            self._click(self.MY_COMPANY_BTN)
            project_card = self.wait.until(
                EC.visibility_of_element_located(project_locator))
            settings_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//*[@data-testid='project-card-menu-button']")))
            settings_btn.click()
            self._click(self.SETTINGS_DELETE_PROJECT)
            self._click(self.CONFIRM_DELETE_PROJECT)

    def create_column(self, name_project: str, name_column: str) -> None:
        """Создает колонку 'name_column' в проекте 'name_project'"""
        with allure.step(f"Создать колонку '{name_column}'"):
            self._click(self.get_project_locator(name_project))
            self._click(self.NEW_COLUMN)
            field = self.wait.until(
                EC.element_to_be_clickable(self.COLUMN_NAME_FIELD))
            self._input(self.COLUMN_NAME_FIELD, name_column)
            field.send_keys(Keys.RETURN)

    def is_column_exist(self, name_column: str):
        """Возвращает булево значение, 
        в зависимости от наличия колонка 
        с  именем 'name'"""
        with allure.step(f"проверить наличие колонки '{name_column}'"):
            column_locator = (By.XPATH, f"//span[text()='{name_column}']")
            try:
                self.wait.until(EC.visibility_of_element_located(column_locator))
                return True
            except Exception:
                return False

    def create_task(self, name_project: str, name_column: str, name_task: str) -> None:
        """Создает задачу 'test_task' в колонке
        'name_column' проекта 'name_project'"""
        with allure.step(f"Создать задачу '{name_task}' в колонке '{name_column}' проект {name_project}"):
            column_locator = (By.XPATH, f"//span[text()='{name_column}']")
            column_elem = self.wait.until(EC.element_to_be_clickable(column_locator))
            column_elem.click(self.NEW_TASK)
            task_field = self.wait.until(
                            EC.element_to_be_clickable(self.TASK_NAME_FIELD))
            self._input(self.TASK_NAME_FIELD, name_task)
            task_field.send_keys(Keys.RETURN)

    def is_task_exist(self, name_task: str):
        """Возвращает булево значение, 
        в зависимости от наличия задачи 
        с  именем 'name_task'"""
        with allure.step(f"проверить наличие колонки '{name_task}'"):
            task_locator = (By.XPATH, f"//span[text()='{name_task}']")
            try:
                self.wait.until(EC.visibility_of_element_located(task_locator))
                return True
            except Exception:
                return False
            

    def delete_task(self, task_locator: tuple) -> None:
        with allure.step("Удалить задачу"):
            task_elem = self.wait.until(EC.element_to_be_clickable(task_locator))
            task_elem.click()  # и дальше по сценарию удаления