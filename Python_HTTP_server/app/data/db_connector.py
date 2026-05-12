import mysql.connector
import sqlite3
import os

class DBConnector:
    def __init__(self):
        # Берем тип БД из переменной окружения, по умолчанию mysql
        self.db_type = os.getenv("DB_TYPE", "mysql")

    def get_connection(self):
        if self.db_type == "mysql":
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "mariadb-server"),
                user=os.getenv("DB_USER", "app_user"),
                password=os.getenv("DB_PASSWORD", "app_password"),
                database=os.getenv("DB_NAME", "currency_db")
            )
        else:
            return sqlite3.connect(os.getenv("SQLITE_PATH", "/app/data/logs.db"))

    def get_placeholder(self):
        """Возвращает %s для MySQL или ? для SQLite"""
        return "%s" if self.db_type == "mysql" else "?"