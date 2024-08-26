# Welcome to Microblog!

## Заметки

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
---
## Назначение переменных окружения для отправки писем на почту

⚠️ **Google не пропускает отправку писем, поэтому используем другие почты, например, Outlook**

```shell
export MAIL_SERVER=smtp-mail.outlook.com
```
```shell
export MAIL_PORT=587
```
```shell
export MAIL_USE_TLS=1
```
```shell
export MAIL_USERNAME=your-mail@outlook.com
```
```shell
export MAIL_PASSWORD=your-password
```

⚠️ Не забываем указать **your-mail@outlook.com** в переменной **ADMINS** в **config.py**

---

## Добавление переводов для нового языка и для существующего

### Маркировка текстов для перевода в исходном коде Python

1. В config.py добавить нужный язык
```python
LANGUAGES = ['en', 'es']
```

2. Добавить переводы в коде:
    - для обычных переводов
        ```python
        flash(_('Your post is now live!'))
        ```
        ```python
        flash(_('User %(username)s not found.', username=username))
        ```
        
    - для переводов, которые назначаются вне запроса, как правило, когда приложение запускается, поэтому в то время, когда эти тексты оцениваются, нет способа узнать, какой язык использовать
        ```python
        from flask_babel import lazy_gettext as _l
        
        class LoginForm(FlaskForm):
            username = StringField(_l('Username'), validators=[DataRequired()])
            # ...
        ```
        ```python
        login = LoginManager(app)
        login.login_view = 'login'
        login.login_message = _l('Please log in to access this page.')
        ```

### Разметка текстов для перевода в шаблонах

```html
<h1>{{ _('File Not Found') }}</h1>
```
```html
<h1>{{ _('Hi, %(username)s!', username=current_user.username) }}</h1>
```

### Извлечение текста для перевода

Чтобы извлечь все тексты в .pot файл, вы можете использовать следующую команду:

```shell
pybabel extract -F babel.cfg -k _l -o messages.pot .
```

Команда pybabel extract считывает файл конфигурации, указанный в параметре -F, а затем сканирует все файлы py и html в каталогах, соответствующих настроенным источникам, начиная с каталога, указанного в команде (текущий каталог или . в этом случае.) По умолчанию, pybabel будем искать _() как текстовый маркер, но я также использовал lazy вариант, который я импортировал как _l(), так что мне нужно сказать об этом инструменту поиска опцией -k _l. Параметр -o указывает имя выходного файла.


Должен отметить, что messages.pot не является файлом, который должен быть включен в проект. Это файл, который можно легко регенерировать в любое время, просто выполнив команду выше снова. Таким образом, нет необходимости передавать этот файл в систему управления версиями.

### Создание перевода для каждого языка

Следующим шагом в процессе является создание перевода для каждого языка, который будет поддерживаться в дополнение к базовому, который в данном случае английский. Я сказал, что собираюсь начать с добавления испанского языка (код языка es), так что команда, которая делает это:

```shell
pybabel init -i messages.pot -d app/translations -l ru
```
```shell
pybabel init -i messages.pot -d app/translations -l en
```
```shell
pybabel init -i messages.pot -d app/translations -l ua
```

Команда pybabel init принимает файл messages.pot в качестве входных данных и создает новый каталог для определенного языка, указанного в параметре -l в каталог, указанный в параметре -d. Я буду сохранять все переводы в директории app/translations, потому что там Flask-Babel будет искать файлы перевода по умолчанию. Команда создаст подкаталог es внутри этого каталога для данных на испанском. В частности, там появится новый файл с названием app/translations/es/LC_MESSAGES/messages.po. То есть там, где переводы должны быть сделаны.

### Добавление/редактирование переводов

В файлах **messages.pot** в папке **app/translations** для нужных языков добавить переводы. Эти генерированные файлы содержат строки **msgid**, которые содержат текст на базовом языке, а строки **msgstr** содержат пустые строки. В этих пустых строках (**msgstr**) нужно указать перевод на целевом языке.

```
#: app/email.py:21
msgid "[Microblog] Reset Your Password"
msgstr ""

#: app/forms.py:12 app/forms.py:19 app/forms.py:50
msgid "Username"
msgstr ""

#: app/forms.py:13 app/forms.py:21 app/forms.py:43
msgid "Password"
msgstr ""
```

### Применение переводов

Файл **messages.po** -это своего рода файл-источник для переводов. Если вы хотите начать использовать эти переведенные тексты, то файл должен быть скомпилирован в формат, который эффективен для использования приложением во время выполнения. Чтобы собрать все переводы для приложения, вы можете использовать команду компиляции pybabel compile следующим образом:

```shell
pybabel compile -d app/translations
```

Эта операция добавляет файл **messages.mo** рядом с messages.po в каждом языковом репозитории. Файл **.mo** — это файл, который **Flask-Babel** будет использовать для загрузки переводов в приложение.
