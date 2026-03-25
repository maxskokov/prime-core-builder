import streamlit as st
import plotly.graph_objects as go
from analysis import analyze_text_with_meta, get_level, get_achievements, get_improvement_plan, get_daily_challenge, MAX_TEXT_LENGTH
import history
import time

def show_analysis_tab(user_id):
    st.subheader("Введите текст для анализа")
    st.caption(f"Опишите свои навыки, подход к работе, ситуации из жизни (макс. {MAX_TEXT_LENGTH} символов).")

    text_input = st.text_area(
        "Текст (минимум 8 слов):",
        height=180,
        placeholder="Например: Я уверен в себе, организую команду и планирую задачи...",
        max_chars=MAX_TEXT_LENGTH,
    )

    if st.button("🔍 Проанализировать", use_container_width=True) and text_input.strip():
        # --- Анимация в стиле Gemini ---
        loader_placeholder = st.empty()
        with loader_placeholder.container():
            st.markdown("""
                <style>
                .gemini-loader {
                    font-size: 1.5rem;
                    font-weight: 800;
                    text-align: center;
                    padding: 2rem;
                    background: linear-gradient(270deg, #a8c7fa, #00d1ff, #a200ff, #f093fb, #a8c7fa);
                    background-size: 200% 200%;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    animation: gradientMove 2s ease infinite;
                }
                @keyframes gradientMove {
                    0% {background-position: 0% 50%;}
                    50% {background-position: 100% 50%;}
                    100% {background-position: 0% 50%;}
                }
                .sparkle { display: inline-block; animation: pulse-spin 2s ease-in-out infinite; }
                @keyframes pulse-spin { 
                    0% { transform: rotate(0deg) scale(0.8); opacity: 0.5; }
                    50% { transform: rotate(180deg) scale(1.2); opacity: 1; }
                    100% { transform: rotate(360deg) scale(0.8); opacity: 0.5; }
                }
                </style>
                <div class="gemini-loader"><span class="sparkle">✨</span> Глубокий анализ нейросетью...</div>
            """, unsafe_allow_html=True)
            time.sleep(1.2) # Искусственная задержка
        loader_placeholder.empty()

        scores = analyze_text_with_meta(text_input)
        st.session_state.current_analysis = scores
        st.session_state.current_text = text_input
        
        if user_id and "message" not in scores:
            overall = scores.get("_meta", {}).get("overall_score", 50.0)
            history.save_score(user_id, text_input, scores, overall)
            st.session_state.analysis_saved = True
        else:
            st.session_state.analysis_saved = False

    if st.session_state.get("current_analysis"):
        scores = st.session_state.current_analysis
        if "message" in scores:
            st.warning(scores["message"])
        else:
            _render_results(scores, user_id)

def _render_results(scores, user_id):
    meta = scores.get("_meta", {})
    level = get_level(scores)
    achievements = get_achievements(scores)

    # Метрики
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Ваш уровень**")
        st.markdown(f"<h3 style='margin:0; color:#00d1ff;'>{level}</h3>", unsafe_allow_html=True)
    with col2:
        conf = meta.get("confidence", 0)
        st.markdown(f"**Уверенность анализа**")
        st.markdown(f"<h3 style='margin:0; color:#f093fb;'>{int(conf * 100)}%</h3>", unsafe_allow_html=True)

    if achievements:
        st.markdown("**Достижения:** " + " | ".join(achievements))

    st.divider()

    # Карточки характеристик
    st.subheader("📊 Оценка характеристик")
    trait_scores = {k: v for k, v in scores.items() if k != "_meta" and isinstance(v, (int, float))}

    cols = st.columns(2)
    for i, (trait, score) in enumerate(trait_scores.items()):
        with cols[i % 2]:
            color = "#2ecc71" if score >= 70 else "#f39c12" if score >= 40 else "#e74c3c"
            st.markdown(f"<div class='score-card' style='border-left-color:{color}'><b>{trait}</b>: <span style='color:{color}; font-size:1.2em'>{score}</span>/100</div>", unsafe_allow_html=True)
            st.progress(score / 100)

    # Визуализация
    st.divider()
    chart_type = st.radio("Тип визуализации:", ["Радар", "Столбцы", "Круговая"], horizontal=True)
    labels, values = list(trait_scores.keys()), list(trait_scores.values())
    
    if chart_type == "Радар":
        fig = go.Figure(go.Scatterpolar(r=values + [values[0]], theta=labels + [labels[0]], fill='toself', line_color='#00d1ff', fillcolor='rgba(0, 209, 255, 0.3)'))
        fig.update_layout(polar={"radialaxis": {"visible": True, "range": [0, 100], "color": "white", "gridcolor": "#444"}, "angularaxis": {"color": "white"}, "bgcolor": "rgba(0,0,0,0)"})
    elif chart_type == "Столбцы":
        fig = go.Figure(go.Bar(x=labels, y=values, marker_color='#00d1ff', text=[f"{v:.0f}" for v in values], textposition='auto'))
        fig.update_layout(yaxis={"range": [0, 105], "gridcolor": "#333", "color": "white"}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    else:
        fig = go.Figure(go.Pie(labels=labels, values=values, hole=.4))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", legend={"font": {"color": "white"}})
                
    st.plotly_chart(fig, use_container_width=True)

    # План развития
    st.divider()
    st.subheader("📈 Планирование успеха")
    plan = get_improvement_plan(scores)
    for trait, advice in plan.items():
        st.markdown(f"- **{trait}**: {advice}")

    if st.button("❌ Закрыть результаты", use_container_width=True):
        st.session_state.current_analysis = None
        st.rerun()
