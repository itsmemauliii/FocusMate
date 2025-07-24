import sqlite3
from datetime import datetime, timedelta

DB_NAME = "tasks.db"

# ---------------------- DB INIT ------------------------
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

# -------------------- ADD TASK -------------------------
def add_task(username, task, due_date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (username, task, due_date) VALUES (?, ?, ?)", (username, task, due_date))
    conn.commit()
    conn.close()

# -------------------- GET TASKS ------------------------
def get_all_tasks(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, task, due_date, completed FROM tasks WHERE username = ?", (username,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

# -------------------- MARK DONE ------------------------
def mark_task_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# ------------------ DELETE TASK ------------------------
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# --------------- STREAK CALCULATION --------------------
def calculate_streak(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT due_date FROM tasks
        WHERE username = ? AND completed = 1
        ORDER BY due_date DESC
        LIMIT 10
    ''', (username,))
    rows = cur.fetchall()
    conn.close()

    streak = 0
    today = datetime.today().date()

    for i in range(len(rows)):
        due = datetime.strptime(rows[i][0], "%Y-%m-%d").date()
        if due == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return streak
