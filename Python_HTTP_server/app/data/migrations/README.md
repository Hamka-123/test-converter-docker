# Запуск миграций

## Общая схема

Миграции запускаются через `db_manage.py` из корня проекта.

Команда принимает два аргумента:

```bash
python db_manage.py migrate <migration_name>
```

где `<migration_name>` — это имя файла из `data/migrations`, но без расширения `.py`.

## Важно

- Файл миграции должен находиться в папке `data/migrations`.
- Имя файла должно быть валидным Python-модулем:
  - разрешены буквы, цифры и `_`
  - дефисы `-` НЕ разрешены
- Например, файл `m001_from_sqlite_to_mariadb.py` импортируется как
  `data.migrations.m001_from_sqlite_to_mariadb`.

## Примеры

Запустить конкретную миграцию:

```bash
python db_manage.py migrate m001_from_sqlite_to_mariadb
```

Для миграции из SQLite в MariaDB обычно перед запуском задают переменную окружения:

```bash
DB_TYPE=mysql python db_manage.py migrate m001_from_sqlite_to_mariadb
```

## Полезно знать

- При попытке запустить миграцию с именем `m001-from-sqlite-to-mariadb` команда выдаст ошибку, потому что дефис не может использоваться в имени модуля.
- Если нужно быстро применить простой скрипт миграции, есть отдельный файл `data/migrations/migrate.py`.
- `db_manage.py` ожидает, что в модуле миграции есть функция `apply(connector)`.
