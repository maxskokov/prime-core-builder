import sqlite3
import hashlib
import secrets
import re
from datetime import datetime


DB_PATH = "scores.db"

# Валидация email
_EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Ограничения
MAX_LOGIN_ATTEMPTS = 5
COOLDOWN_SECONDS = 60
MIN_PASSWORD_LENGTH = 6


def _get_conn():
    """Подключение к БД с WAL-режимом для конкурентности."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Создаёт таблицу пользователей, если не существует."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _hash_password(password: str, salt: str) -> str:
    """PBKDF2-HMAC-SHA256 с 260 000 итераций."""
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        260_000,
    )
    return dk.hex()


def validate_email(email: str) -> bool:
    """Проверяет формат email."""
    return bool(_EMAIL_RE.match(email)) and len(email) <= 254


def validate_password(password: str) -> str | None:
    """Проверяет пароль. Возвращает сообщение об ошибке или None."""
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"Пароль должен быть не менее {MIN_PASSWORD_LENGTH} символов."
    if not any(c.isdigit() for c in password):
        return "Пароль должен содержать хотя бы одну цифру."
    if not any(c.isalpha() for c in password):
        return "Пароль должен содержать хотя бы одну букву."
    return None


def register(email: str, password: str) -> tuple[bool, str]:
    """
    Регистрация пользователя.
    Возвращает (success, message).
    """
    email = email.strip().lower()

    if not validate_email(email):
        return False, "Некорректный формат email."

    pwd_err = validate_password(password)
    if pwd_err:
        return False, pwd_err

    salt = secrets.token_hex(32)
    password_hash = _hash_password(password, salt)
    now = datetime.now().isoformat()

    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
            (email, password_hash, salt, now),
        )
        conn.commit()
        return True, "Регистрация успешна!"
    except sqlite3.IntegrityError:
        return False, "Пользователь с таким email уже существует."
    finally:
        conn.close()


def login(email: str, password: str) -> tuple[bool, str, int | None]:
    """
    Вход пользователя.
    Возвращает (success, message, user_id | None).
    """
    email = email.strip().lower()

    if not validate_email(email):
        return False, "Некорректный формат email.", None

    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT id, password_hash, salt FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if row is None:
            # Не раскрываем, что пользователя нет — единое сообщение
            return False, "Неверный email или пароль.", None

        user_id, stored_hash, salt = row
        candidate_hash = _hash_password(password, salt)

        if not secrets.compare_digest(candidate_hash, stored_hash):
            return False, "Неверный email или пароль.", None

        return True, "Вход выполнен!", user_id
    finally:
        conn.close()


def check_rate_limit(state: dict) -> tuple[bool, int]:
    """
    Проверяет rate limit через session_state.
    Возвращает (allowed, seconds_remaining).
    """
    now = datetime.now()

    # Инициализация если отсутствует или None
    if state.get("last_attempt_time") is None:
        state["login_attempts"] = 0
        state["last_attempt_time"] = now
        return True, 0

    # Сброс после cooldown
    elapsed = (now - state["last_attempt_time"]).total_seconds()
    if elapsed >= COOLDOWN_SECONDS:
        state["login_attempts"] = 0
        state["last_attempt_time"] = now # Обновляем время, чтобы отсчет шел заново если нужно

    if state["login_attempts"] >= MAX_LOGIN_ATTEMPTS:
        remaining = int(COOLDOWN_SECONDS - elapsed)
        return False, max(0, remaining)

    return True, 0


def record_attempt(state: dict):
    """Записывает попытку входа."""
    state["login_attempts"] = state.get("login_attempts", 0) + 1
    state["last_attempt_time"] = datetime.now()


def reset_attempts(state: dict):
    """Сбрасывает счётчик попыток после успешного входа."""
    state["login_attempts"] = 0


# Инициализация БД при импорте
init_db()
