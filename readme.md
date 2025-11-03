# FocusMate - NLP-Powered Task Manager

**FocusMate** is a simple yet smart task management app built with **Streamlit** and **spaCy**.
It helps you stay organized by letting you **add, track, and complete tasks** using natural language like:

> “Submit report by Monday” or “Call client tomorrow morning.”

---

## Features

* **User login & signup** system
* **Natural Language task creation** using spaCy
* **Automatic date extraction** from text
* **Mark tasks as done / delete tasks** easily
* **Persistent task storage** using local database
* **Clean, interactive Streamlit UI**

---

## Project Structure

```
focusmate/
│
├── main.py             # Streamlit entry point
├── login.py            # Handles login and signup logic
├── task_manager.py     # CRUD for task database
├── nlp_utils.py        # NLP parsing for task + date
├── tasks.db            # SQLite DB (auto-created)
├── users.db            # SQLite DB (auto-created)
└── README.md
```

---

## Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/focusmate.git
cd focusmate
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Example `requirements.txt`:

```
streamlit
spacy
sqlite3
```

---

## Run the App

```bash
streamlit run main.py
```

App will open at: **[http://localhost:8501](http://localhost:8501)**

---

## NLP Task Input

Type natural phrases like:

| Input                         | Extracted Task    | Detected Date |
| ----------------------------- | ----------------- | ------------- |
| “Finish AI project by Friday” | Finish AI project | Friday        |
| “Submit report on 5th Nov”    | Submit report     | 2025-11-05    |
| “Call client tomorrow”        | Call client       | Tomorrow      |

If no date is detected, the app politely asks for one

---

## Data Handling

* **SQLite** used for users & tasks
* Each user’s tasks are stored separately
* All updates are live & reactive (no manual refresh needed)

---

## Future Enhancements

* Google Calendar integration
* Task priority levels
* Reminders via email or notifications
* Better NLP (e.g., detect time and task categories)

---

## Author

* **Mauli Patel**
* Data Science & AI Enthusiast
* [LinkedIn](https://linkedin.com/in/maulipatel)
* [maulipatel@example.com](mailto:maulipatel@example.com)


Would you like me to make a **README badge header** (e.g., `![Python](...) ![Streamlit](...) ![spaCy](...)`) and a **screenshot/demo section** with a fake UI preview image link? It makes your repo pop visually.
