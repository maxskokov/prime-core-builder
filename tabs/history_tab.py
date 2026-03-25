import streamlit as st
import history

def show_history_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы видеть историю своих анализов.")
        return

    st.subheader("📜 Ваша история анализов")
    
    scores = history.get_user_scores(user_id)
    
    if not scores:
        st.info("У вас пока нет сохраненных анализов. Попробуйте провести первый анализ во вкладке 'Анализ текста'!")
        return

    st.write(f"Найдено записей: **{len(scores)}**")

    for row in scores:
        # row: {id, text_preview, full_analysis, score, created_at}
        date_str = str(row["created_at"])[:16].replace("T", " ")
        with st.expander(f"📅 {date_str} — Общий балл: {row['score']}"):
            st.markdown(f"**Текст:** {row['text_preview']}")
            
            analysis = row["full_analysis"]
            if isinstance(analysis, dict) and "_meta" in analysis:
                conf = analysis["_meta"].get("confidence", 0)
                st.markdown(f"**Уверенность:** {int(conf * 100)}%")
                
                # Отображаем характеристики
                traits = {k: v for k, v in analysis.items() if k != "_meta" and isinstance(v, (int, float))}
                
                st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 10px;'>", unsafe_allow_html=True)
                for trait, val in traits.items():
                    color = "#00d1ff" if val >= 70 else "#f093fb" if val >= 40 else "#6b7280"
                    st.markdown(f"""
                        <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; border-left: 3px solid {color};'>
                            <div style='font-size: 0.8rem; color: #9ca3af;'>{trait}</div>
                            <div style='font-size: 1.2rem; font-weight: 600; color: {color};'>{val}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Детальный анализ недоступен для этой записи.")

def show_clear_history_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему для управления историей.")
        return

    st.subheader("🗑️ Очистить историю")
    st.warning("⚠️ Это действие удалит **все** ваши результаты анализов безвозвратно.")

    confirm = st.checkbox("Я понимаю последствия")

    if st.button("🗑️ Удалить всю историю", use_container_width=True, disabled=not confirm):
        count = history.delete_user_history(user_id)
        if count > 0:
            st.success(f"✅ Удалено записей: {count}")
            st.rerun()
        else:
            st.info("История уже пуста.")
