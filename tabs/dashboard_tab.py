import streamlit as st
import plotly.graph_objects as go
import history
import json

def show_dashboard_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы использовать дашборд.")
        return

    st.subheader("📊 Дашборд развития")
    
    rows = history.get_user_history(user_id)
    if not rows:
        st.info("У вас пока нет сохраненных анализов. Чтобы увидеть графики развития, проведите хотя бы 2-3 анализа!")
        return

    # Подготовка данных (сортируем по дате для графиков)
    # row: (id, user_id, overall_score, confidence, traits_json, text_sample, created_at)
    dates = [row[6][:10] for row in rows]
    overall_scores = [row[2] for row in rows]
    
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
    
    for row in rows:
        try:
            traits = json.loads(row[4])
            for t, v in traits.items():
                traits_total[t] = traits_total.get(t, 0) + v
                traits_count[t] = traits_count.get(t, 0) + 1
        except:
            pass

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
