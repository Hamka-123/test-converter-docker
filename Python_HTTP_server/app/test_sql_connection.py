import mysql.connector


DB_HOST = "mariadb-server"
DB_PORT = 3306
DB_NAME = "currency_db"
DB_USER = "app_user"
DB_PASSWORD = "app_password"


conn = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD
    
)
print(conn)

SQL_CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS table_test1 (
    name VARCHAR(10),
    age INT
)
'''

conn = mysql.connector.connect(
    host = DB_HOST,
    port = DB_PORT,
    user = DB_USER,
    database = DB_NAME,
    password = DB_PASSWORD)


cursor = conn.cursor()
cursor.execute(SQL_CREATE_TABLE)