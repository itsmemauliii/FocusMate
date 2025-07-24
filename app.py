import streamlit as st
from auth import signup, login
from task_manager import add_task, get_all_tasks, mark_task_done, delete_task
from visualize import show_charts
from db import init_db
from nlp_utils import extract_task_details

st.set_page_config(page_title="FocusMate", layout="centered")
init_db()

st.title("🎯 FocusMate – NLP Task Manager")

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Login / Signup UI
if not st.session_state.logged_in:
    mode = st.selectbox("Login or Sign up", ["Login", "Sign up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if mode == "Login":
            if login(username, password):
                st.success("Logged in!")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid credentials")
        else:
            if signup(username, password):
                st.success("Signup successful, now login.")
            else:
                st.warning("Username already exists.")
else:
    st.sidebar.title(f"👋 Welcome, {st.session_state.username}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False))

    st.subheader("📝 Add a new task (natural language input)")
    task_input = st.text_input("E.g. 'Study ML on Friday'")

    if st.button("Add Task"):
        sentence, due = extract_task_details(task_input)
        if due:
            add_task(st.session_state.username, sentence, due)
            st.success("Task added!")
        else:
            st.warning("Couldn't detect date. Try saying 'on Friday' or 'by 2025-07-25'")

    st.divider()
    st.subheader("📋 Your Tasks")
    tasks = get_all_tasks(st.session_state.username)
    for task in tasks:
        tid, _, content, due, done = task
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{content}** _(Due: {due})_")
        with col2:
            if not done:
                if st.button("✅ Done", key=f"done_{tid}"):
                    mark_task_done(tid)
                    st.experimental_rerun()
        with col3:
            if st.button("🗑️ Delete", key=f"del_{tid}"):
                delete_task(tid)
                st.experimental_rerun()

    st.divider()
    st.subheader("📊 Your Progress")
    show_charts(st.session_state.username)
