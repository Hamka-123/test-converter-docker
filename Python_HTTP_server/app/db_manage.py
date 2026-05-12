import sys
import importlib
from dependencies import repo, connector

def main():
    if len(sys.argv) < 3:
        print("Usage: python db_manage.py migrate <migration_name>")
        print("Example: python db_manage.py migrate m001_initial")
        return

    command = sys.argv[1]
    migration_name = sys.argv[2]

    
    if command == "init":
        repo.create_schema()
        print("🚀 База данных инициализирована (таблицы созданы).")


    if command == "migrate":
        try:
            # Динамически импортируем указанный файл из папки migrations
            module_path = f"data.migrations.{migration_name}"
            migration = importlib.import_module(module_path)
            
            # Запускаем функцию apply
            migration.apply(connector)
            print(f"✨ Migration '{migration_name}' applied successfully!")
        except ImportError:
            print(f"❌ Error: Migration '{migration_name}' not found in data/migrations/")
        except Exception as e:
            print(f"💥 Migration failed: {e}")
            

if __name__ == "__main__":
    main()
    


#     Запуск миграции:
# python db_manage.py migrate (сидя внутри контейнера /app).
# DB_TYPE=mysql python db_manage.py migrate m001_initial

# DB_TYPE ?
# Задача	Что указать в DB_TYPE	Что делает скрипт
# Переезд в облако/Docker	mysql	Берет данные из файла logs.db и пишет в MariaDB.
# Создание бэкапа в файл	mysql	Читает из MariaDB и записывает в файл logs_backup.db.
# Работа сервера на SQLite	sqlite	Сервер просто читает/пишет в локальный файл.
# Работа сервера на MariaDB	mysql	Сервер работает с полноценной БД в Docker.