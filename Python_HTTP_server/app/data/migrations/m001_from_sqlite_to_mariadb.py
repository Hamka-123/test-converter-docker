import os
import sqlite3

# Автоматическая миграция всех таблиц
def apply(connector):
    print("🚀 Starting initial migration...")
    
    # 1. Читаем структуру из SQLite
    sl_path = os.getenv("SQLITE_PATH", "/app/data/logs.db")
    if not os.path.exists(sl_path):
        print("⚠️ SQLite file not found, creating default schema in MariaDB.")
        # Тут можно просто прописать дефолтные CREATE TABLE
        return

    sl_conn = sqlite3.connect(sl_path)
    sl_cursor = sl_conn.cursor()
    sl_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = sl_cursor.fetchall()

    # 2. Переносим в MariaDB
    mr_conn = connector.get_connection()
    mr_cursor = mr_conn.cursor()

    for name, sql in tables:
        # Адаптируем синтаксис SQLite под MariaDB
        new_sql = sql.replace("INTEGER PRIMARY KEY", "INT AUTO_INCREMENT PRIMARY KEY")
        new_sql = new_sql.replace("REAL", "DOUBLE")
        
        print(f"📦 Creating table: {name}")
        mr_cursor.execute(f"DROP TABLE IF EXISTS {name}")
        mr_cursor.execute(new_sql)
        
        # Переливаем данные
        sl_cursor.execute(f"SELECT * FROM {name}")
        data = sl_cursor.fetchall()
        if data:
            placeholders = ", ".join(["%s"] * len(data[0]))
            mr_cursor.executemany(f"INSERT INTO {name} VALUES ({placeholders})", data)
            print(f"✅ Migrated {len(data)} rows for {name}")

    mr_conn.commit()
    mr_cursor.close()
    mr_conn.close()
    sl_conn.close()
