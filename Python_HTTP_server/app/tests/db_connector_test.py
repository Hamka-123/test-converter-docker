import os
import pytest
import importlib
# Импортируем ваш модуль db_connector
import dependencies

def test_db_connector_reads_env_and_connects_to_mariadb(monkeypatch):
    """
    Тест проверяет, что при DB_TYPE=mysql (или mariadb)
    db_connector корректно инициализирует подключение к MariaDB через mysql.connector.
    """
    
    # 1. С помощью monkeypatch гарантируем, что DB_TYPE установлен в mysql
    # Это изолирует тест от того, что написано в вашем реальном файле .env
    monkeypatch.setenv("DB_TYPE", "mysql")
    
    # СБИВАЕМ КЭШ ИМПОРТА VS CODE: принудительно перезагружаем модуль коннектора,
    # чтобы он прочитал новое окружение, созданное monkeypatch!
    importlib.reload(dependencies)
    
    # Вытаскиваем свежесозданный коннектор из перезагруженного модуля
    connector = dependencies.connector
    
    # Можно также временно прописать тестовые доступы, если это необходимо:
    # monkeypatch.setenv("DB_HOST", "localhost")
    # monkeypatch.setenv("DB_USER", "test_user")
    
    # 2. Действие: вызываем подключение
    try:
        connection = connector.get_connection()
    except Exception as e:
        pytest.fail(f"Не удалось установить соединение при DB_TYPE=mysql: {e}")
        
    cursor = connection.cursor()
    
    try:
        # 3. Проверка 1: Проверяем класс объекта соединения и его модуль.
        # У mysql.connector имя класса может быть просто "Connection", 
        # поэтому мы дополнительно проверяем имя модуля (__module__).
        connection_class = type(connection).__name__.lower()
        connection_module = type(connection).__module__.lower()
        
        assert "mysql" in connection_class or "mysql" in connection_module, \
            f"Ожидалось подключение к MySQL/MariaDB, но получен класс {connection_module}.{type(connection).__name__}"
            
        # 4. Проверка 2: Делаем запрос к самой БД, чтобы убедиться, что это MariaDB/MySQL
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()[0].lower()
        
        # Так как в докере у вас крутится MariaDB, в версии будет слово 'mariadb' или 'mysql'
        assert "mariadb" in db_version or "mysql" in db_version, \
            f"База данных ответила, но в версии нет упоминания mysql/mariadb: {db_version}"
        
        print(f"\n[УСПЕХ] Коннектор прочитал DB_TYPE и успешно подключился к базе. Версия: {db_version}")
        
    finally:
        # 5. Обязательно закрываем за собой ресурсы
        cursor.close()
        connection.close()