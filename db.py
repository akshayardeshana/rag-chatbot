import sqlite3
from datetime import datetime
import uuid

DB_NAME = 'complaints.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone_number TEXT,
            complaint_details TEXT,
            status TEXT DEFAULT 'In Progress',
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_complaint(name, email, phone, details):
    complaint_id = f"CMP{uuid.uuid4().hex[:6].upper()}"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (complaint_id, name, email, phone, details, 'In Progress', created_at))
    conn.commit()
    cursor.execute("SELECT * FROM complaints")
    result = cursor.fetchall()
    print("result=",result)
    conn.close()
    return complaint_id

def get_complaint_by_complaint_id(complaint_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ? ORDER BY created_at DESC LIMIT 1", (complaint_id,))
    result = cursor.fetchone()
    conn.close()
    return result