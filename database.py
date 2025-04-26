import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = "plant_data.db"

def init_db():
    """Initialize the database if it doesn't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        soil_moisture INTEGER,
        motor_status TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully")

def save_reading(data):
    """Save sensor readings to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO sensor_readings (timestamp, temperature, humidity, soil_moisture, motor_status)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        data["timestamp"],
        data["temperature"],
        data["humidity"],
        data["soil_moisture"],
        data["motor_status"]
    ))
    
    conn.commit()
    conn.close()

def get_latest_reading():
    """Get the most recent sensor reading"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM sensor_readings
    ORDER BY id DESC
    LIMIT 1
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return dict(result)
    return None

def get_readings(hours=24):
    """Get sensor readings for the past specified hours"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Calculate the timestamp for 'hours' ago
    time_ago = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
    SELECT * FROM sensor_readings
    WHERE timestamp > ?
    ORDER BY timestamp
    ''', (time_ago,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results
