import sqlite3
import os

# ==========================================
# CREATE DATABASE FOLDER
# ==========================================

DATABASE_FOLDER = "database"

DATABASE_NAME = "summarai.db"

os.makedirs(DATABASE_FOLDER, exist_ok=True)

DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    DATABASE_NAME
)

# ==========================================
# CONNECT DATABASE
# ==========================================

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

# ==========================================
# HISTORY TABLE
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    original_text TEXT,

    summary TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id) REFERENCES users(id)

)

""")

# ==========================================
# SETTINGS TABLE
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS settings(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER UNIQUE,

    theme TEXT DEFAULT 'dark',

    language TEXT DEFAULT 'English',

    FOREIGN KEY(user_id) REFERENCES users(id)

)

""")

# ==========================================
# SAVE DATABASE
# ==========================================

connection.commit()

connection.close()

print("===================================")
print(" SummarAI Database Created")
print("===================================")
print("Database Location:", DATABASE_PATH)
print("Tables:")
print(" - users")
print(" - history")
print(" - settings")
print("===================================")