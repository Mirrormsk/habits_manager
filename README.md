# Habits API

RESTful API для создания новых привычек. 
Проект содержит модели привычки, а также функционал напоминания о привычках.


## Docker
Для запуска через Docker выполните команду: 

```bash
docker compose up --build
```



## Первичная настройка
Установите зависимости:

```bash
poetry install
```

Примените миграции:

```bash
python3 manage.py migrate
```

Создание суперпользователя:

```bash
python3 manage.py csu
```

## Использование

При регистрации нового пользователя в ответе приходит ссылка-приглашение в telegram бот, пройдя по которой пользователь регистрирует свой Telegram аккаунт в системе.

Запуск celery и периодических задач:
```bash
make run-celery-and-beat
```

Запуск Django-сервера:
```bash
python3 manage.py runserver
```

Запуск тестов:
```bash
python manage.py test 
```