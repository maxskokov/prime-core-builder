import streamlit as st

def show_about_tab():
    # ── ПРЕМИУМ ДИЗАЙН "PURE CSS REVEAL" 4.0 ──
    # Этот вариант использует st.markdown БЕЗ отступов.
    # Это гарантирует, что дизайн будет работать на 100% стабильно.
    
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Montserrat:wght@900&display=swap');

.stApp { overflow-x: hidden; }

/* Контейнеры секций */
.about-section {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
    padding: 20px;
    view-timeline-name: --section-scroll;
    view-timeline-axis: block;
}

/* Эффект свечения */
.glow-bg {
    position: absolute;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 209, 255, 0.15) 0%, transparent 70%);
    filter: blur(50px);
    z-index: -1;
}

/* Заголовки */
.p-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 20px;
    letter-spacing: -3px;
    line-height: 1;
    background: linear-gradient(90deg, #fff, #888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.g-cyan { background: linear-gradient(135deg, #00d1ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.g-mag { background: linear-gradient(135deg, #a200ff, #ff00d1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.p-desc {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    color: #9ca3af;
    max-width: 700px;
    font-weight: 300;
}

/* КАРТОЧКА С АНИМАЦИЕЙ СКРОЛЛА */
.premium-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 40px;
    padding: 50px;
    max-width: 850px;
    width: 90%;
    
    /* Магия скролла: работает в Chrome 115+ */
    animation: reveal-card both;
    animation-timeline: --section-scroll;
    animation-range: entry 25% cover 50%;
}

@keyframes reveal-card {
    0% { opacity: 0; transform: translateY(100px) scale(0.9); filter: blur(10px); }
    100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

.scroll-hint {
    margin-top: 40px;
    color: #00d1ff;
    letter-spacing: 5px;
    font-size: 0.8rem;
    animation: bounce 2s infinite;
}
@keyframes bounce { 0%, 100% {transform:translateY(0); opacity: 0.3;} 50% {transform:translateY(10px); opacity: 1;} }
</style>

<div class="about-section">
    <div class="glow-bg" style="top:20%; left:10%;"></div>
    <h1 class="p-title" style="font-size: 5.5rem;">Prime Core <span class="g-cyan">BUILDER</span></h1>
    <p class="p-desc">Будущее анализа личности уже здесь. 🦾✨</p>
    <div class="scroll-hint">ЛИСТАЙ ВНИЗ ▼</div>
</div>

<div class="about-section">
    <div class="glow-bg" style="top:30%; right:10%; background: radial-gradient(circle, rgba(162, 0, 255, 0.1) 0%, transparent 70%);"></div>
    <div class="premium-card">
        <h2 class="p-title g-cyan">Умный Анализ.</h2>
        <p class="p-desc">Нейросеть считывает ваш характер через текст. Это точнее, чем любой психологический опросник.</p>
    </div>
</div>

<div class="about-section">
    <div class="premium-card">
        <h2 class="p-title g-mag">Ваш Потенциал.</h2>
        <p class="p-desc">7 векторов развития, которые помогут вам понять, в чем ваша истинная сила и лидерство.</p>
    </div>
</div>

<div class="about-section">
    <div class="premium-card" style="border-color: rgba(255, 215, 0, 0.2);">
        <h2 class="p-title" style="background: linear-gradient(90deg, #fceabb, #f8b500); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">План Роста.</h2>
        <p class="p-desc">Получайте ежедневные задания, чтобы прокачать слабые стороны и закрепить успех.</p>
    </div>
</div>

<div style="height: 30vh; display: flex; justify-content: center; align-items: center;">
    <p style="color: #4b5563; font-size: 1.5rem;">Готовы начать? 💪🚀</p>
</div>
""", unsafe_allow_html=True)
