from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.keys import Keys
import time


class YouGile_Main_Page:
    """Page Object главной страницы YouGile /team/."""

    URL = "https://ru.yougile.com/team/"

    # --- Локаторы: проекты ---
    CREATE_NEW_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='add-project-button']",
    )
    CREATE_PR_WITH_TASKS: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-add-default-project']",
    )
    PROJECT_NAME_FIELD: tuple[str, str] = (
        By.XPATH,
        "//input[@placeholder='Введите название проекта…']",
    )
    ADD_BUTTON: tuple[str, str] = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Добавить проект с задачами')]",
    )
    PROJECT_SETTINGS_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='project-card-menu-button']",
    )
    SETTINGS_DELETE_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-remove']",
    )
    SETTINGS_EDITED_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-edit']",
    )
    CONFIRM_DELETE_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Удалить')]",
    )
    SETTINGS_EDIT_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='project-card-menu-button']",
    )

    # --- Локаторы: колонки ---
    NEW_COLUMN: tuple[str, str] = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Создать колонку')]",
    )
    COLUMN_NAME_FIELD: tuple[str, str] = (
        By.XPATH,
        "//textarea[@placeholder='Введите имя колонки…']",
    )
    DELETE_COLUMN_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-delete']",
    )
    CONFIRM_DELETE_COLUMN: tuple[str, str] = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Удалить')]",
    )
    COLUMN_MENU_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[contains(@class, 'hint__cnt') and contains(@class, 'group/icon-button')]",
    )
    COLUMN_EDIT_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-rename']",
    )
    COLUMN_COLOR_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[contains(text(), 'Цвет колонки')]/following::div[position()=6]",
    )

    # --- Локаторы: задачи ---
    NEW_TASK: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='link-button-new' and contains(., 'Добавить задачу')]",
    )
    TASK_NAME_FIELD: tuple[str, str] = (
        By.XPATH,
        "//textarea[contains(@placeholder, 'название задачи')]",
    )
    TASK_DELETE_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='menu-item-delete']",
    )
    CONFIRM_DELETE_TASK: tuple[str, str] = (
        By.XPATH,
        "//div[@role='button' and contains(., 'Удалить')]",
    )

    # --- Прочие локаторы ---
    MY_COMPANY_BTN: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='my-company-item']",
    )
    FIRST_TEST_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-testid='project-item'][2]",
    )
    EXAMPLE_PROJECT: tuple[str, str] = (
        By.XPATH,
        "//div[@data-itemid='18f57770-ccd3-4010-a7bc-224a0170ee1a']",
    )

    def __init__(self, driver: WebDriver) -> None:
        """Инициализация Page Object.

        Args:
            driver: Экземпляр WebDriver для управления браузером.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    def _click(self, locator: tuple[str, str]) -> None:
        """Вспомогательный метод: ждёт кликабельности элемента
        и кликает по нему.

        Args:
            locator: Кортеж (By, значение) для поиска элемента.
        """
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

    def _input(self, locator: tuple[str, str], text: str) -> None:
        """Вспомогательный метод: очищает поле и вводит в него текст.

        Args:
            locator: Кортеж (By, значение) для поиска элемента.
            text: Текст для ввода.
        """
        with allure.step(f"Ввод текста '{text}' в поле: {locator}"):

            with allure.step("Очистка поля ввода"):
                element_to_clear = self.wait.until(
                    EC.visibility_of_element_located(locator)
                )
                element_to_clear.clear()
            with allure.step(f"Перепоиск элемента и отправка текста '{text}'"):
                element_to_type = self.wait.until(
                    EC.visibility_of_element_located(locator)
                )
                element_to_type.send_keys(text)

    def create_project(self, name: str) -> None:
        """Создаёт новый проект с указанным именем.

        Args:
            name: Имя создаваемого проекта.
        """
        with allure.step(f"Создать проект '{name}'"):
            self._click(self.CREATE_NEW_PROJECT)
            self._click(self.CREATE_PR_WITH_TASKS)
            self._input(self.PROJECT_NAME_FIELD, name)
            self._click(self.ADD_BUTTON)

    def get_project_locator(self, name: str) -> tuple[str, str]:
        """Возвращает локатор проекта по его имени.

        Args:
            name: Имя проекта для поиска.

        Returns:
            Кортеж (By.XPATH, xpath-строка).
        """
        return (
            By.XPATH,
            f"//div[@data-testid='project-item' and .//*[text()='{name}']]",
        )

    def is_project_exist(self, name: str) -> bool:
        """Проверяет, существует ли проект с указанным именем.

        Args:
            name: Имя проекта для проверки.

        Returns:
            True, если проект найден; False, если не найден.
        """
        with allure.step(f"Проверить наличие проекта '{name}'"):
            project_locator = self.get_project_locator(name)
            try:
                self.wait.until(EC.visibility_of_element_located(project_locator))
                return True
            except Exception:
                return False

    def rename_project(self, old_name: str, new_name: str) -> None:
        """Переименовывает проект.

        Args:
            old_name: Текущее имя проекта.
            new_name: Новое имя проекта.
        """
        with allure.step(f"Переименовать проект '{old_name}' → '{new_name}'"):
            self._click(self.MY_COMPANY_BTN)
            project_locator = self.get_project_locator(old_name)
            self.wait.until(EC.visibility_of_element_located(project_locator))
            time.sleep(2)
            self._click(self.SETTINGS_EDIT_PROJECT)
            time.sleep(2)
            self._click(self.SETTINGS_EDITED_PROJECT)
            with allure.step(f"Безопасный ввод нового имени проекта: '{new_name}'"):
                field = self.wait.until(
                    EC.visibility_of_element_located(self.PROJECT_NAME_FIELD)
                )
                field.send_keys(Keys.CONTROL + "a")
                field.send_keys(Keys.BACKSPACE)
                field.send_keys(new_name)
                field.send_keys(Keys.RETURN)

    def delete_project(self, name: str) -> None:
        """Удаляет проект по его имени.
        Args:
            name: Имя проекта для удаления.
        """
        with allure.step("Удалить проект"):
            project_locator = self.get_project_locator(name)
            self._click(self.MY_COMPANY_BTN)
            self.wait.until(EC.visibility_of_element_located(project_locator))
            settings_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//*[@data-testid='project-card-menu-button']")
                )
            )
            settings_btn.click()
            self._click(self.SETTINGS_DELETE_PROJECT)
            self._click(self.CONFIRM_DELETE_PROJECT)

    def create_column(self, name_project: str, name_column: str) -> None:
        """Создаёт колонку в указанном проекте.

        Args:
            name_project: Имя проекта, в котором создаётся колонка.
            name_column: Имя создаваемой колонки.
        """
        with allure.step(f"Создать колонку '{name_column}' в проекте '{name_project}'"):
            self._click(self.get_project_locator(name_project))
            self._click(self.NEW_COLUMN)
            field = self.wait.until(EC.element_to_be_clickable(self.COLUMN_NAME_FIELD))
            self._input(self.COLUMN_NAME_FIELD, name_column)
            field.send_keys(Keys.RETURN)

    def is_column_exist(self, name_column: str) -> bool:
        """Проверяет, существует ли колонка с указанным именем.

        Args:
            name_column: Имя колонки для проверки.

        Returns:
            True, если колонка найдена; False, если не найдена.
        """
        with allure.step(f"Проверить наличие колонки '{name_column}'"):
            column_locator = (By.XPATH, f"//span[text()='{name_column}']")
            try:
                self.wait.until(EC.visibility_of_element_located(column_locator))
                return True
            except Exception:
                return False

    def update_column(
        self, name_project: str, name_column: str, new_name: str, color_index: int = 0
    ) -> None:
        """Изменяет название и цвет колонки.

        Args:
            name_project: Имя проекта, в котором находится колонка.
            name_column: Текущее имя колонки.
            new_name: Новое имя колонки.
            color_index: Индекс цвета.
        """
        with allure.step(
            f"Изменить колонку '{name_column}' → '{new_name}', цвет {color_index}"
        ):
            self._click(self.get_project_locator(name_project))
            self._click(
                (
                    By.XPATH,
                    f"//div[@data-testid='board-column' and contains(., '{name_column}')]"
                    "//div[contains(@class, 'group/icon-button')]",
                )
            )
            self._click(
                (
                    By.XPATH,
                    f"//div[contains(text(), 'Цвет колонки')]/following::div[position()={color_index}]",
                )
            )
            self._click(self.COLUMN_EDIT_BTN)
            with allure.step(f"Безопасный ввод нового имени колонки: '{new_name}'"):
                field = self.wait.until(
                    EC.visibility_of_element_located(self.COLUMN_NAME_FIELD)
                )
                field.send_keys(Keys.CONTROL + "a")
                field.send_keys(Keys.BACKSPACE)
                field.send_keys(new_name)
                field.send_keys(Keys.RETURN)

    def create_task(self, name_project: str, name_column: str, name_task: str) -> None:
        """Создаёт задачу в указанной колонке проекта.

        Args:
            name_project: Имя проекта.
            name_column: Имя колонки, в которой создаётся задача.
            name_task: Имя создаваемой задачи.
        """
        with allure.step(
            f"Создать задачу '{name_task}' в колонке '{name_column}' проекта '{name_project}'"
        ):
            new_task_in_name_column_locator = (
                By.XPATH,
                f"//div[@data-testid='board-column' and contains(., '{name_column}')]"
                "//div[@data-testid='link-button-new' and contains(., 'Добавить задачу')]",
            )
            self._click(new_task_in_name_column_locator)
            self._input(self.TASK_NAME_FIELD, name_task)
            task_field = self.wait.until(
                EC.element_to_be_clickable(self.TASK_NAME_FIELD)
            )
            task_field.send_keys(Keys.RETURN)

    def delete_task(self, name_task: str) -> None:
        """Удаляет задачу по её имени.

        Args:
            name_task: Имя задачи для удаления.
        """
        with allure.step(f"Удалить задачу '{name_task}'"):
            task_to_delete_locator = (
                By.XPATH,
                f"//div[@data-testid='tw-task-container' and contains(., '{name_task}')]"
                "//div[@data-testid='board-task-menu']",
            )
            self._click(task_to_delete_locator)
            self._click(self.TASK_DELETE_BTN)
            self._click(self.CONFIRM_DELETE_TASK)
            self.wait.until(EC.invisibility_of_element_located(task_to_delete_locator))

    def is_task_exist(self, name_task: str) -> bool:
        """Проверяет, существует ли задача с указанным именем.

        Args:
            name_task: Имя задачи для проверки.

        Returns:
            True, если задача найдена; False, если не найдена.
        """
        with allure.step(f"Проверить наличие задачи '{name_task}'"):
            task_locator = (
                By.XPATH,
                f"//div[@data-testid='tw-task-container' and contains(., '{name_task}')]",
            )
            try:
                self.wait.until(EC.visibility_of_element_located(task_locator))
                return True
            except Exception:
                return False
