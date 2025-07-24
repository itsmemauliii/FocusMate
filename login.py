import sqlite3

def init_user_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def login_signup(username, password, mode):
    init_user_db()
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if mode == "Login":
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return c.fetchone() is not None
    elif mode == "Signup":
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    return False
