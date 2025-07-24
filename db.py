import sqlite3

def get_connection():
    return sqlite3.connect('tasks.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    content TEXT,
                    due_date TEXT,
                    completed BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()
