import sqlite3

DB_NAME = "winx.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # returns dict-like rows
    return conn
