import sqlite3
from datetime import datetime, timedelta

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            task TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_task(user, task, due_date=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (user, task, due_date) VALUES (?, ?, ?)", 
                    (user, task, due_date))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error adding task:", e)

def get_all_tasks(user):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT id, task, due_date, completed FROM tasks WHERE user=?", (user,))
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching tasks:", e)
        return []

def mark_task_done(task_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error marking task as done:", e)

def delete_task(task_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error deleting task:", e)

def calculate_streak(user):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            SELECT date(created_at) as task_date 
            FROM tasks 
            WHERE user=? AND completed=1 
            GROUP BY task_date 
            ORDER BY task_date DESC
        """, (user,))
        dates = [row[0] for row in cur.fetchall()]
        conn.close()

        streak = 0
        today = datetime.today().date()

        for i, date_str in enumerate(dates):
            task_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if task_date == today - timedelta(days=i):
                streak += 1
            else:
                break

        return streak
    except Exception as e:
        print("Error calculating streak:", e)
        return 0
