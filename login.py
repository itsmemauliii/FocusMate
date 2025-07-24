import streamlit as st

# Hardcoded user data for demo (you can hook it to SQLite or Firebase later)
users = {
    "mauli@example.com": {"password": "focus123"},
    "demo@example.com": {"password": "test123"}
}

def login_signup():
    st.title("🔐 Login / Signup to FocusMate")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if email in users and users[email]["password"] == password:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")

    with tab2:
        new_email = st.text_input("New Email", key="signup_email")
        new_password = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if new_email in users:
                st.warning("User already exists.")
            else:
                users[new_email] = {"password": new_password}
                st.success("Account created. You can now login.")
