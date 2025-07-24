from db import get_connection

def add_task(username, content, due_date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (username, content, due_date) VALUES (?, ?, ?)",
              (username, content, due_date))
    conn.commit()

def get_all_tasks(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE username=?", (username,))
    return c.fetchall()

def mark_task_done(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()

def delete_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
