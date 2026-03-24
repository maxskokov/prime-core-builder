import streamlit as st
import history

def show_history_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему, чтобы видеть историю своих анализов.")
        return

    st.subheader("📜 Ваша история анализов")
    
    rows = history.get_user_history(user_id)
    
    if not rows:
        st.info("У вас пока нет сохраненных анализов. Попробуйте провести первый анализ во вкладке 'Анализ текста'!")
        return

    st.write(f"Найдено записей: **{len(rows)}**")

    for row in rows:
        # row: (id, user_id, overall_score, confidence, traits_json, text_sample, created_at)
        date_str = row[6][:16].replace("T", " ")
        with st.expander(f"📅 {date_str} — Общий балл: {row[2]}"):
            st.markdown(f"**Текст:** {row[5][:200]}...")
            st.markdown(f"**Уверенность:** {int(row[3] * 100)}%")
            
            import json
            try:
                traits = json.loads(row[4])
                cols = st.columns(3)
                for i, (trait, val) in enumerate(traits.items()):
                    with cols[i % 3]:
                        st.metric(trait, val)
            except:
                st.error("Ошибка при чтении данных оценок.")

def show_clear_history_tab(user_id):
    if user_id is None:
        st.warning("⚠️ Пожалуйста, войдите в систему для управления историей.")
        return

    st.subheader("🗑️ Очистить историю")
    st.warning("⚠️ Это действие удалит **все** ваши результаты анализов безвозвратно.")

    confirm = st.checkbox("Я понимаю последствия")

    if st.button("🗑️ Удалить всю историю", use_container_width=True, disabled=not confirm):
        count = history.clear_history(user_id)
        if count > 0:
            st.success(f"✅ Удалено записей: {count}")
            st.rerun()
        else:
            st.info("История уже пуста.")
