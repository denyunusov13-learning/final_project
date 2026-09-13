Final Project: Automation Testing for YouGile API
Финальный проект по курсу автоматизации тестирования.
Цель — автоматизировать проверку базового функционала YouGile (создание, редактирование, удаление проектов, досок, колонок и задач) через API и UI.

Стек
Тестовый фреймворк: pytest (маркеры positive / negative)
Отчётность: allure-pytest
HTTP-клиент: requests
Генерация данных: Faker
UI-автоматизация: Selenium + webdriver-manager
Ручное API-тестирование: Postman (Collection Runner, негативные сценарии)
Версионирование: Git
Быстрый старт
bash
git clone <ссылка_на_репозиторий>
cd final_project
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
Создайте файл .env в корне проекта:

env
YOUGILE_TOKEN=ваш_токен_api
YOUGILE_PASS=ваш пароль от yougile
YOUGILE_EMAIL=ваш логин от yougile

Запуск тестов
bash
# Все тесты
pytest tests/ --alluredir=allure-results


# Просмотр отчёта
allure generate allure-results --clean -o allure-report
allure open allure-report
Структура проекта
text
final_project/
├── .gitignore
├── .env
├── requirements.txt
├── README.md
├── tests/
│   ├── conftest.py
│   ├── test_API_YouGile.py
│   └── test_UI_YouGile.py
├── pages/
    └── page_company.py

Что протестировано
Создание, редактирование, удаление проектов, досок, колонок, задач
Негативные сценарии: несуществующие ID, некорректные данные
UI-проверки через Selenium
Ручное API-тестирование в Postman (8 запросов, позитивные и негативные)