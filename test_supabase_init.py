import streamlit as st
from supabase import create_client
import sys

def run_diagnostic():
    print("--- Диагностика подключения к Supabase ---")
    
    # 1. Проверка секретов
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        print("[OK] Секреты SUPABASE_URL и SUPABASE_KEY найдены.")
    except Exception as e:
        print(f"[ERROR] Секреты не найдены: {e}")
        print("Подсказка: Создайте файл .streamlit/secrets.toml")
        return

    # 2. Попытка инициализации клиента
    try:
        sb = create_client(url, key)
        print("[OK] Клиент Supabase успешно инициализирован.")
    except Exception as e:
        print(f"[ERROR] Ошибка при создании клиента: {e}")
        return

    # 3. Проверка таблиц (простой select)
    try:
        sb.table("users").select("id").limit(1).execute()
        print("[OK] Таблица 'users' доступна.")
    except Exception as e:
        print(f"[WARNING] Таблица 'users' недоступна или пуста: {e}")
        print("Подсказка: Возможно, нужно запустить SQL скрипты для создания таблиц.")

if __name__ == "__main__":
    run_diagnostic()
