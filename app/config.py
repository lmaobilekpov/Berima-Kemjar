import logging
import os
import secrets
from datetime import timedelta

logger = logging.getLogger(__name__)


def _is_production():
    environment = os.environ.get("FLASK_ENV") or os.environ.get("APP_ENV") or "development"
    return environment.lower() in {"production", "prod"}


def _resolve_secret_key():
    secret_key = os.environ.get("SECRET_KEY") or os.environ.get("FLASK_SECRET_KEY")
    if secret_key:
        return secret_key
    if _is_production():
        raise ValueError("Environment variable 'SECRET_KEY' belum disetel! Dilarang menggunakan hardcoded secret key.")
    logger.warning("SECRET_KEY belum disetel; memakai secret key acak sementara untuk lingkungan development.")
    return secrets.token_hex(32)


def _resolve_database_uri():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url
    if _is_production():
        raise ValueError("Environment variable 'DATABASE_URL' belum disetel! Wajib menggunakan koneksi PostgreSQL.")
    logger.warning("DATABASE_URL belum disetel; memakai SQLite lokal untuk development.")
    return "sqlite:///berima_dev.db"

class SecurityConfig:
    # Kunci rahasia untuk menandatangani session cookie secara kriptografis (Wajib disetel)
    SECRET_KEY = _resolve_secret_key()
    
    # Konfigurasi Database (PostgreSQL di produksi, SQLite untuk development lokal)
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- IMPLEMENTASI OSI LAYER 5: MANAJEMEN SESI AMAN ---
    # Mencegah akses cookie via JavaScript (Mitigasi XSS / Session Hijacking)
    SESSION_COOKIE_HTTPONLY = True
    
    # Memastikan cookie HANYA dikirimkan melalui jalur terenkripsi HTTPS
    SESSION_COOKIE_SECURE = True
    
    # Mitigasi serangan Cross-Site Request Forgery (CSRF)
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Batasan umur sesi (Session Timeout) jika pengguna tidak aktif
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)