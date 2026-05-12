import sqlite3
import os

DB_PATH = "/app/data/logs.db"

def apply_migrations():
    if not os.path.exists(DB_PATH):
        print("Database file not found. Migration skipped (it will be created by app.py).")
        return

    print(f"Starting migration for {DB_PATH}...")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Пытаемся добавить колонку
            conn.execute("ALTER TABLE conversions ADD COLUMN rate REAL")
            conn.commit()
            print("SUCCESS: Column 'rate' added to 'conversions' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("INFO: Column 'rate' already exists. Nothing to do.")
        else:
            print(f"ERROR: Migration failed: {e}")

if __name__ == "__main__":
    apply_migrations()