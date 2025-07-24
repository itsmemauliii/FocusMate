# app.py

import streamlit as st
from chatbot import process_input
from task_manager import get_all_tasks
from visualize import show_charts
from streaks import get_streak_badge
from calendar_view import show_calendar
from login import login_signup

# -------------- App Config --------------
st.set_page_config(page_title="FocusMate ✨", layout="wide")

# -------------- Session Login Check --------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_signup()
    st.stop()

# -------------- Header Section --------------
st.title("🌟 Welcome to FocusMate")
st.markdown("Type tasks like: `Add Study ML on Sunday` or `Mark Submit report as done`")

# -------------- NLP Input Section --------------
user_input = st.text_input("🔊 What would you like to do today?")
if user_input:
    try:
        response = process_input(user_input)
        st.success(response)
    except Exception as e:
        st.error(f"Oops! Something went wrong: {e}")

# -------------- Task View Section --------------
st.subheader("📅 Your Tasks")
try:
    tasks = get_all_tasks()
    if tasks:
        for task in tasks:
            status_icon = "✅" if task['status'] == 'done' else "🔘"
            st.markdown(f"- {status_icon} **{task['task']}** → Due: {task['due_date']}")
    else:
        st.info("No tasks yet. Add some!")
except Exception as e:
    st.error(f"Couldn't load tasks: {e}")

# -------------- Charts Section --------------
st.subheader("🌈 Your Progress")
show_charts()

# -------------- Streak & Badge Section --------------
st.subheader("🥇 Your Streaks & Badges")
try:
    streak, badge = get_streak_badge()
    st.write(f"**Current Streak:** `{streak}` days")
    st.write(f"**Badge:** `{badge}`")
except:
    st.info("No streak data yet. Complete a task to start tracking!")

# -------------- Calendar View Section --------------
st.subheader("🗓️ Calendar View")
show_calendar()
