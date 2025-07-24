# calendar_view.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import calendar

def get_tasks():
    conn = sqlite3.connect("data/tasks.db")
    c = conn.cursor()
    c.execute("SELECT title, due_date, status FROM tasks")
    data = c.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Title", "Due Date", "Status"])

def calendar_view():
    st.title("📅 Task Calendar View")
    df = get_tasks()

    if df.empty:
        st.info("No tasks to display.")
        return

    df["Due Date"] = pd.to_datetime(df["Due Date"])
    df["Due Date"] = df["Due Date"].dt.date

    grouped = df.groupby("Due Date")["Title"].apply(lambda x: ", ".join(x)).reset_index()
    grouped.columns = ["Date", "Tasks"]

    today = datetime.today()
    year = today.year
    month = today.month

    st.subheader(f"📆 {calendar.month_name[month]} {year}")

    cal = calendar.monthcalendar(year, month)
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].empty()
            else:
                task_str = ""
                task_date = datetime(year, month, day).date()
                row = grouped[grouped["Date"] == task_date]
                if not row.empty:
                    task_str = row.iloc[0]["Tasks"]
                if task_date == today.date():
                    cols[i].markdown(f"**:orange[{day}]**<br>{task_str}", unsafe_allow_html=True)
                else:
                    cols[i].markdown(f"**{day}**<br>{task_str}", unsafe_allow_html=True)

if __name__ == "__main__":
    calendar_view()
