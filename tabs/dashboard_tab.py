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

    # Подготовка данных (сортируем по дате для графиков)
    # scores_list: [{id, text_preview, full_analysis, score, created_at}, ...]
    # Сортировка по времени (на всякий случай, если база вернула не так)
    scores_list.sort(key=lambda x: str(x["created_at"]))

    dates = [str(row["created_at"])[:10] for row in scores_list]
    overall_scores = [row["score"] for row in scores_list]
    
    # ── 1) Общий тренд ────────────
    st.markdown("### 📈 Динамика общего балла")
    fig = go.Figure(go.Scatter(x=dates, y=overall_scores, mode='lines+markers', line_color='#00d1ff'))
    fig.update_layout(yaxis={"range": [0, 100], "gridcolor": "#333", "color": "white"}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin={"l": 20, "r": 20, "t": 20, "b": 20})
    st.plotly_chart(fig, use_container_width=True)

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
