import os
import pytest
from dependencies import connector

# def test_database_connection_is_alive():
#     """Проверяем, что подключение к реальной БД успешно устанавливается"""
#     # 1. Пытаемся получить соединение
#     connection = connector.get_connection()
#     cursor = connection.cursor()
    
#     try:
#         # 2. Выполняем простейший пинг-запрос
#         cursor.execute("SELECT 1;")
#         result = cursor.fetchone()
#         # assert False - проверка при падении
        
#         # 3. Проверяем, что БД вернула ожидаемый результат
#         assert result is not None
#         assert result[0] == 1
#         print(f"\n[УСПЕШНОЕ ПОДКЛЮЧЕНИЕ]")
        
#     except Exception as e:
#         pytest.fail(def_missing_exec=f"Не удалось подключиться к БД: {e}")
        
#     finally:
#         # 4. Всегда закрываем за собой соединение
#         cursor.close()
#         connection.close()
        
# def test_get_db_system_info():
#     """Тест проверяет коннект и выводит в консоль версию базы данных"""
#     connection = connector.get_connection()
#     cursor = connection.cursor()
    
#     try:
#         # Запрашиваем версию аптайма или сервера
#         cursor.execute("SELECT version();")
#         db_version = cursor.fetchone()[0]
        
#         # Проверяем, что строка с версией не пустая
#         assert db_version != ""
        
#         # Печатаем информацию (чтобы увидеть её в консоли, запускайте pytest с флагом -s: pytest -s)
#         print(f"\n[УСПЕШНОЕ ПОДКЛЮЧЕНИЕ] Версия БД: {db_version}")
        
#     finally:
#         cursor.close()
#         connection.close()

def test_db_connection_matches_env_type():
    """
    Тест проверяет, что тип активного подключения к БД 
    строго соответствует установленному флагу DB_TYPE в .env
    """
    # 1. Получаем текущее значение флага из окружения (по умолчанию sqlite, если не задано)
    expected_db_type = os.getenv("DB_TYPE", "sqlite").lower()
    
    # 2. Инициализируем реальное подключение через ваш коннектор
    connection = connector.get_connection()
    cursor = connection.cursor()
    
    try:
        # 3. Выясняем у самой базы данных, кто она такая.
        # Запрос 'SELECT sqlite_version()' уронит MySQL, а специфичные запросы MySQL уронят SQLite.
        # Поэтому используем универсальный трюк или проверяем тип объекта подключения.
        
        connection_class_name = type(connection).__name__.lower()
        
        if expected_db_type == "sqlite":
            # Проверяем, что класс соединения относится к sqlite (например, sqlite3.Connection)
            assert "sqlite" in connection_class_name, f"Ожидался SQLite, но получен класс {connection_class_name}"
            
            # Делаем проверочный запрос версии именно для SQLite
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            print(f"\n[УСПЕШНО] Работаем с SQLite (Версия: {version})")
            
        elif expected_db_type == "mysql":
            # Проверяем, что класс соединения относится к MySQL (например, CMySQLConnection или MySQLConnection)
            assert "mysql" in connection_class_name, f"Ожидался MySQL, но получен класс {connection_class_name}"
            
            # Делаем проверочный запрос версии для MySQL
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            print(f"\n[УСПЕШНО] Работаем с MySQL (Версия: {version})")
            
        else:
            pytest.fail(f"Неизвестный тип БД в конфигурации: {expected_db_type}")
            
    finally:
        cursor.close()
        connection.close()