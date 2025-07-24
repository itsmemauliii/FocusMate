import sqlite3
from datetime import datetime, timedelta

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Force recreate table (optional during testing)
    cur.execute("DROP TABLE IF EXISTS tasks")
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            task TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_task(user, task, due_date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (user, task, due_date) VALUES (?, ?, ?)", (user, task, due_date))
    conn.commit()
    conn.close()

def get_all_tasks(user=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if user:
        cur.execute("SELECT * FROM tasks WHERE user = ?", (user,))
    else:
        cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return rows

def complete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def calculate_streak(user):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT DATE(created_at) FROM tasks 
        WHERE user = ? AND completed = 1
        ORDER BY created_at DESC
    ''', (user,))
    
    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in cur.fetchall()]
    conn.close()
    
    streak = 0
    today = datetime.today().date()

    for i in range(len(dates)):
        if (today - dates[i]).days == streak:
            streak += 1
        else:
            break
    return streak

def get_due_tasks(user):
    today = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM tasks 
        WHERE user = ? AND completed = 0 AND due_date <= ?
        ORDER BY due_date ASC
    ''', (user, today))
    tasks = cur.fetchall()
    conn.close()
    return tasks

init_db()
