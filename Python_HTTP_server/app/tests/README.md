# Тестирование проекта

## Требования

- Python 3.x
- `pytest`
- `mysql-connector-python`
- Доступная MariaDB/Mysql в окружении, если вы запускаете тесты с `DB_TYPE=mysql`

## Быстрый запуск

Из корня проекта выполните:

```bash
cd /app
python -m pytest -q
```

Это запустит все тесты в папке `tests`.

Чтобы увидеть вывод всех `print()` из тестов, добавьте флаг `-s`:

```bash
cd /app
python -m pytest -s
```

## Запуск конкретного теста

```bash
cd /app
python -m pytest tests/db_connector_test.py -q
python -m pytest tests/db_conn_tiny_test.py -q
python -m pytest tests/test_sql_connection.py -q
```

## Настройка среды

В проекте используется `data/db_connector.py`, который выбирает тип БД по переменной окружения `DB_TYPE`.

- По умолчанию используется `mysql`.
- Для SQLite укажите:

```bash
DB_TYPE=sqlite
```

- Для MySQL/MariaDB укажите:

```bash
DB_TYPE=mysql
DB_HOST=<адрес>
DB_USER=<пользователь>
DB_PASSWORD=<пароль>
DB_NAME=<имя_базы>
```

Пример для MariaDB:

```bash
cd /app
DB_TYPE=mysql DB_HOST=mariadb-server DB_USER=app_user DB_PASSWORD=app_password DB_NAME=currency_db python -m pytest -q
```

## Что проверяют тесты

- `tests/db_connector_test.py` проверяет, что при `DB_TYPE=mysql` коннектор из `dependencies` подключается к MySQL/MariaDB. Тест использует `monkeypatch.setenv` и `importlib.reload(dependencies)`, чтобы перезаписать окружение перед созданием коннектора.
- `tests/db_conn_tiny_test.py` проверяет фактический тип активного подключения, анализируя имя класса и модуля объекта соединения, а затем выполняет соответствующий запрос версии для SQLite или MySQL/MariaDB.
- `tests/test_sql_connection.py` не содержит обычных тестовых функций: при импорте он пытается подключиться к MariaDB и создать таблицу `table_test2`. Поэтому этот файл тоже требует доступной MariaDB и корректных параметров подключения.

## Полезные заметки

- В текущей реализации `DB_TYPE` по умолчанию равен `mysql`, поэтому даже без установки переменной окружения тесты будут пытаться подключиться к MySQL/MariaDB.
- Для SQLite-тестирования установите `DB_TYPE=sqlite` и убедитесь, что файл `data/logs.db` доступен.
- Если вы используете `pytest` внутри контейнера, запускайте команды из `/app`.
- Файл `tests/how_to_run.md` содержит краткую команду запуска; этот `README.md` описывает текущие особенности и поведение тестовой среды.
