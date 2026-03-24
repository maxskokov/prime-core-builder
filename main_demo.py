import streamlit as st
import plotly.graph_objects as go
import html as html_lib
from analysis import (
    analyze_text_with_meta, get_level, get_achievements,
    get_improvement_plan, get_daily_challenge, TRAITS, MAX_TEXT_LENGTH,
)
import history
import auth
import extra_streamlit_components as stx

# ─── Настройки страницы ─────────────────────────────────────────────────────

st.set_page_config(
    page_title="Prime Core Builder",
    page_icon="🏙️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Адаптивный CSS ─────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Montserrat:wght@700;900&display=swap');

    /* Убираем лишнее */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Убираем кнопку Manage app и другие элементы Streamlit */
    button[data-testid="manage-app-button"],
    [data-testid="stConnectionStatus"],
    footer {
        display: none !important;
    }

    /* Глубокий темный фон приложения с "сеткой" или радиальным градиентом */
    .stApp {
        background: radial-gradient(circle at center top, #111827 0%, #050505 100%) !important;
        color: #e3e3e3;
        font-family: 'Inter', sans-serif;
    }
    
    /* Стеклянный Сайдбар (Glassmorphism) */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 20, 25, 0.45) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(0, 209, 255, 0.15) !important;
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Неоновый Логотип */
    .logo-container {
        padding: 0;
        margin: 0 auto 20px auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .logo-text {
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.35rem !important;
        line-height: 1.1;
        background: linear-gradient(90deg, #00d1ff, #a200ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 209, 255, 0.3);
        font-family: 'Montserrat', sans-serif;
    }
    .logo-subtext {
        font-size: 0.8rem !important;
        letter-spacing: 0.25rem !important;
        color: #a200ff;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(162, 0, 255, 0.6);
        margin-top: -2px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }

    /* Заголовки с легким свечением */
    h1, h2, h3, .stSubheader {
        color: #ffffff !important;
        font-family: 'Montserrat', 'Inter', sans-serif !important;
        text-shadow: 0 0 10px rgba(0, 209, 255, 0.25);
        font-weight: 700 !important;
    }

    .auth-box {
        text-align: center;
        width: 100%;
        padding: 20px;
    }

    /* Поля ввода (Инпуты) */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(10, 15, 20, 0.6) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #00d1ff !important;
        box-shadow: 0 0 15px rgba(0, 209, 255, 0.3) !important;
        background-color: rgba(15, 20, 30, 0.8) !important;
    }
    
    /* Кнопки (Ключевой Cyberpunk элемент) */
    div.stButton > button {
        background: rgba(0, 209, 255, 0.05) !important;
        color: #00d1ff !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0, 209, 255, 0.5) !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 10px rgba(0, 209, 255, 0.1) !important;
        font-family: 'Inter', sans-serif !important;
    }
    div.stButton > button:hover {
        background: rgba(0, 209, 255, 0.15) !important;
        box-shadow: 0 0 20px rgba(0, 209, 255, 0.5) !important;
        border-color: #00d1ff !important;
        transform: translateY(-2px);
    }

    /* Главная кнопка действия (Primary) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #0099ff, #8a2be2) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 209, 255, 0.4) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(0, 209, 255, 0.7) !important;
        background: linear-gradient(45deg, #00b3ff, #9d4edd) !important;
    }

    /* Стеклянные карточки результатов */
    .score-card {
        background: rgba(25, 30, 40, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-left-width: 4px !important; /* Цвет бордера задается в python коде */
        border-radius: 12px !important;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .score-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 209, 255, 0.15) !important;
    }

    /* Метрики (Уровень, Уверенность) */
    [data-testid="stMetric"] {
        background: rgba(15, 20, 30, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 209, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: inset 0 0 15px rgba(0, 209, 255, 0.05), 0 4px 15px rgba(0,0,0,0.5) !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        color: #a8c7fa !important;
        font-weight: 600 !important;
        justify-content: center;
    }
    [data-testid="stMetricValue"] {
        color: #00d1ff !important;
        text-shadow: 0 0 15px rgba(0, 209, 255, 0.5) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Диалоговые окна (Auth modal) */
    div[role="dialog"] > div {
        background: rgba(15, 20, 25, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 209, 255, 0.3) !important;
        border-radius: 16px !important;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 209, 255, 0.1) !important;
    }

    /* Отступы */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Логотип (Текстовый) ─────────────────────────────────────────────────────

def show_logo(width=220):
    """Отображает текстовое лого Prime Core Builder."""
    st.markdown(f"""
    <div class="logo-container" style="margin-bottom: 2rem; margin-top: 1rem;">
        <div class="logo-text">PRIME</div>
        <div class="logo-subtext">CORE BUILDER</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Футер ──────────────────────────────────────────────────────────────────

def show_footer():
    """Отображает футер с дисклеймером."""
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 3rem; padding-bottom: 1rem;'>
        © 2026 Prime Core Builder | <b>AI can make mistakes.</b> Check important info.
    </div>
    """, unsafe_allow_html=True)

# ─── Инициализация session_state ────────────────────────────────────────────

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Инициализация попыток входа
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
    st.session_state.last_attempt_time = 0.0

# ─── Управление Cookies ───────────────────────────────────────────────────

if "cookie_manager" not in st.session_state:
    st.session_state.cookie_manager = stx.CookieManager()

cookie_manager = st.session_state.cookie_manager

# Авто-вход через куки
if st.session_state.user_id is None:
    c_user_id = cookie_manager.get("user_id")
    if c_user_id:
        try:
            u_info = auth.get_user_by_id(int(c_user_id))
            if u_info:
                st.session_state.user_id = u_info["id"]
                st.session_state.user_email = u_info["email"]
                st.rerun()
        except:
            pass

# ─── Google Sheets (Бессмертный резерв - больше не нужен) ────────────────
conn_gs = None 


if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
    st.session_state.last_attempt_time = None

# ─── Утилита: безопасный вывод текста ───────────────────────────────────────

def safe_text(text: str) -> str:
    """Экранирует HTML-спецсимволы для защиты от XSS."""
    return html_lib.escape(str(text))


# ─── Экран авторизации (Диалог) ─────────────────────────────────────────────

@st.dialog("Вход в систему")
def show_auth_screen():
    """Форма входа / регистрации."""
    st.markdown("<br>", unsafe_allow_html=True)
    auth_mode = st.radio("", ["Вход", "Регистрация"], horizontal=True, label_visibility="collapsed")

    email = st.text_input("📧 Email", placeholder="user@example.com", max_chars=254)
    password = st.text_input("🔒 Пароль", type="password", placeholder="Минимум 6 символов", max_chars=128)

    if auth_mode == "Вход":
        if st.button("Войти", use_container_width=True):
            # Rate limit
            allowed, remaining = auth.check_rate_limit(st.session_state)
            if not allowed:
                st.error(f"⏱️ Слишком много попыток. Подождите {remaining} сек.")
                return

            auth.record_attempt(st.session_state)

            if not email.strip() or not password:
                st.warning("Заполните все поля.")
                return

            success, msg, user_id = auth.login(email, password)
            if success:
                auth.reset_attempts(st.session_state)
                st.session_state.user_id = user_id
                st.session_state.user_email = email.strip().lower()
                # Сохраняем куки и даем Streamlit время отрисовать компонент перед перезагрузкой
                cookie_manager.set("user_id", str(user_id), key="set_id_login")
                st.success("✅ Вход успешен!")
                if st.button("Нажмите здесь, чтобы продолжить", type="primary", use_container_width=True):
                    st.rerun()
            else:
                st.error(msg)

    else:  # Регистрация
        password2 = st.text_input("🔒 Повторите пароль", type="password", max_chars=128)

        if st.button("Зарегистрироваться", use_container_width=True):
            if not email.strip() or not password:
                st.warning("Заполните все поля.")
                return

            if password != password2:
                st.error("Пароли не совпадают.")
                return

            success, msg = auth.register(email, password)
            if success:
                st.success(msg + " Теперь войдите.")
                # При регистрации тоже можно сохранить ID если мы сразу заходим
            else:
                st.error(msg)
    
    # Вторая метка для закрытия (необязательно, но помогает структуре)
    # st.markdown("</div>", unsafe_allow_html=True)

# ─── Проверка авторизации ───────────────────────────────────────────────────

# Если раньше мы блокировали доступ, то теперь вход опциональный.
# Убираем жесткую блокировку и рисуем кнопку входа сверху справа.

# Топ-панель (показываем кнопку входа или профиль текущего пользователя)
top_col1, top_col2 = st.columns([7, 3])
with top_col2:
    if st.session_state.user_id is None:
        if st.button("🔑 Войти / Регистрация", use_container_width=True):
            show_auth_screen()
    else:
        email_prefix = st.session_state.user_email.split("@")[0]
        st.markdown(f"<div style='text-align: right; padding-top: 10px;'>👤 <b>{safe_text(email_prefix)}</b></div>", unsafe_allow_html=True)

# ─── Сайдбар ────────────────────────────────────────────────────────────────

with st.sidebar:
    show_logo(width=160) # Компактный логотип для меню
    st.divider()

if st.session_state.user_id is not None:
    if st.sidebar.button("Выйти"):
        st.session_state.user_id = None
        st.session_state.user_email = None
        cookie_manager.delete("user_id", key="delete_id")
        st.rerun()

tabs = ["Анализ текста", "История", "Дашборд", "О нейросети", "Очистить историю"]
selected_tab = st.sidebar.radio("Навигация:", tabs)

user_id = st.session_state.user_id

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 1: Анализ текста
# ═══════════════════════════════════════════════════════════════════════════

if selected_tab == "Анализ текста":
    st.subheader("Введите текст для анализа")
    st.caption(f"Опишите свои навыки, подход к работе, ситуации из жизни (макс. {MAX_TEXT_LENGTH} символов).")

    text_input = st.text_area(
        "Текст (минимум 8 слов):",
        height=180,
        placeholder="Например: Я уверен в себе, организую команду и планирую задачи...",
        max_chars=MAX_TEXT_LENGTH,
    )

    if st.button("🔍 Проанализировать", use_container_width=True) and text_input.strip():
        scores = analyze_text_with_meta(text_input)

        if "message" in scores:
            st.warning(scores["message"])
        else:
            meta = scores.get("_meta", {})
            level = get_level(scores)
            achievements = get_achievements(scores)

            # ── Уровень и уверенность ───────────────────────────────
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ваш уровень", level)
            with col2:
                conf = meta.get("confidence", 0)
                st.metric("Уверенность анализа", f"{int(conf * 100)}%")

            # ── Достижения ──────────────────────────────────────────
            if achievements:
                st.markdown("**Достижения:** " + " | ".join(achievements))

            st.divider()

            # ── Оценки по чертам ────────────────────────────────────
            st.subheader("📊 Оценка характеристик")
            trait_scores = {k: v for k, v in scores.items()
                           if k != "_meta" and isinstance(v, (int, float))}

            cols = st.columns(2)
            for i, (trait, score) in enumerate(trait_scores.items()):
                with cols[i % 2]:
                    if score >= 70:
                        color = "#2ecc71"
                    elif score >= 40:
                        color = "#f39c12"
                    else:
                        color = "#e74c3c"
                    st.markdown(
                        f"<div class='score-card' style='border-left-color:{color}'>"
                        f"<b>{safe_text(trait)}</b>: "
                        f"<span style='color:{color}; font-size:1.2em'>{score}</span>/100"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    st.progress(score / 100)

            # ── Radar-чарт ──────────────────────────────────────────
            # The original radar chart code is replaced by a chart picker section.
            # The original radar chart was here:
            # fig = go.Figure(data=go.Scatterpolar(
            #     r=list(trait_scores.values()) + [list(trait_scores.values())[0]],
            #     theta=list(trait_scores.keys()) + [list(trait_scores.keys())[0]],
            #     fill="toself",
            #     fillcolor="rgba(102, 126, 234, 0.25)",
            #     line=dict(color="#667eea"),
            # ))
            # fig.update_layout(
            #     polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            #     showlegend=False,
            #     margin=dict(l=40, r=40, t=20, b=20),
            # )
            # st.plotly_chart(fig, use_container_width=True)
            st.divider()
            st.subheader("Визуализация профиля")
            
            # Выбор типа графика
            chart_type = st.radio("Тип визуализации:", ["Радар", "Столбцы", "Круговая"], horizontal=True, key="analysis_chart_type")
            
            labels = list(trait_scores.keys())
            values = list(trait_scores.values())
            
            if chart_type == "Радар":
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=labels + [labels[0]],
                    fill='toself',
                    line_color='#00d1ff',
                    fillcolor='rgba(0, 209, 255, 0.3)'
                ))
                fig.update_layout(
                    polar={
                        "radialaxis": {"visible": True, "range": [0, 100], "color": "white", "gridcolor": "#444"},
                        "angularaxis": {"color": "white", "gridcolor": "#444"},
                        "bgcolor": "rgba(0,0,0,0)"
                    },
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 40, "r": 40, "t": 20, "b": 20}
                )
            elif chart_type == "Столбцы":
                fig = go.Figure(go.Bar(
                    x=labels,
                    y=values,
                    marker_color='#00d1ff',
                    text=[f"{v:.0f}" for v in values],
                    textposition='auto',
                ))
                fig.update_layout(
                    yaxis={"range": [0, 105], "gridcolor": "#333", "color": "white"},
                    xaxis={"color": "white"},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 20, "r": 20, "t": 20, "b": 20}
                )
            else: # Круговая
                fig = go.Figure(go.Pie(
                    labels=labels,
                    values=values,
                    hole=.4,
                    marker=dict(colors=['#00d1ff', '#0099ff', '#0066ff', '#0033ff', '#3300ff', '#6600ff', '#9900ff'])
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    legend={"font": {"color": "white"}}
                )
                
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # ── План развития ───────────────────────────────────────
            st.subheader("📈 План развития")
            plan = get_improvement_plan(scores)
            for trait, advice in plan.items():
                st.markdown(f"- **{safe_text(trait)}**: {safe_text(advice)}")

            # ── Ежедневное задание ──────────────────────────────────
            st.subheader("🎯 Задание на сегодня")
            challenges = get_daily_challenge(scores)
            for trait, challenge in challenges.items():
                st.info(f"**{safe_text(trait)}**: {safe_text(challenge)}")

            # ── Рекомендации ────────────────────────────────────────
            suggestions = meta.get("suggestions", [])
            if suggestions:
                st.subheader("💡 Рекомендации")
                for s in suggestions:
                    st.caption(f"• {safe_text(s)}")

            # ── Сохранение ──────────────────────────────────────────
            if user_id:
                history.save_scores(user_id, scores, text_input)
                st.success("✅ Результаты сохранены в вашу историю!")
            else:
                st.info("💡 Войдите в систему, чтобы сохранять результаты в Историю и строить Дашборд.")

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 2: История
# ═══════════════════════════════════════════════════════════════════════════
elif selected_tab == "История":
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы использовать Историю анализов.")
    else:
        st.subheader("📜 История анализов")
        df = history.load_history(user_id)

        if df.empty:
            st.info("У вас пока нет сохранённых анализов. Перейдите во вкладку «Анализ текста».")
        else:
            display_cols = ["timestamp"] + TRAITS
            existing_cols = [c for c in display_cols if c in df.columns]
            st.dataframe(df[existing_cols], use_container_width=True)

            # Тренд по дням
            if "timestamp" in df.columns:
                st.subheader("📈 Тренд по дням")
                df["date"] = df["timestamp"].dt.date
                trait_cols = [c for c in TRAITS if c in df.columns]
                daily_avg = df.groupby("date")[trait_cols].mean()

                if not daily_avg.empty:
                    fig = go.Figure()
                    colors = ["#667eea", "#764ba2", "#f093fb", "#f5576c",
                              "#4facfe", "#43e97b", "#fa709a"]
                    for i, col in enumerate(daily_avg.columns):
                        fig.add_trace(go.Scatter(
                            x=daily_avg.index, y=daily_avg[col],
                            mode="lines+markers", name=col,
                            line=dict(color=colors[i % len(colors)]),
                        ))
                    fig.update_layout(
                        xaxis_title="Дата", yaxis_title="Средний балл",
                        yaxis=dict(range=[0, 100]),
                        margin=dict(l=40, r=20, t=20, b=40),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            st.markdown("**💪 Совет:** Анализируйте регулярно — отслеживайте прогресс!")

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 3: Дашборд
# ═══════════════════════════════════════════════════════════════════════════

elif selected_tab == "Дашборд":
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы просматривать персональный Дашборд.")
    else:
        st.subheader("📊 Персональный дашборд")
        stats = history.get_stats(user_id)

        if not stats or stats.get("total_analyses", 0) == 0:
            st.info("У вас пока нет сохраненных анализов. Проведите свой первый анализ в первой вкладке!")
        else:
            total = stats.pop("total_analyses", 0)
            st.metric("Всего анализов", total)

            st.divider()
            st.subheader("Визуализация профиля")
            
            # Выбор типа графика
            chart_type = st.radio("Тип визуализации:", ["Радар", "Столбцы", "Круговая"], horizontal=True, key="dashboard_chart_type")
            
            labels = list(stats.keys())
            values = list(stats.values())
            
            if chart_type == "Радар":
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=labels + [labels[0]],
                    fill='toself',
                    line_color='#00d1ff',
                    fillcolor='rgba(0, 209, 255, 0.3)'
                ))
                fig.update_layout(
                    polar={
                        "radialaxis": {"visible": True, "range": [0, 100], "color": "white", "gridcolor": "#444"},
                        "angularaxis": {"color": "white", "gridcolor": "#444"},
                        "bgcolor": "rgba(0,0,0,0)"
                    },
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 40, "r": 40, "t": 20, "b": 20}
                )
            elif chart_type == "Столбцы":
                fig = go.Figure(go.Bar(
                    x=labels,
                    y=values,
                    marker_color='#00d1ff',
                    text=[f"{v:.0f}" for v in values],
                    textposition='auto',
                ))
                fig.update_layout(
                    yaxis={"range": [0, 105], "gridcolor": "#333", "color": "white"},
                    xaxis={"color": "white"},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 20, "r": 20, "t": 20, "b": 20}
                )
            else: # Круговая
                fig = go.Figure(go.Pie(
                    labels=labels,
                    values=values,
                    hole=.4,
                    marker={"colors": ['#00d1ff', '#0099ff', '#0066ff', '#0033ff', '#3300ff', '#6600ff', '#9900ff']}
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    legend={"font": {"color": "white"}}
                )
                
            st.plotly_chart(fig, use_container_width=True)

            # Сильные и слабые стороны
            trait_stats = {k: v for k, v in stats.items() if isinstance(v, (int, float))}
            sorted_traits = sorted(trait_stats.items(), key=lambda x: x[1], reverse=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 💪 Сильные стороны")
                for trait, val in sorted_traits[:3]:
                    st.markdown(f"- **{safe_text(trait)}**: {val:.0f}/100")
            with col2:
                st.markdown("### 🎯 Зоны роста")
                for trait, val in sorted_traits[-3:]:
                    st.markdown(f"- **{safe_text(trait)}**: {val:.0f}/100")

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 4: О нейросети
# ═══════════════════════════════════════════════════════════════════════════

elif selected_tab == "О нейросети":
    st.subheader("ℹ️ О Prime Core Builder")

    st.markdown("""
    **Prime Core Builder** — система анализа личностных качеств на основе текста.

    ### Как это работает?

    1. **Ввод текста** — опишите свой подход к работе, навыки, ситуации из жизни
    2. **Анализ** — система разбирает текст по 7 ключевым чертам личности
    3. **Оценка** — каждая черта получает балл от 0 до 100
    4. **План развития** — персональные рекомендации по улучшению слабых сторон

    ### 7 черт личности

    | Черта | Что оценивается |
    |---|---|
    | 🎯 Дисциплина | Планирование, соблюдение сроков, системность |
    | 💪 Уверенность | Принятие решений, ответственность, самооценка |
    | 👑 Лидерство | Организация, координация, инициативность |
    | 💡 Креативность | Генерация идей, нестандартные решения |
    | ❤️ Эмпатия | Понимание, поддержка, активное слушание |
    | 🔄 Адаптивность | Гибкость, приспособляемость к изменениям |
    | 💬 Коммуникация | Ясность изложения, навыки общения |

    ### Методология

    - **Лексический анализ** — поиск ключевых фраз и корней
    - **Контекстный анализ** — учёт отрицаний и тональности
    - **Морфологический анализ** — лемматизация (pymorphy2)
    - **Нормализация** — взвешенная формула для шкалы 0–100

    ### Безопасность

    - 🔒 Пароли хешируются (PBKDF2-SHA256, 260 000 итераций)
    - 🛡️ Защита от SQL-инъекций (параметризованные запросы)
    - ⏱️ Защита от брутфорса (rate limiting)
    - 🧹 Защита от XSS (экранирование ввода)
    """)

    st.caption("Версия 2.0 • Prime Core Builder")

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 5: Очистить историю
# ═══════════════════════════════════════════════════════════════════════════

elif selected_tab == "Очистить историю":
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему для управления профилем.")
    else:
        st.subheader("🗑️ Очистить историю анализов")
        st.warning("⚠️ Это действие удалит **все** ваши результаты анализов. Данные невозможно восстановить.")

        confirm = st.checkbox("Я понимаю, что это действие необратимо")

        if st.button("🗑️ Удалить всю историю", use_container_width=True, disabled=not confirm):
            deleted = history.clear_history(user_id)
            if deleted > 0:
                st.success(f"✅ Удалено {deleted} записей.")
            else:
                st.info("История уже пуста.")

# ─── Финальный футер для всех страниц ───────────────────────────────────────
show_footer()
