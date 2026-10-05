import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "restaurant_ai")

try:
    print(f"Connecting to MySQL ({MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE})...")
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    if connection.is_connected():
        print("[SUCCESS] MySQL connection successful!")
        db_info = connection.server_info
        print(f"Connected to MySQL Server version: {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Active database: {record[0]}")
        cursor.close()
        connection.close()

except Error as e:
    if e.errno == 1045:
        print("\n[ERROR 1045] Access denied for user 'root'@'localhost'.")
        print(">> The password specified in MYSQL_PASSWORD does not match your MySQL root password.")
        print(">> Please set your correct MySQL password in `.env`:")
        print("   MYSQL_PASSWORD=your_actual_mysql_password")
    elif e.errno == 1049:
        print(f"\n[ERROR 1049] Database '{MYSQL_DATABASE}' does not exist.")
        print(">> Create it in MySQL CLI: CREATE DATABASE restaurant_ai;")
    else:
        print(f"\n[ERROR] MySQL Connection Error: {e}")