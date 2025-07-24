import re
from textblob import TextBlob
import dateparser

def process_input(user_input):
    intent = extract_intent(user_input)
    task = extract_task(user_input)
    due_date = extract_date(user_input)

    from task_manager import add_task, mark_task_done, delete_task, get_all_tasks

    if intent == "add" and task and due_date:
        add_task(task, due_date)
        return f"✅ Task '{task}' added for {due_date}"
    elif intent == "mark_done" and task:
        mark_task_done(task)
        return f"✔️ Task '{task}' marked as done."
    elif intent == "delete" and task:
        delete_task(task)
        return f"🗑️ Task '{task}' deleted."
    elif intent == "view":
        tasks = get_all_tasks()
        if tasks:
            return "\n".join([f"- {t['task']} → Due: {t['due_date']} | Status: {t['status']}" for t in tasks])
        else:
            return "📭 No tasks found."
    else:
        return "❓ Sorry, I didn't understand. Try: 'Add Study ML on Friday'"

def extract_intent(text):
    text = text.lower()
    if "add" in text:
        return "add"
    elif "delete" in text or "remove" in text:
        return "delete"
    elif "mark" in text and "done" in text:
        return "mark_done"
    elif "show" in text or "view" in text or "list" in text:
        return "view"
    return "unknown"

def extract_task(text):
    match = re.search(r"(?:add|mark|delete) ['\"]?(.+?)['\"]?(?: for| on|$)", text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_date(text):
    date = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'future'})
    return date.strftime("%Y-%m-%d") if date else None
