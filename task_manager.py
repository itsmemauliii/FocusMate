import sqlite3

DB_NAME = "focusmate.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Patch schema to add new columns safely
    patch_schema(conn)

    conn.close()


def patch_schema(conn):
    cur = conn.cursor()
    # Try to add new columns. Ignore errors if they already exist.
    try:
        cur.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP")
    except sqlite3.OperationalError:
        pass

    conn.commit()


def add_task(task, due_date=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, due_date, completed) VALUES (?, ?, ?)", (task, due_date, 0))
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, task, due_date, completed, created_at FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return tasks


def update_task_status(task_id, completed):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
