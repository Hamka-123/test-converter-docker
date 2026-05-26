import os
import pytest
# Импортируем именно ваш модуль db_connector
from dependencies import connector 

def test_db_connector_reads_env_and_connects_to_mariadb(monkeypatch):
    """
    Тест проверяет, что при DB_TYPE=mariadb (или mysql)
    db_connector корректно инициализирует подключение к MariaDB.
    """
    
    # 1. С помощью monkeypatch гарантируем, что DB_TYPE установлен в mariadb
    # Это изолирует тест от того, что написано в вашем реальном файле .env
    monkeypatch.setenv("DB_TYPE", "mariadb")
    
    # Можно также временно прописать тестовые доступы, если это необходимо:
    # monkeypatch.setenv("DB_HOST", "localhost")
    # monkeypatch.setenv("DB_USER", "test_user")
    
    # 2. Действие: вызываем подключение
    try:
        connection = connector.get_connection()
    except Exception as e:
        pytest.fail(f"Не удалось установить соединение при DB_TYPE=mariadb: {e}")
        
    cursor = connection.cursor()
    
    try:
        # 3. Проверка 1: Проверяем класс объекта соединения.
        # Для MariaDB/MySQL это обычно объекты с "mysql" в названии класса
        connection_class = type(connection).__name__.lower()
        assert "mysql" in connection_class or "mariadb" in connection_class, \
            f"Ожидалось подключение к MariaDB, но получен класс {type(connection).__name__}"
            
        # 4. Проверка 2: Делаем запрос к самой БД, чтобы убедиться, что это MariaDB
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()[0].lower()
        
        # В строке версии у MariaDB практически всегда есть упоминание "mariadb"
        assert "mariadb" in db_version, f"База данных ответила, но это не MariaDB: {db_version}"
        
        print(f"\n[УСПЕХ] Коннектор прочитал DB_TYPE и успешно подключился к {db_version}")
        
    finally:
        # 5. Обязательно закрываем за собой ресурсы
        cursor.close()
        connection.close()