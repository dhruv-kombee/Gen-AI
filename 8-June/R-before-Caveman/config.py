import os
from datetime import timedelta
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    SECRET_KEY = os.getenv("SECRET_KEY", "college-registration-secret-key")
    DATABASE_PATH = BASE_DIR / "database" / "college_registration.db"
    SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
    SAMPLE_DATA_PATH = BASE_DIR / "database" / "sample_data.sql"
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)
