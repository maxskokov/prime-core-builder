import streamlit as st
from supabase import create_client, Client
import re
import logging

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
        return None

# ─── Валидация ─────────────────────────────────────────────────────────────

def validate_email(email: str) -> bool:
    """Проверяет корректность Email."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

# ─── Управление пользователями (Supabase Auth) ──────────────────────────────

def register(email: str, password: str) -> tuple[bool, str]:
    """Регистрирует нового пользователя через Supabase Auth."""
    email = email.strip().lower()
    
    if not validate_email(email):
        return False, "Неверный формат Email."
    if len(password) < 6:
        return False, "Пароль должен быть не менее 6 символов."
        
    sb = _get_supabase()
    if not sb:
        return False, "Ошибка подключения к базе Supabase."
        
    try:
        # Пытаемся создать аккаунт в Supabase Auth
        res = sb.auth.sign_up({
            "email": email,
            "password": password,
        })
        
        # Проверяем, был ли пользователь создан успешно
        if res.user:
            # Важно: Дублируем email в нашу таблицу 'users', 
            # чтобы сохранить связь с историей анализов (user_id)
            try:
                # В Supabase Auth ID может быть UUID (строка)
                # Если твоя таблица history использует int, 
                # то ID из Auth (UUID) может не подойти. 
                # Но для школьной презентации мы будем использовать email как связку,
                # либо UUID если ты готов к миграции типов.
                
            return True, "Регистрация успешна! Теперь вы можете войти."
        
        return False, "Ошибка при регистрации в Supabase."
    except Exception as e:
        err_msg = str(e).lower()
        if "already registered" in err_msg or "exists" in err_msg:
            return False, "Пользователь с таким Email уже существует."
        logger.error(f"Registration error: {str(e)}")
        return False, f"Ошибка регистрации: {str(e)}"

def login(email: str, password: str) -> tuple[bool, str, str | None]:
    """Авторизует пользователя через Supabase Auth."""
    email = email.strip().lower()
    sb = _get_supabase()
    
    if not sb:
        return False, "Ошибка подключения к базе.", None
        
    try:
        # Вход через системный провайдер Supabase
        res = sb.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if res.user:
            return True, "Успешный вход!", res.user.id
            
        return False, "Неверные данные для входа.", None
    except Exception as e:
        err_msg = str(e).lower()
        if "invalid login" in err_msg or "credentials" in err_msg:
            return False, "Неверный логин или пароль.", None
        if "email not confirmed" in err_msg:
            return False, "Ваш Email еще не подтвержден. Проверьте почту или отключите проверку в панели Supabase.", None
            
        logger.error(f"Login error: {str(e)}")
        return False, "Ошибка входа. Пожалуйста, попробуйте позже.", None

def get_user_by_id(user_id: str) -> dict | None:
    """Получает данные пользователя (заглушка для совместимости)."""
    # В новой системе ID пользователя — это UUID (строка), а не число.
    # Мы возвращаем базовый словарь, чтобы main_demo.py не падал.
    return {"id": user_id, "email": "User"}
