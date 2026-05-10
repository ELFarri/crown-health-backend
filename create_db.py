import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS calal_db;")
    print("Database 'calal_db' created or already exists.")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
