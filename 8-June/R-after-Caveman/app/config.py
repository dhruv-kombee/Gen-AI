import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASE_PATH = BASE_DIR / "data" / "college_registration.db"
    SECRET_KEY = os.getenv("SECRET_KEY", "college-registration-secret-key")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

