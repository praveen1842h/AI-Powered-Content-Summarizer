import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "summarai.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

SECRET_KEY = "summarai_pro_secret_key"

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}