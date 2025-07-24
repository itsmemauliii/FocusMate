import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'tasks.db'


# -----------------------------
# ✅ Initialize Database
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# -----------------------------
# 📥 Add New Task
# -----------------------------
def add_task(task, due_date=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)", (task, due_date))
    conn.commit()
    conn.close()


# -----------------------------
# 📋 Get All Tasks
# -----------------------------
def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------
# ✅ Mark Task as Complete
# -----------------------------
def mark_task_complete(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# -----------------------------
# ❌ Delete Task
# -----------------------------
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# -----------------------------
# 🔥 Calculate Streak
# -----------------------------
def calculate_streak():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get completed task dates
    cur.execute("SELECT created_at FROM tasks WHERE completed = 1 ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()

    dates = [datetime.strptime(row[0][:10], "%Y-%m-%d").date() for row in rows if row[0]]

    if not dates:
        return 0

    streak = 0
    today = datetime.today().date()
    previous_date = today

    for date in dates:
        if date == previous_date:
            continue
        elif date == previous_date - timedelta(days=1):
            streak += 1
            previous_date = date
        else:
            break

    return streak + 1  # Include today


# -----------------------------
# 📦 Initialize on Import
# -----------------------------
init_db()
