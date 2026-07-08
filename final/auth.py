from flask import session
from models import register_user, login_user


# ==========================================
# REGISTER
# ==========================================

def register(username, email, password):

    if not username.strip():
        return False, "Username cannot be empty."

    if not email.strip():
        return False, "Email cannot be empty."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    success = register_user(
        username,
        email,
        password
    )

    if success:
        return True, "Registration Successful."

    return False, "Email already exists."


# ==========================================
# LOGIN
# ==========================================

def login(email, password):

    user = login_user(email, password)

    if user:

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]

        return True

    return False


# ==========================================
# LOGOUT
# ==========================================

def logout():

    session.clear()


# ==========================================
# CHECK LOGIN
# ==========================================

def is_logged_in():

    return "user_id" in session


# ==========================================
# CURRENT USER
# ==========================================

def current_user():

    if not is_logged_in():
        return None

    return {

        "id": session["user_id"],

        "username": session["username"],

        "email": session["email"]

    }