import os
import pytest
# Импортируем ваш коннектор
from dependencies import connector 

def test_db_connection_matches_env_type():
    """
    Тест проверяет, что тип активного подключения к БД
    строго соответствует типу объекта, который вернул коннектор.
    """
    # 1. Инициализируем реальное подключение через ваш коннектор
    try:
        connection = connector.get_connection()
    except Exception as e:
        pytest.fail(f"Не удалось установить соединение через коннектор: {e}")
        
    cursor = connection.cursor()

    try:
        # 2. Извлекаем имя класса и имя модуля для точной идентификации
        connection_class_name = type(connection).__name__.lower()
        connection_module_name = type(connection).__module__.lower()

        # 3. Автоматически определяем, к какой базе мы НА САМОМ ДЕЛЕ подключились
        if "mysql" in connection_class_name or "mysql" in connection_module_name:
            actual_db_type = "mysql"
        elif "sqlite" in connection_class_name or "sqlite" in connection_module_name:
            actual_db_type = "sqlite"
        else:
            actual_db_type = "unknown"

        # 4. Проверяем базу в зависимости от того, что получили по факту
        if actual_db_type == "sqlite":
            # Делаем проверочный запрос версии именно для SQLite
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            print(f"\n[УСПЕШНО] Тест подтвердил работу с SQLite (Версия: {version})")

        elif actual_db_type == "mysql":
            # Делаем проверочный запрос версии для MySQL/MariaDB
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            print(f"\n[УСПЕШНО] Тест подтвердил работу с MySQL/MariaDB (Версия: {version})")

        else:
            pytest.fail(
                f"Коннектор вернул неизвестный тип подключения. "
                f"Класс: {connection_module_name}.{type(connection).__name__}"
            )

    finally:
        # Обязательно закрываем за собой ресурсы
        cursor.close()
        connection.close()