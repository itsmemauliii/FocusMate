import sqlite3

def init_task_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    task TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'pending')''')
    conn.commit()
    conn.close()

def add_task(username, task, due_date):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (username, task, due_date) VALUES (?, ?, ?)",
              (username, task, due_date))
    conn.commit()
    conn.close()

def get_all_tasks(username):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT id, task, due_date, status FROM tasks WHERE username=?", (username,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def mark_task_done(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
