import sqlite3
from datetime import datetime

DATABASE = "crowd.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people_count (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            total_in INTEGER NOT NULL,
            total_out INTEGER NOT NULL,
            current_inside INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_count(total_in, total_out):
    current_inside = total_in - total_out

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO people_count
        (timestamp, total_in, total_out, current_inside)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        total_in,
        total_out,
        current_inside
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()

    rows = conn.execute("""
        SELECT timestamp, total_in, total_out, current_inside
        FROM people_count
        ORDER BY id
    """).fetchall()

    conn.close()

    return rows