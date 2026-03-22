import streamlit as st
from supabase import create_client, Client
import hashlib
import re
import time

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
    """Хеширует пароль для хранения в БД."""
    salt = "prime_core_builder_v1_salt_2024"
    return hashlib.sha256((password + salt).encode()).hexdigest()

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
        return False, f"Ошибка при регистрации: {str(e)}"

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
        if user["password_hash"] == _hash_password(password):
            return True, "Успешный вход!", user["id"]
        
        return False, "Неверный пароль.", None
    except Exception as e:
        return False, f"Ошибка входа: {str(e)}", None

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

def increment_attempts(state: dict):
    """Увеличивает счетчик при ошибке."""
    state["login_attempts"] = state.get("login_attempts", 0) + 1
    state["last_attempt_time"] = time.time()
