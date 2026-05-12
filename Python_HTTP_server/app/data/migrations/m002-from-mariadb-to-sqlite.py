import sqlite3
import os


# Миграция указанных таблиц и колонок
SQLITE_PATH = '/app/data/logs_backup.db'

def apply(connector):
    print("🔄 Starting migration: MariaDB ➡️ SQLite...")
    
    sqlite_path = os.getenv("SQLITE_PATH", "/app/data/logs_backup.db")
    
    mr_conn = connector.get_connection()
    mr_cursor = mr_conn.cursor()

    sl_conn = sqlite3.connect(sqlite_path)
    sl_cursor = sl_conn.cursor()

    # 1. Получаем список таблиц
    mr_cursor.execute("SHOW TABLES")
    tables = [t[0] for t in mr_cursor.fetchall()]

    for table_name in tables:
        print(f"📦 Processing table: {table_name}")

        # 2. Вместо использования SHOW CREATE TABLE (который слишком специфичен),
        # мы просто создадим универсальный запрос создания.
        # Для твоих таблиц это безопаснее всего.
        
        if table_name == 'logs':
            sl_sql = """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    asctime TEXT, 
                    levelname TEXT, 
                    message TEXT
                )
            """
        elif table_name == 'conversions':
            sl_sql = """
                CREATE TABLE IF NOT EXISTS conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    from_currency TEXT, 
                    to_currency TEXT, 
                    amount REAL, 
                    result REAL, 
                    rate REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
        else:
            print(f"⚠️ Unknown table {table_name}, skipping structure creation.")
            continue

        sl_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        sl_cursor.execute(sl_sql)

        # 3. Переливаем данные
        mr_cursor.execute(f"SELECT * FROM {table_name}")
        rows = mr_cursor.fetchall()
        
        if rows:
            # Считаем количество колонок для генерации знаков вопроса
            placeholders = ", ".join(["?"] * len(rows[0]))
            sl_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)
            print(f"✅ Migrated {len(rows)} rows to SQLite.")

    sl_conn.commit()
    sl_conn.close()
    mr_cursor.close()
    mr_conn.close()
    print(f"✨ Migration finished! Saved to: {sqlite_path}")