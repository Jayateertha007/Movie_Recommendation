# auth.py
import streamlit as st
import hashlib
import json
import os

USER_FILE = "users.json"

# Load user data from JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user data to JSON file
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup logic
def signup(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

# Login logic
def login(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)

# Login/Signup UI
def show_login():
    st.title("🔐 Login / Signup")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        uname = st.text_input("Username", key="login_user")
        passwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login(uname, passwd):
                st.session_state.logged_in = True
                st.session_state.username = uname
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        new_user = st.text_input("Create Username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", key="signup_pass")
        if st.button("Signup"):
            if signup(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists.")
