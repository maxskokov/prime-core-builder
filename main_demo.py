import streamlit as st
import plotly.graph_objects as go
import auth
import history

# Импортируем модули вкладок
from tabs import analysis_tab, history_tab, dashboard_tab, about_tab

# ─── Настройки страницы ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prime Core Builder",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Глобальный CSS стиль ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Montserrat:wght@700;900&display=swap');
    #MainMenu, footer, [data-testid="stConnectionStatus"], button[data-testid="manage-app-button"] { display: none !important; }
    
    .stApp {
        background: radial-gradient(circle at center top, #111827 0%, #050505 100%) !important;
        color: #e3e3e3; font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 20, 25, 0.45) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(0, 209, 255, 0.15) !important;
    }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-text {
        font-size: 3.2rem; font-weight: 900; letter-spacing: 0.35rem; line-height: 1.1;
        background: linear-gradient(90deg, #00d1ff, #a200ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-family: 'Montserrat', sans-serif;
    }
    .logo-subtext { font-size: 0.8rem; letter-spacing: 0.25rem; color: #a200ff; font-weight: 700; }
    
    /* Кнопки и Карточки */
    div.stButton > button {
        background: rgba(0, 209, 255, 0.05) !important; color: #00d1ff !important;
        border: 1px solid rgba(0, 209, 255, 0.5) !important; border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover { background: rgba(0, 209, 255, 0.15) !important; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# ─── Общие компоненты UI ────────────────────────────────────────────────────
def show_logo():
    st.markdown('<div class="logo-container"><div class="logo-text">PRIME</div><div class="logo-subtext">CORE BUILDER</div></div>', unsafe_allow_html=True)

def show_footer():
    st.markdown("<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 3rem;'>© 2026 Prime Core Builder | AI can make mistakes.</div>", unsafe_allow_html=True)

# ─── Инициализация состояний ────────────────────────────────────────────────
if "user_id" not in st.session_state: st.session_state.user_id = None
if "user_email" not in st.session_state: st.session_state.user_email = None

# Инициализируем CookieManager один раз
# cookie_manager = stx.CookieManager(key="global_cookie_manager") # Removed as per instruction

# Пытаемся восстановить сессию только один раз при старте
# if st.session_state.user_id is None: # Removed as per instruction
#     all_cookies = cookie_manager.get_all() # Removed as per instruction
#     # Если куки загрузились # Removed as per instruction
#     if all_cookies: # Removed as per instruction
#         c_id = all_cookies.get("user_id") # Removed as per instruction
#         if c_id: # Removed as per instruction
#             try: # Removed as per instruction
#                 u = auth.get_user_by_id(int(c_id)) # Removed as per instruction
#                 if u: # Removed as per instruction
#                     st.session_state.user_id = u["id"] # Removed as per instruction
#                     st.session_state.user_email = u["email"] # Removed as per instruction
#                     st.rerun() # Removed as per instruction
#             except: pass # Removed as per instruction

# ─── Экран авторизации ──────────────────────────────────────────────────────
@st.dialog("Вход в систему")
def show_auth_screen():
    auth_mode = st.radio("", ["Вход", "Регистрация"], horizontal=True, label_visibility="collapsed")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Пароль", type="password")

    if auth_mode == "Вход":
        if st.button("Войти", use_container_width=True):
            success, msg, u_id = auth.login(email, password)
            if success:
                st.session_state.user_id, st.session_state.user_email = u_id, email
                # cookie_manager.set("user_id", str(u_id), key="cookie_set_login") # Removed as per instruction
                st.rerun()
            else: st.error(msg)
    else:
        p2 = st.text_input("🔒 Повторите пароль", type="password")
        if st.button("Зарегистрироваться", use_container_width=True):
            if password == p2:
                success, msg = auth.register(email, password)
                if success: st.success(msg + ". Теперь войдите.")
                else: st.error(msg)
            else: st.error("Пароли не совпадают.")

# ─── Основной интерфейс ─────────────────────────────────────────────────────
top_col1, top_col2 = st.columns([7, 3])
with top_col2:
    if st.session_state.user_id is None:
        if st.button("🔑 Вход / Регистрация", use_container_width=True): show_auth_screen()
    else:
        st.markdown(f"<div style='text-align: right; padding-top: 10px;'>👤 <b>{st.session_state.user_email.split('@')[0]}</b></div>", unsafe_allow_html=True)

with st.sidebar:
    show_logo()
    st.divider()
    tabs = ["Анализ текста", "История", "Дашборд", "О нейросети", "Очистить историю"]
    selected_tab = st.sidebar.radio("Навигация:", tabs)
    
    if st.session_state.user_id and st.sidebar.button("Выйти"):
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.rerun()

# ─── Рендеринг вкладок ─────────────────────────────────────────────────────
user_id = st.session_state.user_id

if selected_tab == "Анализ текста":
    analysis_tab.show_analysis_tab(user_id)
elif selected_tab == "История":
    history_tab.show_history_tab(user_id)
elif selected_tab == "Дашборд":
    dashboard_tab.show_dashboard_tab(user_id)
elif selected_tab == "О нейросети":
    about_tab.show_about_tab()
elif selected_tab == "Очистить историю":
    history_tab.show_clear_history_tab(user_id)

show_footer()
