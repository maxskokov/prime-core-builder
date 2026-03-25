import streamlit as st
import plotly.graph_objects as go
import history
import json

def show_dashboard_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы использовать дашборд.")
        return

    st.subheader("📊 Дашборд развития")
    
    scores_list = history.get_user_scores(user_id)
    if not scores_list:
        st.info("У вас пока нет сохраненных анализов. Чтобы увидеть графики развития, проведите хотя бы 2-3 анализа!")
        return

    # Подготовка данных (сортируем по дате)
    scores_list.sort(key=lambda x: str(x["created_at"]))

    # Создаем подписи: "Анализ №1 (Время)", "Анализ №2 (Время)"
    labels = []
    for i, row in enumerate(scores_list, 1):
        time_str = str(row["created_at"])[11:16] # Часы:Минуты
        labels.append(f"№{i} ({time_str})")
        
    overall_scores = [row["score"] for row in scores_list]
    
    # ── 1) Общий тренд ────────────
    st.markdown("### 📈 Динамика развития")
    st.caption("График показывает изменения баллов от анализа к анализу.")
    
    fig = go.Figure()
    
    # Основная линия
    fig.add_trace(go.Scatter(
        x=labels, 
        y=overall_scores, 
        mode='lines+markers+text',
        name='Общий балл',
        line=dict(color='#00d1ff', width=3),
        marker=dict(size=10, color='#00d1ff', symbol='diamond'),
        text=[f"{s}" for s in overall_scores],
        textposition="top center"
    ))
    
    fig.update_layout(
        yaxis={"range": [0, 110], "gridcolor": "rgba(255,255,255,0.1)", "color": "white", "title": "Балл"},
        xaxis={"gridcolor": "rgba(255,255,255,0.05)", "color": "white", "title": "Порядковый номер анализа"},
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Сравнение последних двух результатов ────────────
    if len(scores_list) >= 2:
        st.divider()
        col_left, col_right = st.columns(2)
        last = scores_list[-1]
        prev = scores_list[-2]
        diff = last['score'] - prev['score']
        
        with col_left:
            st.markdown("#### 🔄 Прогресс")
            st.metric("Текущий балл", last['score'], delta=f"{diff:.1f}")
        with col_right:
            st.markdown("#### 🕒 Предыдущий")
            st.metric("Прошлый балл", prev['score'])

    # ── 2) Сильные и слабые стороны ────────────
    st.divider()
    st.markdown("### 🏹 Анализ характеристик")
    
    traits_total = {}
    traits_count = {}
    
    for row in scores_list:
        analysis = row["full_analysis"]
        if isinstance(analysis, dict):
            for t, v in analysis.items():
                if t != "_meta" and isinstance(v, (int, float)):
                    traits_total[t] = traits_total.get(t, 0) + v
                    traits_count[t] = traits_count.get(t, 0) + 1

    if traits_total:
        trait_stats = {t: traits_total[t] / traits_count[t] for t in traits_total}
        sorted_traits = sorted(trait_stats.items(), key=lambda x: x[1], reverse=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💪 Сильные стороны")
            for trait, val in sorted_traits[:3]:
                st.markdown(f"- **{trait}**: {val:.0f}/100")
        with col2:
            st.markdown("#### 🎯 Зоны роста")
            for trait, val in sorted_traits[-3:]:
                st.markdown(f"- **{trait}**: {val:.0f}/100")
