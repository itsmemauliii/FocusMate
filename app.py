import streamlit as st
from login import login_signup
from task_manager import *
from nlp_utils import parse_task_input

st.set_page_config(page_title="FocusMate", page_icon="🧠")

# Initialize DBs
init_task_db()
init_user_db()

# Login/Signup
if "logged_in" not in st.session_state:
    st.title("🔐 Login or Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    mode = st.selectbox("Mode", ["Login", "Signup"])
    if st.button(mode):
        if login_signup(username, password, mode):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials or username taken.")

# Main app
if st.session_state.get("logged_in"):
    st.title("🎯 FocusMate — Task Manager")
    st.write(f"Welcome back, **{st.session_state.username}**!")

    # Add task using NLP
    with st.form("add_task_form"):
        raw_input = st.text_input("Add task (e.g. 'Submit report by Monday')")
        submit = st.form_submit_button("Add Task")
        if submit and raw_input:
            task, due_date = parse_task_input(raw_input)
            if not due_date:
                st.warning("Couldn't find a date. Please include it.")
            else:
                add_task(st.session_state.username, task, due_date)
                st.success(f"Task added: {task} (Due: {due_date})")

    # View tasks
    tasks = get_all_tasks(st.session_state.username)
    if tasks:
        for task_id, task, due_date, status in tasks:
            cols = st.columns([4, 2, 1, 1])
            cols[0].write(f"📌 {task}")
            cols[1].write(f"📅 {due_date}")
            if cols[2].button("✅", key=f"done_{task_id}"):
                mark_task_done(task_id)
                st.experimental_rerun()
            if cols[3].button("❌", key=f"del_{task_id}"):
                delete_task(task_id)
                st.experimental_rerun()
    else:
        st.info("No tasks yet. Try adding some!")

    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
