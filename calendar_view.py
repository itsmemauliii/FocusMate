import streamlit as st
import pandas as pd
from task_manager import get_all_tasks

def show_calendar():
    tasks = get_all_tasks()
    if not tasks:
        st.info("No tasks to show on the calendar.")
        return

    df = pd.DataFrame(tasks)
    df['due_date'] = pd.to_datetime(df['due_date'])
    df = df.sort_values(by='due_date')

    st.write("### 📅 Task Calendar")
    st.dataframe(df[['task', 'due_date', 'status']].rename(columns={
        'task': 'Task',
        'due_date': 'Due Date',
        'status': 'Status'
    }), use_container_width=True)
