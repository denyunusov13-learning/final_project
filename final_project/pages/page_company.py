from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.keys import Keys

class YouGile_Main_Page:
    """Page Object главной страницы YouGile /team/."""

    URL = "https://ru.yougile.com/team/"

    # локаторы взаимодействия с проектами
    EXAMPLE_PROJECT = (By.XPATH, "//div[@data-itemid='18f57770-ccd3-4010-a7bc-224a0170ee1a']")
    CREATE_NEW_PROJECT = (By.XPATH, "//div[@data-testid='add-project-button'")
    CREATE_PR_WITH_TASKS = (By.XPATH, "//div[@data-testid='menu-item-add-default-project'")
    PROJECT_NAME_FIELD = (By.XPATH, "//input[@placeholder='Введите название проекта…']")
    ADD_BUTTON = (By.XPATH, "//div[@role='button' and contains(., 'Добавить проект с задачами')]")

    # локаторы взаимодействия с колонками
    NEW_COLUMN = (By.XPATH, "//div[@role='button' and contains(., 'Создать колонку')]")
    COLUMN_NAME_FIELD = (By.XPATH, "//textarea[@placeholder='Введите имя колонки…']")
    COLUMN_ICON_BTN = None
    DELETE_COLUMN_BTN = (By.XPATH, "//div[@data-testid='menu-item-delete'")
    CONFIRM_DELETE_COLUMN = (By.XPATH, "//div[@role='button' and contains(., 'Удалить')]")

    # локаторы взаимодействия с задачами
    NEW_TASK = (By.XPATH, "//div[@data-testid='link-button-new'")
    TASK_NAME_FIELD = (By.XPATH, "//div[@data-testid='board-task-input-name'")

    # общие локаторы
    MY_COMPANY_BTN = (By.XPATH, "//div[@data-testid='my-company-item'")
    FIRST_TEST_PROJECT = (By.XPATH, "//div[@data-testid='project-item'][2]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _click(self, locator: tuple) -> None:
        """Метод-помощник, нажимающик на кнопку по локатору"""
        with allure.step(f"Кликнуть по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

    def _input(self, locator: tuple, text: str) -> None:
        """Метод-помощник, заполняющий поле по локатору"""
        with allure.step(f"Ввести текст '{text}' в поле: {locator}"):
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)

    def create_project(self, name: str) -> None:
        with allure.step(f"Создать проект '{name}'"):
            self._click(CREATE_NEW_PROJECT)        

    def delete_project(self, name: str) -> None:
        with allure.step(f"Удалить проект '{name}'"):
            project_to_delete = self.wait.until(EC.element_to_be_clickable())

    def create_column(self, name: str) -> None:
        with allure.step(f"Создать колонку '{name}'"):
            self._click(self.NEW_COLUMN)
            textarea_field = self.wait.until(EC.element_to_be_clickable(self.COLUMN_NAME_FIELD))
            textarea_field.clear()
            textarea_field.send_keys(name)
            textarea_field.send_keys(Keys.RETURN)

    def is_colums_exist(self, name):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[text()='{name}']")))

    def delete_column(self, name: str) -> None:
        with allure.step(f"Удалить колонку '{name}'"):
            column_to_delete = self.wait_until(EC.element_to_be_clickable())

    def click_firs_project(self):
        self._click(self.FIRST_TEST_PROJECT)

    def click_column(self):
        
        self.driver.execute_cdp_cmd('Debugger.enable', {})
        self.driver.execute_cdp_cmd('Debugger.pause', {})
        pass


    # def create_task(se)lf, name: str, column_name: str) -> None:
    #     with allure.step(f"Создать задачу '{name}'"):
    #     pass

    # def delete_task(self, name: str) -> None:
    #     with allure.step(f"Удалить задачу '{name}'"):
