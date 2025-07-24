import streamlit as st
import hashlib
import sqlite3

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return hashed_text == hashlib.sha256(str.encode(password)).hexdigest()

def create_users_table():
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data
