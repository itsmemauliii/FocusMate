import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/tasks.db"

# Initialize DB if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        xp INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

def add_task(task, due_date):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)", (task, due_date))
    conn.commit()
    conn.close()

def mark_task_done(task):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status='done', xp = xp + 5 WHERE task=?", (task,))
    conn.commit()
    conn.close()

def delete_task(task):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE task=?", (task,))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY due_date ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_completed_today():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks WHERE status='done' AND due_date=?", (today,))
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_task_summary():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("SELECT due_date, status FROM tasks").fetchall()
    conn.close()
    return df

def calculate_streak():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    streak = 0
    today = datetime.now().date()
    for i in range(0, 10):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        cur.execute("SELECT COUNT(*) FROM tasks WHERE due_date=? AND status='done'", (day,))
        count = cur.fetchone()[0]
        if count > 0:
            streak += 1
        else:
            break
    conn.close()
    return streak
