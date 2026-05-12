import sqlite3


class CurrencyRepository:
    def __init__(self, connector):
        self.connector = connector
        self.p = self.connector.get_placeholder()

    def add_conversion(self, from_curr, to_curr, amount, result, rate):
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        query = f"""
            INSERT INTO conversions (from_currency, to_currency, amount, result, rate) 
            VALUES ({self.p}, {self.p}, {self.p}, {self.p}, {self.p})
        """
        
        cursor.execute(query, (from_curr, to_curr, amount, result, rate))
        conn.commit()
        cursor.close()
        conn.close()
        
    def create_schema(self):
        """Создает структуру таблиц, если их нет. Универсально для всех БД."""
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        # Определяем типы данных в зависимости от БД
        is_mysql = self.connector.db_type == "mysql"
        id_type = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql else "INTEGER PRIMARY KEY"
        text_type = "TEXT"
        
        queries = [
            f"""CREATE TABLE IF NOT EXISTS logs (
                id {id_type}, asctime VARCHAR(50), levelname VARCHAR(10), message {text_type}
            )""",
            f"""CREATE TABLE IF NOT EXISTS conversions (
                id {id_type}, from_currency VARCHAR(10), to_currency VARCHAR(10), 
                amount DOUBLE, result DOUBLE, rate DOUBLE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )"""
        ]
        
        for q in queries:
            cursor.execute(q)
        
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_conversions(self):
        conn = self.connector.get_connection()
        # Включаем режим словаря для обеих БД
        if self.connector.db_type == "mysql":
            cursor = conn.cursor(dictionary=True)
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
        cursor.execute("SELECT * FROM conversions ORDER BY timestamp DESC")
        rows = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        return rows
    
    def add_system_log(self, asctime, levelname, message):
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO logs (asctime, levelname, message) VALUES ({self.p}, {self.p}, {self.p})"
        cursor.execute(query, (asctime, levelname, message))
        conn.commit()
        cursor.close()
        conn.close()