import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'focusmate.db'

# ---------- DB Initialization ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
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

# ---------- Add Task ----------
def add_task(username, task, due_date=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (username, task, due_date) VALUES (?, ?, ?)",
                (username, task, due_date))
    conn.commit()
    conn.close()

# ---------- Get Tasks ----------
def get_all_tasks(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, task, due_date, completed FROM tasks WHERE username = ? ORDER BY created_at DESC", (username,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

# ---------- Mark Task Done ----------
def mark_task_done(task_id, username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND username = ?", (task_id, username))
    conn.commit()
    conn.close()

# ---------- Get Completion Stats ----------
def get_completion_stats(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks WHERE username = ?", (username,))
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM tasks WHERE username = ? AND completed = 1", (username,))
    completed = cur.fetchone()[0]
    conn.close()
    return total, completed

# ---------- Streak Calculation ----------
def calculate_streak(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT DATE(created_at) FROM tasks WHERE username = ? AND completed = 1 ORDER BY created_at DESC", (username,))
    dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in cur.fetchall()]
    conn.close()

    if not dates:
        return 0

    streak = 1
    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak
