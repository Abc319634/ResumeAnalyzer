import bcrypt
from database import fetch_one, execute_query

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def signup_user(username, password):
    hashed = hash_password(password)
    try:
        execute_query("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed), commit=True)
        return True
    except Exception as e:
        print(f"Signup error: {e}")
        return False

def login_user(username, password):
    user = fetch_one("SELECT * FROM users WHERE username = ?", (username,))
    if user and check_password(password, user['password']):
        return user
    return None
