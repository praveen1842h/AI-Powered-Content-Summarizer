from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

import sqlite3
import os

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from config import (
    DATABASE,
    UPLOAD_FOLDER,
    SECRET_KEY
)

from ai_engine import (
    summarize_text,
    get_text_details
)

from pdf_processor import (
    validate_pdf,
    extract_pdf_text
)

# ==========================================
# CREATE APP
# ==========================================

app = Flask(
    __name__,
    static_folder="static"
)

app.secret_key = SECRET_KEY

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection
    # ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        db.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:

            flash(
                "Please fill all fields.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        db = get_db()

        existing = db.execute(
            """
            SELECT id
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        if existing:

            db.close()

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(password)

        db.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hashed_password
            )
        )

        db.commit()
        db.close()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )
    # ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html"
    )


# ==========================================
# SUMMARIZE TEXT
# ==========================================

@app.route("/summarize", methods=["POST"])
def summarize():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    text = request.form.get("text", "").strip()

    if not text:

        flash(
            "Please enter some text.",
            "warning"
        )

        return redirect(
            url_for("dashboard")
        )

    summary = summarize_text(text)

    details = get_text_details(text)

    db = get_db()

    db.execute(

        """
        INSERT INTO history
        (
            user_id,
            original_text,
            summary
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,

        (
            session["user_id"],
            text,
            summary
        )

    )

    db.commit()

    db.close()

    return render_template(

        "dashboard.html",

        summary=summary,

        details=details,

        original=text

    )


# ==========================================
# PDF UPLOAD
# ==========================================

@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    if "pdf" not in request.files:

        flash(
            "Please choose a PDF.",
            "warning"
        )

        return redirect(
            url_for("dashboard")
        )

    pdf = request.files["pdf"]

    if not validate_pdf(pdf):

        flash(
            "Invalid PDF file.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    filename = secure_filename(
        pdf.filename
    )

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )

    pdf.save(filepath)

    text = extract_pdf_text(filepath)

    if not text:

        flash(
            "Unable to read PDF.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    summary = summarize_text(text)

    details = get_text_details(text)

    db = get_db()

    db.execute(

        """
        INSERT INTO history
        (
            user_id,
            original_text,
            summary
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,

        (
            session["user_id"],
            text,
            summary
        )

    )

    db.commit()

    db.close()

    return render_template(

        "dashboard.html",

        summary=summary,

        details=details,

        original=text

    )
    # ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    db = get_db()

    history = db.execute(

        """
        SELECT *
        FROM history
        WHERE user_id=?
        ORDER BY created_at DESC
        """,

        (
            session["user_id"],
        )

    ).fetchall()

    db.close()

    return render_template(

        "history.html",

        history=history

    )


# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    db = get_db()

    user = db.execute(

        """
        SELECT *
        FROM users
        WHERE id=?
        """,

        (
            session["user_id"],
        )

    ).fetchone()

    total_summaries = db.execute(

        """
        SELECT COUNT(*)
        FROM history
        WHERE user_id=?
        """,

        (
            session["user_id"],
        )

    ).fetchone()[0]

    total_words = db.execute(

        """
        SELECT
        COALESCE(SUM(LENGTH(original_text)),0)
        FROM history
        WHERE user_id=?
        """,

        (
            session["user_id"],
        )

    ).fetchone()[0]

    db.close()

    return render_template(

        "profile.html",

        user=user,

        total_summaries=total_summaries,

        total_words=total_words,

        total_pdfs=0

    )


# ==========================================
# SETTINGS
# ==========================================

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    db = get_db()

    if request.method == "POST":

        theme = request.form.get(
            "theme",
            "dark"
        )

        language = request.form.get(
            "language",
            "English"
        )

        existing = db.execute(

            """
            SELECT id
            FROM settings
            WHERE user_id=?
            """,

            (
                session["user_id"],
            )

        ).fetchone()

        if existing:

            db.execute(

                """
                UPDATE settings
                SET
                theme=?,
                language=?
                WHERE user_id=?
                """,

                (
                    theme,
                    language,
                    session["user_id"]
                )

            )

        else:

            db.execute(

                """
                INSERT INTO settings
                (
                    user_id,
                    theme,
                    language
                )
                VALUES
                (
                    ?,
                    ?,
                    ?
                )
                """,

                (
                    session["user_id"],
                    theme,
                    language
                )

            )

        db.commit()

        flash(

            "Settings saved successfully.",

            "success"

        )

    settings_data = db.execute(

        """
        SELECT *
        FROM settings
        WHERE user_id=?
        """,

        (
            session["user_id"],
        )

    ).fetchone()

    db.close()

    if settings_data is None:

        settings_data = {

            "theme": "dark",

            "language": "English"

        }

    return render_template(

        "settings.html",

        settings=settings_data

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True

    )