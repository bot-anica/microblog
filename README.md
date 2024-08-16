# Welcome to Microblog!

Для использования базы данных (SQLite) и выполнения миграций используются 2 библиотеки:
1. flask-sqlalchemy 
```shell
pip install flask-sqlalchemy
```
2. flask-migrate
```shell
pip install flask-migrate
```
---
#### Инициализация базы данных и репозитория миграций
```shell
flask db init
```
```
Creating directory '/Users/kostasavcenko/PycharmProjects/microblog/migrations' ...  done
  Creating directory '/Users/kostasavcenko/PycharmProjects/microblog/migrations/versions' ...  done
  Generating /Users/kostasavcenko/PycharmProjects/microblog/migrations/script.py.mako ...  done
  Generating /Users/kostasavcenko/PycharmProjects/microblog/migrations/env.py ...  done
  Generating /Users/kostasavcenko/PycharmProjects/microblog/migrations/README ...  done
  Generating /Users/kostasavcenko/PycharmProjects/microblog/migrations/alembic.ini ...  done
  Please edit configuration/connection/logging settings in
  '/Users/kostasavcenko/PycharmProjects/microblog/migrations/alembic.ini' before proceeding.
```
---
#### Миграция базы данных после внесения изменений в базу данных
1. Генерация миграции
```shell
flask db migrate -m "CHANGES DESCRIPTION"
```
```
flask db migrate -m "users table"

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_user_email'' on '('email',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_user_username'' on '('username',)'
  Generating
  /Users/kostasavcenko/PycharmProjects/microblog/migrations/versions/2930c7acca22_users_table.py ...  done
```
2. Применение миграции
```shell
flask db upgrade
```
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 2930c7acca22, users table
```
3. Отмена последней миграции
```shell
flask db downgrade
```
---
При работе с интерпретатором Python в терминале, приходится постоянно импортировать необходимые зависимости:
```
python3
Python 3.12.4 (main, Jun  7 2024, 04:37:10) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from app import db
>>> from app.models import User, Post
```
Чтобы избавится от необходимости импортов нужно использовать команду
```
flask shell
```
Тогда мы будем иметь доступ ко всему без импортов
```
flask shell
Python 3.12.4 (main, Jun  7 2024, 04:37:10) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
App: app
Instance: /Users/kostasavcenko/PycharmProjects/microblog/instance
```
```
>>> app
<Flask 'app'>
>>> users = User.query.all()
>>> users
[]
>>> User
<class 'app.models.User'>
>>> Post
<class 'app.models.Post'>
>>> db
<SQLAlchemy sqlite:////Users/kostasavcenko/PycharmProjects/microblog/app.db>
```
