import streamlit as st
import pandas as pd
import altair as alt
import sqlite3

DB_PATH = "data/tasks.db"

def show_charts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT due_date, completed as status FROM tasks", conn)
    conn.close()

    if df.empty:
        st.info("No data to visualize yet.")
        return

    df['due_date'] = pd.to_datetime(df['due_date'])
    df['count'] = 1
    summary = df.groupby(['due_date', 'status']).count().reset_index()

    chart = alt.Chart(summary).mark_bar().encode(
        x='due_date:T',
        y='count:Q',
        color='status:N',
        tooltip=['due_date:T', 'status:N', 'count:Q']
    ).properties(
        width=700,
        height=400,
        title='Task Completion Overview'
    )

    st.altair_chart(chart, use_container_width=True)
