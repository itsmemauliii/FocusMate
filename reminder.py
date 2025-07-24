import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime

# Set your email and app password here
EMAIL_ADDRESS = "youremail@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def fetch_pending_tasks():
    conn = sqlite3.connect("data/tasks.db")
    c = conn.cursor()
    c.execute("SELECT task, due_date FROM tasks WHERE completed = 0")
    tasks = c.fetchall()
    conn.close()
    return tasks

def send_reminder_email(receiver_email):
    tasks = fetch_pending_tasks()
    if not tasks:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "⏰ FocusMate Task Reminder"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    html_tasks = "".join([f"<li>{task[0]} - Due: {task[1]}</li>" for task in tasks])
    html = f"""
    <html>
      <body>
        <h3>You have pending tasks to focus on today:</h3>
        <ul>{html_tasks}</ul>
        <p>Stay productive 💪</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Email failed: {e}")
