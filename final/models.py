from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


# ==============================
# USER FUNCTIONS
# ==============================

def register_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    password = generate_password_hash(password)

    try:

        cursor.execute(
            """
            INSERT INTO users(username, email, password)
            VALUES (?, ?, ?)
            """,
            (username, email, password)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        if check_password_hash(user["password"], password):

            return user

    return None


# ==============================
# SUMMARY FUNCTIONS
# ==============================

def save_summary(
        user_id,
        original_text,
        summary,
        original_words,
        summary_words,
        processing_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO summaries(

    user_id,

    original_text,

    summary,

    original_words,

    summary_words,

    processing_time

    )

    VALUES(?,?,?,?,?,?)

    """, (

        user_id,

        original_text,

        summary,

        original_words,

        summary_words,

        processing_time

    ))

    conn.commit()

    conn.close()


def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM summaries

    WHERE user_id=?

    ORDER BY created_at DESC

    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history


def delete_summary(summary_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM summaries WHERE id=?",

        (summary_id,)

    )

    conn.commit()

    conn.close()


# ==============================
# PROFILE
# ==============================

def update_theme(user_id, theme):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE users

    SET theme=?

    WHERE id=?

    """, (

        theme,

        user_id

    ))

    conn.commit()

    conn.close()