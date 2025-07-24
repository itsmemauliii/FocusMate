import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from db import get_connection

def show_charts(username):
    conn = get_connection()
    df = pd.read_sql_query("SELECT due_date, completed FROM tasks WHERE username=?", conn, params=(username,))
    
    if df.empty:
        st.write("No data to show charts.")
        return

    status_count = df['completed'].value_counts().rename({0: 'Pending', 1: 'Done'})
    st.bar_chart(status_count)
