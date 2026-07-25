# Интернет магазин 
Интернет магазин 

## Стек технологий

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT (python-jose)
* Argon2
* Docker

## Возможности

* Регистрация пользователей
* Авторизация через JWT токены
* Хеширование паролей (Argon2)
* Сохранение данных в PostgreSQL
* Миграции базы данных через Alembic
* Контейнеризация с Docker


## Запуск

Клонировать репозиторий:

```bash
git clone <repository_url>
cd project
```

Запустить приложение:

```bash
docker-compose up --build
```

## Миграции

```bash
alembic upgrade head
```

## Документация API

После запуска:

```text
http://localhost:8000/docs
```

## Статус проекта

🚧 Проект находится в разработке.

Реализовано:

* Авторизация и аутентификация
* Работа с PostgreSQL
* Docker-конфигурация
* Миграции Alembic


