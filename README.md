Habit Tracker Backend
Это бэкенд-часть для трекера полезных привычек, 
реализованного с использованием Django и Django REST Framework (DRF). 
Проект создан как часть курсовой работы по разработке SPA веб-приложения для отслеживания привычек.

# **# Оглавление**

- [Функциональность](#Функциональность)
- [Требования](#Требования)
- [Установка](#Установка)
- [Запуск проекта](#Запуск-проекта)
- [Переменные окружения](#Переменные-окружения)
- [Тестирование](#Тестирование)
- [Запуск на удаленном сервере](#Тестирование)

# ****# Функциональность****

Проект включает следующие возможности:

- CRUD для управления привычками.
- Возможность указывать связанные приятные привычки и вознаграждения.
- Пагинация (вывод по 5 привычек на страницу).
- Регистрация и авторизация пользователей.
- Работа с публичными и приватными привычками.
- Интеграция с Telegram для отправки напоминаний.
- Асинхронные задачи с использованием Celery для рассылки уведомлений.
- CORS настройки для взаимодействия с фронтендом.
- Валидация для исключения конфликтующих данных о привычках.

# **## Требования**

Для работы проекта необходимы:

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- Redis (для Celery)
- PostgreSQL (или другая СУБД)
- Docker и Docker Compose (для деплоя)

# **## Установка**

1. Клонируйте репозиторий:

   git clone https://github.com/ваш_аккаунт/habit_tracker.git

2. Установите зависимости с помощью Poetry:

poetry install

3. Создайте файл .env для переменных окружения см. файл .env.sample

4. Выполните миграции базы данных:

poetry run python manage.py migrate

5. Создайте суперпользователя:

poetry run python manage.py createsuperuser

# **Запуск проекта**

1. Запустите сервер разработки Django:

poetry run python manage.py runserver

2. Запустите Celery для выполнения отложенных задач:

poetry run celery -A config worker --loglevel=INFO

3. Запустите Celery Beat для периодических задач:
4. 
poetry run celery -A config beat --loglevel=INFO

# **Тестирование**

Проект покрыт тестами. Для запуска тестов выполните команду:

poetry run python manage.py test

Также в проекте настроена проверка покрытия тестами с использованием coverage. 
Для запуска покрытия тестов выполните:

poetry run coverage run --source='.' manage.py test
poetry run coverage report

# **Запуск на удаленном сервере**

1. Установка Docker и Docker Compose
На сервере выполните следующие команды для установки Docker и Docker Compose:

sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt install docker-compose

2. Клонирование проекта
Клонируйте репозиторий на удаленный сервер:

git clone https://github.com/ваш_аккаунт/habit_tracker.git
cd habit_tracker

3. Настройка переменных окружения
Создайте файл .env на сервере, используя пример:

cp .env.sample .env
nano .env

Заполните необходимые переменные, включая данные для подключения к базе данных и Redis.

4. Запуск проекта
Используйте Docker Compose для запуска проекта. Все сервисы (Django, PostgreSQL, Redis, Celery) будут автоматически запущены:

docker-compose up --build -d


5. Миграции базы данных
Выполните миграции базы данных:

docker-compose run app poetry run python manage.py migrate

6. Создание суперпользователя
Создайте суперпользователя для доступа к административной панели:

docker-compose run app poetry run python manage.py createsuperuser

Теперь проект доступен по IP-адресу сервера на порте 8000. Вы можете открыть браузер и перейти по адресу:

http://your-server-ip:8000
