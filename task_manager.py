import sqlite3
from datetime import datetime
import re
from dateutil import parser
import spacy

nlp = spacy.load("en_core_web_sm")

DB_NAME = "focusmate.db"

def create_task_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    task TEXT NOT NULL,
                    due_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def parse_nlp_task_input(user_input):
    doc = nlp(user_input)
    task = user_input
    due_date = None

    # Try to parse date from sentence
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            try:
                due_date = str(parser.parse(ent.text, fuzzy=True).date())
                task = user_input.replace(ent.text, '').strip()
                break
            except:
                pass

    return task.strip().capitalize(), due_date

def add_task(username, task_input):
    task, due_date = parse_nlp_task_input(task_input)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (username, task, due_date) VALUES (?, ?, ?)", (username, task, due_date))
    conn.commit()
    conn.close()

def get_all_tasks(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, task, due_date, completed FROM tasks WHERE username = ?", (username,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def mark_task_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_task_summary(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT completed, COUNT(*) FROM tasks WHERE username=? GROUP BY completed", (username,))
    summary = c.fetchall()
    conn.close()
    return summary
