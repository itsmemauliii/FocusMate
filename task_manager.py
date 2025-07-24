import sqlite3
from datetime import datetime, timedelta

DB_FILE = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            task TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_task(username, task, due_date):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (username, task, due_date) VALUES (?, ?, ?)",
                (username, task, due_date))
    conn.commit()
    conn.close()

def get_all_tasks(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, task, due_date, completed FROM tasks WHERE username=? ORDER BY due_date ASC", (username,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

def mark_task_done(task_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def calculate_streak(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        SELECT DATE(created_at) as day
        FROM tasks
        WHERE username=? AND completed=1
        ORDER BY day DESC
    ''', (username,))
    rows = cur.fetchall()
    conn.close()

    today = datetime.now().date()
    streak = 0
    prev_day = today

    for row in rows:
        task_day = datetime.strptime(row[0], '%Y-%m-%d').date()
        if task_day == prev_day:
            streak += 1
            prev_day -= timedelta(days=1)
        elif task_day == prev_day - timedelta(days=1):
            streak += 1
            prev_day = task_day
        else:
            break

    return streak
