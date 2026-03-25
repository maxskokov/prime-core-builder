import streamlit as st
from supabase import create_client, Client
import bcrypt
import re
import time
import logging
import hashlib

# Настройка логирования
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ─── Инициализация Supabase ────────────────────────────────────────────────

def _get_supabase() -> Client | None:
    """Подключается к облачной базе Supabase через Secrets."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        # Если секреты еще не настроены, возвращаем None
        return None

def _hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt."""
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

def _verify_password(password: str, hashed: str) -> bool:
    """Проверяет пароль против хеша bcrypt с поддержкой старого SHA256."""
    try:
        # Проверка Bcrypt
        if hashed.startswith('$2b$') or hashed.startswith('$2a$'):
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
        # Фолбек на старый SHA256
        salt = "prime_core_builder_v1_salt_2024"
        old_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return old_hash == hashed
    except Exception:
        return False

# ─── Функции управления пользователями ─────────────────────────────────────

def init_db():
    """Заглушка для обратной совместимости."""
    pass

def validate_email(email: str) -> bool:
    """Проверяет корректность Email."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def register(email: str, password: str) -> tuple[bool, str]:
    """Регистрирует нового пользователя в Supabase."""
    email = email.strip().lower()
    
    if not validate_email(email):
        return False, "Неверный формат Email."
    if len(password) < 6:
        return False, "Пароль должен быть не менее 6 символов."
        
    sb = _get_supabase()
    if not sb:
        return False, "Облачная база не настроена в Secrets (нужны SUPABASE_URL и SUPABASE_KEY)."
        
    try:
        # Проверяем наличие пользователя
        res = sb.table("users").select("id").eq("email", email).execute()
        if res.data:
            return False, "Пользователь с таким Email уже существует."
            
        # Создаем запись
        new_user = {
            "email": email,
            "password_hash": _hash_password(password)
        }
        sb.table("users").insert(new_user).execute()
        return True, "Регистрация успешна! Теперь вы можете войти."
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return False, "Ошибка при регистрации. Пожалуйста, попробуйте позже."

def login(email: str, password: str) -> tuple[bool, str, int | None]:
    """Проверяет данные пользователя в Supabase."""
    email = email.strip().lower()
    sb = _get_supabase()
    
    if not sb:
        return False, "Ошибка подключения к базе.", None
        
    try:
        res = sb.table("users").select("id", "password_hash").eq("email", email).execute()
        if not res.data:
            return False, "Пользователь не найден.", None
            
        user = res.data[0]
        if _verify_password(password, user["password_hash"]):
            # Автоматическое обновление хеша до Bcrypt, если он старый
            if not (user["password_hash"].startswith('$2b$') or user["password_hash"].startswith('$2a$')):
                try:
                    new_hash = _hash_password(password)
                    sb.table("users").update({"password_hash": new_hash}).eq("id", user["id"]).execute()
                except Exception as e:
                    logger.error(f"Hash upgrade error: {str(e)}")
            
            return True, "Успешный вход!", user["id"]
        
        return False, "Неверный пароль.", None
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return False, "Ошибка входа. Пожалуйста, попробуйте позже.", None

def get_user_by_id(user_id: int) -> dict | None:
    """Получает данные пользователя по ID."""
    sb = _get_supabase()
    if not sb: return None
    try:
        res = sb.table("users").select("id", "email").eq("id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

# ─── Rate Limiting (через session_state) ───────────────────────────────────

def check_rate_limit(state: dict) -> tuple[bool, int]:
    """Предотвращает брутфорс паролей."""
    if "login_attempts" not in state:
        state["login_attempts"] = 0
        state["last_attempt_time"] = 0
        
    now = time.time()
    # Если прошло больше минуты, сбрасываем счетчик
    if now - state.get("last_attempt_time", 0) > 60:
        state["login_attempts"] = 0
        
    if state["login_attempts"] >= 5:
        wait_time = int(60 - (now - state["last_attempt_time"]))
        return False, max(0, wait_time)
        
    return True, 0

def reset_attempts(state: dict):
    """Сбрасывает счетчик попыток после успешного входа."""
    state["login_attempts"] = 0
    state["last_attempt_time"] = 0

def record_attempt(state: dict):
    """Алиас для обратной совместимости."""
    increment_attempts(state)

def increment_attempts(state: dict):
    """Увеличивает счетчик при ошибке."""
    state["login_attempts"] = state.get("login_attempts", 0) + 1
    state["last_attempt_time"] = time.time()
