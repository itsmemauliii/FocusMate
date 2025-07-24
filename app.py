import streamlit as st
from chatbot import process_input
from task_manager import get_all_tasks, add_task, mark_task_done, delete_task
from visualize import show_charts
from streaks import get_streak_badge
from calendar_view import show_calendar
from login import login_signup
import datetime

st.set_page_config(page_title="FocusMate ✨", layout="wide")

# Session state for user login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_signup()
    st.stop()

st.title("🌟 Welcome to FocusMate")
st.markdown("Type things like: 'Add Study ML on Sunday' or 'Mark Submit report as done'")

user_input = st.text_input("🔊 What would you like to do today?")
if user_input:
    response = process_input(user_input)
    st.success(response)

st.subheader("📅 Your Tasks")
tasks = get_all_tasks()
for task in tasks:
    st.markdown(f"- {'✅' if task['status'] == 'done' else '🔘'} **{task['task']}** → Due: {task['due_date']}")

st.subheader("🌈 Your Progress")
show_charts()

st.subheader("🥇 Your Streaks & Badges")
streak, badge = get_streak_badge()
st.write(f"Current Streak: {streak} days")
st.write(f"Badge: {badge}")

st.subheader("🗓️ Calendar View")
show_calendar()
