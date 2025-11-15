import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import json

def get_db():
    """
    Creates and returns a new MySQL connection using credentials
    from config.py. Each request should open and close its own connection.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("[DB] Connection error:", e)
        return None


def insert_reading(data):
    """
    Insert a sensor reading into the 'readings' table.
    `data` should be a dictionary containing the keys:
        - device_id
        - temp
        - humidity
        - pressure
        - light
        - raw_json (optional)
    """
    sql = """
        INSERT INTO readings
        (device_id, temp, humidity, pressure, light, raw_json)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data.get("device_id"),
        data.get("temp"),
        data.get("humidity"),
        data.get("pressure"),
        data.get("light"),
        json.dumps(data)   # <-- valid JSON for MySQL JSON column
    )

    conn = get_db()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        return True
    except Error as e:
        print("[DB] Insert error:", e)
        return False
    finally:
        conn.close()
