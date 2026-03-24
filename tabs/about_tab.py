import streamlit as st

def show_about_tab():
    # ── ПРЕМИУМ ДИЗАЙН "DEPTH SCROLL" 2.0 ──────────────────────────────────
    # Этот модуль полностью переписан для максимального "ВАУ-эффекта" на конкурсе.
    
    st.markdown("""
    <style>
    /* Глобальные настройки скролла */
    .stApp { overflow-x: hidden; }

    /* Контейнер для блоков */
    .scroll-section {
        height: 100vh;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        view-timeline-name: --section-scroll;
        view-timeline-axis: block;
        perspective: 1000px;
    }

    /* Карточка с эффектом стекла и анимацией */
    .premium-card {
        max-width: 800px;
        width: 85%;
        padding: 4rem;
        background: rgba(20, 25, 40, 0.4);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 209, 255, 0.15);
        border-radius: 50px;
        text-align: center;
        
        /* Плавное появление и исчезновение при скролле */
        animation: card-appear both;
        animation-timeline: --section-scroll;
        animation-range: entry 15% cover 50%;
        
        box-shadow: 0 40px 100px -30px rgba(0, 209, 255, 0.2);
        transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    @keyframes card-appear {
        from { 
            opacity: 0; 
            transform: translateZ(-200px) translateY(100px) rotateX(10deg); 
            filter: blur(15px);
        }
        to { 
            opacity: 1; 
            transform: translateZ(0) translateY(0) rotateX(0deg); 
            filter: blur(0);
        }
    }

    /* Заголовки */
    .p-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 2rem;
        letter-spacing: -2px;
        line-height: 1;
    }

    .p-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        color: #d1d5db;
        line-height: 1.6;
        font-weight: 300;
    }

    /* Градиенты для жюри */
    .g-cyan { background: linear-gradient(135deg, #00d1ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .g-mag   { background: linear-gradient(135deg, #a200ff, #ff00d1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .g-gold  { background: linear-gradient(135deg, #fceabb, #f8b500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    /* Декоративные частицы на фоне */
    .bg-glow {
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0, 209, 255, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        z-index: -1;
        filter: blur(50px);
    }
    </style>

    <!-- ПРИВЕТСТВИЕ -->
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative;">
        <div class="bg-glow" style="top: 20%; left: 30%;"></div>
        <div class="bg-glow" style="bottom: 10%; right: 20%; background: radial-gradient(circle, rgba(162, 0, 255, 0.1) 0%, transparent 70%);"></div>
        
        <h1 style="font-size: 5rem; font-weight: 900; letter-spacing: -3px; margin-bottom: 0;">Prime Core <span class="g-cyan">BUILDER</span></h1>
        <p style="color: #6b7280; font-size: 1.5rem; margin-top: 10px; font-weight: 300;">Ваш персональный архитектор личности на базе ИИ.</p>
        <div style="margin-top: 40px; animation: bounce 2s infinite; color: #00d1ff; font-size: 0.9rem; letter-spacing: 5px;">СКРОЛЛ ВНИЗ ▼</div>
    </div>

    <!-- БЛОК 1: ПОНЯТНО О ТЕХНОЛОГИИ -->
    <div class="scroll-section">
        <div class="premium-card">
            <h2 class="p-title g-cyan">Как это работает?</h2>
            <p class="p-text">Забудьте про скучные тесты. Мы анализируем <b>ваш реальный текст</b> — то, как вы мыслите и выражаете идеи. Нейросеть находит скрытые таланты, которые вы могли не замечать.</p>
        </div>
    </div>

    <!-- БЛОК 2: 7 ХАРАКТЕРИСТИК -->
    <div class="scroll-section">
        <div class="premium-card">
            <h2 class="p-title g-mag">7 Измерений.</h2>
            <p class="p-text">Мы оцениваем вас по семи ключевым направлениям: от <b>лидерских качеств</b> до <b>креативного мышления</b>. Это позволяет создать максимально точную цифровую модель вашего потенциала.</p>
        </div>
    </div>

    <!-- БЛОК 3: ПРАКТИЧЕСКАЯ ПОЛЬЗА ДЛЯ ЖЮРИ -->
    <div class="scroll-section">
        <div class="premium-card">
            <h2 class="p-title g-gold">Ваш План Роста.</h2>
            <p class="p-text">Система не просто ставит оценки, а дает <b>реальные советы</b> на каждый день. Это ваш личный тренер, который помогает становиться лучше с каждым новым анализом.</p>
        </div>
    </div>

    <!-- ФИНАЛ -->
    <div style="height: 60vh; display: flex; justify-content: center; align-items: center; text-align: center;">
        <h3 style="font-size: 2.5rem; font-weight: 700; color: #4b5563;">Готовы начать трансформацию? 🚀</h3>
    </div>
    """, unsafe_allow_html=True)
