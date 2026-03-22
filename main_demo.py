import streamlit as st
import plotly.graph_objects as go
import html as html_lib
from analysis import (
    analyze_text_with_meta, get_level, get_achievements,
    get_improvement_plan, get_daily_challenge, TRAITS, MAX_TEXT_LENGTH,
)
import history
import auth

# ─── Настройки страницы ─────────────────────────────────────────────────────

st.set_page_config(
    page_title="Prime Core Builder",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Адаптивный CSS ─────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Адаптив для мобильных */
    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.5rem !important; }
        h1 { font-size: 1.5rem !important; }
        .stTextArea textarea { font-size: 14px !important; }
    }
    /* Основной стиль */
    h1.main-title {
        text-align: center;
        font-family: 'Segoe UI', monospace;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem 0;
    }
    .score-card {
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid;
    }
    .auth-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ─── Логотип ────────────────────────────────────────────────────────────────

def show_logo(width=250):
    """Отображает логотип, если файл существует."""
    import os
    if os.path.exists("logo.png"):
        st.image("logo.png", width=width)
    else:
        st.markdown("<h1 class='main-title'>💻 Prime Core Builder</h1>", unsafe_allow_html=True)

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
    st.session_state.user_email = None
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
    st.session_state.last_attempt_time = None


# ─── Утилита: безопасный вывод текста ───────────────────────────────────────

def safe_text(text: str) -> str:
    """Экранирует HTML-спецсимволы для защиты от XSS."""
    return html_lib.escape(str(text))


# ─── Экран авторизации ──────────────────────────────────────────────────────

def show_auth_screen():
    """Форма входа / регистрации."""
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo(width=280)
    
    st.markdown("<br>", unsafe_allow_html=True)
    auth_mode = st.radio("", ["Вход", "Регистрация"], horizontal=True)

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
            else:
                st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── Проверка авторизации ───────────────────────────────────────────────────

if st.session_state.user_id is None:
    show_auth_screen()
    show_footer()
    st.stop()

# ─── Сайдбар ────────────────────────────────────────────────────────────────

with st.sidebar:
    show_logo(width=180)
    st.divider()
    st.markdown(f"👤 **{safe_text(st.session_state.user_email)}**")

if st.sidebar.button("🚪 Выйти"):
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.rerun()

tabs = ["📝 Анализ текста", "📜 История", "📊 Дашборд", "ℹ️ О нейросети", "🗑️ Очистить историю"]
selected_tab = st.sidebar.radio("Навигация:", tabs)

user_id = st.session_state.user_id

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 1: Анализ текста
# ═══════════════════════════════════════════════════════════════════════════

if selected_tab == "📝 Анализ текста":
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
            fig = go.Figure(data=go.Scatterpolar(
                r=list(trait_scores.values()) + [list(trait_scores.values())[0]],
                theta=list(trait_scores.keys()) + [list(trait_scores.keys())[0]],
                fill="toself",
                fillcolor="rgba(102, 126, 234, 0.25)",
                line=dict(color="#667eea"),
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                margin=dict(l=40, r=40, t=20, b=20),
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
            history.save_scores(user_id, scores)
            st.success("✅ Результаты сохранены в вашу историю!")

# ═══════════════════════════════════════════════════════════════════════════
# ВКЛАДКА 2: История
# ═══════════════════════════════════════════════════════════════════════════

elif selected_tab == "📜 История":
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

elif selected_tab == "📊 Дашборд":
    st.subheader("📊 Персональный дашборд")
    stats = history.get_stats(user_id)

    if not stats:
        st.info("Пока нет данных. Проведите хотя бы один анализ.")
    else:
        total = stats.pop("total_analyses", 0)
        st.metric("Всего анализов", total)

        # Средний radar-чарт
        trait_vals = [stats.get(t, 0) for t in TRAITS]
        fig = go.Figure(data=go.Scatterpolar(
            r=trait_vals + [trait_vals[0]],
            theta=TRAITS + [TRAITS[0]],
            fill="toself",
            fillcolor="rgba(118, 75, 162, 0.3)",
            line=dict(color="#764ba2", width=2),
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Средний профиль по всем анализам",
            margin=dict(l=40, r=40, t=60, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Столбчатая диаграмма
        colors = ["#2ecc71" if v >= 70 else "#f39c12" if v >= 40 else "#e74c3c"
                  for v in trait_vals]
        bar_fig = go.Figure(data=go.Bar(
            x=TRAITS, y=trait_vals,
            marker_color=colors,
            text=[f"{v:.0f}" for v in trait_vals],
            textposition="auto",
        ))
        bar_fig.update_layout(
            yaxis=dict(range=[0, 100], title="Средний балл"),
            margin=dict(l=40, r=20, t=20, b=40),
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        # Сильные и слабые стороны
        sorted_traits = sorted(stats.items(), key=lambda x: x[1], reverse=True)
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

elif selected_tab == "ℹ️ О нейросети":
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

elif selected_tab == "🗑️ Очистить историю":
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
